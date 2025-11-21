#!/usr/bin/env python3
# ULTRA SIMPLE QtVCP Panel Handler
# Minimal code for single axis jog control

from PyQt5.QtCore import Qt, QTimer
from qtvcp.core import Status
from qtvcp import logger
import linuxcnc
import time

# Set up logging
LOG = logger.getLogger(__name__)

STATUS = Status()
COMMAND = linuxcnc.command()

class HandlerClass:
    def __init__(self, halcomp, widgets, paths):
        self.hal = halcomp
        self.w = widgets
        self.stat = linuxcnc.stat()

        # Create HAL pins for jogging
        self.hal.newpin("jog-pos", self.hal.HAL_BIT, self.hal.HAL_OUT)
        self.hal.newpin("jog-neg", self.hal.HAL_BIT, self.hal.HAL_OUT)

        # Timer for position updates and state monitoring
        self.timer = QTimer()
        self.timer.timeout.connect(self.periodic_update)
        self.timer.start(100)  # Update every 100ms

    def initialized__(self):
        # Connect buttons
        self.w.jogPosButton.pressed.connect(lambda: self.jog_start(True))
        self.w.jogPosButton.released.connect(self.jog_stop)
        self.w.jogNegButton.pressed.connect(lambda: self.jog_start(False))
        self.w.jogNegButton.released.connect(self.jog_stop)

        self.w.enableButton.clicked.connect(self.toggle_enable)
        self.w.stopButton.clicked.connect(self.emergency_stop)

        # Start with machine in E-stop, user needs to enable
        LOG.info("Machine started in E-stop state. Click 'Enable' to start.")

    def jog_start(self, positive):
        """Start jogging"""
        try:
            self.stat.poll()

            # Only jog if machine is ON and not in E-stop
            if self.stat.estop == 0 and self.stat.enabled:
                if positive:
                    COMMAND.jog(linuxcnc.JOG_CONTINUOUS, 0, 0, 10)
                else:
                    COMMAND.jog(linuxcnc.JOG_CONTINUOUS, 0, 0, -10)
                LOG.info(f"Jogging {'positive' if positive else 'negative'}")
            else:
                LOG.warning("Machine must be enabled to jog")
        except Exception as e:
            LOG.error(f"Jog error: {e}")

    def jog_stop(self):
        """Stop jogging"""
        try:
            COMMAND.jog(linuxcnc.JOG_STOP, 0, 0)
        except:
            pass

    def toggle_enable(self):
        """Toggle machine enable"""
        try:
            self.stat.poll()

            if self.w.enableButton.isChecked():
                # E-stop is active, need to reset it
                if self.stat.estop:
                    COMMAND.state(linuxcnc.STATE_ESTOP_RESET)
                    time.sleep(0.1)  # Small delay

                # Now turn on
                COMMAND.state(linuxcnc.STATE_ON)
                self.w.enableButton.setText("Disable")
                self.w.enableButton.setStyleSheet("QPushButton { background-color: green; }")
                LOG.info("Enabling machine...")
            else:
                COMMAND.state(linuxcnc.STATE_OFF)
                self.w.enableButton.setText("Enable")
                self.w.enableButton.setStyleSheet("")
                LOG.info("Machine disabled")
        except Exception as e:
            LOG.error(f"Error toggling enable: {e}")
            self.w.enableButton.setChecked(False)

    def emergency_stop(self):
        """Emergency stop"""
        COMMAND.state(linuxcnc.STATE_ESTOP)
        self.w.enableButton.setChecked(False)
        self.w.enableButton.setText("Enable")
        self.w.enableButton.setStyleSheet("")
        LOG.info("EMERGENCY STOP")

    def periodic_update(self):
        """Update position display and check machine state"""
        try:
            self.stat.poll()

            # Update position
            pos = self.stat.position[0]  # Get X axis position
            self.w.positionDisplay.setText(f"{pos:.3f}")

            # Update enable button state based on actual machine state
            if self.stat.estop == 0 and self.stat.enabled:
                if not self.w.enableButton.isChecked():
                    self.w.enableButton.setChecked(True)
                    self.w.enableButton.setText("Disable")
                    self.w.enableButton.setStyleSheet("QPushButton { background-color: green; }")
            else:
                if self.w.enableButton.isChecked():
                    self.w.enableButton.setChecked(False)
                    self.w.enableButton.setText("Enable")
                    self.w.enableButton.setStyleSheet("")
        except:
            pass

    def keyPressEvent(self, event):
        """Handle keyboard jog"""
        if event.key() == Qt.Key_Right:
            self.jog_start(True)
        elif event.key() == Qt.Key_Left:
            self.jog_start(False)

    def keyReleaseEvent(self, event):
        """Stop jog on key release"""
        if event.key() in (Qt.Key_Right, Qt.Key_Left):
            self.jog_stop()

def get_handlers(halcomp, widgets, paths):
    return [HandlerClass(halcomp, widgets, paths)]
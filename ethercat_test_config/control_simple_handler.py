#!/usr/bin/env python3
# ULTRA SIMPLE QtVCP Panel Handler
# Minimal code for single axis jog control

from PyQt5.QtCore import Qt, QTimer
from qtvcp.core import Status
from qtvcp import logger
import linuxcnc

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

        # Timer for position updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_position)
        self.timer.start(100)  # Update every 100ms

    def initialized__(self):
        # Connect buttons
        self.w.jogPosButton.pressed.connect(lambda: self.jog(True))
        self.w.jogPosButton.released.connect(self.stop_jog)
        self.w.jogNegButton.pressed.connect(lambda: self.jog(False))
        self.w.jogNegButton.released.connect(self.stop_jog)

        self.w.enableButton.clicked.connect(self.toggle_enable)
        self.w.stopButton.clicked.connect(self.emergency_stop)

        # Start with machine in E-stop, user needs to enable
        LOG.info("Machine started in E-stop state. Click 'Enable' to start.")

    def jog(self, positive):
        """Start jogging"""
        # Check if machine is enabled first
        self.stat.poll()
        if self.stat.task_state != linuxcnc.STATE_ON:
            LOG.warning("Machine must be enabled to jog")
            return

        if positive:
            self.hal["jog-pos"] = True
            self.hal["jog-neg"] = False
            COMMAND.jog(linuxcnc.JOG_CONTINUOUS, 0, 0, 10)  # X axis, positive, 10mm/s
        else:
            self.hal["jog-pos"] = False
            self.hal["jog-neg"] = True
            COMMAND.jog(linuxcnc.JOG_CONTINUOUS, 0, 0, -10)  # X axis, negative, 10mm/s

    def stop_jog(self):
        """Stop jogging"""
        self.hal["jog-pos"] = False
        self.hal["jog-neg"] = False
        COMMAND.jog(linuxcnc.JOG_STOP, 0, 0)

    def toggle_enable(self):
        """Toggle machine enable"""
        self.stat.poll()
        if self.w.enableButton.isChecked():
            # Reset E-stop first
            COMMAND.state(linuxcnc.STATE_ESTOP_RESET)
            COMMAND.wait_complete()
            # Then turn machine on
            COMMAND.state(linuxcnc.STATE_ON)
            COMMAND.wait_complete()
            self.w.enableButton.setText("Disable")
            self.w.enableButton.setStyleSheet("QPushButton { background-color: green; }")
        else:
            COMMAND.state(linuxcnc.STATE_OFF)
            self.w.enableButton.setText("Enable")
            self.w.enableButton.setStyleSheet("")

    def emergency_stop(self):
        """Emergency stop"""
        COMMAND.state(linuxcnc.STATE_ESTOP)
        self.stop_jog()

    def update_position(self):
        """Update position display"""
        try:
            self.stat.poll()
            pos = self.stat.position[0]  # Get X axis position
            self.w.positionDisplay.setText(f"{pos:.3f}")
        except:
            pass

    def keyPressEvent(self, event):
        """Handle keyboard jog"""
        if event.key() == Qt.Key_Right:
            self.jog(True)
        elif event.key() == Qt.Key_Left:
            self.jog(False)

    def keyReleaseEvent(self, event):
        """Stop jog on key release"""
        if event.key() in (Qt.Key_Right, Qt.Key_Left):
            self.stop_jog()

def get_handlers(halcomp, widgets, paths):
    return [HandlerClass(halcomp, widgets, paths)]
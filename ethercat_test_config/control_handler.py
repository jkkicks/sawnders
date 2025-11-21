#!/usr/bin/env python3
# ULTRA SIMPLE QtVCP Panel Handler
# Minimal code for single axis jog control

from PyQt5.QtCore import Qt, QTimer
from qtvcp.core import Status, Command

STATUS = Status()
COMMAND = Command()

class HandlerClass:
    def __init__(self, halcomp, widgets, paths):
        self.hal = halcomp
        self.w = widgets

        # Create HAL pins for jogging
        self.hal.newpin("jog-pos", self.hal.HAL_BIT, self.hal.HAL_OUT)
        self.hal.newpin("jog-neg", self.hal.HAL_BIT, self.hal.HAL_OUT)
        self.hal.newpin("position", self.hal.HAL_FLOAT, self.hal.HAL_IN)

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

    def jog(self, positive):
        """Start jogging"""
        if positive:
            self.hal["jog-pos"] = True
            self.hal["jog-neg"] = False
        else:
            self.hal["jog-pos"] = False
            self.hal["jog-neg"] = True

    def stop_jog(self):
        """Stop jogging"""
        self.hal["jog-pos"] = False
        self.hal["jog-neg"] = False

    def toggle_enable(self):
        """Toggle machine enable"""
        if self.w.enableButton.isChecked():
            COMMAND.state(self.COMMAND.STATE_ON)
        else:
            COMMAND.state(self.COMMAND.STATE_OFF)

    def emergency_stop(self):
        """Emergency stop"""
        COMMAND.state(self.COMMAND.STATE_ESTOP)
        self.stop_jog()

    def update_position(self):
        """Update position display"""
        try:
            pos = STATUS.get_position()[0]  # Get X axis position
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
#!/usr/bin/env python3
"""
QtVCP Handler for John Sawnders UI Panel
Provides tab switching and UI interaction logic
"""

from PyQt5.QtCore import Qt, QTimer, pyqtSlot
from PyQt5.QtWidgets import QMessageBox, QDialog
from PyQt5.QtGui import QColor
import linuxcnc
import sys
import os

# LinuxCNC interfaces
STAT = linuxcnc.stat()
COMMAND = linuxcnc.command()

class HandlerClass:
    """Main handler class for the UI panel"""

    def __init__(self, halcomp, widgets, paths):
        """Initialize the handler

        Args:
            halcomp: HAL component
            widgets: UI widgets object
            paths: QtVCP paths
        """
        self.hal = halcomp
        self.w = widgets
        self.paths = paths

        print("UI Panel Handler initializing...")

        # Create HAL pins for UI elements
        self.hal.newpin("lift-head", self.hal.HAL_BIT, self.hal.HAL_OUT)
        self.hal.newpin("lower-head", self.hal.HAL_BIT, self.hal.HAL_OUT)
        self.hal.newpin("clamp-fv", self.hal.HAL_BIT, self.hal.HAL_OUT)
        self.hal.newpin("unclamp-fv", self.hal.HAL_BIT, self.hal.HAL_OUT)
        self.hal.newpin("clamp-mv", self.hal.HAL_BIT, self.hal.HAL_OUT)
        self.hal.newpin("unclamp-mv", self.hal.HAL_BIT, self.hal.HAL_OUT)
        self.hal.newpin("cut-active", self.hal.HAL_BIT, self.hal.HAL_OUT)

        # Status tracking
        self.program_running = False
        self.program_paused = False
        self.machine_on = False

        # Timer for periodic updates
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.periodic_update)
        self.update_timer.start(100)  # Update every 100ms

        # Settings storage (in real app, would persist to file)
        self.settings = {
            'setting1': False,
            'setting2': False,
            'setting3': False,
            'setting4': False
        }

    def initialized__(self):
        """Called after UI is fully loaded"""
        print("UI Panel Handler initialized, connecting signals...")

        # Connect Auto Mode buttons
        self.w.startButton.clicked.connect(self.on_start_clicked)
        self.w.pauseButton.clicked.connect(self.on_pause_clicked)
        self.w.stopButton.clicked.connect(self.on_stop_clicked)

        # Connect Manual Mode buttons
        self.w.liftHeadButton.pressed.connect(self.on_lift_head_pressed)
        self.w.liftHeadButton.released.connect(self.on_lift_head_released)
        self.w.lowerHeadButton.pressed.connect(self.on_lower_head_pressed)
        self.w.lowerHeadButton.released.connect(self.on_lower_head_released)

        self.w.clampFVButton.clicked.connect(self.on_clamp_fv_clicked)
        self.w.unclampFVButton.clicked.connect(self.on_unclamp_fv_clicked)
        self.w.clampMVButton.clicked.connect(self.on_clamp_mv_clicked)
        self.w.unclampMVButton.clicked.connect(self.on_unclamp_mv_clicked)

        self.w.cutButton.clicked.connect(self.on_cut_clicked)
        self.w.manualStopButton.clicked.connect(self.on_manual_stop_clicked)

        # Connect Settings buttons
        self.w.saveButton.clicked.connect(self.on_save_settings)
        self.w.cancelButton.clicked.connect(self.on_cancel_settings)

        # Connect settings toggles
        self.w.setting1Toggle.stateChanged.connect(lambda state: self.on_setting_changed('setting1', state))
        self.w.setting2Toggle.stateChanged.connect(lambda state: self.on_setting_changed('setting2', state))
        self.w.setting3Toggle.stateChanged.connect(lambda state: self.on_setting_changed('setting3', state))
        self.w.setting4Toggle.stateChanged.connect(lambda state: self.on_setting_changed('setting4', state))

        # Tab change handler
        self.w.tabWidget.currentChanged.connect(self.on_tab_changed)

        print("All signals connected!")

    # Auto Mode handlers
    def on_start_clicked(self):
        """Handle Start button in Auto Mode"""
        print("Start button clicked")
        try:
            STAT.poll()
            if STAT.task_state == linuxcnc.STATE_ON:
                if self.program_paused:
                    # Resume from pause
                    COMMAND.auto(linuxcnc.AUTO_RESUME)
                    self.program_paused = False
                    print("Program resumed")
                else:
                    # Start new program
                    COMMAND.mode(linuxcnc.MODE_AUTO)
                    COMMAND.wait_complete()
                    COMMAND.auto(linuxcnc.AUTO_RUN, 0)
                    self.program_running = True
                    print("Program started")
                self.update_button_states()
        except Exception as e:
            print(f"Error starting program: {e}")
            self.show_error("Failed to start program", str(e))

    def on_pause_clicked(self):
        """Handle Pause button in Auto Mode"""
        print("Pause button clicked")
        try:
            if self.program_running:
                COMMAND.auto(linuxcnc.AUTO_PAUSE)
                self.program_paused = True
                print("Program paused")
                self.update_button_states()
        except Exception as e:
            print(f"Error pausing program: {e}")

    def on_stop_clicked(self):
        """Handle Stop button in Auto Mode"""
        print("Stop button clicked")
        try:
            COMMAND.abort()
            self.program_running = False
            self.program_paused = False
            print("Program stopped")
            self.update_button_states()
        except Exception as e:
            print(f"Error stopping program: {e}")

    # Manual Mode handlers
    def on_lift_head_pressed(self):
        """Handle Lift Head button press"""
        print("Lift Head pressed")
        self.hal["lift-head"] = True

    def on_lift_head_released(self):
        """Handle Lift Head button release"""
        print("Lift Head released")
        self.hal["lift-head"] = False

    def on_lower_head_pressed(self):
        """Handle Lower Head button press"""
        print("Lower Head pressed")
        self.hal["lower-head"] = True

    def on_lower_head_released(self):
        """Handle Lower Head button release"""
        print("Lower Head released")
        self.hal["lower-head"] = False

    def on_clamp_fv_clicked(self):
        """Handle Clamp Fixed Vice button"""
        print("Clamp Fixed Vice clicked")
        self.hal["clamp-fv"] = True
        QTimer.singleShot(1000, lambda: setattr(self.hal, "clamp-fv", False))
        self.show_info("Vice Control", "Fixed Vice Clamped")

    def on_unclamp_fv_clicked(self):
        """Handle Unclamp Fixed Vice button"""
        print("Unclamp Fixed Vice clicked")
        self.hal["unclamp-fv"] = True
        QTimer.singleShot(1000, lambda: setattr(self.hal, "unclamp-fv", False))
        self.show_info("Vice Control", "Fixed Vice Unclamped")

    def on_clamp_mv_clicked(self):
        """Handle Clamp Moving Vice button"""
        print("Clamp Moving Vice clicked")
        self.hal["clamp-mv"] = True
        QTimer.singleShot(1000, lambda: setattr(self.hal, "clamp-mv", False))
        self.show_info("Vice Control", "Moving Vice Clamped")

    def on_unclamp_mv_clicked(self):
        """Handle Unclamp Moving Vice button"""
        print("Unclamp Moving Vice clicked")
        self.hal["unclamp-mv"] = True
        QTimer.singleShot(1000, lambda: setattr(self.hal, "unclamp-mv", False))
        self.show_info("Vice Control", "Moving Vice Unclamped")

    def on_cut_clicked(self):
        """Handle Cut button in Manual Mode"""
        print("Cut! button clicked")
        self.hal["cut-active"] = True
        QTimer.singleShot(2000, lambda: setattr(self.hal, "cut-active", False))
        self.show_info("Manual Operation", "Cutting operation started")

    def on_manual_stop_clicked(self):
        """Handle Stop button in Manual Mode"""
        print("Manual Stop clicked")
        # Stop all manual operations
        self.hal["lift-head"] = False
        self.hal["lower-head"] = False
        self.hal["cut-active"] = False
        self.show_warning("Manual Mode", "All manual operations stopped")

    # Settings handlers
    def on_setting_changed(self, setting_name, state):
        """Handle settings toggle change"""
        self.settings[setting_name] = (state == Qt.Checked)
        print(f"Setting {setting_name} changed to {self.settings[setting_name]}")

    def on_save_settings(self):
        """Handle Save button in Settings"""
        print("Saving settings...")
        # In a real application, would save to file
        self.show_info("Settings", "Settings saved successfully")

    def on_cancel_settings(self):
        """Handle Cancel button in Settings"""
        print("Canceling settings changes...")
        # Reset toggles to saved values
        self.w.setting1Toggle.setChecked(self.settings.get('setting1', False))
        self.w.setting2Toggle.setChecked(self.settings.get('setting2', False))
        self.w.setting3Toggle.setChecked(self.settings.get('setting3', False))
        self.w.setting4Toggle.setChecked(self.settings.get('setting4', False))
        self.show_info("Settings", "Changes canceled")

    def on_tab_changed(self, index):
        """Handle tab change"""
        tab_names = ["Auto Mode", "Manual Mode", "Settings"]
        print(f"Switched to {tab_names[index]}")

        # Update UI based on current tab
        if index == 0:  # Auto Mode
            self.update_gcode_preview()
        elif index == 1:  # Manual Mode
            self.update_position_readouts()

    # Update methods
    def periodic_update(self):
        """Periodic status update"""
        try:
            STAT.poll()

            # Update status chips
            self.update_status_indicators()

            # Update position readouts if on Manual tab
            if self.w.tabWidget.currentIndex() == 1:
                self.update_position_readouts()

        except Exception as e:
            pass  # Silently handle errors in periodic update

    def update_status_indicators(self):
        """Update the status indicator chips"""
        try:
            # Status 1: Machine state
            if STAT.task_state == linuxcnc.STATE_ESTOP:
                self.w.statusChip1.setText("E-STOP")
                self.w.statusChip1.setStyleSheet("background-color: #b83219; border-radius: 9px; padding: 5px 10px;")
            elif STAT.task_state == linuxcnc.STATE_OFF:
                self.w.statusChip1.setText("OFF")
                self.w.statusChip1.setStyleSheet("background-color: #ffa500; border-radius: 9px; padding: 5px 10px;")
            elif STAT.task_state == linuxcnc.STATE_ON:
                self.w.statusChip1.setText("ON")
                self.w.statusChip1.setStyleSheet("background-color: #5da21f; border-radius: 9px; padding: 5px 10px;")

            # Status 2: Program state
            if self.program_running:
                if self.program_paused:
                    self.w.statusChip2.setText("PAUSED")
                    self.w.statusChip2.setStyleSheet("background-color: #ffa500; border-radius: 9px; padding: 5px 10px;")
                else:
                    self.w.statusChip2.setText("RUNNING")
                    self.w.statusChip2.setStyleSheet("background-color: #5da21f; border-radius: 9px; padding: 5px 10px;")
            else:
                self.w.statusChip2.setText("IDLE")
                self.w.statusChip2.setStyleSheet("background-color: #2b2b2b; border-radius: 9px; padding: 5px 10px;")

            # Status 3: Mode
            if STAT.task_mode == linuxcnc.MODE_MDI:
                self.w.statusChip3.setText("MDI")
            elif STAT.task_mode == linuxcnc.MODE_AUTO:
                self.w.statusChip3.setText("AUTO")
            elif STAT.task_mode == linuxcnc.MODE_MANUAL:
                self.w.statusChip3.setText("MANUAL")
            else:
                self.w.statusChip3.setText("UNKNOWN")

        except Exception as e:
            pass

    def update_button_states(self):
        """Update button enable states based on machine state"""
        try:
            # Auto mode buttons
            can_start = not self.program_running or self.program_paused
            self.w.startButton.setEnabled(can_start)
            self.w.pauseButton.setEnabled(self.program_running and not self.program_paused)
            self.w.stopButton.setEnabled(self.program_running)
        except Exception as e:
            print(f"Error updating button states: {e}")

    def update_position_readouts(self):
        """Update position displays in Manual Mode"""
        try:
            # Get current position
            z_pos = STAT.position[2]  # Z axis position

            # Update readouts
            self.w.headHeightReadout.setText(f"{z_pos:.3f}\"   Head Height")
            self.w.zAxisReadout.setText(f"{z_pos:.3f}\"   Z Axis")
        except Exception as e:
            pass

    def update_gcode_preview(self):
        """Update G-code preview in Auto Mode"""
        # In a real implementation, would load and display actual G-code
        pass

    # Helper methods for dialogs
    def show_info(self, title, message):
        """Show information dialog"""
        if hasattr(self.w, 'show'):  # Only show if UI is visible
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle(title)
            msg.setText(message)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    def show_warning(self, title, message):
        """Show warning dialog"""
        if hasattr(self.w, 'show'):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle(title)
            msg.setText(message)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    def show_error(self, title, message):
        """Show error dialog"""
        if hasattr(self.w, 'show'):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle(title)
            msg.setText(message)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    def closing_cleanup__(self):
        """Called when the UI is closing"""
        print("UI Panel Handler shutting down...")
        self.update_timer.stop()

def get_handlers(halcomp, widgets, paths):
    """Required function that returns handler instances"""
    return [HandlerClass(halcomp, widgets, paths)]
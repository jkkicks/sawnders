#!/usr/bin/env python3
# ULTRA SIMPLE QtVCP Panel Handler
# Minimal code for single axis jog control

from PyQt5.QtCore import Qt, QTimer
import linuxcnc
import sys

# Create command and stat channels
STAT = linuxcnc.stat()
COMMAND = linuxcnc.command()

class HandlerClass:
    def __init__(self, halcomp, widgets, paths):
        self.hal = halcomp
        self.w = widgets

        print("Handler initializing...")

        # Create HAL pins for jogging
        self.hal.newpin("jog-pos", self.hal.HAL_BIT, self.hal.HAL_OUT)
        self.hal.newpin("jog-neg", self.hal.HAL_BIT, self.hal.HAL_OUT)

        # Timer for position updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_position)
        self.timer.start(250)  # Update every 250ms (slower to reduce load)

    def initialized__(self):
        print("Handler initialized, connecting buttons...")

        # Connect buttons - use lambda to ensure we capture the event
        self.w.enableButton.clicked.connect(self.enable_clicked)
        self.w.stopButton.clicked.connect(self.stop_clicked)
        self.w.homeButton.clicked.connect(self.home_clicked)

        self.w.jogPosButton.pressed.connect(self.jog_pos_pressed)
        self.w.jogPosButton.released.connect(self.jog_released)
        self.w.jogNegButton.pressed.connect(self.jog_neg_pressed)
        self.w.jogNegButton.released.connect(self.jog_released)

        print("Buttons connected!")

    def enable_clicked(self):
        """Handle enable button click"""
        print("Enable button clicked!")
        import time

        try:
            if self.w.enableButton.isChecked():
                # Get initial state
                STAT.poll()
                print(f"Initial state - E-stop: {STAT.estop}, Enabled: {STAT.enabled}, Task mode: {STAT.task_mode}, Task state: {STAT.task_state}")

                # Make sure we're in manual mode
                print("Setting mode to MANUAL...")
                COMMAND.mode(linuxcnc.MODE_MANUAL)
                time.sleep(0.2)

                # Try multiple times to reset E-stop
                for attempt in range(3):
                    STAT.poll()
                    if STAT.estop != 0:
                        print(f"Attempt {attempt + 1}: Resetting E-stop...")
                        COMMAND.state(linuxcnc.STATE_ESTOP_RESET)
                        time.sleep(0.5)

                        STAT.poll()
                        if STAT.estop == 0:
                            print("E-stop successfully reset!")
                            break
                        else:
                            print(f"E-stop still active after attempt {attempt + 1}")
                    else:
                        print("E-stop already reset")
                        break

                # Now try to turn on if E-stop is clear
                STAT.poll()
                if STAT.estop == 0:
                    print("Turning machine ON...")
                    COMMAND.state(linuxcnc.STATE_ON)
                    time.sleep(0.5)

                    # Check final state
                    STAT.poll()
                    print(f"Final state - E-stop: {STAT.estop}, Enabled: {STAT.enabled}, Task state: {STAT.task_state}")

                    if STAT.enabled:
                        self.w.enableButton.setText("Disable")
                        self.w.enableButton.setStyleSheet("background-color: green;")
                        print("SUCCESS! Machine is enabled!")

                        # Don't auto-home - let user do it manually if needed
                        if not STAT.homed[0]:
                            print("Note: Joint 0 is not homed. Click 'Home All' if needed.")
                    else:
                        print("Machine not fully enabled yet")
                        print(f"Task state value: {STAT.task_state}")
                        print(f"STATE_ON value: {linuxcnc.STATE_ON}")

                        # Force it one more time
                        print("Forcing machine ON state...")
                        COMMAND.state(linuxcnc.STATE_ON)
                else:
                    print("ERROR: Could not reset E-stop after 3 attempts!")
                    print("This might be a HAL configuration issue.")
                    self.w.enableButton.setChecked(False)

            else:
                print("Disabling machine...")
                COMMAND.state(linuxcnc.STATE_OFF)
                self.w.enableButton.setText("Enable")
                self.w.enableButton.setStyleSheet("")
                print("Machine disabled")

        except Exception as e:
            print(f"Error in enable_clicked: {e}")
            import traceback
            traceback.print_exc()
            self.w.enableButton.setChecked(False)

    def stop_clicked(self):
        """Handle stop button click"""
        print("STOP button clicked!")
        try:
            COMMAND.state(linuxcnc.STATE_ESTOP)
            self.w.enableButton.setChecked(False)
            self.w.enableButton.setText("Enable")
            self.w.enableButton.setStyleSheet("")
            print("E-STOP activated")
        except Exception as e:
            print(f"Error in stop_clicked: {e}")

    def home_clicked(self):
        """Handle home button click"""
        print("Home button clicked!")
        import time
        try:
            STAT.poll()
            if STAT.enabled:
                print("Homing joint 0...")
                COMMAND.home(0)  # Home joint 0 (X axis)

                # Wait a moment for homing to complete
                time.sleep(0.5)
                STAT.poll()

                if STAT.homed[0]:
                    print("SUCCESS! Joint 0 is now homed!")
                    self.w.positionDisplay.setText("HOMED: 0.000")
                else:
                    print("Homing in progress or failed...")
                    print(f"Homed status: {STAT.homed}")
            else:
                print("Machine must be enabled before homing")
        except Exception as e:
            print(f"Error in home_clicked: {e}")

    def jog_pos_pressed(self):
        """Start positive jog"""
        print("Jog+ pressed")
        try:
            STAT.poll()
            if STAT.enabled:
                # Try axis mode jogging (axis 0 = X)
                # jog(command, axis_or_joint, axis_num, velocity)
                COMMAND.jog(linuxcnc.JOG_CONTINUOUS, 1, 0, 10)  # Axis mode (1), axis 0 (X), +10 units/sec
                self.hal["jog-pos"] = True
                print("Jogging X axis positive")
            else:
                print("Machine not enabled, cannot jog")
        except Exception as e:
            print(f"Error in jog_pos: {e}")
            # Try alternative joint jog format
            try:
                COMMAND.jog(linuxcnc.JOG_CONTINUOUS, 0, 10)
                print("Using alternative jog format")
            except:
                pass

    def jog_neg_pressed(self):
        """Start negative jog"""
        print("Jog- pressed")
        try:
            STAT.poll()
            if STAT.enabled:
                # Try axis mode jogging (axis 0 = X)
                # jog(command, axis_or_joint, axis_num, velocity)
                COMMAND.jog(linuxcnc.JOG_CONTINUOUS, 1, 0, -10)  # Axis mode (1), axis 0 (X), -10 units/sec
                self.hal["jog-neg"] = True
                print("Jogging X axis negative")
            else:
                print("Machine not enabled, cannot jog")
        except Exception as e:
            print(f"Error in jog_neg: {e}")
            # Try alternative joint jog format
            try:
                COMMAND.jog(linuxcnc.JOG_CONTINUOUS, 0, -10)
                print("Using alternative jog format")
            except:
                pass

    def jog_released(self):
        """Stop jogging"""
        print("Jog released")
        try:
            # Stop axis 0 (X)
            COMMAND.jog(linuxcnc.JOG_STOP, 1, 0)  # Axis mode, axis 0
            self.hal["jog-pos"] = False
            self.hal["jog-neg"] = False
            print("Jog stopped")
        except Exception as e:
            print(f"Error stopping jog: {e}")
            # Try alternative stop format
            try:
                COMMAND.jog(linuxcnc.JOG_STOP, 0)
                print("Using alternative stop format")
            except:
                pass

    def update_position(self):
        """Update position display"""
        try:
            STAT.poll()
            pos = STAT.position[0]

            # Show position and state
            if STAT.estop:
                self.w.positionDisplay.setText("E-STOP")
            elif not STAT.enabled:
                self.w.positionDisplay.setText("DISABLED")
            else:
                # Show homed status with position
                if STAT.homed[0]:
                    self.w.positionDisplay.setText(f"✓ {pos:.3f}")
                else:
                    self.w.positionDisplay.setText(f"? {pos:.3f}")

            # Keep button state in sync
            if STAT.enabled and not self.w.enableButton.isChecked():
                self.w.enableButton.setChecked(True)
                self.w.enableButton.setText("Disable")
                self.w.enableButton.setStyleSheet("background-color: green;")
            elif not STAT.enabled and self.w.enableButton.isChecked():
                self.w.enableButton.setChecked(False)
                self.w.enableButton.setText("Enable")
                self.w.enableButton.setStyleSheet("")

            # Update home button color based on homed status
            if STAT.homed[0]:
                self.w.homeButton.setStyleSheet("background-color: lightgreen;")
            else:
                self.w.homeButton.setStyleSheet("")
        except:
            pass

def get_handlers(halcomp, widgets, paths):
    return [HandlerClass(halcomp, widgets, paths)]
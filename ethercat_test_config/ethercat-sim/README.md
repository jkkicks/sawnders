# EtherCAT Simulator Configuration

This folder contains the simulator configuration for testing LinuxCNC with a simulated single-axis system without requiring actual EtherCAT hardware.

## Files

- `ethercat_sim.ini` - LinuxCNC configuration file for the simulator
- `ethercat_sim.hal` - HAL configuration for simulated motor
- `control_simple.ui` - Qt Designer UI file for the simple control panel
- `vcp.py` - QtVCP handler file for the control panel

## Usage

To run the simulator:
```bash
linuxcnc ethercat_sim.ini
```

## Features

- Single X-axis simulation
- Simple jog controls (+ and -)
- Enable/Disable machine control
- E-Stop button
- Home button
- Position display with homing status

## Purpose

This configuration is useful for:
- Testing UI changes without hardware
- Developing control logic
- Learning LinuxCNC/QtVCP basics
- Debugging HAL configurations
# EtherCAT Raspberry Pi Test Configuration

This folder contains the real hardware configuration for testing LinuxCNC with EtherCAT on a Raspberry Pi 4B.

## Files

- `ethercat.ini` - LinuxCNC configuration file for EtherCAT hardware
- `ethercat.hal` - HAL configuration for EtherCAT motor control
- `control.ui` - Qt Designer UI file for the control panel
- `control_handler.py` - QtVCP handler file for the control panel

## Usage

To run on Raspberry Pi with EtherCAT hardware:
```bash
linuxcnc ethercat.ini
```

## Requirements

- Raspberry Pi 4B
- EtherCAT master installed
- EtherCAT servo drive connected
- LinuxCNC with EtherCAT support

## Features

- Single X-axis EtherCAT control
- Advanced control panel with more options than simulator
- Real hardware motor control
- Position feedback from EtherCAT drive

## Purpose

This configuration is for:
- Testing real EtherCAT hardware
- Production single-axis control
- Hardware integration testing
- Performance validation on Raspberry Pi
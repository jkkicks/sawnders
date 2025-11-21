# Simple EtherCAT Single Axis Control

EXTREMELY SIMPLE implementation for controlling one axis via EtherCAT with QtVCP panel.

## Files:
- `ethercat.ini` - Minimal INI configuration
- `ethercat.hal` - Basic HAL setup for EtherCAT
- `control.ui` - QtVCP UI (position display + jog buttons)
- `vcp.py` - Minimal Python handler

## Features:
- Single X axis control
- Jog with buttons or arrow keys (← →)
- Real-time position display
- Enable/Disable and Emergency Stop buttons

## To Run:
```bash
linuxcnc ethercat.ini
```

## Requirements:
- LinuxCNC with QtVCP support
- LinuxCNC-EtherCAT installed
- EtherCAT device configured

## Notes:
- Adjust EtherCAT device address in HAL file (currently lcec.0.0)
- Modify axis limits in INI file as needed
- Jog speed is set to 10 mm/s (change in HAL)
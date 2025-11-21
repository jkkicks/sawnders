# Simple EtherCAT Single Axis Control

EXTREMELY SIMPLE implementation for controlling one axis via EtherCAT with QtVCP panel.

## Quick Start (No Hardware Required)

### Test Without EtherCAT Hardware:
```bash
# Run the simulator version to test the UI immediately
linuxcnc ethercat_sim.ini
```

This simulator version lets you test the jogging UI and position display without any hardware connected.

## Files

### For Testing (No Hardware):
- `ethercat_sim.ini` - Simulator configuration
- `ethercat_sim.hal` - Simulated HAL (no hardware needed)
- `control.ui` - QtVCP UI (position display + jog buttons)
- `vcp.py` - Minimal Python handler
- `tool.tbl` - Tool table file

### For Real EtherCAT Hardware:
- `ethercat.ini` - Real EtherCAT configuration
- `ethercat.hal` - HAL setup for EtherCAT hardware

## Features:
- Single X axis control
- Jog with buttons or arrow keys (← →)
- Real-time position display
- Enable/Disable and Emergency Stop buttons

## Installation & Setup

### Step 1: Test Without Hardware
```bash
cd ~/linuxcnc/sawnders/ethercat_test_config
linuxcnc ethercat_sim.ini
```

### Step 2: Install EtherCAT Support (For Real Hardware)

#### Option A: Install from Package (Easiest)
```bash
sudo apt update
sudo apt install linuxcnc-ethercat
```

#### Option B: Build from Source (If Package Not Available)
```bash
# Install dependencies
sudo apt-get update
sudo apt-get install git build-essential automake autoconf libtool

# Clone and build LinuxCNC-EtherCAT
cd ~/
git clone https://github.com/linuxcnc-ethercat/linuxcnc-ethercat.git
cd linuxcnc-ethercat
make
sudo make install

# For EtherLab master (if needed):
cd ~/
git clone https://gitlab.com/etherlab.org/ethercat.git
cd ethercat
./bootstrap
./configure --enable-generic --disable-8139too --disable-eoe --enable-cycles
make
sudo make install
sudo modprobe ec_master
sudo modprobe ec_generic
```

### Step 3: Run with Real Hardware
```bash
linuxcnc ethercat.ini
```

## Troubleshooting

### Error: "lcec.so: cannot open shared object file"
- **Solution**: LinuxCNC-EtherCAT is not installed. See installation steps above.
- **Quick Fix**: Use `ethercat_sim.ini` for testing without hardware

### Error: "can't load tool table"
- **Solution**: Already fixed - `tool.tbl` file is now included

### Error: Version/update dialog appears
- **Solution**: Already fixed - configs are now compatible with LinuxCNC 2.8+

## Configuration Notes:
- Adjust EtherCAT device address in HAL file (currently lcec.0.0)
- Modify axis limits in INI file as needed
- Jog speed is set to 10 mm/s (change in HAL)
- Works on Raspberry Pi 4B with LinuxCNC 2.9+
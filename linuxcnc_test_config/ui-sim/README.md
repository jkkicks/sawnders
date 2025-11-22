# John Sawnders UI Simulator

This is a QtVCP-based UI simulator for LinuxCNC, designed to test and develop the user interface without requiring actual hardware.

## Overview

The UI implements a three-tab interface based on the HTML reference designs:
- **Auto Mode**: For running G-code programs with start/pause/stop controls
- **Manual Mode**: For manual machine operations (lift/lower head, vice control, cutting)
- **Settings**: For configuration options

## Files

- `ui_sim.ini` - LinuxCNC configuration file for the simulator
- `ui_sim.hal` - Minimal HAL configuration for simulation
- `ui_panel.ui` - Qt Designer UI file (converted from HTML references)
- `ui_panel_handler.py` - Python handler with UI logic
- `reference/` - Original HTML design files

## Features

### Auto Mode Tab
- Start/Pause/Stop buttons for program control
- G-code preview window
- Visualizer placeholder window
- Status indicators

### Manual Mode Tab
- Lift/Lower Head controls (press and hold)
- Fixed Vice Clamp/Unclamp
- Moving Vice Clamp/Unclamp
- Position readouts (Head Height, Z Axis)
- Cut and Stop buttons

### Settings Tab
- Four configurable settings with toggle switches
- Save/Cancel buttons
- Grid layout for settings organization

### Status Bar
- Three status chips showing machine state
- Version information display

## Running the Simulator

To run the UI simulator:

```bash
cd linuxcnc_test_config/ui-sim
linuxcnc ui_sim.ini
```

## UI Design

The interface uses:
- Dark theme (#1c1c1c background, #121212 content area)
- Color coding:
  - Green (#5da21f) for active/start operations
  - Red (#b83219) for stop/danger operations
  - Orange (#ffa500) for warnings/clamp operations
  - Gray (#2b2b2b) for inactive buttons
- Large touch-friendly buttons (48px font, 88px minimum height)
- Jaldi font family for consistency

## HAL Pins Created

The handler creates the following HAL pins:
- `ui_panel.lift-head` (bit, out) - Lift head control
- `ui_panel.lower-head` (bit, out) - Lower head control
- `ui_panel.clamp-fv` (bit, out) - Fixed vice clamp
- `ui_panel.unclamp-fv` (bit, out) - Fixed vice unclamp
- `ui_panel.clamp-mv` (bit, out) - Moving vice clamp
- `ui_panel.unclamp-mv` (bit, out) - Moving vice unclamp
- `ui_panel.cut-active` (bit, out) - Cut operation active

## Modal Dialogs

The UI includes modal dialog support for:
- Information messages (vice control feedback)
- Warning messages (stop operations)
- Error messages (operation failures)
- Settings confirmations

## Development Notes

### Modifying the UI
1. Edit `ui_panel.ui` in Qt Designer
2. Modify styles in the stylesheet section
3. Update handler logic in `ui_panel_handler.py`

### Adding New Features
1. Add widgets in Qt Designer
2. Connect signals in the `initialized__` method
3. Implement handler methods for new functionality
4. Create HAL pins if hardware interface needed

### Testing
- The simulator runs without hardware dependencies
- All manual controls provide visual feedback
- Status indicators update based on LinuxCNC state
- Settings changes are tracked (not persisted in this demo)

## Limitations

This is a UI development simulator:
- No actual machine control
- G-code preview is static placeholder
- Visualizer window is empty placeholder
- Settings are not persisted to file
- Position values are simulated

## Future Enhancements

Potential improvements:
- Load actual G-code files
- Implement 3D visualizer
- Persist settings to file
- Add more machine parameters
- Implement MDI mode
- Add jog controls
- Tool management interface
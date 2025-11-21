# Bandsaw UI Design Specification

## Design Principles

- **Touch-first**: All interactive elements minimum 48x48 pixels
- **High contrast**: Suitable for shop environment
- **Status visibility**: Current state always clear
- **Safe defaults**: Destructive actions require confirmation
- **Responsive feedback**: Immediate visual response to all inputs

## Screen Layout Structure

```
+--------------------------------------------------+
|  STATUS BAR                                      |
|  [Machine State] [Job: 2/5] [Time] [Warnings]   |
+--------------------------------------------------+
|  TAB BAR                                         |
|  [Main] [Queue] [Program] [Manual] [Settings]   |
+--------------------------------------------------+
|                                                  |
|            MAIN CONTENT AREA                     |
|                                                  |
+--------------------------------------------------+
|  PERSISTENT CONTROLS                             |
|  [E-STOP] [Start] [Pause] [Speed: 85%]         |
+--------------------------------------------------+
```

## Screen 1: Main Operation

### Layout
```
+------------------------+------------------------+
|   CURRENT JOB INFO     |    POSITION DISPLAY    |
|   Material: 4140       |    Z: 0.000            |
|   Cut Length: 5.000"   |    Head: 4.500"        |
|   Piece: 2 of 5        |    [Visual Height Bar] |
+------------------------+------------------------+
|              MACHINE STATUS                     |
|   [READY] [SPINDLE ON] [VICES CLAMPED]        |
+--------------------------------------------------+
|              CYCLE CONTROLS                      |
|   [START CUT]  [PAUSE]  [STOP]                 |
|                                                  |
|   Feed Override: [-----|-----] 100%            |
|   Speed Override: [-----|-----] 85%            |
+--------------------------------------------------+
|              MANUAL CONTROLS                     |
| Head: [UP] [DOWN] | Vices: [FIXED] [MOVING]   |
| Shuttle: [<--] [HOME] [-->]                    |
+--------------------------------------------------+
```

### Key Features
- Large status indicators
- Real-time position feedback
- Override sliders always visible
- Quick access to manual controls

## Screen 2: Job Queue

### Layout
```
+--------------------------------------------------+
|  QUEUE CONTROLS                                  |
|  [Add Job] [Clear Complete] [Stop Queue]        |
+--------------------------------------------------+
|  ACTIVE JOB                                      |
|  > Job #001 - 4x4 Square - 5.0" cuts (2/5)     |
|    [==========>........] 60% complete           |
+--------------------------------------------------+
|  QUEUE (Drag to reorder)                        |
|  ☐ Job #002 - 2" Round - 3.5" cuts (0/10)      |
|  ☐ Job #003 - 3x5 Rect - 7.25" cuts (0/3)      |
|  ☐ Job #004 - 2" Pipe - 12.0" cuts (0/8)       |
|                                                  |
|  [Edit] [Delete] [Move Up] [Move Down]          |
+--------------------------------------------------+
|  QUEUE STATS                                     |
|  Total Cuts: 26 | Est. Time: 45 min             |
|  Material Needed: [Show List]                    |
+--------------------------------------------------+
```

### Key Features
- Drag-and-drop reordering
- Visual progress indicators
- Batch operations
- Material requirements summary

## Screen 3: Conversational Programming

### Step 1: Material Selection
```
+--------------------------------------------------+
|  SELECT MATERIAL SHAPE                           |
|                                                  |
|  [■ Square]  [● Round]  [▭ Rectangular]        |
|                                                  |
|  [⬟ Hex]    [⭘ Tube]   [∟ Angle]              |
|                                                  |
+--------------------------------------------------+
```

### Step 2: Dimensions (Adapts to shape)
```
+--------------------------------------------------+
|  ENTER DIMENSIONS (Square Bar)                   |
|                                                  |
|  Side: [  4.000  ] inches                       |
|       [-1] [-0.1] [+0.1] [+1]                  |
|                                                  |
|  Material: [▼ 4140 Steel        ]              |
|                                                  |
|  [Visual Preview Box]                           |
|                                                  |
|  [Back]                    [Next]               |
+--------------------------------------------------+
```

### Step 3: Cut Parameters
```
+--------------------------------------------------+
|  CUT PARAMETERS                                  |
|                                                  |
|  Cut Length: [  5.000  ] inches                 |
|            [-1] [-0.1] [+0.1] [+1]             |
|                                                  |
|  Quantity: [   5   ] pieces                     |
|          [-1] [+1] [+10]                       |
|                                                  |
|  Blade Speed: [ 85 ]%  (Auto-calculated)        |
|             [Override ☐]                        |
|                                                  |
|  Total Material: 25.0 inches                    |
|                                                  |
|  [Back]    [Add to Queue]    [Run Now]         |
+--------------------------------------------------+
```

### Key Features
- Visual shape selector
- Adaptive input fields
- Increment/decrement buttons for touch
- Auto-calculation with override option
- Visual preview where applicable

## Screen 4: Manual G-Code

### Layout
```
+--------------------------------------------------+
|  G-CODE ENTRY                                    |
|  +--------------------------------------------+ |
|  | ; Custom cutting program                   | |
|  | #<_material_height> = 4.0                 | |
|  | #<_cut_length> = 5.0                      | |
|  | ...                                        | |
|  |                                            | |
|  +--------------------------------------------+ |
|                                                  |
|  [Load File] [Save] [Clear] [Insert Template]   |
|                                                  |
|  MDI: [ G0 Z5.0                            ]    |
|       [Execute]                                  |
+--------------------------------------------------+
```

### Key Features
- Syntax highlighting
- Template insertion
- MDI command line
- File operations

## Screen 5: Settings & Maintenance

### Layout
```
+--------------------------------------------------+
|  SETTINGS TABS                                   |
|  [Timing] [Calibration] [Maintenance] [About]   |
+--------------------------------------------------+
|  TIMING ADJUSTMENTS                             |
|                                                  |
|  Vice Clamp Time:    [1.0] seconds             |
|                    [-0.1] [+0.1]               |
|                                                  |
|  Vice Release Time:  [0.5] seconds             |
|                    [-0.1] [+0.1]               |
|                                                  |
|  Head Settle Time:   [0.5] seconds             |
|                    [-0.1] [+0.1]               |
|                                                  |
|  Feed Rate Default:  [10.0] IPM                |
|                    [-1.0] [+1.0]               |
|                                                  |
|  [Apply]  [Reset Defaults]  [Cancel]           |
+--------------------------------------------------+
```

## Color Scheme

```css
/* Primary Colors */
--ready-green:    #00C851
--running-blue:   #0099CC
--warning-yellow: #FFB300
--error-red:      #CC0000
--neutral-gray:   #757575

/* UI Elements */
--background:     #F5F5F5
--card-white:     #FFFFFF
--text-primary:   #212121
--text-secondary: #757575
--border:         #E0E0E0

/* States */
--active:         #2196F3
--inactive:       #BDBDBD
--disabled:       #E0E0E0
```

## Interaction Patterns

### Touch Gestures
- **Tap**: Select/activate
- **Long press**: Show context menu
- **Drag**: Reorder queue items
- **Swipe**: Navigate between tabs
- **Pinch**: Zoom (in G-code view)

### Confirmations Required
- Starting a cut cycle
- Deleting a job
- Clearing the queue
- Changing settings
- E-stop reset

### Visual Feedback
- Button press: Immediate color change
- State change: Animated transition
- Error: Red flash + message
- Success: Green checkmark animation
- Loading: Spinner or progress bar

## Responsive Behavior

### Screen Sizes
- **Primary**: 1024x768 (Standard industrial touchscreen)
- **Minimum**: 800x600
- **Maximum**: 1920x1080

### Scaling Rules
- Text: Minimum 14pt
- Buttons: Minimum 48x48px
- Touch targets: 8px padding minimum
- Maintain aspect ratios for visual elements

## Implementation Notes

### QtVCP Structure
```
sawcontrol/
├── sawcontrol.ui          # Qt Designer file
├── sawcontrol_handler.py  # Python logic
├── sawcontrol.qss         # Stylesheet
├── resources/             # Icons and images
│   ├── icons/
│   └── images/
└── config.ini            # UI configuration
```

### Key Python Handler Methods
```python
def __init__(self):
    # Initialize UI state

def initialized__(self):
    # Connect signals after LinuxCNC ready

def update_job_display(self):
    # Refresh current job info

def handle_queue_change(self):
    # Queue modifications

def start_cut_cycle(self):
    # Begin cutting operation

def update_machine_status(self):
    # Real-time status updates
```

## Next Steps

1. Create HTML/CSS mockups for testing layout
2. Build Qt Designer layouts for each screen
3. Implement Python handlers for business logic
4. Test touch interactions on target hardware
5. Iterate based on operator feedback

---

*Version: 1.0.0 - Initial Design*
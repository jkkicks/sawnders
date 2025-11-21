# Bandsaw CNC Conversion - Design Specification

## System Architecture Overview

This document captures all design decisions for the LinuxCNC bandsaw conversion project. It serves as the single source of truth for implementation.

## Axis and Coordinate System

- **Z-Axis**: Shuttle movement (material positioning) - AC servo via EtherCAT
- **Head Movement**: NOT an axis - controlled via M-codes with analog position feedback
- **Vices**: NOT axes - controlled via M-codes as discrete I/O operations

*Rationale: Similar to surface grinder kinematics where Z is along spindle direction*

## M-Code Definitions

### Vice Control
- **M101**: Clamp fixed vice
- **M102**: Unclamp fixed vice (0.5 second pulse)
- **M103**: Fixed vice neutral (no pressure either direction)
- **M104**: Clamp moving vice (stays clamped)
- **M105**: Ensure moving vice unclamped (minimum 1 second)

### Head Control
- **M64 P1**: Hydraulic lift solenoid ON
- **M65 P1**: Hydraulic lift solenoid OFF
- **M64 P2**: Downfeed solenoid ON (cutting)
- **M65 P2**: Downfeed solenoid OFF
- **M67 E0 Q#**: Set target head height (analog out)
- **M66 P0**: Wait for head at target height
- **M66 P1**: Wait for bottom limit switch (cut complete)

## Head Position Control Strategy

Uses analog feedback with comparator, NOT a full axis:

```hal
# Analog input from draw-wire encoder scaled to inches
net head-pos     hm2.7c81.0.analogin0 => scale.0.in
net head-height  scale.0.out

# Compare actual height to G-code target
net head-height    => comp.0.in1
net target-height  => comp.0.in2
net head-at-target <= comp.0.out

# G-code sets target via analog output
net target-height <= motion.analog-out-00
```

G-code controls head by:
1. Setting target height with M67
2. Activating lift/lower solenoid with M64
3. Waiting for position with M66
4. Stopping solenoid with M65

## G-Code Structure

### File Philosophy
- Each G-code file represents ONE cut operation
- Multiple quantities handled by scheduler (runs same file multiple times)
- G-code files are temporary (generated, executed, deleted on startup)
- Complex operations use subroutine calls
- No material database lookups in G-code

### Standard Cut Cycle Template

```ngc
; === PARAMETERS (Set by conversational or manual edit) ===
#<_material_height> = 4.0        ; Actual material dimension
#<_cut_length> = 5.0             ; Length to cut
#<_blade_speed> = 85             ; Spindle speed percentage
#<_clearance> = 1.0              ; Clearance above material

; === TIMING PARAMETERS (Defaults, can override) ===
#<_vice_clamp_dwell> = 1.0
#<_vice_release_dwell> = 0.5
#<_head_settle_time> = 0.5

; === CALCULATED VALUES ===
#<_head_target> = [#<_material_height> + #<_clearance>]

; === MAIN PROGRAM ===
O<cut_cycle> sub

; Start spindle
S#<_blade_speed> M3
G4 P2.0                          ; Spindle spin-up time

; Initial state
M101                             ; Fixed vice clamp
M105                             ; Moving vice released
G4 P#<_vice_clamp_dwell>

; Feed sequence
G1 Z#<_cut_length> F10          ; Position material
M104                             ; Clamp moving vice
G4 P#<_vice_clamp_dwell>
M102                             ; Release fixed vice pulse
G4 P#<_vice_release_dwell>
M103                             ; Fixed vice neutral
G1 Z0 F10                        ; Shuttle return home
M101                             ; Re-clamp fixed vice
G4 P#<_vice_clamp_dwell>

; Head positioning
M67 E0 Q#<_head_target>          ; Set target height
M64 P1                           ; Lift solenoid ON
M66 P0 L3 Q10                    ; Wait for height (10s timeout)
M65 P1                           ; Lift solenoid OFF
G4 P#<_head_settle_time>

; Cutting
M64 P2                           ; Downfeed ON
M66 P1 L3 Q60                    ; Wait for bottom limit (60s timeout)
M65 P2                           ; Downfeed OFF

; Retract
M67 E0 Q6.0                      ; Safe height
M64 P1                           ; Lift ON
M66 P0 L3 Q10                    ; Wait for height
M65 P1                           ; Lift OFF

O<cut_cycle> endsub

; Program end
M5                               ; Spindle stop
M30
```

## Job Queue System

### Queue File Structure

Single JSON file (`job_queue.json`) as source of truth:

```json
{
  "active_job": null,
  "queue": [
    {
      "id": "job_001",
      "nc_file": "temp_001.ngc",
      "index": 0,
      "status": "pending|running|complete|error",
      "total_qty": 5,
      "completed_qty": 0,
      "metadata": {
        "material_type": "4140 Steel",
        "material_shape": "square|round|rectangular|tube|angle",
        "stock_dimensions": {
          "type": "square",
          "size": 4.0
        },
        "cut_length": 5.0,
        "blade_speed": 85,
        "created_timestamp": "2024-01-20T10:30:00",
        "customer": "Optional",
        "notes": "Optional notes"
      }
    }
  ]
}
```

### Queue Manager Responsibilities
1. Generate temporary G-code from job parameters
2. Load G-code into LinuxCNC
3. Monitor execution status
4. Update completed quantities
5. Delete temporary files after execution
6. Auto-advance to next job (if enabled)

## Material Input Types

Conversational UI adapts input fields based on shape:

| Shape | Required Inputs | Head Clearance Calculation |
|-------|----------------|---------------------------|
| Round | Diameter | diameter + clearance |
| Square | Side dimension | side + clearance |
| Rectangular | Width × Height | height + clearance |
| Hex | Across flats | flats × 1.155 + clearance |
| Tube/Pipe | OD × Wall thickness | OD + clearance |
| Angle | Leg1 × Leg2 × Thickness | max(leg1, leg2) + clearance |

## User Interface Design

### Primary Screens

1. **Main Operation Screen**
   - Current job display
   - Manual controls (jog, vice, head)
   - Spindle speed override
   - E-stop and cycle start/stop

2. **Job Queue Screen**
   - Queue visualization
   - Add/edit/delete jobs
   - Reorder capability
   - Material requirements preview

3. **Conversational Programming**
   - Material shape selector
   - Dimension inputs (adapt to shape)
   - Cut length and quantity
   - Generate and queue job

4. **Manual G-Code Screen**
   - Direct G-code entry
   - File loading
   - MDI mode

5. **Settings/Maintenance**
   - Timing adjustments
   - Calibration
   - Diagnostics

### UI Technology
- **QtVCP** for LinuxCNC integration
- **Touch-optimized** design
- **Python handlers** for business logic

## E-Stop and Safety

### E-Stop Actions
1. Servo: Safe Torque Off (STO)
2. Hydraulic pump: Power killed
3. VFD: Power removed (not just stop command)
4. Solenoids: All de-energized
5. Recovery: Manual only, no automatic recovery

### Safety Interlocks
- No shuttle movement with vices open
- No cutting without fixed vice clamped
- No vice operations during cutting
- Head must be raised before shuttle movement

## Development Phases

### Phase 1: UI and G-Code Format (Current)
- Design UI mockups
- Finalize G-code conventions
- Create job queue structure
- Document workflows

### Phase 2: Proof of Concept
- Raspberry Pi + LinuxCNC setup
- EtherCAT testing with small servo
- Basic HAL configuration
- Simple Python queue manager

### Phase 3: Bench Testing
- MESA 7C81 setup
- Hydraulic valve control
- Encoder feedback testing
- M-code implementation

### Phase 4: Machine Integration
- Physical installation
- Calibration and tuning
- Safety system verification
- Production testing

## Testing Hardware for POC

Before full implementation, test with:
1. Raspberry Pi running LinuxCNC
2. Small EtherCAT servo (bench test)
3. Simple relay board for valve simulation
4. Potentiometer for head position simulation
5. LEDs for valve state visualization

## Configuration Management

- All configs in Git repository
- Separate branches for development/production
- Tagged releases for stable versions
- README files in each directory
- No remote auto-updates initially (manual pull)

---

*Last Updated: [Current Date]*
*Version: 0.1.0 - Pre-Implementation Design*
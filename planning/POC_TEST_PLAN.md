# Proof of Concept Test Plan

## Objective
Validate core technical components before full implementation on actual hardware.

## Test Environment Setup

### Hardware Required
1. **Raspberry Pi 4** (8GB recommended)
   - Running LinuxCNC with RT kernel
   - Ethernet for EtherCAT communication

2. **EtherCAT Components**
   - Small servo drive (any EtherCAT-compatible)
   - OR: Beckhoff EK1100 + EL2004 (digital outputs) for simpler testing

3. **I/O Simulation**
   - Breadboard with LEDs for valve states
   - Potentiometer for head position simulation
   - Pushbuttons for limit switches
   - Relay module (4-channel) for solenoid simulation

4. **Development Machine**
   - For UI development and testing
   - SSH access to Raspberry Pi

## Phase 1: Basic LinuxCNC on Raspberry Pi

### Test 1.1: LinuxCNC Installation
```bash
# Install LinuxCNC on Raspberry Pi
# Document any issues with RT kernel
# Verify servo thread timing achievable
```

**Success Criteria:**
- LinuxCNC runs without RT violations
- Servo thread stable at 1ms
- HAL components load successfully

### Test 1.2: Basic HAL Configuration
```hal
# Create test configuration with:
loadrt hal_pi_gpio
loadrt threads
loadrt and2
loadrt or2
loadrt timedelay

# Map Pi GPIO pins
# Test digital I/O response times
```

**Success Criteria:**
- GPIO pins respond < 10ms
- No missed steps in thread execution
- Can read inputs and set outputs

## Phase 2: EtherCAT Integration

### Test 2.1: EtherCAT Master Setup
```bash
# Install EtherCAT master
sudo apt-get install ethercat-master
# Configure for Raspberry Pi ethernet port
```

**Success Criteria:**
- EtherCAT master initializes
- Can scan and detect slave devices
- Stable communication at 1kHz cycle rate

### Test 2.2: Servo Control via EtherCAT
```hal
# Configure single axis with EtherCAT servo
loadrt lcec
loadrt trivkins
loadrt motmod
```

**Test Operations:**
1. Command position moves
2. Measure response time
3. Test E-stop behavior (STO)
4. Verify position feedback

**Success Criteria:**
- Servo follows commanded position
- Position error < 0.001"
- E-stop immediately disables drive
- Recovery from E-stop works

## Phase 3: M-Code Implementation

### Test 3.1: Vice Control M-Codes
```ngc
; Test vice sequencing
M101  ; Fixed vice clamp
M105  ; Moving vice release
M104  ; Moving vice clamp
M102  ; Fixed vice release pulse
M103  ; Fixed vice neutral
```

**Physical Setup:**
- LEDs indicate valve states
- Timing measurement with oscilloscope/logic analyzer

**Success Criteria:**
- Correct valve sequencing
- Pulse timing accurate (±50ms)
- No overlapping unsafe states

### Test 3.2: Head Control with Analog Feedback
```hal
# Potentiometer simulates draw-wire encoder
net head-position <= hal_pi_gpio.analog0
net head-position => scale.0.in
net scaled-height <= scale.0.out
```

```ngc
; Test head positioning
M67 E0 Q4.5  ; Set target to 4.5"
M64 P1       ; Lift solenoid
M66 P0 L3 Q10  ; Wait for position
M65 P1       ; Stop lift
```

**Success Criteria:**
- Head position tracks potentiometer
- M66 wait completes when position reached
- Timeout works if position not reached

## Phase 4: Job Queue System

### Test 4.1: Queue Manager Basic Operations
```python
# Test script for queue manager
queue = JobQueue("test_queue.json")

# Add jobs
job1 = Job(id="001", cut_length=5.0, qty=3)
queue.add_job(job1)

# Process queue
queue.start_next_job()
```

**Test Cases:**
1. Add single job
2. Add multiple jobs
3. Delete job from queue
4. Reorder queue
5. Save/load queue from file

**Success Criteria:**
- Queue persists across restarts
- JSON file updates correctly
- No race conditions

### Test 4.2: G-Code Generation
```python
# Test conversational to G-code
params = {
    "material_height": 4.0,
    "cut_length": 5.0,
    "blade_speed": 85
}
gcode = generate_gcode(params)
```

**Validation:**
- Generated G-code syntax valid
- Parameters correctly inserted
- File saved to temp location
- Loads in LinuxCNC without errors

## Phase 5: UI Development

### Test 5.1: QtVCP Basic Screen
Create minimal UI with:
- Start/stop button
- Position display
- Status indicator

**Success Criteria:**
- UI launches with LinuxCNC
- HAL pins connect to UI elements
- Real-time updates work

### Test 5.2: Touch Interface
Test on actual touchscreen (or tablet via VNC):
- Button size adequate
- Response time acceptable
- Gesture support works

## Phase 6: Integration Testing

### Test 6.1: Complete Cycle Simulation
Run full cutting cycle with simulated hardware:
1. Load job into queue
2. Start cycle
3. Vice sequencing
4. Head positioning
5. Simulated cut (timer)
6. Retract and complete

**Success Criteria:**
- Complete cycle without errors
- Timing matches expected
- Status updates properly
- Queue advances

### Test 6.2: Error Handling
Test failure modes:
1. E-stop during cut
2. Position feedback loss
3. Timeout conditions
4. Queue file corruption

**Success Criteria:**
- Safe behavior in all cases
- Clear error reporting
- Recovery procedures work

## Performance Benchmarks

### Timing Requirements
| Operation | Target | Maximum |
|-----------|--------|---------|
| GPIO Response | 1ms | 10ms |
| EtherCAT Cycle | 1ms | 2ms |
| UI Update | 100ms | 200ms |
| Vice Operation | 1s | 2s |
| Head Position | 5s | 10s |

### Resource Usage
- CPU Usage: < 70% during operation
- Memory: < 2GB total
- Disk I/O: Minimal except queue updates

## Test Hardware Shopping List

Essential items for POC:
1. Raspberry Pi 4 (8GB) - $75
2. MicroSD Card (32GB) - $10
3. 4-Channel Relay Module - $10
4. Breadboard & Jumpers - $15
5. LEDs, Resistors, Buttons - $10
6. Potentiometer (10k linear) - $5
7. 24V Power Supply - $20

Optional for fuller testing:
1. Small EtherCAT servo kit - $500-800
2. 7" Touchscreen for Pi - $60
3. Logic Analyzer - $30
4. Beckhoff EK1100 + I/O - $300

Total Budget: $150 (minimum) to $1200 (complete)

## Development Milestones

### Week 1-2: Environment Setup
- [ ] LinuxCNC on Pi running
- [ ] Basic HAL configuration
- [ ] GPIO control working

### Week 3-4: M-Code Implementation
- [ ] Vice control logic
- [ ] Head positioning simulation
- [ ] Timing verification

### Week 5-6: Queue System
- [ ] Python queue manager
- [ ] G-code generation
- [ ] File management

### Week 7-8: UI Development
- [ ] Basic QtVCP screens
- [ ] Touch testing
- [ ] Integration with HAL

### Week 9-10: Integration
- [ ] Full cycle testing
- [ ] Error handling
- [ ] Performance optimization

## Documentation During Testing

For each test, document:
1. Configuration files used
2. Issues encountered
3. Solutions/workarounds
4. Performance measurements
5. Photos/videos of operation

This becomes reference for full implementation.

---

*Version: 1.0.0 - Initial POC Plan*
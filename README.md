# LinuxCNC Bandsaw Conversion Project

## Project Goal
Convert a PLC-driven automated bandsaw into a LinuxCNC G-code controlled system with advanced automation capabilities and remote update functionality.

## Current Hardware Overview

### Existing Bandsaw Components
- **Shuttle Movement**: Currently PLC controlled, will add AC servo + ballscrew with 17-bit absolute encoder via EtherCAT
- **Vice System**:
  - Moving vice: Single-acting hydraulic cylinder (spring return)
  - Fixed vice: Double-acting hydraulic cylinder
- **Head Movement**: Hydraulic lift/lower (needs encoder feedback - considering glass scale or draw wire)
- **Blade Speed**: VFD with low voltage start/stop inputs and potentiometer for speed control
- **Fast Downfeed**: Solenoid valve for rapid descent
- **Blade Speed Feedback**: Pulse generator/photo eye on bandsaw pulley

### Planned Control Hardware
- **MESA 7C81**: FPGA card with parallel port breakouts for I/O
- **EtherCAT Master**: For servo communication
- **Control PC**: Running LinuxCNC with real-time kernel

## Key Design Challenges & Considerations

### 1. Axis Definition Philosophy
The bandsaw doesn't follow traditional CNC mill/lathe axis conventions. We need to decide:
- **What is an "axis" vs just an I/O operation?**
  - Shuttle movement (X): Clear axis with position control
  - Head height (Y): Axis-like but hydraulically driven
  - Vices: Pure I/O operations, not axes
- **How to handle the hybrid nature of hydraulic positioning?**
  - Head moves via hydraulics but needs position feedback
  - Do we treat it as a true axis or custom M-codes?

### 2. HAL Component Architecture
Need to create custom HAL component(s) that:
- Bridge between LinuxCNC's standard axis model and bandsaw operations
- Handle sequencing of hydraulic operations with timeouts
- Manage safety interlocks between operations
- Coordinate blade speed, feed rate, and cutting parameters

### 3. Job Queue System Design
The saw needs to run multiple jobs automatically:
- **Queue Management**: How to store and sequence jobs?
- **Material Handling**: How to signal operator for material changes?
- **Cut Optimization**: Should we optimize cut order for material usage?
- **State Persistence**: How to handle power loss mid-queue?

### 4. User Interface Requirements
QtVCP custom interface needs to handle:
- **Operator Modes**: Manual, Semi-auto, Full-auto
- **Job Management**: Queue display, reordering, editing
- **Material Database**: Store cutting parameters per material
- **Diagnostics**: Real-time system status, maintenance tracking

### 5. Remote Update Strategy
GitHub-based configuration management:
- **What can be safely updated remotely?**
  - Configuration files (INI, HAL)
  - UI layouts
  - Job programs
- **What requires local intervention?**
  - HAL component updates
  - System-level changes
- **How to handle rollback if update fails?**

## Technical Questions to Research

### LinuxCNC Integration
1. Can we use standard G-code for non-traditional axes?
2. How to implement hydraulic axis with position feedback?
3. Best practice for custom M-codes vs HAL pins?
4. How to handle job queue in G-code vs Python?

### Real-time Constraints
1. What servo thread rate for hydraulic control?
2. EtherCAT timing requirements vs LinuxCNC threads?
3. How fast must vice operations respond?
4. VFD response time for blade speed changes?

### Safety Implementation
1. How to implement E-stop that dumps hydraulics?
2. Should blade breakage detection stop all motion?
3. How to handle loss of position feedback?
4. Interlock requirements between operations?

## Development Approach

### Phase 1: Proof of Concept
- [ ] Set up basic LinuxCNC with MESA 7C81
- [ ] Control one hydraulic valve as digital output
- [ ] Read one encoder for position feedback
- [ ] Create minimal HAL component for testing

### Phase 2: Core Functionality
- [ ] Implement shuttle axis with EtherCAT servo
- [ ] Add hydraulic head control with feedback
- [ ] Integrate vice control sequences
- [ ] Basic cutting cycle in G-code

### Phase 3: Automation Layer
- [ ] Python job queue system
- [ ] QtVCP interface development
- [ ] Material database implementation
- [ ] Auto-sequencing logic

### Phase 4: Production Features
- [ ] Remote update system
- [ ] Diagnostics and logging
- [ ] Maintenance tracking
- [ ] Performance optimization

## Open Questions for Decision

1. **Coordinate System**: Should we use X for shuttle, Y for head, or create custom naming?

2. **G-code Dialect**: Standard G-code or custom macro language for saw operations?

3. **Vice Control Interface**:
   - M-codes (M101 for clamp, M102 for release)?
   - HAL pins controlled by UI?
   - Automatic based on program?

4. **Job Definition Format**:
   - Pure G-code files?
   - JSON with parameters + G-code?
   - Database entries?

5. **Operator Interaction Level**:
   - How much manual control during auto operation?
   - Override capabilities?
   - Pause/resume granularity?

## Experimental Ideas

- **Blade Wear Compensation**: Automatically adjust feed rate based on cut count
- **Vibration Monitoring**: Detect blade problems via accelerometer
- **Vision System**: Camera for cut verification or automatic measurement
- **Remnant Tracking**: Database of leftover material pieces
- **Predictive Maintenance**: Track cutting hours and predict service needs

## Resources Needed

### Documentation
- MESA 7C81 manual and examples
- LinuxCNC HAL component development guide
- EtherCAT for LinuxCNC documentation
- QtVCP development tutorials

### Hardware for Testing
- Spare hydraulic valves for bench testing
- Encoder for position feedback experiments
- Small servo for EtherCAT testing
- VFD with similar interface for blade speed tests

### Software Tools
- LinuxCNC development environment
- Qt Designer for UI development
- Python IDE for job scheduler
- Git for version control

## Next Steps

1. **Hardware Audit**: Document every I/O point, sensor, and actuator
2. **Create System Diagram**: Complete electrical and hydraulic schematic
3. **Bench Test Setup**: MESA card + few I/O points for initial testing
4. **LinuxCNC Installation**: Set up development environment
5. **Simple HAL Test**: Blink an LED, read a switch
6. **Community Input**: Post design questions to LinuxCNC forums

---

## Notes & Thoughts

This is a complex integration project that bridges:
- Modern CNC control (LinuxCNC + G-code)
- Industrial automation (Hydraulics + PLC-style logic)
- Custom automation (Job queuing + material optimization)
- Connected systems (Remote updates + monitoring)

The key is to start simple and build complexity gradually. Get basic motion working first, then add the automation layers.

The custom HAL component will be the heart of this system - it needs to be robust, well-tested, and maintainable.
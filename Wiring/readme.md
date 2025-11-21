n# Wiring Diagrams Documentation

This directory contains WireViz wiring diagram definitions for the Sawnders CNC control system.

## Setup Instructions

### Prerequisites

1. **UV Package Manager** is used for Python dependency management
2. **Python 3.13** is configured as the project Python version

### Installation

WireViz has been installed via UV:

```bash
# WireViz is already added to the project dependencies
uv add wireviz

# To reinstall or update:
uv sync
```

### Generating Diagrams

To generate wiring diagrams from the YAML files:

```bash
# Generate all output formats (default)
uv run wireviz wiring/wiring-main.yml

# Generate multiple specific formats
uv run wireviz wiring/wiring-main.yml -f png -f svg # PDF, and TSV available too

# Generate BOM only
uv run wireviz wiring/wiring-main.yml -f tsv
```

Generated outputs will be created in the same directory as the source files:

- `.svg` - Scalable vector graphics (recommended for documentation)
- `.png` - Raster image
- `.pdf` - PDF document
- `.html` - Interactive HTML with embedded SVG
- `.bom.tsv` - Bill of materials in tab-separated format

## File Naming Convention

The naming convention you suggested is excellent for organization:

- `wiring-main.yml` - Main control panel wiring
- `wiring-external.yml` - External device connections (motors, sensors)
- `wiring-mesa.yml` - Mesa board specific connections
- `wiring-power.yml` - Power distribution
- `wiring-safety.yml` - Safety circuits (e-stop, interlocks)
- `wiring-spindle.yml` - Spindle control wiring
- `wiring-coolant.yml` - Coolant system wiring

This naming scheme provides:

- Clear categorization by system/subsystem
- Easy identification of diagram purpose
- Consistent structure for documentation
- Simple wildcard operations (e.g., `wiring-*.yml`)

## Diagram Structure

Each WireViz YAML file contains:

### Connectors

Define physical connectors, terminals, and devices:

```yaml
connectors:
  connector_name:
    type: Type description
    subtype: Optional subtype
    pinlabels: [pin1, pin2, ...]
    notes: Optional notes
```

### Cables

Define cable specifications:

```yaml
cables:
  cable_name:
    wirecount: number
    gauge: wire gauge
    colors: [color1, color2, ...]
    shield: true/false
    notes: Optional notes
```

### Connections

Define how connectors and cables connect:

```yaml
connections:
  - - connector1: [pins]
    - cable: [wires]
    - connector2: [pins]
```

### Metadata

Document information:

```yaml
metadata:
  title: Diagram title
  description: Description
  revision: Version number
  date: Creation/update date
  author: Author name
```

## Best Practices

1. **Modular Design**: Keep diagrams focused on specific subsystems
2. **Consistent Naming**: Use descriptive names for connectors and cables
3. **Color Coding**: Follow standard wire color conventions
4. **Documentation**: Include notes for non-obvious connections
5. **Version Control**: Track changes with revision numbers and dates
6. **Safety First**: Clearly mark safety-critical circuits
7. **Cross-References**: Reference other diagrams when connections span multiple sheets

## Viewing Diagrams

After generation, diagrams can be viewed:

- SVG files can be opened in any web browser
- HTML files provide interactive viewing with zoom capabilities
- PDF files are suitable for printing and archival
- PNG files can be embedded in documentation

## Troubleshooting

If you encounter issues:

1. **GraphViz not found**: WireViz requires GraphViz to be installed separately

   ```bash
   # On Windows with Chocolatey:
   choco install graphviz

   # Or download from: https://graphviz.org/download/
   ```

2. **Import errors**: Ensure virtual environment is activated

   ```bash
   uv sync
   ```

3. **YAML syntax errors**: Validate YAML syntax using:
   ```bash
   uv run python -c "import yaml; yaml.safe_load(open('wiring/wiring-main.yml'))"
   ```

## Additional Resources

- [WireViz Documentation](https://github.com/formatc1702/WireViz)
- [WireViz Syntax Guide](https://github.com/formatc1702/WireViz/blob/main/docs/syntax.md)
- [Example Diagrams](https://github.com/formatc1702/WireViz/tree/main/examples)

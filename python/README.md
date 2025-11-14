# Wire Sizing Calculator - Python

A Python application for electrical wire sizing calculations, converted from the original C# Windows Store Application. This tool helps electrical engineers and electricians select appropriate wire gauge based on current requirements and voltage drop constraints.

## Features

- **Graphical User Interface**: Easy-to-use GUI with dropdown menus for selections
- **Material Support**: Calculations for both Copper (Cu) and Aluminum (Al) conductors
- **Phase Support**: Single-phase and three-phase system calculations
- **Comprehensive Calculations**:
  - Voltage drop
  - Percent voltage drop
  - Power loss
  - Automatic wire size selection
- **Input Validation**: Real-time validation with visual feedback
- **Reusable Library**: Core calculation functions available as a Python library

## Project Structure

```
python/
├── wire_sizing/              # Core library package
│   ├── __init__.py          # Package initialization
│   ├── lookup_tables.py     # Wire size, ampacity, and resistance data
│   └── calculations.py      # Calculation functions
├── wire_sizing_gui.py       # GUI application
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Requirements

- Python 3.6 or higher
- tkinter (usually included with Python)

### Installing tkinter

If tkinter is not available on your system:

- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **Fedora**: `sudo dnf install python3-tkinter`
- **macOS**: tkinter is included with Python from python.org
- **Windows**: tkinter is included with the Python installer

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Ampacity-App/python
   ```

2. No additional packages need to be installed (tkinter is part of Python standard library)

## Usage

### GUI Application

Run the graphical interface:

```bash
python wire_sizing_gui.py
```

Or make it executable:

```bash
chmod +x wire_sizing_gui.py
./wire_sizing_gui.py
```

#### Using the GUI:

1. **Enter Wire Length**: Length of the wire run in feet
2. **Enter System Voltage**: System voltage in volts (e.g., 120, 240, 480)
3. **Enter Current**: Required current in amperes
4. **Enter Max Voltage Drop**: Maximum acceptable voltage drop as a percentage (typically 3-5%)
5. **Select Conductor Material**: Choose Copper (Cu) or Aluminum (Al) from dropdown
6. **Select System Phase**: Choose Single Phase or Three Phase from dropdown
7. **Click Calculate**: Results will display wire size, voltage drop, and power loss

### Using the Library in Your Code

You can import and use the wire sizing library in your own Python projects:

```python
from wire_sizing import select_wire_size, MATERIALS, PHASES

# Perform a wire sizing calculation
result = select_wire_size(
    wire_length=100,              # feet
    voltage=120,                  # volts
    current=20,                   # amperes
    max_voltage_drop_percent=3,   # percent
    material=MATERIALS[0],         # "Copper (Cu)"
    phase=PHASES[0]               # "Single Phase"
)

if result:
    print(f"Wire Size: {result.wire_size}")
    print(f"Voltage Drop: {result.voltage_drop:.3f} V")
    print(f"Percent VD: {result.percent_voltage_drop:.3f}%")
    print(f"Power Loss: {result.power_loss/1000:.3f} kW")
else:
    print("No suitable wire size found")
```

### Available Library Functions

```python
from wire_sizing import (
    select_wire_size,              # Main wire selection function
    calculate_voltage_drop,        # Calculate voltage drop
    calculate_percent_voltage_drop,# Calculate percent voltage drop
    calculate_power_loss,          # Calculate power loss
    validate_inputs,               # Validate input parameters
    get_calculation_details,       # Get formatted results
    MATERIALS,                     # List of available materials
    PHASES,                        # List of available phases
    WIRE_SIZES,                    # List of available wire sizes
    COPPER_AMPACITY,               # Copper ampacity lookup table
    ALUMINUM_AMPACITY,             # Aluminum ampacity lookup table
    COPPER_RESISTANCE,             # Copper resistance lookup table
    ALUMINUM_RESISTANCE            # Aluminum resistance lookup table
)
```

## Technical Details

### Lookup Tables

The calculator uses NEC (National Electrical Code) standard tables:

- **Ampacity Tables**: Based on 30°C ambient, single insulated conductors, 0-2000V, 72°C conductor rating
- **Resistance Tables**: Based on 600V cables, 3-phase, 60Hz, 75°C
- **Wire Sizes**: Ranges from 14 AWG to 750 kcmil

### Calculation Formulas

**Single-Phase Voltage Drop:**
```
VD = (2 × length × resistance × current) / 1000
```

**Three-Phase Voltage Drop:**
```
VD = (√3 × length × resistance × current) / 1000
```

**Percent Voltage Drop:**
```
Percent_VD = (VD / system_voltage) × 100
```

**Power Loss:**
```
Power_Loss = I² × (resistance/1000) × 2 × length
```

### Wire Selection Criteria

The calculator selects the smallest wire size that meets both:
1. **Ampacity Requirement**: Wire ampacity exceeds the required current
2. **Voltage Drop Requirement**: Voltage drop does not exceed the specified percentage

## Examples

### Example 1: Residential Circuit

Calculate wire size for a 20A, 120V single-phase circuit with 50 feet of copper wire and 3% max voltage drop:

**Inputs:**
- Wire Length: 50 ft
- Voltage: 120 V
- Current: 20 A
- Max Voltage Drop: 3%
- Material: Copper (Cu)
- Phase: Single Phase

**Expected Results:**
- Wire Size: 12 AWG
- Voltage Drop: ~2.0 V
- Percent VD: ~1.67%
- Power Loss: ~40 W

### Example 2: Commercial Three-Phase Circuit

Calculate wire size for a 100A, 480V three-phase circuit with 200 feet of aluminum wire and 2% max voltage drop:

**Inputs:**
- Wire Length: 200 ft
- Voltage: 480 V
- Current: 100 A
- Max Voltage Drop: 2%
- Material: Aluminum (Al)
- Phase: Three Phase

**Expected Results:**
- Wire size and parameters will be calculated based on NEC tables

## Differences from C# Version

The Python version includes several enhancements:

1. **Cross-Platform**: Works on Windows, macOS, and Linux (not limited to Windows Store)
2. **Three-Phase Support**: Added three-phase calculations (not implemented in C# version)
3. **Modular Design**: Core logic separated into reusable library
4. **Better Validation**: Enhanced input validation with detailed error messages
5. **Type Hints**: Added Python type hints for better code documentation

## Future Integration

This calculator is designed to be integrated with Excel-based voltage drop calculations. The library can be:

- Imported into other Python projects
- Used with pandas for Excel integration
- Extended with additional features like:
  - Conduit fill calculations
  - Temperature correction factors
  - Multiple parallel conductors
  - Custom wire tables

## Contributing

When extending this library, please ensure:

1. All functions include type hints
2. Docstrings follow Google style
3. Calculations are based on NEC standards
4. Tests are added for new functionality

## License

Converted from the original C# Ampacity Calculator.

## Support

For issues, questions, or contributions, please refer to the project repository.

## References

- National Electrical Code (NEC)
- NFPA 70
- Electrical Engineering Standards for Wire Sizing

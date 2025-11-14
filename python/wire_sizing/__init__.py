"""
Wire Sizing Library

A Python library for electrical wire sizing calculations based on NEC standards.

This library provides:
- Lookup tables for wire sizes, ampacity, and resistance
- Calculation functions for voltage drop, power loss, and wire selection
- Support for both copper and aluminum conductors
- Support for single-phase and three-phase systems

Example usage:
    from wire_sizing import select_wire_size, MATERIALS, PHASES

    result = select_wire_size(
        wire_length=100,  # feet
        voltage=120,      # volts
        current=20,       # amperes
        max_voltage_drop_percent=3,  # percent
        material=MATERIALS[0],  # Copper
        phase=PHASES[0]         # Single Phase
    )

    if result:
        print(f"Wire Size: {result.wire_size}")
        print(f"Voltage Drop: {result.voltage_drop:.3f} V")
        print(f"Power Loss: {result.power_loss/1000:.3f} kW")
"""

from .calculations import (
    calculate_voltage_drop,
    calculate_percent_voltage_drop,
    calculate_power_loss,
    select_wire_size,
    validate_inputs,
    get_calculation_details,
    WireSizingResult
)

from .lookup_tables import (
    WIRE_SIZES,
    COPPER_AMPACITY,
    ALUMINUM_AMPACITY,
    COPPER_RESISTANCE,
    ALUMINUM_RESISTANCE,
    MATERIALS,
    PHASES,
    get_material_data,
    get_wire_size_index
)

__version__ = "1.0.0"
__author__ = "Converted from C# Ampacity Calculator"

__all__ = [
    # Calculation functions
    'calculate_voltage_drop',
    'calculate_percent_voltage_drop',
    'calculate_power_loss',
    'select_wire_size',
    'validate_inputs',
    'get_calculation_details',
    'WireSizingResult',

    # Lookup tables and constants
    'WIRE_SIZES',
    'COPPER_AMPACITY',
    'ALUMINUM_AMPACITY',
    'COPPER_RESISTANCE',
    'ALUMINUM_RESISTANCE',
    'MATERIALS',
    'PHASES',
    'get_material_data',
    'get_wire_size_index',
]

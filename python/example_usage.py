#!/usr/bin/env python3
"""
Example usage of the wire_sizing library.

This script demonstrates how to use the wire sizing library
in your own Python projects.
"""

import sys
from pathlib import Path

# Add the current directory to the path to import wire_sizing module
sys.path.insert(0, str(Path(__file__).parent))

from wire_sizing import (
    select_wire_size,
    calculate_voltage_drop,
    calculate_percent_voltage_drop,
    calculate_power_loss,
    get_calculation_details,
    MATERIALS,
    PHASES,
    WIRE_SIZES
)


def example_1_basic_calculation():
    """Example 1: Basic wire sizing calculation."""
    print("\n" + "="*70)
    print("Example 1: Basic Wire Sizing Calculation")
    print("="*70)

    # Define circuit parameters
    wire_length = 100        # feet
    voltage = 120           # volts
    current = 20            # amperes
    max_vd_percent = 3      # percent
    material = MATERIALS[0] # Copper
    phase = PHASES[0]       # Single Phase

    print(f"\nCircuit Parameters:")
    print(f"  Wire Length: {wire_length} ft")
    print(f"  Voltage: {voltage} V")
    print(f"  Current: {current} A")
    print(f"  Max VD: {max_vd_percent}%")
    print(f"  Material: {material}")
    print(f"  Phase: {phase}")

    # Calculate wire size
    result = select_wire_size(
        wire_length=wire_length,
        voltage=voltage,
        current=current,
        max_voltage_drop_percent=max_vd_percent,
        material=material,
        phase=phase
    )

    if result:
        print(f"\nResults:")
        print(f"  Selected Wire Size: {result.wire_size}")
        print(f"  Voltage Drop: {result.voltage_drop:.3f} V")
        print(f"  Percent VD: {result.percent_voltage_drop:.3f}%")
        print(f"  Power Loss: {result.power_loss:.1f} W ({result.power_loss/1000:.3f} kW)")
    else:
        print("\n✗ No suitable wire size found!")


def example_2_comparing_materials():
    """Example 2: Comparing copper vs aluminum for the same circuit."""
    print("\n" + "="*70)
    print("Example 2: Comparing Copper vs Aluminum")
    print("="*70)

    # Circuit parameters
    wire_length = 150
    voltage = 240
    current = 50
    max_vd_percent = 2.5
    phase = PHASES[0]

    print(f"\nCircuit Parameters:")
    print(f"  Wire Length: {wire_length} ft")
    print(f"  Voltage: {voltage} V")
    print(f"  Current: {current} A")
    print(f"  Max VD: {max_vd_percent}%")

    for material in MATERIALS:
        print(f"\n--- {material} ---")

        result = select_wire_size(
            wire_length=wire_length,
            voltage=voltage,
            current=current,
            max_voltage_drop_percent=max_vd_percent,
            material=material,
            phase=phase
        )

        if result:
            print(f"  Wire Size: {result.wire_size}")
            print(f"  Voltage Drop: {result.voltage_drop:.3f} V")
            print(f"  Percent VD: {result.percent_voltage_drop:.3f}%")
            print(f"  Power Loss: {result.power_loss/1000:.3f} kW")
        else:
            print("  No suitable wire found")


def example_3_three_phase_calculation():
    """Example 3: Three-phase system calculation."""
    print("\n" + "="*70)
    print("Example 3: Three-Phase System")
    print("="*70)

    # Three-phase circuit
    wire_length = 200
    voltage = 480
    current = 100
    max_vd_percent = 2
    material = MATERIALS[0]  # Copper
    phase = PHASES[1]        # Three Phase

    print(f"\nCircuit Parameters:")
    print(f"  Wire Length: {wire_length} ft")
    print(f"  Voltage: {voltage} V")
    print(f"  Current: {current} A")
    print(f"  Max VD: {max_vd_percent}%")
    print(f"  Material: {material}")
    print(f"  Phase: {phase}")

    result = select_wire_size(
        wire_length=wire_length,
        voltage=voltage,
        current=current,
        max_voltage_drop_percent=max_vd_percent,
        material=material,
        phase=phase
    )

    if result:
        print(f"\nResults:")
        print(f"  Wire Size: {result.wire_size}")
        print(f"  Voltage Drop: {result.voltage_drop:.3f} V")
        print(f"  Percent VD: {result.percent_voltage_drop:.3f}%")
        print(f"  Power Loss: {result.power_loss/1000:.3f} kW")

        # Get formatted details
        details = get_calculation_details(result, material)
        print(f"\nFormatted Details:")
        for key, value in details.items():
            print(f"  {key}: {value}")


def example_4_individual_calculations():
    """Example 4: Using individual calculation functions."""
    print("\n" + "="*70)
    print("Example 4: Individual Calculation Functions")
    print("="*70)

    # Calculate voltage drop for a specific wire
    wire_length = 100
    resistance = 1.2  # 10 AWG copper resistance
    current = 30
    phase = PHASES[0]

    print(f"\nCalculating voltage drop:")
    print(f"  Wire: 10 AWG Copper (resistance = {resistance} Ω/1000ft)")
    print(f"  Length: {wire_length} ft")
    print(f"  Current: {current} A")
    print(f"  Phase: {phase}")

    vd = calculate_voltage_drop(wire_length, resistance, current, phase)
    print(f"  → Voltage Drop: {vd:.3f} V")

    # Calculate percent voltage drop
    voltage = 120
    percent_vd = calculate_percent_voltage_drop(vd, voltage)
    print(f"  → Percent VD at {voltage}V: {percent_vd:.3f}%")

    # Calculate power loss
    power = calculate_power_loss(current, resistance, wire_length)
    print(f"  → Power Loss: {power:.1f} W ({power/1000:.3f} kW)")


def example_5_wire_size_list():
    """Example 5: Listing available wire sizes."""
    print("\n" + "="*70)
    print("Example 5: Available Wire Sizes")
    print("="*70)

    print(f"\nTotal wire sizes available: {len(WIRE_SIZES)}")
    print("\nWire sizes:")

    for i, size in enumerate(WIRE_SIZES):
        print(f"  {i+1:2d}. {size}")


def main():
    """Run all examples."""
    print("\n" + "="*70)
    print(" Wire Sizing Library - Usage Examples")
    print("="*70)

    examples = [
        example_1_basic_calculation,
        example_2_comparing_materials,
        example_3_three_phase_calculation,
        example_4_individual_calculations,
        example_5_wire_size_list
    ]

    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\n✗ Example failed with error: {e}")

    print("\n" + "="*70)
    print(" Examples Complete")
    print("="*70)
    print()


if __name__ == "__main__":
    main()

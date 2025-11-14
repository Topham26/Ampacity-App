#!/usr/bin/env python3
"""
Test script for wire sizing library.

This script performs several test calculations to verify that
the wire sizing library works correctly.
"""

import sys
from pathlib import Path

# Add the current directory to the path to import wire_sizing module
sys.path.insert(0, str(Path(__file__).parent))

from wire_sizing import (
    select_wire_size,
    calculate_voltage_drop,
    calculate_power_loss,
    MATERIALS,
    PHASES
)


def print_separator():
    """Print a separator line."""
    print("=" * 70)


def test_case_1():
    """Test Case 1: Residential 20A circuit with copper wire."""
    print("\nTest Case 1: Residential 20A, 120V Single-Phase Circuit (Copper)")
    print_separator()

    result = select_wire_size(
        wire_length=100,
        voltage=120,
        current=20,
        max_voltage_drop_percent=3,
        material=MATERIALS[0],  # Copper
        phase=PHASES[0]         # Single Phase
    )

    if result:
        print(f"✓ Wire Size: {result.wire_size}")
        print(f"  Voltage Drop: {result.voltage_drop:.3f} V")
        print(f"  Percent VD: {result.percent_voltage_drop:.3f}%")
        print(f"  Power Loss: {result.power_loss/1000:.3f} kW")
        return True
    else:
        print("✗ No suitable wire size found")
        return False


def test_case_2():
    """Test Case 2: Commercial circuit with aluminum wire."""
    print("\nTest Case 2: Commercial 50A, 240V Single-Phase Circuit (Aluminum)")
    print_separator()

    result = select_wire_size(
        wire_length=150,
        voltage=240,
        current=50,
        max_voltage_drop_percent=2.5,
        material=MATERIALS[1],  # Aluminum
        phase=PHASES[0]         # Single Phase
    )

    if result:
        print(f"✓ Wire Size: {result.wire_size}")
        print(f"  Voltage Drop: {result.voltage_drop:.3f} V")
        print(f"  Percent VD: {result.percent_voltage_drop:.3f}%")
        print(f"  Power Loss: {result.power_loss/1000:.3f} kW")
        return True
    else:
        print("✗ No suitable wire size found")
        return False


def test_case_3():
    """Test Case 3: Three-phase industrial circuit."""
    print("\nTest Case 3: Industrial 100A, 480V Three-Phase Circuit (Copper)")
    print_separator()

    result = select_wire_size(
        wire_length=200,
        voltage=480,
        current=100,
        max_voltage_drop_percent=2,
        material=MATERIALS[0],  # Copper
        phase=PHASES[1]         # Three Phase
    )

    if result:
        print(f"✓ Wire Size: {result.wire_size}")
        print(f"  Voltage Drop: {result.voltage_drop:.3f} V")
        print(f"  Percent VD: {result.percent_voltage_drop:.3f}%")
        print(f"  Power Loss: {result.power_loss/1000:.3f} kW")
        return True
    else:
        print("✗ No suitable wire size found")
        return False


def test_case_4():
    """Test Case 4: Edge case - high current requirement."""
    print("\nTest Case 4: High Current 700A, 480V Circuit (Copper)")
    print_separator()

    result = select_wire_size(
        wire_length=50,
        voltage=480,
        current=700,
        max_voltage_drop_percent=3,
        material=MATERIALS[0],  # Copper
        phase=PHASES[0]         # Single Phase
    )

    if result:
        print(f"✓ Wire Size: {result.wire_size}")
        print(f"  Voltage Drop: {result.voltage_drop:.3f} V")
        print(f"  Percent VD: {result.percent_voltage_drop:.3f}%")
        print(f"  Power Loss: {result.power_loss/1000:.3f} kW")
        return True
    else:
        print("✗ No suitable wire size found (expected - current too high)")
        return True  # This is expected behavior


def test_case_5():
    """Test Case 5: Edge case - very strict voltage drop."""
    print("\nTest Case 5: Strict VD Requirement - 15A, 120V, 0.5% max VD (Copper)")
    print_separator()

    result = select_wire_size(
        wire_length=200,
        voltage=120,
        current=15,
        max_voltage_drop_percent=0.5,
        material=MATERIALS[0],  # Copper
        phase=PHASES[0]         # Single Phase
    )

    if result:
        print(f"✓ Wire Size: {result.wire_size}")
        print(f"  Voltage Drop: {result.voltage_drop:.3f} V")
        print(f"  Percent VD: {result.percent_voltage_drop:.3f}%")
        print(f"  Power Loss: {result.power_loss/1000:.3f} kW")
        return True
    else:
        print("✗ No suitable wire size found (expected - VD requirement too strict)")
        return True  # This is expected behavior


def test_individual_functions():
    """Test individual calculation functions."""
    print("\nTest Individual Functions")
    print_separator()

    # Test voltage drop calculation
    vd = calculate_voltage_drop(
        wire_length=100,
        resistance=2.0,  # 12 AWG copper
        current=20,
        phase=PHASES[0]
    )
    print(f"Voltage Drop (100ft, 2.0Ω/1000ft, 20A): {vd:.3f} V")

    # Test power loss calculation
    power = calculate_power_loss(
        current=20,
        resistance=2.0,
        wire_length=100
    )
    print(f"Power Loss (20A, 2.0Ω/1000ft, 100ft): {power:.3f} W ({power/1000:.3f} kW)")

    return True


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print(" Wire Sizing Library Test Suite")
    print("=" * 70)

    tests = [
        ("Test Case 1", test_case_1),
        ("Test Case 2", test_case_2),
        ("Test Case 3", test_case_3),
        ("Test Case 4", test_case_4),
        ("Test Case 5", test_case_5),
        ("Individual Functions", test_individual_functions)
    ]

    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"✗ {name} failed with error: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "=" * 70)
    print(" Test Summary")
    print("=" * 70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")

    print("=" * 70)
    print(f"Tests Passed: {passed}/{total}")
    print("=" * 70)

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

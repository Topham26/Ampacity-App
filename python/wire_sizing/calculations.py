"""
Wire sizing calculation functions.

This module provides functions for calculating electrical parameters
for wire sizing including voltage drop, power loss, and selecting
appropriate wire gauge based on current and voltage drop requirements.
"""

from typing import Optional, Tuple, Dict
from .lookup_tables import (
    WIRE_SIZES,
    get_material_data
)


class WireSizingResult:
    """
    Data class to hold wire sizing calculation results.
    """
    def __init__(self, wire_size: str, voltage_drop: float,
                 percent_voltage_drop: float, power_loss: float,
                 wire_index: int):
        """
        Initialize wire sizing result.

        Args:
            wire_size: Selected wire size (e.g., "12 AWG")
            voltage_drop: Voltage drop in volts
            percent_voltage_drop: Voltage drop as percentage
            power_loss: Power loss in watts
            wire_index: Index of the wire in the lookup table
        """
        self.wire_size = wire_size
        self.voltage_drop = voltage_drop
        self.percent_voltage_drop = percent_voltage_drop
        self.power_loss = power_loss
        self.wire_index = wire_index

    def __repr__(self):
        return (f"WireSizingResult(wire_size={self.wire_size}, "
                f"voltage_drop={self.voltage_drop:.3f}V, "
                f"percent_vd={self.percent_voltage_drop:.3f}%, "
                f"power_loss={self.power_loss/1000:.3f}kW)")


def calculate_voltage_drop(wire_length: float, resistance: float,
                          current: float, phase: str = "Single Phase") -> float:
    """
    Calculate voltage drop for a given wire configuration.

    Formula for single phase: VD = (2 × length × resistance × current) / 1000
    Formula for three phase: VD = (√3 × length × resistance × current) / 1000

    Args:
        wire_length: Length of wire run in feet
        resistance: Wire resistance in ohms per 1000 ft
        current: Current in amperes
        phase: "Single Phase" or "Three Phase"

    Returns:
        Voltage drop in volts
    """
    if phase == "Single Phase":
        # Factor of 2 accounts for current path (out and back)
        vd = (2 * wire_length * resistance * current) / 1000
    else:  # Three Phase
        # Factor of √3 (1.732) for three-phase systems
        vd = (1.732 * wire_length * resistance * current) / 1000

    return vd


def calculate_percent_voltage_drop(voltage_drop: float,
                                   system_voltage: float) -> float:
    """
    Calculate voltage drop as a percentage of system voltage.

    Args:
        voltage_drop: Voltage drop in volts
        system_voltage: System voltage in volts

    Returns:
        Voltage drop as a percentage
    """
    return (voltage_drop / system_voltage) * 100


def calculate_power_loss(current: float, resistance: float,
                        wire_length: float) -> float:
    """
    Calculate power loss in the wire.

    Formula: Power_Loss = I² × (resistance/1000) × 2 × length

    Args:
        current: Current in amperes
        resistance: Wire resistance in ohms per 1000 ft
        wire_length: Length of wire run in feet

    Returns:
        Power loss in watts
    """
    # Factor of 2 accounts for both conductors (out and back)
    power_loss = current * current * (resistance / 1000) * 2 * wire_length
    return power_loss


def select_wire_size(wire_length: float, voltage: float, current: float,
                    max_voltage_drop_percent: float, material: str,
                    phase: str = "Single Phase") -> Optional[WireSizingResult]:
    """
    Select appropriate wire size based on ampacity and voltage drop requirements.

    This function iterates through available wire sizes and selects the smallest
    wire that meets both criteria:
    1. Ampacity exceeds the required current
    2. Voltage drop does not exceed the maximum allowed percentage

    Args:
        wire_length: Length of wire run in feet
        voltage: System voltage in volts
        current: Required current in amperes
        max_voltage_drop_percent: Maximum allowable voltage drop as percentage
        material: Either "Copper (Cu)" or "Aluminum (Al)"
        phase: Either "Single Phase" or "Three Phase"

    Returns:
        WireSizingResult object if suitable wire is found, None otherwise

    Raises:
        ValueError: If material is not recognized
    """
    # Get material-specific lookup data
    ampacity_list, resistance_list = get_material_data(material)

    # Iterate through wire sizes to find the first suitable one
    for i in range(len(WIRE_SIZES)):
        # Check if wire can handle the current (ampacity requirement)
        if ampacity_list[i] > current:
            # Calculate voltage drop for this wire size
            vd = calculate_voltage_drop(wire_length, resistance_list[i],
                                       current, phase)
            percent_vd = calculate_percent_voltage_drop(vd, voltage)

            # Check if voltage drop is within acceptable range
            if percent_vd <= max_voltage_drop_percent:
                # Calculate power loss
                power = calculate_power_loss(current, resistance_list[i],
                                            wire_length)

                # Return successful result
                return WireSizingResult(
                    wire_size=WIRE_SIZES[i],
                    voltage_drop=vd,
                    percent_voltage_drop=percent_vd,
                    power_loss=power,
                    wire_index=i
                )

    # No suitable wire size found
    return None


def validate_inputs(wire_length: float, voltage: float, current: float,
                   max_voltage_drop_percent: float) -> Tuple[bool, str]:
    """
    Validate user inputs for wire sizing calculation.

    Args:
        wire_length: Length of wire run in feet
        voltage: System voltage in volts
        current: Required current in amperes
        max_voltage_drop_percent: Maximum allowable voltage drop as percentage

    Returns:
        Tuple of (is_valid, error_message)
        If valid, error_message will be empty string
    """
    errors = []

    if wire_length <= 0:
        errors.append("Wire length must be greater than 0")

    if voltage <= 0:
        errors.append("Voltage must be greater than 0")

    if current <= 0:
        errors.append("Current must be greater than 0")

    if max_voltage_drop_percent <= 0 or max_voltage_drop_percent > 100:
        errors.append("Voltage drop percentage must be between 0 and 100")

    if errors:
        return False, "; ".join(errors)

    return True, ""


def get_calculation_details(result: WireSizingResult,
                           material: str) -> Dict[str, str]:
    """
    Get formatted calculation details as a dictionary.

    Args:
        result: WireSizingResult object
        material: Material name

    Returns:
        Dictionary with formatted calculation results
    """
    return {
        "wire_size": result.wire_size,
        "voltage_drop": f"{result.voltage_drop:.3f} V",
        "percent_voltage_drop": f"{result.percent_voltage_drop:.3f}%",
        "power_loss": f"{result.power_loss/1000:.3f} kW",
        "material": material
    }

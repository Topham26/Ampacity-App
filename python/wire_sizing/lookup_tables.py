"""
Lookup tables for wire sizing calculations.

This module contains standard electrical wire sizing data including:
- Wire sizes (AWG and kcmil)
- Ampacity ratings for copper and aluminum conductors
- Resistance values for copper and aluminum conductors

All data is based on NEC (National Electrical Code) standards:
- Ampacity: 30°C ambient, Single insulated conductors, 0-2000V, 72°C conductor rating
- Resistance: 600V cables, 3-phase, 60Hz, 75°C
"""

# Wire sizes from 14 AWG to 750 kcmil
WIRE_SIZES = [
    "14 AWG",
    "12 AWG",
    "10 AWG",
    "8 AWG",
    "6 AWG",
    "4 AWG",
    "3 AWG",
    "2 AWG",
    "1 AWG",
    "1/0 AWG",
    "2/0 AWG",
    "3/0 AWG",
    "4/0 AWG",
    "250 kcmil",
    "300 kcmil",
    "350 kcmil",
    "400 kcmil",
    "500 kcmil",
    "600 kcmil",
    "750 kcmil"
]

# Copper ampacity values (Amps)
# 30°C ambient, Single insulated conductors, 0-2000V, 72°C conductor rating
COPPER_AMPACITY = [
    30,   # 14 AWG
    35,   # 12 AWG
    50,   # 10 AWG
    70,   # 8 AWG
    95,   # 6 AWG
    125,  # 4 AWG
    145,  # 3 AWG
    170,  # 2 AWG
    195,  # 1 AWG
    230,  # 1/0 AWG
    265,  # 2/0 AWG
    310,  # 3/0 AWG
    360,  # 4/0 AWG
    405,  # 250 kcmil
    445,  # 300 kcmil
    505,  # 350 kcmil
    545,  # 400 kcmil
    620,  # 500 kcmil
    690,  # 600 kcmil
    785   # 750 kcmil
]

# Aluminum ampacity values (Amps)
# Note: 14 AWG aluminum is not typically used (value set to 0)
ALUMINUM_AMPACITY = [
    0,    # 14 AWG (not used)
    30,   # 12 AWG
    40,   # 10 AWG
    55,   # 8 AWG
    75,   # 6 AWG
    100,  # 4 AWG
    115,  # 3 AWG
    135,  # 2 AWG
    155,  # 1 AWG
    180,  # 1/0 AWG
    210,  # 2/0 AWG
    240,  # 3/0 AWG
    280,  # 4/0 AWG
    315,  # 250 kcmil
    350,  # 300 kcmil
    395,  # 350 kcmil
    425,  # 400 kcmil
    485,  # 500 kcmil
    540,  # 600 kcmil
    620   # 750 kcmil
]

# Copper resistance values (ohms per 1000 ft)
# 600V cables, 3-phase, 60Hz, 75°C
COPPER_RESISTANCE = [
    3.1,    # 14 AWG
    2.0,    # 12 AWG
    1.2,    # 10 AWG
    0.78,   # 8 AWG
    0.49,   # 6 AWG
    0.31,   # 4 AWG
    0.25,   # 3 AWG
    0.19,   # 2 AWG
    0.15,   # 1 AWG
    0.12,   # 1/0 AWG
    0.10,   # 2/0 AWG
    0.077,  # 3/0 AWG
    0.062,  # 4/0 AWG
    0.052,  # 250 kcmil
    0.044,  # 300 kcmil
    0.038,  # 350 kcmil
    0.033,  # 400 kcmil
    0.027,  # 500 kcmil
    0.023,  # 600 kcmil
    0.019   # 750 kcmil
]

# Aluminum resistance values (ohms per 1000 ft)
# Note: Array has 21 values to match the original C# implementation
ALUMINUM_RESISTANCE = [
    0,      # 14 AWG (not used)
    3,      # 12 AWG
    2,      # 10 AWG
    2.0,    # 8 AWG
    1.3,    # 6 AWG
    0.81,   # 4 AWG
    0.51,   # 3 AWG
    0.40,   # 2 AWG
    0.32,   # 1 AWG
    0.25,   # 1/0 AWG
    0.20,   # 2/0 AWG
    0.16,   # 3/0 AWG
    0.13,   # 4/0 AWG
    0.10,   # 250 kcmil
    0.085,  # 300 kcmil
    0.071,  # 350 kcmil
    0.061,  # 400 kcmil
    0.054,  # 500 kcmil
    0.043,  # 600 kcmil
    0.036,  # 750 kcmil
    0.029   # Extra value from original C# code
]

# Material types
MATERIALS = ["Copper (Cu)", "Aluminum (Al)"]

# Phase types
PHASES = ["Single Phase", "Three Phase"]


def get_material_data(material_name):
    """
    Get ampacity and resistance data for a specific material.

    Args:
        material_name (str): Either "Copper (Cu)" or "Aluminum (Al)"

    Returns:
        tuple: (ampacity_list, resistance_list)

    Raises:
        ValueError: If material_name is not recognized
    """
    if material_name == "Copper (Cu)":
        return COPPER_AMPACITY, COPPER_RESISTANCE
    elif material_name == "Aluminum (Al)":
        return ALUMINUM_AMPACITY, ALUMINUM_RESISTANCE
    else:
        raise ValueError(f"Unknown material: {material_name}")


def get_wire_size_index(wire_size):
    """
    Get the index of a wire size in the WIRE_SIZES list.

    Args:
        wire_size (str): Wire size string (e.g., "12 AWG")

    Returns:
        int: Index in WIRE_SIZES list

    Raises:
        ValueError: If wire size is not found
    """
    try:
        return WIRE_SIZES.index(wire_size)
    except ValueError:
        raise ValueError(f"Wire size '{wire_size}' not found in lookup table")

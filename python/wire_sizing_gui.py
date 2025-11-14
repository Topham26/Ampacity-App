#!/usr/bin/env python3
"""
Wire Sizing Calculator GUI

A graphical user interface for electrical wire sizing calculations.
Converted from C# Windows Store Application to Python with tkinter.

Features:
- Dropdown menus for material and phase selection
- Input validation with visual feedback
- Real-time calculation of voltage drop and power loss
- Support for both copper and aluminum conductors
- Support for single-phase and three-phase systems
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
from pathlib import Path

# Add the parent directory to the path to import wire_sizing module
sys.path.insert(0, str(Path(__file__).parent))

from wire_sizing import (
    select_wire_size,
    validate_inputs,
    MATERIALS,
    PHASES
)


class WireSizingCalculatorGUI:
    """
    Main GUI application for wire sizing calculations.
    """

    def __init__(self, root):
        """
        Initialize the GUI application.

        Args:
            root: tkinter root window
        """
        self.root = root
        self.root.title("Wire Sizing Calculator")
        self.root.geometry("600x550")
        self.root.resizable(False, False)

        # Configure style
        self.setup_styles()

        # Create GUI components
        self.create_widgets()

    def setup_styles(self):
        """Configure ttk styles for the application."""
        style = ttk.Style()
        style.theme_use('clam')

        # Configure button style
        style.configure('Calculate.TButton',
                       font=('Arial', 12, 'bold'),
                       padding=10)

        # Configure label styles
        style.configure('Title.TLabel',
                       font=('Arial', 16, 'bold'),
                       foreground='#2c3e50')

        style.configure('Section.TLabel',
                       font=('Arial', 11, 'bold'),
                       foreground='#34495e')

        style.configure('Result.TLabel',
                       font=('Arial', 10),
                       foreground='#27ae60')

        style.configure('Error.TLabel',
                       font=('Arial', 10),
                       foreground='#e74c3c')

    def create_widgets(self):
        """Create and layout all GUI widgets."""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title
        title_label = ttk.Label(main_frame, text="Wire Sizing Calculator",
                               style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Input section
        self.create_input_section(main_frame)

        # Calculate button
        calc_button = ttk.Button(main_frame, text="Calculate Wire Size",
                                command=self.calculate,
                                style='Calculate.TButton')
        calc_button.grid(row=6, column=0, columnspan=2, pady=20)

        # Results section
        self.create_results_section(main_frame)

        # Error message label
        self.error_label = ttk.Label(main_frame, text="",
                                    style='Error.TLabel',
                                    wraplength=500)
        self.error_label.grid(row=8, column=0, columnspan=2, pady=5)

    def create_input_section(self, parent):
        """
        Create input fields section.

        Args:
            parent: Parent frame widget
        """
        # Wire Length
        ttk.Label(parent, text="Wire Length (ft):",
                 style='Section.TLabel').grid(row=1, column=0, sticky=tk.W, pady=5)
        self.length_entry = ttk.Entry(parent, width=30)
        self.length_entry.grid(row=1, column=1, sticky=tk.W, pady=5, padx=10)

        # Voltage
        ttk.Label(parent, text="System Voltage (V):",
                 style='Section.TLabel').grid(row=2, column=0, sticky=tk.W, pady=5)
        self.voltage_entry = ttk.Entry(parent, width=30)
        self.voltage_entry.grid(row=2, column=1, sticky=tk.W, pady=5, padx=10)

        # Current
        ttk.Label(parent, text="Current (A):",
                 style='Section.TLabel').grid(row=3, column=0, sticky=tk.W, pady=5)
        self.current_entry = ttk.Entry(parent, width=30)
        self.current_entry.grid(row=3, column=1, sticky=tk.W, pady=5, padx=10)

        # Max Voltage Drop Percentage
        ttk.Label(parent, text="Max Voltage Drop (%):",
                 style='Section.TLabel').grid(row=4, column=0, sticky=tk.W, pady=5)
        self.vdrop_entry = ttk.Entry(parent, width=30)
        self.vdrop_entry.grid(row=4, column=1, sticky=tk.W, pady=5, padx=10)

        # Material dropdown
        ttk.Label(parent, text="Conductor Material:",
                 style='Section.TLabel').grid(row=5, column=0, sticky=tk.W, pady=5)
        self.material_var = tk.StringVar()
        self.material_combo = ttk.Combobox(parent, textvariable=self.material_var,
                                          values=MATERIALS, state='readonly', width=27)
        self.material_combo.current(0)  # Default to Copper
        self.material_combo.grid(row=5, column=1, sticky=tk.W, pady=5, padx=10)

        # Phase dropdown
        ttk.Label(parent, text="System Phase:",
                 style='Section.TLabel').grid(row=6, column=0, sticky=tk.W, pady=5)
        self.phase_var = tk.StringVar()
        self.phase_combo = ttk.Combobox(parent, textvariable=self.phase_var,
                                       values=PHASES, state='readonly', width=27)
        self.phase_combo.current(0)  # Default to Single Phase
        self.phase_combo.grid(row=6, column=1, sticky=tk.W, pady=5, padx=10)

        # Store entry widgets for validation highlighting
        self.entry_widgets = [
            self.length_entry,
            self.voltage_entry,
            self.current_entry,
            self.vdrop_entry
        ]

    def create_results_section(self, parent):
        """
        Create results display section.

        Args:
            parent: Parent frame widget
        """
        # Results frame
        results_frame = ttk.LabelFrame(parent, text="Results", padding="10")
        results_frame.grid(row=7, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))

        # Wire Size
        ttk.Label(results_frame, text="Wire Size:",
                 font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=3)
        self.wire_size_label = ttk.Label(results_frame, text="-",
                                        style='Result.TLabel')
        self.wire_size_label.grid(row=0, column=1, sticky=tk.W, pady=3, padx=10)

        # Voltage Drop
        ttk.Label(results_frame, text="Voltage Drop:",
                 font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=3)
        self.vdrop_label = ttk.Label(results_frame, text="-",
                                    style='Result.TLabel')
        self.vdrop_label.grid(row=1, column=1, sticky=tk.W, pady=3, padx=10)

        # Percent Voltage Drop
        ttk.Label(results_frame, text="Percent VD:",
                 font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky=tk.W, pady=3)
        self.percent_vd_label = ttk.Label(results_frame, text="-",
                                         style='Result.TLabel')
        self.percent_vd_label.grid(row=2, column=1, sticky=tk.W, pady=3, padx=10)

        # Power Loss
        ttk.Label(results_frame, text="Power Loss:",
                 font=('Arial', 10, 'bold')).grid(row=3, column=0, sticky=tk.W, pady=3)
        self.power_loss_label = ttk.Label(results_frame, text="-",
                                         style='Result.TLabel')
        self.power_loss_label.grid(row=3, column=1, sticky=tk.W, pady=3, padx=10)

    def clear_error_highlighting(self):
        """Remove error highlighting from all entry widgets."""
        for entry in self.entry_widgets:
            entry.configure(style='TEntry')

    def highlight_invalid_entries(self, values):
        """
        Highlight entry widgets with invalid values.

        Args:
            values: List of parsed values (None indicates invalid entry)
        """
        for i, value in enumerate(values):
            if value is None:
                # Create a red border style for invalid entries
                self.entry_widgets[i].configure(foreground='red')
            else:
                self.entry_widgets[i].configure(foreground='black')

    def parse_inputs(self):
        """
        Parse and validate user inputs.

        Returns:
            Tuple of (wire_length, voltage, current, max_vd_percent, material, phase)
            or (None, None, None, None, None, None) if parsing fails
        """
        # Try to parse numeric inputs
        values = []
        inputs = [
            self.length_entry.get(),
            self.voltage_entry.get(),
            self.current_entry.get(),
            self.vdrop_entry.get()
        ]

        for input_str in inputs:
            try:
                value = float(input_str)
                values.append(value)
            except ValueError:
                values.append(None)

        # Check if any parsing failed
        if None in values:
            self.highlight_invalid_entries(values)
            return None, None, None, None, None, None

        # Get dropdown selections
        material = self.material_var.get()
        phase = self.phase_var.get()

        return values[0], values[1], values[2], values[3], material, phase

    def clear_results(self):
        """Clear all result labels."""
        self.wire_size_label.config(text="-")
        self.vdrop_label.config(text="-")
        self.percent_vd_label.config(text="-")
        self.power_loss_label.config(text="-")

    def calculate(self):
        """
        Perform wire sizing calculation when Calculate button is clicked.
        """
        # Clear previous error highlighting
        self.clear_error_highlighting()
        self.error_label.config(text="")
        self.clear_results()

        # Parse inputs
        wire_length, voltage, current, max_vd_percent, material, phase = self.parse_inputs()

        if wire_length is None:
            self.error_label.config(text="*There are errors with your inputs.")
            return

        # Validate inputs
        is_valid, error_message = validate_inputs(wire_length, voltage,
                                                  current, max_vd_percent)
        if not is_valid:
            self.error_label.config(text=f"*{error_message}")
            return

        # Perform wire sizing calculation
        result = select_wire_size(
            wire_length=wire_length,
            voltage=voltage,
            current=current,
            max_voltage_drop_percent=max_vd_percent,
            material=material,
            phase=phase
        )

        # Display results
        if result:
            self.wire_size_label.config(text=result.wire_size)
            self.vdrop_label.config(text=f"{result.voltage_drop:.3f} V")
            self.percent_vd_label.config(text=f"{result.percent_voltage_drop:.3f}%")
            self.power_loss_label.config(text=f"{result.power_loss/1000:.3f} kW")
        else:
            self.error_label.config(
                text="*Your voltage drop could not be met or too much current exists."
            )


def main():
    """Main entry point for the application."""
    root = tk.Tk()
    app = WireSizingCalculatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

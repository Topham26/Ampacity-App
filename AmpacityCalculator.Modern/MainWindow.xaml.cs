using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using System;

namespace AmpacityCalculator;

/// <summary>
/// Main window for the Ampacity Calculator application
/// </summary>
public sealed partial class MainWindow : Window
{
    private Visibility _resultsVisibility = Visibility.Collapsed;

    public MainWindow()
    {
        this.InitializeComponent();
        Title = "Ampacity Calculator - Voltage Drop & Wire Sizing";

        // Set window size
        AppWindow.Resize(new Windows.Graphics.SizeInt32(1200, 800));
    }

    public Visibility ResultsVisibility
    {
        get => _resultsVisibility;
        set
        {
            _resultsVisibility = value;
        }
    }

    /// <summary>
    /// Calculate button click handler - determines proper wire size based on ampacity and voltage drop
    /// </summary>
    private void CalculateButton_Click(object sender, RoutedEventArgs e)
    {
        // Hide previous error and results
        error_message.IsOpen = false;

        // Validate all inputs
        if (!ValidateInputs(out string errorMsg))
        {
            error_message.Message = errorMsg;
            error_message.IsOpen = true;
            HideResults();
            return;
        }

        // Get validated input values
        double length = wire_length.Value;
        double current_val = current.Value;
        double system_voltage = voltage.Value;
        double desired_VD = volt_drop_percent.Value;
        int material_index = material.SelectedIndex;

        // Wire size reference data
        // 30°C ambient, Single insulated conductors, 0-2000V, 72°C conductor rating
        string[] wire_size_key = {
            "14 AWG", "12 AWG", "10 AWG", "8 AWG", "6 AWG", "4 AWG",
            "3 AWG", "2 AWG", "1 AWG", "1/0 AWG", "2/0 AWG", "3/0 AWG",
            "4/0 AWG", "250 kcmil", "300 kcmil", "350 kcmil", "400 kcmil",
            "500 kcmil", "600 kcmil", "750 kcmil"
        };

        double[] Cu_ampacity_key = { 30, 35, 50, 70, 95, 125, 145, 170, 195, 230,
                                     265, 310, 360, 405, 445, 505, 545, 620, 690, 785 };

        double[] Al_ampacity_key = { 0, 30, 40, 55, 75, 100, 115, 135, 155, 180,
                                     210, 240, 280, 315, 350, 395, 425, 485, 540, 620 };

        // 600V cables, 3 phase, 60Hz, 75°C - Resistance in ohms per 1000 ft
        double[] Cu_res_key = { 3.1, 2.0, 1.2, 0.78, 0.49, 0.31, 0.25, 0.19, 0.15, 0.12,
                                0.10, 0.077, 0.062, 0.052, 0.044, 0.038, 0.033, 0.027, 0.023, 0.019 };

        double[] Al_res_key = { 0, 3, 2, 2.0, 1.3, 0.81, 0.51, 0.40, 0.32, 0.25,
                                0.20, 0.16, 0.13, 0.10, 0.085, 0.071, 0.061, 0.054, 0.043, 0.036 };

        // Select appropriate lookup tables based on material
        double[] ampacity_key = material_index == 0 ? Cu_ampacity_key : Al_ampacity_key;
        double[] res_key = material_index == 0 ? Cu_res_key : Al_res_key;

        // Find the appropriate wire size
        bool correct_wire_size = false;
        double VD = 0;
        double percent_VD = 0;
        double power = 0;
        int wireIndex = 0;

        for (int j = 0; j < 20; j++)
        {
            // Check if this wire size can handle the current
            if (ampacity_key[j] > current_val)
            {
                // Calculate voltage drop: VD = (2 × L × R × I) / 1000
                VD = (2 * length * res_key[j] * current_val) / 1000;
                percent_VD = (VD / system_voltage) * 100;

                // Check if voltage drop meets requirement
                if (percent_VD <= desired_VD)
                {
                    correct_wire_size = true;

                    // Calculate power loss: P = I² × R × 2 × L
                    power = current_val * current_val * (res_key[j] / 1000) * 2 * length;
                    wireIndex = j;
                    break;
                }
            }
        }

        if (correct_wire_size)
        {
            // Display results
            chosenSize.Text = wire_size_key[wireIndex];
            ResultsVD.Text = $"{Math.Round(VD, 3)} V";
            ResultsVDper.Text = $"{Math.Round(percent_VD, 3)}%";
            powerloss.Text = $"{Math.Round(power / 1000, 3)} kW";

            ShowResults();
        }
        else
        {
            error_message.Message = "No suitable wire size found. Either the current is too high or the voltage drop requirement cannot be met with available wire sizes.";
            error_message.IsOpen = true;
            HideResults();
        }
    }

    /// <summary>
    /// Validates all input fields
    /// </summary>
    private bool ValidateInputs(out string errorMessage)
    {
        errorMessage = string.Empty;

        if (double.IsNaN(wire_length.Value) || wire_length.Value <= 0)
        {
            errorMessage = "Please enter a valid wire length greater than 0.";
            return false;
        }

        if (double.IsNaN(current.Value) || current.Value <= 0)
        {
            errorMessage = "Please enter a valid current greater than 0.";
            return false;
        }

        if (double.IsNaN(voltage.Value) || voltage.Value <= 0)
        {
            errorMessage = "Please enter a valid voltage greater than 0.";
            return false;
        }

        if (double.IsNaN(volt_drop_percent.Value) || volt_drop_percent.Value <= 0 || volt_drop_percent.Value > 100)
        {
            errorMessage = "Please enter a valid voltage drop percentage between 0 and 100.";
            return false;
        }

        if (material.SelectedIndex < 0)
        {
            errorMessage = "Please select a conductor material.";
            return false;
        }

        if (phases.SelectedIndex < 0)
        {
            errorMessage = "Please select an electrical system type.";
            return false;
        }

        return true;
    }

    /// <summary>
    /// Shows the results section
    /// </summary>
    private void ShowResults()
    {
        _resultsVisibility = Visibility.Visible;
        // Force UI update
        this.Content = this.Content;
    }

    /// <summary>
    /// Hides the results section
    /// </summary>
    private void HideResults()
    {
        _resultsVisibility = Visibility.Collapsed;
        chosenSize.Text = string.Empty;
        ResultsVD.Text = string.Empty;
        ResultsVDper.Text = string.Empty;
        powerloss.Text = string.Empty;
        // Force UI update
        this.Content = this.Content;
    }
}

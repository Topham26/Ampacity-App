# Ampacity Calculator - Modern Windows App

A professional electrical wire sizing calculator for Windows 10/11, built with WinUI 3 and Windows App SDK.

## Features

- **Wire Size Calculation**: Automatically determines the correct wire gauge based on:
  - Current requirements (ampacity)
  - Voltage drop constraints
  - Wire run length
  - System voltage

- **Material Support**:
  - Copper (Cu)
  - Aluminum (Al)

- **Calculations Include**:
  - Actual voltage drop
  - Percentage voltage drop
  - Power loss in conductors
  - Recommended wire size (14 AWG - 750 kcmil)

- **Modern UI**:
  - WinUI 3 Fluent Design
  - Light/Dark theme support
  - Responsive layout
  - Input validation with NumberBox controls
  - Professional card-based results display

## Technical Details

- **Framework**: .NET 8.0
- **UI**: WinUI 3 (Windows App SDK 1.6)
- **Target**: Windows 10 version 1809 (10.0.17763.0) and later
- **Package Type**: MSIX

## Building the Application

### Prerequisites

- Visual Studio 2022 (17.8 or later)
- .NET 8.0 SDK
- Windows App SDK 1.6
- Windows 10 SDK (10.0.19041.0 or later)

### Build Steps

1. Open `AmpacityCalculator.csproj` in Visual Studio 2022
2. Restore NuGet packages
3. Select your target platform (x64, x86, or ARM64)
4. Build and run (F5)

**Command Line Build**:
```bash
dotnet restore
dotnet build -c Release
```

### Deployment

**MSIX Package**:
```bash
dotnet publish -c Release -r win-x64 --self-contained
```

The app is packaged as an MSIX for Windows Store distribution or sideloading.

## Electrical Engineering Reference

### Ampacity Tables

Based on NEC (National Electrical Code) standards:
- Temperature rating: 72°C
- Ambient temperature: 30°C
- Installation: Single insulated conductors
- Voltage rating: 0-2000V

### Voltage Drop Formula

```
VD = (2 × L × R × I) / 1000
```

Where:
- VD = Voltage drop (volts)
- L = One-way length of circuit (feet)
- R = Resistance of conductor (ohms per 1000 ft)
- I = Current (amperes)
- Factor of 2 accounts for both supply and return conductors

### Power Loss Formula

```
P = I² × (R/1000) × 2 × L
```

Where:
- P = Power loss (watts)
- I = Current (amperes)
- R = Resistance (ohms per 1000 ft)
- L = Length (feet)

## NEC Recommendations

- **Branch circuits**: Maximum 3% voltage drop
- **Feeders**: Maximum 5% voltage drop combined with branch circuit
- Lower voltage drop = higher efficiency and better equipment performance

## Project Structure

```
AmpacityCalculator.Modern/
├── App.xaml                    # Application resources
├── App.xaml.cs                 # Application logic
├── MainWindow.xaml             # Main UI layout
├── MainWindow.xaml.cs          # Calculation logic
├── Package.appxmanifest        # App manifest
├── app.manifest                # Windows compatibility
├── AmpacityCalculator.csproj   # Project file
├── Assets/                     # App icons and images
└── Properties/
    └── launchSettings.json     # Debug settings
```

## Migration from Windows 8.1

This is a complete rewrite of the original Windows 8.1 app, modernized for 2025:

### What's New
- ✅ WinUI 3 modern UI with Fluent Design
- ✅ .NET 8.0 (latest LTS)
- ✅ NumberBox controls with built-in validation
- ✅ InfoBar for error messages
- ✅ Responsive card-based layout
- ✅ Theme-aware styling
- ✅ MSIX packaging for Store distribution
- ✅ Improved input validation
- ✅ Better error handling

### Architecture Changes
- **Old**: Windows 8.1 UWP with LayoutAwarePage base class
- **New**: WinUI 3 Desktop with modern Window class
- **Old**: Manual validation with TextBox border colors
- **New**: NumberBox with built-in validation
- **Old**: Simple Grid layout
- **New**: Responsive ScrollViewer with max-width constraints
- **Old**: Windows.UI.Xaml namespace
- **New**: Microsoft.UI.Xaml namespace

## Version History

- **v2.0** (2025): Modern Windows App SDK rewrite
  - WinUI 3 UI framework
  - .NET 8.0
  - Enhanced UX
  - Store-ready MSIX package

- **v1.0** (Original): Windows 8.1 UWP application

## License

Original application by Scott Hummel

## Support

For issues or questions, please refer to the project repository.

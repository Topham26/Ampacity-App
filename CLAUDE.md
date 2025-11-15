# CLAUDE.md - Ampacity Calculator App

## Project Overview

**Ampacity Calculator** is a Windows 8.1 Universal Windows Platform (UWP) application that calculates proper wire sizing for electrical installations based on voltage drop requirements, ampacity ratings, and power loss calculations.

- **Version**: 1.0
- **Platform**: Windows 8.1+ (Minimum OS: 6.2.1)
- **Framework**: .NET Framework for Windows Store Apps
- **Language**: C# with XAML UI
- **Author**: Scott Hummel

## Purpose

This application helps electricians and engineers determine the appropriate wire gauge for electrical installations by:
- Calculating voltage drop across wire runs
- Ensuring ampacity requirements are met
- Computing power loss in conductors
- Supporting both Copper (Cu) and Aluminum (Al) wire materials
- Validating against NEC-based ampacity tables

## Repository Structure

```
Ampacity-App/
├── README.txt                              # Project description
├── CLAUDE.md                               # This file - AI assistant guide
└── Ampacity_Calculator/
    ├── Ampacity_Calculator.sln            # Visual Studio solution file
    └── Ampacity_Calculator/
        ├── Ampacity_Calculator.csproj     # Project file
        ├── Package.appxmanifest           # UWP app manifest
        ├── Ampacity_Calculator_TemporaryKey.pfx  # Development certificate
        │
        ├── App.xaml                       # Application resources
        ├── App.xaml.cs                    # Application lifecycle logic
        ├── MainPage.xaml                  # Main UI layout
        ├── MainPage.xaml.cs               # Main calculation logic
        │
        ├── Assets/                        # Application images
        │   ├── Logo.png
        │   ├── SmallLogo.png
        │   ├── SplashScreen.png
        │   └── StoreLogo.png
        │
        ├── Common/                        # Shared helper classes
        │   ├── BindableBase.cs            # MVVM base class
        │   ├── BooleanNegationConverter.cs # XAML converter
        │   ├── BooleanToVisibilityConverter.cs # XAML converter
        │   ├── LayoutAwarePage.cs         # Page base class with navigation
        │   ├── RichTextColumns.cs         # Multi-column text helper
        │   ├── SuspensionManager.cs       # State persistence
        │   ├── StandardStyles.xaml        # Common UI styles
        │   └── ReadMe.txt                 # Common classes documentation
        │
        ├── Properties/
        │   └── AssemblyInfo.cs            # Assembly metadata
        │
        ├── bin/                           # Build output (ignored in git)
        └── obj/                           # Build intermediates (ignored in git)
```

## Technology Stack

### Core Technologies
- **C#**: Primary programming language
- **XAML**: UI markup language
- **Windows Runtime**: Windows Store App APIs
- **MSBuild**: Build system (Visual Studio 2012+)

### Frameworks & APIs Used
- `Windows.UI.Xaml` - UI framework
- `Windows.ApplicationModel` - App lifecycle
- `Windows.Foundation` - Core Windows Runtime types

### Build Configurations
- **Debug**: Full symbols, no optimization
- **Release**: Optimized, PDB-only symbols
- **Platforms**: AnyCPU, ARM, x64, x86

## Application Architecture

### Entry Point
- **App.xaml.cs**: Application singleton that handles:
  - Application initialization
  - Launch activation
  - Suspend/resume lifecycle
  - Navigation to MainPage

### Main Page (MainPage.xaml.cs:22-196)
The core calculation logic resides in the `Button_Click` event handler:

**Input Fields**:
- `wire_length` - Distance in feet
- `current` - Load current in amperes
- `voltage` - System voltage
- `volt_drop_percent` - Maximum allowable voltage drop percentage
- `material` - Conductor material (Cu/Al)
- `phases` - Electrical system type (Single/Three)

**Calculation Process**:
1. Input validation with visual feedback (red borders on invalid inputs)
2. Material selection determines which lookup tables to use
3. Iterates through wire sizes from 14 AWG to 750 kcmil
4. For each size, checks if ampacity > current requirement
5. Calculates voltage drop: `VD = (2 × length × resistance × current) / 1000`
6. Calculates percentage: `%VD = (VD / system_voltage) × 100`
7. Calculates power loss: `P = I² × R × 2 × length` (MainPage.xaml.cs:172)
8. Returns first wire size meeting both ampacity and voltage drop requirements

**Reference Tables** (MainPage.xaml.cs:126-132):
- **Wire Sizes**: 14 AWG through 750 kcmil (20 standard sizes)
- **Cu Ampacity**: 30-785A @ 72°C, single insulated conductors
- **Al Ampacity**: 30-620A @ 72°C, single insulated conductors
- **Cu Resistance**: 3.1-0.019 Ω/1000ft @ 600V, 3-phase, 60Hz, 75°C
- **Al Resistance**: 3-0.029 Ω/1000ft @ 600V, 3-phase, 60Hz, 75°C

### UI Layout (MainPage.xaml)
- Grid-based responsive design
- 4 columns × 7 rows layout
- Visual states for: FullScreenLandscape, Filled, FullScreenPortrait, Snapped
- Back button navigation support
- Real-time error messaging with red text

### Common Classes
- **LayoutAwarePage**: Base class providing state management and navigation
- **SuspensionManager**: Handles application state persistence
- **Converters**: XAML data binding helpers

## Development Workflows

### Building the Application

**Requirements**:
- Visual Studio 2012 or later
- Windows 8.1 SDK
- MSBuild 4.0+

**Build Commands**:
```bash
# Using MSBuild (from project directory)
msbuild Ampacity_Calculator.sln /p:Configuration=Debug /p:Platform=AnyCPU

# Build for specific platform
msbuild Ampacity_Calculator.sln /p:Configuration=Release /p:Platform=x86
```

**Build Output Locations**:
- Debug: `bin/Debug/`
- Release: `bin/Release/`
- Platform-specific: `bin/{Platform}/{Configuration}/`

### Testing the Application

**Manual Testing**:
1. Open solution in Visual Studio
2. Select target platform (Local Machine, Simulator, or Remote Machine)
3. Press F5 to build and run with debugging
4. Test various input combinations:
   - Valid inputs: numeric values within expected ranges
   - Invalid inputs: text, negative numbers, empty fields
   - Edge cases: very small/large currents, long wire runs

**Expected Behaviors**:
- Invalid inputs show red borders
- Error messages appear in red text (MainPage.xaml.cs:106)
- Results display voltage drop, percentage, wire size, and power loss
- "Too much current" error if no wire size is adequate (MainPage.xaml.cs:188)

### Debugging

**Key Debug Points**:
- `MainPage.xaml.cs:56` - Button click entry
- `MainPage.xaml.cs:84-98` - Input validation loop
- `MainPage.xaml.cs:161-176` - Wire size calculation loop
- `MainPage.xaml.cs:177-184` - Results output

**Common Issues**:
- **Red borders persist**: Inputs contain non-numeric characters
- **No results**: Current too high or voltage drop too restrictive
- **Unexpected calculations**: Check material/phase selection

## Git Workflow

### Branch Strategy
- **Main Branch**: Stable releases (branch name not explicitly configured)
- **Feature Branches**: Use `claude/*` prefix for AI-assisted development
- **Current Branch**: `claude/claude-md-mhzo2qt6zb0ubr2e-01DXUc9WR1ZfR4TfpE8Eh2id`

### Commit History Pattern
Based on recent commits:
1. `6fe75af` - Initial C# project creation
2. `f232289` - Initial layout design
3. `3364808` - Added features and input validation
4. `c79cd28` - Added more functionality
5. `3a2d1a3` - Allows double inputs and power loss calculation

**Commit Message Style**:
- Imperative mood ("Add", "Fix", "Update")
- Concise description of changes
- Focus on what changed functionally

### Making Changes

**Standard Workflow**:
```bash
# 1. Ensure you're on the correct feature branch
git status

# 2. Make code changes
# Edit files as needed

# 3. Stage changes
git add <files>

# 4. Commit with descriptive message
git commit -m "Brief description of changes"

# 5. Push to remote (use -u flag for feature branches)
git push -u origin claude/claude-md-mhzo2qt6zb0ubr2e-01DXUc9WR1ZfR4TfpE8Eh2id
```

**Network Retry Strategy**:
- For push/fetch failures, retry up to 4 times
- Use exponential backoff: 2s, 4s, 8s, 16s
- Critical: Branch must start with 'claude/' and match session ID

## Key Conventions for AI Assistants

### Code Style

**C# Conventions**:
- **Naming**:
  - PascalCase for classes, methods, properties
  - camelCase for local variables
  - snake_case for UI element names (existing convention: `wire_length`, `volt_drop_percent`)
- **Indentation**: 4 spaces (no tabs)
- **Braces**: K&R style (opening brace on same line)
- **Comments**: XML doc comments for public methods

**XAML Conventions**:
- Element names use `x:Name` attribute
- Use meaningful, descriptive names
- Grid positioning via `Grid.Row` and `Grid.Column` attached properties
- Font sizes in points (25pt for inputs, 30pt for results, 15pt for errors)

### Input Validation Pattern

When adding new input fields, follow the existing pattern (MainPage.xaml.cs:84-98):
```csharp
// 1. Add TextBox to user_inputs array
// 2. Loop validates with Double.TryParse
// 3. Set BorderBrush to Red on error, null on success
// 4. Set error_flag to true if any validation fails
// 5. Early return if error_flag is true
```

### Mathematical Calculations

**Voltage Drop Formula** (MainPage.xaml.cs:166):
```
VD = (2 × L × R × I) / 1000
```
- L = wire length (feet)
- R = resistance (ohms per 1000 ft)
- I = current (amperes)
- Factor of 2 accounts for both conductors in circuit

**Power Loss Formula** (MainPage.xaml.cs:172):
```
P = I² × (R/1000) × 2 × L
```
- Result in watts
- Displayed in kilowatts (P/1000)

### Error Handling

**Error Message Display** (MainPage.xaml.cs:106, 188):
- Use `error_message.Text` TextBlock for all errors
- Clear result fields when displaying errors
- Prefix messages with asterisk: `"*There are errors..."`
- Two error types:
  1. Input validation errors
  2. Calculation constraint errors (no valid wire size)

### Adding New Features

**When adding wire sizes**:
1. Update all 5 arrays in sync (MainPage.xaml.cs:126-132)
2. Adjust loop limit (currently `j<=19` for 20 sizes)
3. Ensure ampacity and resistance values correspond to same wire size

**When adding UI elements**:
1. Add to XAML grid with appropriate Row/Column
2. Follow existing sizing conventions (Height="50" for inputs)
3. Add to validation loop if it's an input field
4. Update results clearing code in error handler

**When modifying calculations**:
1. Document formulas in comments
2. Use `Math.Round()` for display values (3 decimal places)
3. Maintain unit consistency (feet, amps, volts, ohms)

### Common Files to Modify

**Adding Features**:
- `MainPage.xaml.cs` - Calculation logic
- `MainPage.xaml` - UI layout

**Changing App Metadata**:
- `Package.appxmanifest` - App name, publisher, capabilities
- `Properties/AssemblyInfo.cs` - Version, copyright

**Updating Resources**:
- `Assets/` - Replace logo/splash screen images
- `Common/StandardStyles.xaml` - App-wide styling

### Code Patterns to Preserve

**Do NOT modify**:
- `Common/` directory classes without understanding Visual Studio template dependencies
- LayoutAwarePage inheritance (required for navigation)
- Standard Windows 8.1 app lifecycle events
- Visual state management structure

**Safe to modify**:
- MainPage calculation logic
- Input validation rules
- Wire size lookup tables
- UI layout and styling
- Error messages

### Testing Checklist

Before committing changes:
- [ ] App builds without errors (`msbuild`)
- [ ] All input validations work (try invalid text, negatives, empty)
- [ ] Calculations produce expected results for known inputs
- [ ] Error messages display correctly
- [ ] Results clear properly when errors occur
- [ ] No regression in existing functionality
- [ ] UI remains responsive in all visual states

## Electrical Engineering Context

### Understanding Ampacity
**Ampacity** = Current-carrying capacity of a conductor without exceeding temperature rating

Factors affecting ampacity:
- Conductor material (Cu has higher conductivity than Al)
- Conductor size (larger = more ampacity)
- Insulation temperature rating (this app uses 72°C)
- Installation method (single insulated conductors)
- Ambient temperature (30°C basis)

### Understanding Voltage Drop
**Voltage Drop** = Voltage lost due to conductor resistance

NEC recommendations:
- 3% maximum for branch circuits
- 5% maximum combined (feeder + branch)
- Lower voltage drop = more efficient system

### Wire Sizing Priority
1. **Ampacity**: Wire must handle current without overheating
2. **Voltage Drop**: Wire must deliver adequate voltage to load
3. **Physical**: Wire must fit in conduit/connections
4. **Economic**: Larger wire costs more but reduces energy loss

This app sizes primarily by voltage drop, which often requires larger wire than ampacity alone.

## Troubleshooting

### Build Errors

**"Cannot find Windows SDK"**:
- Install Windows 8.1 SDK
- Update project to target installed SDK version

**"Certificate error"**:
- Regenerate `Ampacity_Calculator_TemporaryKey.pfx`
- Or disable package signing for development

### Runtime Errors

**"Failed to create initial page"** (App.xaml.cs:69):
- Check MainPage constructor
- Verify XAML compiles without errors
- Ensure InitializeComponent() succeeds

**Application suspends immediately**:
- Check app manifest capabilities
- Verify app certificate is valid

### Calculation Issues

**No results for valid inputs**:
1. Check if current exceeds maximum ampacity (785A for Cu, 620A for Al)
2. Verify voltage drop requirement is achievable
3. Ensure resistance/ampacity tables are indexed correctly

**Incorrect voltage drop**:
- Verify formula uses resistance in Ω/1000ft (not Ω/ft)
- Check that "2×L" factor is present (accounts for both wires)
- Confirm system voltage is correct

## Future Enhancement Ideas

Potential improvements for AI assistants to implement:

1. **Three-Phase Support**: Currently UI has phase selector but calculation doesn't use it
2. **Temperature Correction**: Adjust ampacity for ambient temperature
3. **Conduit Fill**: Warn when too many conductors in conduit
4. **Cost Analysis**: Calculate wire cost vs. energy savings
5. **Unit Conversion**: Support metric units (meters, mm²)
6. **Save/Load**: Persist calculations for later reference
7. **Print/Export**: Generate professional calculation reports
8. **More Materials**: Add tinned copper, silver, etc.
9. **Code Compliance**: Flag NEC violations
10. **Multi-Run**: Calculate wire sizing for multiple circuits

## Additional Resources

### Microsoft Documentation
- [Windows Store App Development](https://docs.microsoft.com/windows/apps/)
- [XAML Overview](https://docs.microsoft.com/windows/uwp/xaml-platform/)
- [App Lifecycle](https://docs.microsoft.com/windows/uwp/launch-resume/app-lifecycle)

### Electrical Standards
- NEC (National Electrical Code) - Wire sizing requirements
- NEC Table 310.15(B)(16) - Ampacity ratings (basis for this app's tables)
- NEC Chapter 9, Table 8 - Conductor resistance values

### Tools
- Visual Studio 2012+ for development
- Windows App Certification Kit for store submission
- MSBuild for command-line builds

## Version History

- **v1.0** (Current): Initial release with core calculator functionality
  - Wire sizing based on ampacity and voltage drop
  - Cu/Al material support
  - Input validation
  - Power loss calculation

---

**Last Updated**: 2025-11-15
**Maintained By**: AI assistants working with this codebase
**Contact**: Scott Hummel (original author)

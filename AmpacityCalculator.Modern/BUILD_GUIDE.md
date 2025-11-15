# Build Guide - Ampacity Calculator MSIX Package

This guide explains how to build the MSIX package for the Ampacity Calculator Windows App SDK application.

## Prerequisites

### Required Software

1. **Windows 10 SDK** (10.0.19041.0 or later)
   - Download from: https://developer.microsoft.com/windows/downloads/windows-sdk/

2. **.NET 8.0 SDK**
   - Download from: https://dotnet.microsoft.com/download/dotnet/8.0

3. **Visual Studio 2022** (Optional but recommended)
   - Edition: Community, Professional, or Enterprise (17.8+)
   - Workloads:
     - ".NET desktop development"
     - "Universal Windows Platform development"
     - "Windows application development"

4. **Windows App SDK 1.6**
   - Installed automatically via NuGet during build
   - Package: `Microsoft.WindowsAppSDK` version 1.6.241114003

### System Requirements

- **OS**: Windows 10 version 1809 (build 17763) or later
- **Architecture**: x64, x86, or ARM64
- **Disk Space**: ~2 GB free for build outputs
- **RAM**: 4 GB minimum, 8 GB recommended

## Build Methods

### Method 1: Using Build Scripts (Recommended)

#### Windows (PowerShell)

```powershell
# Navigate to project directory
cd AmpacityCalculator.Modern

# Build Release x64 package
.\build-msix.ps1

# Build with specific configuration
.\build-msix.ps1 -Configuration Release -Platform x64

# Build self-contained package
.\build-msix.ps1 -Configuration Release -Platform x64 -SelfContained

# Build for ARM64
.\build-msix.ps1 -Configuration Release -Platform ARM64
```

#### Linux/macOS (Bash)

```bash
# Navigate to project directory
cd AmpacityCalculator.Modern

# Build Release x64 package
./build-msix.sh

# Build with specific configuration
./build-msix.sh Release x64

# Build self-contained package
./build-msix.sh Release x64 true

# Build for ARM64
./build-msix.sh Release ARM64
```

### Method 2: Using .NET CLI

```bash
# Navigate to project directory
cd AmpacityCalculator.Modern

# Restore NuGet packages
dotnet restore

# Build the project
dotnet build -c Release

# Publish as MSIX (framework-dependent)
dotnet publish -c Release -r win-x64

# Publish as MSIX (self-contained)
dotnet publish -c Release -r win-x64 --self-contained

# Publish for other platforms
dotnet publish -c Release -r win-x86      # 32-bit
dotnet publish -c Release -r win-arm64    # ARM64
```

### Method 3: Using Visual Studio 2022

1. **Open the project**
   - File → Open → Project/Solution
   - Select: `AmpacityCalculator.csproj`

2. **Set build configuration**
   - Configuration: Release
   - Platform: x64 (or x86, ARM64)

3. **Build the project**
   - Build → Build Solution (Ctrl+Shift+B)

4. **Publish MSIX package**
   - Right-click project → Publish
   - Select "Create MSIX Package"
   - Follow the wizard

## Build Outputs

### Directory Structure

```
bin/
└── Release/
    └── net8.0-windows10.0.19041.0/
        └── win-x64/
            ├── AmpacityCalculator.exe       # Application executable
            ├── AmpacityCalculator.dll       # Application library
            ├── *.msix                       # MSIX package (if generated)
            └── publish/
                └── *.msix                   # Published MSIX package
```

### Package Sizes (Approximate)

| Type | Size |
|------|------|
| Framework-dependent | 8-15 MB |
| Self-contained | 70-90 MB |

## Package Identity

The MSIX package is configured with:

- **Name**: `ScottHummel.AmpacityCalculator`
- **Publisher**: `CN=Scott Hummel`
- **Version**: `2.0.0.0`
- **App ID**: `App`

### For Store Submission

Before submitting to Microsoft Store, update these values in `Package.appxmanifest`:

```xml
<Identity
  Name="[YourPublisherId].AmpacityCalculator"
  Publisher="CN=[Your Publisher Name]"
  Version="2.0.0.0" />
```

You'll receive your Publisher ID from [Microsoft Partner Center](https://partner.microsoft.com/dashboard).

## Signing the Package

### For Development/Testing

Windows automatically generates a test certificate. No action needed.

### For Store Submission

The Microsoft Store will sign your package automatically.

### For Enterprise/Sideloading

```powershell
# Create a self-signed certificate
New-SelfSignedCertificate -Type CodeSigningCert -Subject "CN=YourCompany" -KeyUsage DigitalSignature -FriendlyName "App Signing Cert" -CertStoreLocation "Cert:\CurrentUser\My"

# Sign the MSIX package
SignTool sign /fd SHA256 /a /f YourCertificate.pfx /p CertPassword AmpacityCalculator.msix
```

## Testing the Package

### Install Locally

```powershell
# Install the MSIX package
Add-AppxPackage -Path "path\to\AmpacityCalculator.msix"

# Launch the app
Start-Process "shell:AppsFolder\ScottHummel.AmpacityCalculator_[hash]!App"

# Uninstall
Remove-AppxPackage -Package "ScottHummel.AmpacityCalculator_2.0.0.0_x64__[hash]"
```

### Enable Developer Mode

For sideloading, enable Developer Mode in Windows:
- Settings → Update & Security → For developers → Developer mode

## Troubleshooting

### Build Errors

**"Windows SDK not found"**
```
Solution: Install Windows 10 SDK (10.0.19041.0 or later)
```

**"The command dotnet was not found"**
```
Solution: Install .NET 8.0 SDK and ensure it's in PATH
```

**"Package signature validation failed"**
```
Solution: Enable Developer Mode in Windows Settings
```

**"Application failed to launch"**
```
Solution: Check Windows Event Viewer → Application logs
Ensure Windows App SDK runtime is installed
```

### Runtime Errors

**Missing DLLs**
```
Solution: Build as self-contained:
dotnet publish -c Release -r win-x64 --self-contained
```

**Access Denied**
```
Solution: Run PowerShell as Administrator for installation
```

## Publishing to Microsoft Store

### Steps

1. **Create Partner Center Account**
   - Visit: https://partner.microsoft.com/dashboard
   - Enroll in Windows Developer Program ($19 one-time fee for individuals)

2. **Reserve App Name**
   - Dashboard → Create a new app
   - Reserve "Ampacity Calculator" or desired name

3. **Update Package Identity**
   - Copy Publisher ID from Partner Center
   - Update `Package.appxmanifest` with correct Name and Publisher

4. **Rebuild Package**
   - Use the build scripts with updated manifest

5. **Create Submission**
   - Dashboard → App overview → Start your submission
   - Upload MSIX package
   - Complete pricing, properties, and age rating
   - Add descriptions and screenshots
   - Submit for certification

6. **Certification**
   - Microsoft reviews app (typically 1-3 days)
   - Fix any issues reported
   - Once approved, app goes live on Store

### Store Listing Requirements

- **Screenshots**: At least 1 (1920x1080 or 1366x768)
- **Description**: Clear explanation of features
- **Keywords**: "wire sizing", "electrical", "ampacity", "voltage drop", "NEC"
- **Privacy Policy**: URL if app collects data (not required for this app)
- **Age Rating**: IARC rating questionnaire

## Asset Requirements

All required assets are included in `Assets/` directory:

| Asset | Size | Purpose |
|-------|------|---------|
| Square150x150Logo.png | 150×150 | Medium tile |
| Square44x44Logo.png | 44×44 | App list icon |
| Wide310x150Logo.png | 310×150 | Wide tile |
| SplashScreen.png | 620×300 | Splash screen |
| StoreLogo.png | 50×50 | Store listing |

All assets feature wire-themed graphics with copper and aluminum wire colors.

## Version Management

To update the version number:

1. Open `Package.appxmanifest`
2. Update `<Identity Version="X.Y.Z.0" />`
3. Rebuild package
4. Submit update to Store

Version format: `Major.Minor.Build.Revision`
- Increment Major for breaking changes
- Increment Minor for new features
- Increment Build for bug fixes

## Advanced Configuration

### Custom Build Properties

Edit `AmpacityCalculator.csproj` to customize:

```xml
<PropertyGroup>
  <!-- Change target Windows version -->
  <TargetFramework>net8.0-windows10.0.22621.0</TargetFramework>

  <!-- Change minimum Windows version -->
  <TargetPlatformMinVersion>10.0.17763.0</TargetPlatformMinVersion>

  <!-- Change package type -->
  <WindowsPackageType>MSIX</WindowsPackageType>

  <!-- Enable trimming for smaller package -->
  <PublishTrimmed>true</PublishTrimmed>
</PropertyGroup>
```

### Continuous Integration

For automated builds in CI/CD:

```yaml
# GitHub Actions example
- name: Build MSIX
  run: |
    dotnet restore
    dotnet build -c Release
    dotnet publish -c Release -r win-x64
```

## Support

For build issues:
- Check [Windows App SDK Documentation](https://docs.microsoft.com/windows/apps/windows-app-sdk/)
- Review [.NET 8 Documentation](https://docs.microsoft.com/dotnet/core/whats-new/dotnet-8)
- File issues on the project repository

---

**Last Updated**: 2025-11-15
**App Version**: 2.0.0
**Build System**: .NET 8.0 + Windows App SDK 1.6

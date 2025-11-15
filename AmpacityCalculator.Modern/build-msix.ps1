# Build MSIX Package for Ampacity Calculator
# This script builds the Windows App SDK application and creates an MSIX package

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet('Debug', 'Release')]
    [string]$Configuration = 'Release',

    [Parameter(Mandatory=$false)]
    [ValidateSet('x64', 'x86', 'ARM64')]
    [string]$Platform = 'x64',

    [Parameter(Mandatory=$false)]
    [switch]$SelfContained = $false
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Ampacity Calculator - MSIX Build Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Configuration: $Configuration" -ForegroundColor Yellow
Write-Host "Platform: $Platform" -ForegroundColor Yellow
Write-Host "Self-Contained: $SelfContained" -ForegroundColor Yellow
Write-Host ""

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# Step 1: Clean previous builds
Write-Host "[1/5] Cleaning previous builds..." -ForegroundColor Green
if (Test-Path "bin") { Remove-Item -Recurse -Force "bin" }
if (Test-Path "obj") { Remove-Item -Recurse -Force "obj" }
Write-Host "      ✓ Cleaned" -ForegroundColor Gray

# Step 2: Restore NuGet packages
Write-Host "[2/5] Restoring NuGet packages..." -ForegroundColor Green
dotnet restore
if ($LASTEXITCODE -ne 0) {
    Write-Host "      ✗ Restore failed!" -ForegroundColor Red
    exit $LASTEXITCODE
}
Write-Host "      ✓ Packages restored" -ForegroundColor Gray

# Step 3: Build the project
Write-Host "[3/5] Building project..." -ForegroundColor Green
dotnet build --configuration $Configuration --no-restore
if ($LASTEXITCODE -ne 0) {
    Write-Host "      ✗ Build failed!" -ForegroundColor Red
    exit $LASTEXITCODE
}
Write-Host "      ✓ Build succeeded" -ForegroundColor Gray

# Step 4: Publish with MSIX packaging
Write-Host "[4/5] Publishing MSIX package..." -ForegroundColor Green
$PublishArgs = @(
    'publish'
    '--configuration', $Configuration
    '--runtime', "win-$Platform"
    '--no-build'
)

if ($SelfContained) {
    $PublishArgs += '--self-contained'
} else {
    $PublishArgs += '--no-self-contained'
}

& dotnet @PublishArgs
if ($LASTEXITCODE -ne 0) {
    Write-Host "      ✗ Publish failed!" -ForegroundColor Red
    exit $LASTEXITCODE
}
Write-Host "      ✓ Published successfully" -ForegroundColor Gray

# Step 5: Locate MSIX package
Write-Host "[5/5] Locating MSIX package..." -ForegroundColor Green
$MsixPath = Get-ChildItem -Path "bin\$Configuration" -Filter "*.msix" -Recurse | Select-Object -First 1

if ($MsixPath) {
    Write-Host "      ✓ MSIX package created:" -ForegroundColor Gray
    Write-Host "        $($MsixPath.FullName)" -ForegroundColor White
    Write-Host "        Size: $([math]::Round($MsixPath.Length / 1MB, 2)) MB" -ForegroundColor White
} else {
    Write-Host "      ⚠ MSIX package not found (may need Windows SDK)" -ForegroundColor Yellow
    Write-Host "        Check: bin\$Configuration\net8.0-windows10.0.19041.0\win-$Platform\publish\" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Build Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Test the package: Add-AppxPackage -Path <msix-file>" -ForegroundColor White
Write-Host "  2. Sign for distribution (required for Store)" -ForegroundColor White
Write-Host "  3. Submit to Microsoft Partner Center" -ForegroundColor White
Write-Host ""

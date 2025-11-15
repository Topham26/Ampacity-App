#!/bin/bash
# Build MSIX Package for Ampacity Calculator
# This script builds the Windows App SDK application and creates an MSIX package

set -e

# Configuration
CONFIGURATION="${1:-Release}"
PLATFORM="${2:-x64}"
SELF_CONTAINED="${3:-false}"

echo "========================================"
echo "Ampacity Calculator - MSIX Build Script"
echo "========================================"
echo ""
echo "Configuration: $CONFIGURATION"
echo "Platform: $PLATFORM"
echo "Self-Contained: $SELF_CONTAINED"
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Step 1: Clean previous builds
echo "[1/5] Cleaning previous builds..."
rm -rf bin obj
echo "      ✓ Cleaned"

# Step 2: Restore NuGet packages
echo "[2/5] Restoring NuGet packages..."
dotnet restore
echo "      ✓ Packages restored"

# Step 3: Build the project
echo "[3/5] Building project..."
dotnet build --configuration "$CONFIGURATION" --no-restore
echo "      ✓ Build succeeded"

# Step 4: Publish with MSIX packaging
echo "[4/5] Publishing MSIX package..."
if [ "$SELF_CONTAINED" = "true" ]; then
    dotnet publish --configuration "$CONFIGURATION" --runtime "win-$PLATFORM" --self-contained --no-build
else
    dotnet publish --configuration "$CONFIGURATION" --runtime "win-$PLATFORM" --no-self-contained --no-build
fi
echo "      ✓ Published successfully"

# Step 5: Locate MSIX package
echo "[5/5] Locating MSIX package..."
MSIX_FILE=$(find bin/$CONFIGURATION -name "*.msix" -type f | head -1)

if [ -n "$MSIX_FILE" ]; then
    MSIX_SIZE=$(du -h "$MSIX_FILE" | cut -f1)
    echo "      ✓ MSIX package created:"
    echo "        $MSIX_FILE"
    echo "        Size: $MSIX_SIZE"
else
    echo "      ⚠ MSIX package not found (may need Windows SDK)"
    echo "        Check: bin/$CONFIGURATION/net8.0-windows10.0.19041.0/win-$PLATFORM/publish/"
fi

echo ""
echo "========================================"
echo "Build Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "  1. Test the package: Add-AppxPackage -Path <msix-file>"
echo "  2. Sign for distribution (required for Store)"
echo "  3. Submit to Microsoft Partner Center"
echo ""

# Usage information
if [ "$1" = "--help" ]; then
    echo "Usage: $0 [Configuration] [Platform] [SelfContained]"
    echo ""
    echo "Arguments:"
    echo "  Configuration: Debug or Release (default: Release)"
    echo "  Platform: x64, x86, or ARM64 (default: x64)"
    echo "  SelfContained: true or false (default: false)"
    echo ""
    echo "Examples:"
    echo "  $0                          # Build Release x64"
    echo "  $0 Debug                    # Build Debug x64"
    echo "  $0 Release ARM64            # Build Release ARM64"
    echo "  $0 Release x64 true         # Build Release x64 self-contained"
    echo ""
fi

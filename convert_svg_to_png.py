#!/usr/bin/env python3
"""Convert SVG icons to PNG format for Windows App packaging."""

import cairosvg
import os

# Define the assets directory
assets_dir = "/home/user/Ampacity-App/AmpacityCalculator.Modern/Assets"

# Define conversions: (svg_file, png_file, width, height)
conversions = [
    ("Square150x150Logo.svg", "Square150x150Logo.png", 150, 150),
    ("Square44x44Logo.svg", "Square44x44Logo.png", 44, 44),
    ("Wide310x150Logo.svg", "Wide310x150Logo.png", 310, 150),
    ("SplashScreen.svg", "SplashScreen.png", 620, 300),
    ("StoreLogo.svg", "StoreLogo.png", 50, 50),
]

print("Converting SVG files to PNG...")
print("-" * 50)

for svg_name, png_name, width, height in conversions:
    svg_path = os.path.join(assets_dir, svg_name)
    png_path = os.path.join(assets_dir, png_name)

    if os.path.exists(svg_path):
        try:
            cairosvg.svg2png(
                url=svg_path,
                write_to=png_path,
                output_width=width,
                output_height=height
            )
            print(f"✓ Created {png_name} ({width}x{height})")
        except Exception as e:
            print(f"✗ Failed to convert {svg_name}: {e}")
    else:
        print(f"✗ SVG file not found: {svg_name}")

print("-" * 50)
print("Conversion complete!")

# List all PNG files in the Assets directory
print("\nPNG files in Assets directory:")
for file in sorted(os.listdir(assets_dir)):
    if file.endswith('.png'):
        file_path = os.path.join(assets_dir, file)
        size = os.path.getsize(file_path)
        print(f"  {file} ({size:,} bytes)")

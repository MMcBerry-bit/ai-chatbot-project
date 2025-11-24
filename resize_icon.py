# Resize icon to all required Microsoft Store sizes
from PIL import Image
import os

# Ask for the downloaded icon path
print("Icon Resizer for Microsoft Store")
print("=" * 50)

icon_path = input("Enter path to your Canva icon (or drag & drop file here): ").strip('"').strip("'")

if not os.path.exists(icon_path):
    print(f"Error: File not found: {icon_path}")
    input("Press Enter to exit...")
    exit(1)

# Load the original icon
try:
    original = Image.open(icon_path)
    print(f"Loaded icon: {icon_path}")
    print(f"Original size: {original.size}")
except Exception as e:
    print(f"Error loading image: {e}")
    input("Press Enter to exit...")
    exit(1)

# Create Assets folder if it doesn't exist
os.makedirs('Assets', exist_ok=True)

# Required sizes for Microsoft Store
sizes = {
    'Square44x44Logo.png': (44, 44),
    'StoreLogo.png': (50, 50),
    'Square71x71Logo.png': (71, 71),
    'Square150x150Logo.png': (150, 150),
    'Square310x310Logo.png': (310, 310),
}

# Wide logo (different aspect ratio - crop from center)
wide_size = {
    'Wide310x150Logo.png': (310, 150),
}

# Splash screen
splash_size = {
    'SplashScreen.png': (620, 300),
}

print("\nResizing to square sizes...")
for filename, size in sizes.items():
    # Use high-quality Lanczos resampling
    resized = original.resize(size, Image.Resampling.LANCZOS)
    output_path = os.path.join('Assets', filename)
    resized.save(output_path, 'PNG')
    print(f"  Created: {filename} ({size[0]}x{size[1]})")

print("\nCreating wide logo (310x150)...")
# For wide logo, crop the center portion
wide_img = original.resize((310, 310), Image.Resampling.LANCZOS)
# Crop to 310x150 (remove top and bottom)
left = 0
top = (310 - 150) // 2
right = 310
bottom = top + 150
wide_cropped = wide_img.crop((left, top, right, bottom))
wide_cropped.save('Assets/Wide310x150Logo.png', 'PNG')
print(f"  Created: Wide310x150Logo.png (310x150)")

print("\nCreating splash screen (620x300)...")
# For splash screen, scale up the wide version
splash_img = wide_cropped.resize((620, 300), Image.Resampling.LANCZOS)
splash_img.save('Assets/SplashScreen.png', 'PNG')
print(f"  Created: SplashScreen.png (620x300)")

print("\n" + "=" * 50)
print("SUCCESS! All icons created in Assets/ folder")
print("\nFiles created:")
print("  - Square44x44Logo.png (44x44)")
print("  - StoreLogo.png (50x50)")
print("  - Square71x71Logo.png (71x71)")
print("  - Square150x150Logo.png (150x150)")
print("  - Square310x310Logo.png (310x310)")
print("  - Wide310x150Logo.png (310x150)")
print("  - SplashScreen.png (620x300)")

print("\nNext steps:")
print("  1. Review icons in Assets/ folder")
print("  2. Rebuild MSIX: .\\create_msix_simple.ps1")
print("  3. Test the app with new icons")

input("\nPress Enter to exit...")

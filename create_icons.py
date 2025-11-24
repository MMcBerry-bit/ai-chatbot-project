# Create placeholder icons for Microsoft Store
from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, filename):
    """Create a simple icon with gradient background"""
    # Create image with gradient
    img = Image.new('RGB', (size, size), color=(0, 122, 204))  # Microsoft blue
    draw = ImageDraw.Draw(img)
    
    # Add gradient effect
    for i in range(size):
        alpha = int(255 * (1 - i / size * 0.3))
        draw.rectangle([(0, i), (size, i+1)], fill=(0, 122, 204, alpha))
    
    # Add text "AI"
    try:
        # Try to use a nice font
        font_size = size // 2
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    # Draw "AI" in center
    text = "AI"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((size - text_width) // 2, (size - text_height) // 2 - bbox[1])
    
    draw.text(position, text, fill='white', font=font)
    
    # Save
    os.makedirs('Assets', exist_ok=True)
    img.save(f'Assets/{filename}', 'PNG')
    print(f"✅ Created {filename} ({size}x{size})")

# Create all required icon sizes
print("🎨 Creating Microsoft Store Icons...")
print("=" * 50)

icons = [
    (44, 'Square44x44Logo.png'),
    (50, 'StoreLogo.png'),
    (71, 'Square71x71Logo.png'),
    (150, 'Square150x150Logo.png'),
    (310, 'Square310x310Logo.png'),
]

# Create wide logo (different aspect ratio)
def create_wide_icon():
    img = Image.new('RGB', (310, 150), color=(0, 122, 204))
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except:
        font = ImageFont.load_default()
    
    text = "AI Chatbot"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((310 - text_width) // 2, (150 - text_height) // 2 - bbox[1])
    
    draw.text(position, text, fill='white', font=font)
    
    os.makedirs('Assets', exist_ok=True)
    img.save('Assets/Wide310x150Logo.png', 'PNG')
    print("✅ Created Wide310x150Logo.png (310x150)")

# Create splash screen
def create_splash():
    img = Image.new('RGB', (620, 300), color=(0, 122, 204))
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("arial.ttf", 80)
    except:
        font = ImageFont.load_default()
    
    text = "AI Chatbot"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((620 - text_width) // 2, (300 - text_height) // 2 - bbox[1])
    
    draw.text(position, text, fill='white', font=font)
    
    os.makedirs('Assets', exist_ok=True)
    img.save('Assets/SplashScreen.png', 'PNG')
    print("✅ Created SplashScreen.png (620x300)")

try:
    for size, filename in icons:
        create_icon(size, filename)
    
    create_wide_icon()
    create_splash()
    
    print("\n" + "=" * 50)
    print("🎉 All icons created in Assets/ folder!")
    print("\n💡 Note: These are placeholder icons.")
    print("   For a professional app, create custom icons with:")
    print("   • Your app logo/branding")
    print("   • Transparent backgrounds")
    print("   • Professional design tools (Adobe Illustrator, Figma, etc.)")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\n📦 Installing Pillow (PIL)...")
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'Pillow'])
    print("✅ Pillow installed! Please run this script again.")

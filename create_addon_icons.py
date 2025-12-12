"""
Create icons for Microsoft Store IAP Add-ons
300x300px icons for Unlimited Messages and Premium Subscription
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def create_unlimited_icon():
    """Create icon for Unlimited Messages add-on"""
    # Create image with gradient background
    size = 300
    img = Image.new('RGB', (size, size), '#4CAF50')
    draw = ImageDraw.Draw(img)
    
    # Draw gradient effect
    for y in range(size):
        alpha = int(255 * (y / size))
        color = (76, 175, 80 - int(30 * (y / size)))
        draw.line([(0, y), (size, y)], fill=color)
    
    # Draw infinity symbol (∞)
    draw.ellipse([60, 110, 140, 190], outline='white', width=12)
    draw.ellipse([160, 110, 240, 190], outline='white', width=12)
    
    # Draw connecting curves for infinity
    draw.arc([100, 120, 200, 180], 180, 0, fill='white', width=12)
    
    # Add text
    try:
        font = ImageFont.truetype("arial.ttf", 40)
        small_font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Text "UNLIMITED"
    text = "UNLIMITED"
    bbox = draw.textbbox((0, 0), text, font=small_font)
    text_width = bbox[2] - bbox[0]
    text_x = (size - text_width) // 2
    draw.text((text_x, 220), text, fill='white', font=small_font)
    
    # Save
    output_path = Path("Assets") / "unlimited_icon.png"
    output_path.parent.mkdir(exist_ok=True)
    img.save(output_path)
    print(f"✅ Created: {output_path}")
    return output_path

def create_premium_icon():
    """Create icon for Premium Subscription add-on"""
    # Create image with gradient background
    size = 300
    img = Image.new('RGB', (size, size), '#9C27B0')
    draw = ImageDraw.Draw(img)
    
    # Draw gradient effect
    for y in range(size):
        alpha = int(255 * (y / size))
        color = (156, 39, 176 - int(40 * (y / size)))
        draw.line([(0, y), (size, y)], fill=color)
    
    # Draw crown shape
    crown_color = '#FFD700'
    
    # Crown base
    draw.polygon([
        (80, 180),
        (220, 180),
        (210, 200),
        (90, 200)
    ], fill=crown_color)
    
    # Crown points
    draw.polygon([
        (90, 180),
        (100, 140),
        (110, 180)
    ], fill=crown_color)
    
    draw.polygon([
        (130, 180),
        (150, 120),
        (170, 180)
    ], fill=crown_color)
    
    draw.polygon([
        (190, 180),
        (200, 140),
        (210, 180)
    ], fill=crown_color)
    
    # Add sparkles
    sparkle_color = 'white'
    draw.line([(60, 100), (70, 100)], fill=sparkle_color, width=3)
    draw.line([(65, 95), (65, 105)], fill=sparkle_color, width=3)
    
    draw.line([(230, 130), (240, 130)], fill=sparkle_color, width=3)
    draw.line([(235, 125), (235, 135)], fill=sparkle_color, width=3)
    
    draw.line([(240, 90), (250, 90)], fill=sparkle_color, width=3)
    draw.line([(245, 85), (245, 95)], fill=sparkle_color, width=3)
    
    # Add text
    try:
        font = ImageFont.truetype("arial.ttf", 40)
        small_font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Text "PREMIUM"
    text = "PREMIUM"
    bbox = draw.textbbox((0, 0), text, font=small_font)
    text_width = bbox[2] - bbox[0]
    text_x = (size - text_width) // 2
    draw.text((text_x, 220), text, fill='white', font=small_font)
    
    # Save
    output_path = Path("Assets") / "premium_icon.png"
    output_path.parent.mkdir(exist_ok=True)
    img.save(output_path)
    print(f"✅ Created: {output_path}")
    return output_path

def main():
    """Create both add-on icons"""
    print("🎨 Creating Microsoft Store Add-on Icons...")
    print("=" * 60)
    
    print("\n📦 Creating Unlimited Messages icon...")
    unlimited_path = create_unlimited_icon()
    
    print("\n👑 Creating Premium Subscription icon...")
    premium_path = create_premium_icon()
    
    print("\n" + "=" * 60)
    print("🎉 Icons created successfully!")
    print(f"\n📁 Location: Assets/")
    print(f"   • unlimited_icon.png (300x300px)")
    print(f"   • premium_icon.png (300x300px)")
    print("\n📋 Next Steps:")
    print("1. Open Assets/ folder")
    print("2. Review the icons")
    print("3. Upload to Partner Center when creating add-ons")
    print("   (Store Listings section for each add-on)")

if __name__ == "__main__":
    main()

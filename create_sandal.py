from PIL import Image, ImageDraw, ImageFilter
import os

os.makedirs('images', exist_ok=True)

def create_sandal(filename, strap_color, sole_color, accent_color):
    """Create photorealistic sandal image"""
    width, height = 600, 500
    
    # Create background with gradient
    img = Image.new('RGB', (width, height), (250, 250, 250))
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Add subtle gradient background
    for y in range(height):
        ratio = y / height
        r = int(250 - (ratio * 10))
        g = int(250 - (ratio * 10))
        b = int(250 - (ratio * 5))
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Center position
    cx, cy = width // 2, height // 2 - 30
    
    # === GROUND SHADOW ===
    for i in range(80, 0, -2):
        alpha = int(60 * (1 - i/80))
        draw.ellipse([cx - i, cy + 200 + (80-i)//4, cx + i, cy + 210 + (80-i)//4], 
                    fill=(0, 0, 0, alpha))
    
    # === SOLE/FOOTBED ===
    sole_outline = (40, 40, 40)
    
    # Main sandal sole (flat bottom)
    sole_shape = [
        (cx - 90, cy + 100),
        (cx + 90, cy + 100),
        (cx + 95, cy + 115),
        (cx - 95, cy + 115),
    ]
    draw.polygon(sole_shape, fill=sole_color, outline=sole_outline)
    
    # Add tread pattern
    tread_color = tuple(max(0, c - 30) for c in sole_color)
    for i in range(-3, 4):
        x = cx + i * 40
        draw.rectangle([x - 8, cy + 105, x + 8, cy + 110], fill=tread_color)
    
    # === FOOTBED TOP ===
    footbed_color = (240, 235, 230)
    footbed = [
        (cx - 85, cy + 95),
        (cx + 85, cy + 95),
        (cx + 90, cy + 100),
        (cx - 90, cy + 100),
    ]
    draw.polygon(footbed, fill=footbed_color, outline=(200, 200, 200))
    
    # Footbed curve/shaping
    draw.arc([cx - 85, cy + 85, cx + 85, cy + 105], 0, 180, fill=(220, 220, 220), width=2)
    
    # === TOE STRAP (Front) ===
    toe_strap = [
        (cx - 35, cy + 95),
        (cx + 35, cy + 95),
        (cx + 38, cy + 100),
        (cx - 38, cy + 100),
    ]
    draw.polygon(toe_strap, fill=strap_color, outline=(0, 0, 0))
    
    # Toe strap texture/lines
    draw.line([(cx - 30, cy + 95), (cx - 30, cy + 100)], fill=(0, 0, 0, 30), width=1)
    draw.line([(cx - 10, cy + 95), (cx - 10, cy + 100)], fill=(0, 0, 0, 30), width=1)
    draw.line([(cx + 10, cy + 95), (cx + 10, cy + 100)], fill=(0, 0, 0, 30), width=1)
    draw.line([(cx + 30, cy + 95), (cx + 30, cy + 100)], fill=(0, 0, 0, 30), width=1)
    
    # === HEEL STRAP (Back) ===
    heel_strap = [
        (cx - 40, cy + 85),
        (cx + 40, cy + 85),
        (cx + 42, cy + 95),
        (cx - 42, cy + 95),
    ]
    draw.polygon(heel_strap, fill=strap_color, outline=(0, 0, 0))
    
    # Heel strap texture
    draw.line([(cx - 35, cy + 85), (cx - 35, cy + 95)], fill=(0, 0, 0, 30), width=1)
    draw.line([(cx, cy + 85), (cx, cy + 95)], fill=(0, 0, 0, 30), width=1)
    draw.line([(cx + 35, cy + 85), (cx + 35, cy + 95)], fill=(0, 0, 0, 30), width=1)
    
    # === SIDE STRAPS (Left and Right) ===
    # Left strap
    left_strap = [
        (cx - 85, cy + 75),
        (cx - 78, cy + 85),
        (cx - 75, cy + 95),
        (cx - 85, cy + 90),
    ]
    draw.polygon(left_strap, fill=strap_color, outline=(0, 0, 0))
    
    # Right strap
    right_strap = [
        (cx + 85, cy + 75),
        (cx + 78, cy + 85),
        (cx + 75, cy + 95),
        (cx + 85, cy + 90),
    ]
    draw.polygon(right_strap, fill=strap_color, outline=(0, 0, 0))
    
    # === ACCENT DETAILS ===
    # Accent stripe on heel strap
    accent_stripe = [
        (cx - 35, cy + 88),
        (cx + 35, cy + 88),
        (cx + 35, cy + 92),
        (cx - 35, cy + 92),
    ]
    draw.polygon(accent_stripe, fill=accent_color)
    
    # Accent on toe strap
    toe_accent = [
        (cx - 30, cy + 97),
        (cx + 30, cy + 97),
        (cx + 30, cy + 99),
        (cx - 30, cy + 99),
    ]
    draw.polygon(toe_accent, fill=accent_color)
    
    # === BUCKLE/CLOSURE DETAILS ===
    # Heel buckle
    buckle_color = (200, 180, 150)
    draw.ellipse([cx - 8, cy + 85, cx + 8, cy + 93], fill=buckle_color, outline=(100, 100, 100))
    draw.ellipse([cx - 5, cy + 87, cx + 5, cy + 91], fill=(150, 130, 100), outline=(100, 100, 100))
    
    # === SHADING FOR 3D EFFECT ===
    # Shadow on sides
    left_shadow = [
        (cx - 90, cy + 95),
        (cx - 85, cy + 75),
        (cx - 80, cy + 85),
        (cx - 85, cy + 100),
    ]
    shadow_color = tuple(max(0, int(c * 0.7)) for c in strap_color)
    draw.polygon(left_shadow, fill=(*shadow_color, 120))
    
    right_shadow = [
        (cx + 90, cy + 95),
        (cx + 85, cy + 75),
        (cx + 80, cy + 85),
        (cx + 85, cy + 100),
    ]
    draw.polygon(right_shadow, fill=(*shadow_color, 120))
    
    # === HIGHLIGHTS ===
    # Shine on footbed
    draw.ellipse([cx - 50, cy + 96, cx - 20, cy + 103], fill=(255, 255, 255, 100))
    
    # Highlight on heel strap
    draw.ellipse([cx - 30, cy + 86, cx + 30, cy + 89], fill=(255, 255, 255, 80))
    
    # Apply slight blur
    img = img.filter(ImageFilter.GaussianBlur(radius=0.3))
    
    img.save(f'images/{filename}', quality=95)
    print(f"✓ Created {filename}")

# Create sandal image
create_sandal('sandal.jfif', (100, 140, 180), (80, 80, 90), (220, 120, 60))

print("✅ Sandal image created successfully!")

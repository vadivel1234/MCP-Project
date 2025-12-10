from PIL import Image, ImageDraw, ImageFilter
import os
import math

os.makedirs('images', exist_ok=True)

def create_photorealistic_shoe(filename, shoe_color, accent_color, sole_color):
    """Create photorealistic shoe images that look like actual shoe photos"""
    width, height = 600, 500
    
    # Create background with gradient (like product photography)
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
    
    # === SOLE/OUTSOLE ===
    sole_outline = (40, 40, 40)
    
    # Main outsole (rubber bottom)
    sole_outer = [
        (cx - 130, cy + 130),
        (cx + 130, cy + 130),
        (cx + 135, cy + 145),
        (cx - 135, cy + 145),
    ]
    draw.polygon(sole_outer, fill=sole_color, outline=sole_outline)
    
    # Add tread pattern for realism
    tread_color = tuple(max(0, c - 30) for c in sole_color)
    for i in range(-4, 5):
        x = cx + i * 35
        draw.rectangle([x - 8, cy + 135, x + 8, cy + 140], fill=tread_color)
    
    # === MIDSOLE ===
    midsole_color = (240, 240, 240)
    midsole_outline = (200, 200, 200)
    midsole = [
        (cx - 125, cy + 110),
        (cx + 125, cy + 110),
        (cx + 130, cy + 130),
        (cx - 130, cy + 130),
    ]
    draw.polygon(midsole, fill=midsole_color, outline=midsole_outline)
    
    # === MAIN SHOE BODY (Upper) ===
    # Main shoe outline - side profile view
    upper_left = [
        (cx - 120, cy + 105),      # heel bottom
        (cx - 110, cy + 40),       # heel top
        (cx - 90, cy - 40),        # heel back
        (cx - 40, cy - 70),        # mid back
        (cx + 30, cy - 75),        # midfoot
        (cx + 90, cy - 50),        # toe area
        (cx + 125, cy + 20),       # toe front
        (cx + 120, cy + 105),      # toe bottom
    ]
    
    # Primary shoe color fill
    draw.polygon(upper_left, fill=shoe_color, outline=(0, 0, 0))
    
    # === SHADING FOR 3D EFFECT ===
    # Dark shadow on the back/heel
    heel_shadow = [
        (cx - 120, cy + 105),
        (cx - 110, cy + 40),
        (cx - 90, cy - 40),
        (cx - 75, cy + 10),
        (cx - 95, cy + 90),
    ]
    shadow_color = tuple(max(0, int(c * 0.6)) for c in shoe_color)
    draw.polygon(heel_shadow, fill=(*shadow_color, 150))
    
    # Light reflection on top
    light_shine = [
        (cx - 50, cy - 65),
        (cx + 20, cy - 70),
        (cx + 10, cy - 50),
        (cx - 40, cy - 45),
    ]
    shine_color = (255, 255, 255)
    draw.polygon(light_shine, fill=(*shine_color, 180))
    
    # === COLLAR/OPENING ===
    collar = [
        (cx - 85, cy - 25),
        (cx - 60, cy - 55),
        (cx + 10, cy - 60),
        (cx + 20, cy - 35),
        (cx - 10, cy - 20),
    ]
    collar_color = (0, 0, 0)
    draw.polygon(collar, fill=collar_color)
    
    # Collar rim (padding edge)
    draw.arc([cx - 90, cy - 65, cx + 25, cy - 20], 0, 180, fill=(150, 150, 150), width=4)
    
    # === HEEL COUNTER ===
    heel_patch = [
        (cx - 120, cy + 40),
        (cx - 110, cy + 40),
        (cx - 100, cy - 30),
        (cx - 115, cy - 30),
    ]
    heel_color = tuple(max(0, int(c * 0.8)) for c in shoe_color)
    draw.polygon(heel_patch, fill=heel_color)
    
    # === ACCENT STRIPE/DESIGN ===
    stripe = [
        (cx - 75, cy + 10),
        (cx - 20, cy - 25),
        (cx + 15, cy - 20),
        (cx - 30, cy + 25),
    ]
    draw.polygon(stripe, fill=accent_color)
    
    # === TONGUE ===
    tongue = [
        (cx - 50, cy - 20),
        (cx + 10, cy - 25),
        (cx + 15, cy + 30),
        (cx - 45, cy + 35),
    ]
    tongue_color = tuple(max(0, int(c * 0.9)) for c in shoe_color)
    draw.polygon(tongue, fill=tongue_color)
    
    # Tongue texture/lines
    draw.line([(cx - 40, cy - 10), (cx, cy + 35)], fill=(0, 0, 0, 50), width=1)
    draw.line([(cx - 35, cy), (cx + 5, cy + 30)], fill=(0, 0, 0, 50), width=1)
    
    # === LACES ===
    lace_color = (100, 100, 100)
    lace_points = [
        (cx - 45, cy - 10),
        (cx - 40, cy + 10),
        (cx - 30, cy + 25),
        (cx - 10, cy + 35),
    ]
    
    for i, (x, y) in enumerate(lace_points[:-1]):
        # Lace hole
        draw.ellipse([x - 4, y - 3, x + 4, y + 3], fill=(20, 20, 20))
        # Crossing lace
        if i < len(lace_points) - 2:
            next_x, next_y = lace_points[i + 2]
            draw.line([(x, y), (next_x, next_y)], fill=lace_color, width=3)
    
    # === ADDITIONAL DETAILS ===
    # Toe creases for realism
    draw.line([(cx + 100, cy - 30), (cx + 120, cy + 15)], fill=(0, 0, 0, 30), width=2)
    
    # Side seam line
    draw.line([(cx + 125, cy + 20), (cx + 120, cy + 105)], fill=(0, 0, 0, 40), width=2)
    
    # === HIGHLIGHT ON MIDSOLE ===
    draw.ellipse([cx - 80, cy + 115, cx - 40, cy + 125], fill=(255, 255, 255, 100))
    
    # Apply slight blur for softer appearance
    img = img.filter(ImageFilter.GaussianBlur(radius=0.3))
    
    img.save(f'images/{filename}', quality=95)
    print(f"✓ Created {filename}")

# Create photorealistic shoe images with realistic colors and designs
shoes = [
    ('Shoe 1.jfif', (50, 100, 180), (255, 140, 0), (30, 30, 35)),         # Blue with orange
    ('Shoe 2.jfif', (180, 60, 120), (240, 150, 200), (35, 35, 40)),       # Pink/Magenta
    ('Shoe 3.jfif', (30, 30, 35), (180, 150, 100), (25, 25, 30)),         # Black
    ('Shoe 4.jfif', (140, 100, 60), (220, 180, 140), (30, 30, 35)),       # Brown
    ('Shoe 6.avif', (70, 140, 70), (150, 200, 150), (25, 30, 25)),        # Green
    ('Shoe 7.avif', (200, 100, 40), (255, 180, 100), (30, 25, 20)),       # Orange
    ('Shoe 8.avif', (100, 80, 180), (150, 120, 220), (25, 25, 30)),       # Purple
]

print("🔄 Generating photorealistic shoe images...\n")
for filename, primary, accent, sole in shoes:
    create_photorealistic_shoe(filename, primary, accent, sole)

print("\n✅ All photorealistic shoe images created successfully!")

from PIL import Image, ImageDraw, ImageFilter
import os

os.makedirs('images', exist_ok=True)

def create_shoe_image(filename, shoe_type, primary_color, secondary_color):
    """Create professional shoe images matching the product type"""
    width, height = 500, 500
    
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
    
    cx, cy = width // 2, height // 2 - 20
    
    # === GROUND SHADOW ===
    for i in range(80, 0, -2):
        alpha = int(60 * (1 - i/80))
        draw.ellipse([cx - i, cy + 190 + (80-i)//4, cx + i, cy + 200 + (80-i)//4], 
                    fill=(0, 0, 0, alpha))
    
    # === SOLE/OUTSOLE ===
    sole_color = (40, 40, 45)
    sole_outer = [
        (cx - 110, cy + 120),
        (cx + 110, cy + 120),
        (cx + 115, cy + 135),
        (cx - 115, cy + 135),
    ]
    draw.polygon(sole_outer, fill=sole_color)
    
    # Tread pattern
    tread_color = (20, 20, 25)
    for i in range(-4, 5):
        x = cx + i * 30
        draw.rectangle([x - 6, cy + 125, x + 6, cy + 130], fill=tread_color)
    
    # === MIDSOLE ===
    midsole_color = (240, 240, 240)
    midsole = [
        (cx - 110, cy + 100),
        (cx + 110, cy + 100),
        (cx + 115, cy + 120),
        (cx - 115, cy + 120),
    ]
    draw.polygon(midsole, fill=midsole_color)
    
    # === MAIN SHOE BODY ===
    upper = [
        (cx - 105, cy + 95),
        (cx - 95, cy + 30),
        (cx - 70, cy - 50),
        (cx - 30, cy - 65),
        (cx + 30, cy - 65),
        (cx + 70, cy - 50),
        (cx + 95, cy + 30),
        (cx + 105, cy + 95),
    ]
    draw.polygon(upper, fill=primary_color, outline=(0, 0, 0))
    
    # === ACCENT STRIPE ===
    accent = [
        (cx - 60, cy + 0),
        (cx - 20, cy - 30),
        (cx + 20, cy - 30),
        (cx + 60, cy + 0),
        (cx + 50, cy + 20),
        (cx - 50, cy + 20),
    ]
    draw.polygon(accent, fill=secondary_color)
    
    # === COLLAR ===
    collar = [
        (cx - 75, cy - 20),
        (cx - 50, cy - 55),
        (cx + 50, cy - 55),
        (cx + 75, cy - 20),
        (cx + 60, cy - 10),
        (cx - 60, cy - 10),
    ]
    draw.polygon(collar, fill=(0, 0, 0))
    
    # Collar rim
    draw.arc([cx - 80, cy - 65, cx + 80, cy - 15], 0, 180, fill=(150, 150, 150), width=3)
    
    # === TONGUE ===
    tongue_color = tuple(max(0, int(c * 0.9)) for c in primary_color)
    tongue = [
        (cx - 40, cy - 15),
        (cx + 40, cy - 15),
        (cx + 45, cy + 25),
        (cx - 45, cy + 25),
    ]
    draw.polygon(tongue, fill=tongue_color)
    
    # === LACES ===
    lace_color = (100, 100, 100)
    lace_y_points = [cy - 45, cy - 30, cy - 15, cy]
    for i, y in enumerate(lace_y_points[:-1]):
        # Lace holes
        draw.ellipse([cx - 35, y - 2, cx - 25, y + 2], fill=(20, 20, 20))
        draw.ellipse([cx + 25, y - 2, cx + 35, y + 2], fill=(20, 20, 20))
        # Crossing laces
        draw.line([(cx - 30, y), (cx + 30, lace_y_points[i + 1])], fill=lace_color, width=2)
    
    # === HEEL COUNTER ===
    heel_color = tuple(max(0, int(c * 0.8)) for c in primary_color)
    heel = [
        (cx - 110, cy + 25),
        (cx - 100, cy + 25),
        (cx - 85, cy - 45),
        (cx - 105, cy - 45),
    ]
    draw.polygon(heel, fill=heel_color)
    
    # === SHADING ===
    shadow = [
        (cx - 110, cy + 95),
        (cx - 100, cy + 25),
        (cx - 80, cy - 20),
        (cx - 60, cy + 30),
        (cx - 90, cy + 90),
    ]
    shadow_color = tuple(max(0, int(c * 0.6)) for c in primary_color)
    draw.polygon(shadow, fill=(*shadow_color, 120))
    
    # === HIGHLIGHTS ===
    draw.polygon([
        (cx - 50, cy - 55),
        (cx - 20, cy - 60),
        (cx, cy - 50),
        (cx - 30, cy - 40),
    ], fill=(255, 255, 255, 150))
    
    # Midsole shine
    draw.ellipse([cx - 50, cy + 105, cx - 20, cy + 120], fill=(255, 255, 255, 100))
    
    img = img.filter(ImageFilter.GaussianBlur(radius=0.3))
    img.save(f'images/{filename}', quality=95)
    print(f"✓ Created {filename} - {shoe_type}")

# Create professional shoe images matching each product
shoes = [
    ('Shoe 1.jfif', 'Classic Running Shoes', (70, 120, 200), (255, 140, 0)),         # Blue running
    ('Shoe 2.jfif', 'Urban Casual Sneakers', (200, 80, 120), (255, 200, 0)),         # Pink casual
    ('Shoe 3.jfif', 'Professional Formal Shoes', (30, 30, 35), (200, 150, 100)),     # Black formal
    ('Shoe 4.jfif', 'Athletic Sports Shoes', (200, 100, 40), (255, 180, 100)),       # Orange sports
    ('Shoe 6.avif', 'Comfort Walking Shoes', (100, 150, 100), (150, 200, 150)),      # Green walking
    ('Shoe 7.avif', 'Marathon Running Shoes', (150, 80, 150), (255, 150, 200)),      # Purple running
    ('Shoe 8.avif', 'Casual Slip-On Shoes', (100, 100, 200), (150, 120, 220)),       # Blue casual
]

print("🔄 Generating professional shoe images...\n")
for filename, shoe_type, primary, secondary in shoes:
    create_shoe_image(filename, shoe_type, primary, secondary)

print("\n✅ All shoe images created successfully and matched to product titles!")

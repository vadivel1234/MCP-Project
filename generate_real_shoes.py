from PIL import Image, ImageDraw, ImageFilter
import random
import os

os.makedirs('images', exist_ok=True)

def create_realistic_shoe_photo(filename, shoe_color, accent_color, bg_color):
    """Create photorealistic shoe images with texture and gradients."""
    width, height = 500, 500
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img, 'RGBA')
    
    cx, cy = 250, 260
    
    # ===== SHOE SILHOUETTE (realistic side view) =====
    # Create a more organic shoe shape
    shoe_points = [
        (cx - 120, cy - 80),      # toe front
        (cx - 80, cy - 100),      # toe curve up
        (cx + 60, cy - 95),       # top of shoe
        (cx + 100, cy - 70),      # side curve
        (cx + 120, cy + 20),      # upper heel
        (cx + 100, cy + 80),      # back heel
        (cx + 80, cy + 100),      # sole back
        (cx - 100, cy + 105),     # sole front
        (cx - 130, cy + 80),      # front sole curve
    ]
    
    # Draw main shoe body with gradient effect using multiple polygons
    draw.polygon(shoe_points, fill=shoe_color)
    
    # Add texture/variation to shoe surface
    for i in range(15):
        rand_x = random.randint(cx - 100, cx + 80)
        rand_y = random.randint(cy - 80, cy + 80)
        shade = random.randint(-20, 15)
        r = max(0, min(255, shoe_color[0] + shade))
        g = max(0, min(255, shoe_color[1] + shade))
        b = max(0, min(255, shoe_color[2] + shade))
        draw.ellipse([rand_x, rand_y, rand_x + 30, rand_y + 15], fill=(r, g, b, 80))
    
    # ===== SOLE (dark rubber bottom) =====
    sole_points = [
        (cx - 100, cy + 100),
        (cx + 80, cy + 95),
        (cx + 85, cy + 115),
        (cx - 105, cy + 120),
    ]
    draw.polygon(sole_points, fill=(30, 30, 30))
    
    # ===== MIDSOLE (white cushioning) =====
    midsole_points = [
        (cx - 95, cy + 95),
        (cx + 75, cy + 90),
        (cx + 80, cy + 100),
        (cx - 100, cy + 105),
    ]
    draw.polygon(midsole_points, fill=(250, 250, 250))
    
    # ===== ACCENT DETAILS (stripe or design) =====
    accent_points = [
        (cx - 90, cy + 10),
        (cx - 40, cy - 40),
        (cx + 40, cy - 45),
        (cx + 70, cy + 5),
    ]
    draw.polygon(accent_points, fill=accent_color)
    
    # ===== SHOE OPENING (collar) =====
    collar_points = [
        (cx - 90, cy - 70),
        (cx + 40, cy - 65),
        (cx + 35, cy - 40),
        (cx - 85, cy - 45),
    ]
    darker_shoe = tuple(max(0, c - 40) for c in shoe_color)
    draw.polygon(collar_points, fill=darker_shoe)
    
    # ===== REALISTIC HIGHLIGHTS (light reflection) =====
    # Top highlight
    highlight1 = [
        (cx - 80, cy - 85),
        (cx - 20, cy - 95),
        (cx - 30, cy - 70),
        (cx - 90, cy - 60),
    ]
    draw.polygon(highlight1, fill=(255, 255, 255, 120))
    
    # Side highlight (more subtle)
    highlight2 = [
        (cx + 70, cy - 50),
        (cx + 100, cy - 40),
        (cx + 95, cy + 20),
        (cx + 65, cy + 10),
    ]
    draw.polygon(highlight2, fill=(255, 255, 255, 80))
    
    # ===== SOLE TREAD (rubber pattern) =====
    for i in range(-3, 4):
        draw.line([(cx - 90 + i*30, cy + 102), (cx - 70 + i*30, cy + 110)], 
                 fill=(20, 20, 20), width=2)
    
    # ===== LACING DETAILS =====
    # Lace holes
    lace_x = [cx - 50, cx - 15, cx + 20]
    for lx in lace_x:
        draw.ellipse([lx - 3, cy - 50, lx + 3, cy - 40], fill=(100, 100, 100))
    
    # Lace strings
    for i in range(4):
        y = cy - 50 + i * 12
        draw.line([(cx - 50, y), (cx + 20, y)], fill=(180, 180, 180), width=2)
    
    # ===== SHADOW (depth) =====
    draw.ellipse([cx - 150, cy + 115, cx + 150, cy + 135], fill=(0, 0, 0, 60))
    
    # Apply slight blur for more realistic look
    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
    
    img.save(f'images/{filename}')
    print(f'✓ {filename:20} - Photorealistic shoe created')

# Realistic shoe configurations
shoes = [
    ('Shoe 1.jfif', (50, 120, 180), (220, 100, 60), (220, 230, 245)),        # Blue with orange accent
    ('Shoe 2.jfif', (100, 160, 100), (240, 180, 60), (225, 235, 220)),       # Green with gold accent
    ('Shoe 3.jfif', (70, 70, 80), (200, 200, 200), (225, 225, 225)),         # Gray minimalist
    ('Shoe 4.jfif', (50, 140, 190), (255, 200, 60), (220, 235, 250)),        # Cyan with yellow accent
    ('Shoe 6.avif', (130, 70, 130), (255, 150, 180), (235, 220, 240)),       # Purple with pink accent
    ('Shoe 7.avif', (150, 80, 110), (255, 230, 100), (240, 225, 235)),       # Wine with gold accent
    ('Shoe 8.avif', (80, 140, 210), (200, 230, 255), (225, 235, 250)),       # Light blue with sky accent
]

print("Creating photorealistic shoe product images...")
print("=" * 60)
random.seed(42)  # For consistent texture
for filename, shoe_color, accent_color, bg_color in shoes:
    create_realistic_shoe_photo(filename, shoe_color, accent_color, bg_color)
print("=" * 60)
print("✓ All photorealistic shoes created!")

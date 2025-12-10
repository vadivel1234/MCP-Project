from PIL import Image, ImageDraw
import os

os.makedirs('images', exist_ok=True)

def create_realistic_shoe(filename, bg_color, shoe_config):
    """Create realistic-looking shoe images with proper anatomy and perspective."""
    width, height = 500, 500
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img, 'RGBA')
    
    primary_color, secondary_color, accent_color, sole_color = shoe_config
    
    # Center the shoe
    cx, cy = 250, 220
    
    # ===== SOLE (Dark rubber bottom) =====
    sole_path = [
        (cx - 140, cy + 115),
        (cx + 140, cy + 110),
        (cx + 145, cy + 130),
        (cx - 145, cy + 135),
    ]
    draw.polygon(sole_path, fill=sole_color)
    
    # Sole tread pattern
    for i in range(-4, 5):
        draw.line([(cx - 130 + i*25, cy + 120), (cx - 110 + i*25, cy + 132)], 
                 fill=(50, 50, 50), width=2)
    
    # ===== MIDSOLE (White cushioning) =====
    midsole_path = [
        (cx - 135, cy + 110),
        (cx + 135, cy + 105),
        (cx + 140, cy + 125),
        (cx - 140, cy + 130),
    ]
    draw.polygon(midsole_path, fill=(250, 250, 250))
    
    # ===== HEEL COUNTER (Back structure) =====
    heel_path = [
        (cx - 135, cy + 65),
        (cx - 150, cy + 80),
        (cx - 155, cy + 110),
        (cx - 140, cy + 110),
    ]
    draw.polygon(heel_path, fill=secondary_color)
    
    # ===== MAIN SHOE UPPER (Main body) =====
    # This forms the main visible shoe
    upper_path = [
        (cx - 130, cy - 75),     # Toe front
        (cx + 145, cy - 65),     # Toe right
        (cx + 155, cy + 40),     # Side right
        (cx + 140, cy + 110),    # Heel right
        (cx - 140, cy + 115),    # Heel left
        (cx - 155, cy + 45),     # Side left
    ]
    draw.polygon(upper_path, fill=primary_color)
    
    # ===== SIDE PANEL (Darker shade for 3D effect) =====
    side_shade = tuple(max(0, c - 25) for c in primary_color[:3])
    side_path = [
        (cx - 140, cy - 55),
        (cx + 155, cy - 45),
        (cx + 160, cy + 50),
        (cx - 155, cy + 60),
    ]
    draw.polygon(side_path, fill=side_shade)
    
    # ===== TOE BOX (Front bulbous area) =====
    toe_shade = tuple(min(255, c + 20) for c in primary_color[:3])
    toe_path = [
        (cx - 120, cy - 65),
        (cx + 145, cy - 55),
        (cx + 150, cy + 5),
        (cx - 115, cy + 0),
    ]
    draw.polygon(toe_path, fill=toe_shade)
    
    # ===== TONGUE (Center padding) =====
    tongue_path = [
        (cx - 35, cy - 85),
        (cx + 45, cy - 80),
        (cx + 40, cy + 15),
        (cx - 30, cy + 10),
    ]
    draw.polygon(tongue_path, fill=accent_color)
    
    # ===== COLLAR (Top ankle opening) =====
    collar_path = [
        (cx - 125, cy - 45),
        (cx + 140, cy - 35),
        (cx + 145, cy - 10),
        (cx - 120, cy - 20),
    ]
    draw.polygon(collar_path, fill=(80, 80, 80, 200))
    
    # ===== ACCENT STRIPE (Swoosh-like design) =====
    stripe_path = [
        (cx - 110, cy + 15),
        (cx - 40, cy - 40),
        (cx + 80, cy - 55),
        (cx + 110, cy + 5),
    ]
    draw.polygon(stripe_path, fill=accent_color)
    
    # ===== LACES (Vertical lines) =====
    lace_positions = [cx - 35, cx + 10, cx + 55]
    for lx in lace_positions:
        draw.line([(lx, cy - 75), (lx, cy + 10)], fill=(210, 210, 210), width=4)
    
    # ===== LACE STRINGS (Horizontal crosses) =====
    for ly in range(cy - 70, cy + 5, 22):
        draw.line([(cx - 35, ly), (cx + 55, ly)], fill=(190, 190, 190), width=2)
    
    # ===== HIGHLIGHT/SHINE (Glossy effect on upper) =====
    shine1_path = [
        (cx - 100, cy - 55),
        (cx - 40, cy - 65),
        (cx - 50, cy - 25),
        (cx - 110, cy - 15),
    ]
    draw.polygon(shine1_path, fill=(255, 255, 255, 130))
    
    # ===== TOE SHINE (Front highlight) =====
    draw.ellipse([cx + 105, cy - 60, cx + 155, cy - 15], fill=(255, 255, 255, 100))
    
    # ===== SHADOW/DEPTH (Ground shadow) =====
    draw.ellipse([cx - 165, cy + 130, cx + 175, cy + 155], fill=(0, 0, 0, 80))
    
    img.save(f'images/{filename}')
    print(f'✓ {filename:20} - Generated')

# Shoe color configurations (primary, secondary, accent, sole)
shoes = [
    ('Shoe 1.jfif', (45, 100, 180), (20, 50, 120), (220, 80, 80), (40, 40, 40)),      # Blue sport
    ('Shoe 2.jfif', (90, 160, 110), (50, 100, 60), (255, 160, 60), (45, 45, 45)),     # Green casual
    ('Shoe 3.jfif', (70, 70, 80), (40, 40, 50), (220, 220, 240), (55, 55, 55)),       # Gray formal
    ('Shoe 4.jfif', (60, 130, 190), (35, 90, 150), (255, 200, 60), (42, 42, 42)),     # Cyan sport
    ('Shoe 6.avif', (120, 70, 130), (80, 40, 90), (255, 150, 190), (50, 50, 50)),     # Purple running
    ('Shoe 7.avif', (150, 90, 120), (100, 50, 80), (255, 230, 100), (55, 55, 55)),    # Pink casual
    ('Shoe 8.avif', (80, 140, 200), (50, 100, 160), (200, 240, 255), (45, 45, 45)),   # Light blue sport
]

print("Generating realistic shoe product images...")
print("=" * 60)
for filename, primary, secondary, accent, sole in shoes:
    create_realistic_shoe(filename, (230, 230, 235), (primary, secondary, accent, sole))
print("=" * 60)
print("✓ All shoe images generated successfully!")









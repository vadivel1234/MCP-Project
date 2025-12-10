from PIL import Image, ImageDraw
import os

os.makedirs('images', exist_ok=True)

def draw_shoe(draw, cx, cy, shoe_color, accent_color, sole_color):
    """Draw a realistic athletic shoe shape."""
    
    # ===== SOLE (Bottom rubber) =====
    sole_outline = [
        (cx - 120, cy + 100),
        (cx + 120, cy + 95),
        (cx + 125, cy + 110),
        (cx - 125, cy + 115),
    ]
    draw.polygon(sole_outline, fill=sole_color)
    
    # ===== MIDSOLE (White cushioning between sole and upper) =====
    midsole = [
        (cx - 115, cy + 95),
        (cx + 115, cy + 90),
        (cx + 120, cy + 105),
        (cx - 120, cy + 110),
    ]
    draw.polygon(midsole, fill=(245, 245, 245))
    
    # ===== BACK HEEL PART =====
    heel = [
        (cx - 110, cy + 50),
        (cx - 130, cy + 60),
        (cx - 135, cy + 95),
        (cx - 115, cy + 95),
    ]
    draw.polygon(heel, fill=shoe_color)
    
    heel_right = [
        (cx + 110, cy + 55),
        (cx + 130, cy + 65),
        (cx + 135, cy + 100),
        (cx + 115, cy + 95),
    ]
    draw.polygon(heel_right, fill=shoe_color)
    
    # ===== MAIN SHOE UPPER BODY (curved like real shoe) =====
    # This is the main curved part that makes it look like a shoe
    upper = [
        (cx - 110, cy - 50),      # Toe front
        (cx + 110, cy - 45),      # Toe front right
        (cx + 125, cy + 30),      # Side right middle
        (cx + 130, cy + 60),      # Side right back
        (cx + 115, cy + 95),      # Heel right bottom
        (cx - 115, cy + 95),      # Heel left bottom
        (cx - 130, cy + 60),      # Side left back
        (cx - 125, cy + 30),      # Side left middle
    ]
    draw.polygon(upper, fill=shoe_color)
    
    # ===== TOE BOX (Front rounded bulbous part - distinctive shoe feature) =====
    toe_bright = tuple(min(255, c + 25) for c in shoe_color[:3])
    toe_box = [
        (cx - 105, cy - 45),
        (cx + 105, cy - 40),
        (cx + 110, cy + 5),
        (cx - 110, cy),
    ]
    draw.polygon(toe_box, fill=toe_bright)
    
    # ===== TONGUE (Center padding piece) =====
    tongue = [
        (cx - 30, cy - 60),
        (cx + 30, cy - 58),
        (cx + 25, cy + 15),
        (cx - 25, cy + 13),
    ]
    draw.polygon(tongue, fill=accent_color)
    
    # ===== SIDE STRIPE/SWOOSH (Design element down the side) =====
    stripe = [
        (cx - 95, cy + 20),
        (cx - 40, cy - 35),
        (cx + 50, cy - 45),
        (cx + 95, cy + 15),
    ]
    draw.polygon(stripe, fill=accent_color)
    
    # ===== COLLAR/ANKLE OPENING =====
    collar_shade = tuple(max(0, c - 30) for c in shoe_color[:3])
    collar = [
        (cx - 100, cy - 30),
        (cx + 100, cy - 25),
        (cx + 105, cy - 5),
        (cx - 105, cy - 10),
    ]
    draw.polygon(collar, fill=collar_shade)
    
    # ===== LACES (Vertical lines for shoe laces) =====
    lace_x = [cx - 25, cx, cx + 25]
    for lx in lace_x:
        draw.line([(lx, cy - 45), (lx, cy + 10)], fill=(200, 200, 200), width=3)
    
    # ===== LACE CROSSINGS (Horizontal) =====
    for ly in range(cy - 40, cy + 10, 18):
        draw.line([(cx - 25, ly), (cx + 25, ly)], fill=(180, 180, 180), width=2)
    
    # ===== SHOE SHINE/GLOSS (Makes it look 3D and realistic) =====
    shine1 = [
        (cx - 80, cy - 40),
        (cx - 30, cy - 50),
        (cx - 40, cy - 15),
        (cx - 90, cy - 5),
    ]
    draw.polygon(shine1, fill=(255, 255, 255, 150))
    
    # Shine on toe
    draw.ellipse([cx + 70, cy - 45, cx + 120, cy - 5], fill=(255, 255, 255, 100))
    
    # ===== SHADOW (Ground shadow for depth) =====
    draw.ellipse([cx - 140, cy + 110, cx + 140, cy + 130], fill=(0, 0, 0, 70))

def create_shoe_image(filename, bg_color, shoe_color, accent_color, sole_color):
    """Create a shoe product image."""
    width, height = 500, 500
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Draw the shoe in the center
    draw_shoe(draw, width // 2, height // 2, shoe_color, accent_color, sole_color)
    
    img.save(f'images/{filename}')
    print(f'✓ {filename:20} created')

# Create realistic shoe images
shoes = [
    # filename, background, shoe_color, accent, sole
    ('Shoe 1.jfif', (200, 220, 240), (30, 80, 150), (220, 100, 100), (40, 40, 40)),      # Blue shoe
    ('Shoe 2.jfif', (210, 230, 210), (70, 130, 90), (255, 170, 80), (45, 45, 45)),       # Green shoe
    ('Shoe 3.jfif', (220, 220, 220), (50, 50, 70), (200, 200, 230), (55, 55, 55)),       # Gray shoe
    ('Shoe 4.jfif', (200, 225, 245), (40, 110, 170), (255, 210, 80), (42, 42, 42)),      # Cyan shoe
    ('Shoe 6.avif', (230, 210, 240), (100, 60, 110), (255, 160, 200), (50, 50, 50)),     # Purple shoe
    ('Shoe 7.avif', (240, 220, 230), (130, 70, 100), (255, 240, 120), (55, 55, 55)),     # Pink shoe
    ('Shoe 8.avif', (210, 230, 250), (80, 120, 180), (200, 240, 255), (45, 45, 45)),     # Light blue shoe
]

print("Creating realistic shoe product images...")
print("=" * 60)
for filename, bg, shoe, accent, sole in shoes:
    create_shoe_image(filename, bg, shoe, accent, sole)
print("=" * 60)
print("✓ All shoe images created successfully!")

from PIL import Image, ImageDraw
import os

os.makedirs('images', exist_ok=True)

def create_simple_shoe(filename, shoe_color, accent_color, bg_color):
    """Create simple, clean, realistic shoe images."""
    width, height = 500, 500
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    cx, cy = 250, 270
    
    # ===== SOLE (rubber bottom - dark) =====
    sole = [(cx-100, cy+90), (cx+95, cy+85), (cx+98, cy+105), (cx-105, cy+110)]
    draw.polygon(sole, fill=(25, 25, 25))
    
    # ===== MIDSOLE (white cushioning) =====
    midsole = [(cx-95, cy+85), (cx+90, cy+80), (cx+95, cy+100), (cx-100, cy+105)]
    draw.polygon(midsole, fill=(255, 255, 255))
    
    # ===== HEEL (back part) =====
    heel = [(cx-95, cy+50), (cx-115, cy+65), (cx-120, cy+85), (cx-95, cy+85)]
    draw.polygon(heel, fill=shoe_color)
    
    heel_right = [(cx+90, cy+55), (cx+110, cy+70), (cx+115, cy+90), (cx+90, cy+85)]
    draw.polygon(heel_right, fill=shoe_color)
    
    # ===== MAIN SHOE UPPER (curved realistic shape) =====
    upper = [
        (cx-95, cy-70),      # toe front
        (cx-60, cy-95),      # toe top curve
        (cx+40, cy-98),      # top middle
        (cx+85, cy-75),      # side top
        (cx+110, cy+20),     # side middle
        (cx+90, cy+85),      # heel
        (cx-95, cy+85),      # back
        (cx-115, cy+50),     # side back
    ]
    draw.polygon(upper, fill=shoe_color)
    
    # ===== SIDE SHADE (darker for 3D) =====
    darker = tuple(max(0, c - 30) for c in shoe_color)
    side = [
        (cx-95, cy-60),
        (cx+85, cy-65),
        (cx+105, cy+15),
        (cx+90, cy+85),
        (cx-95, cy+85),
        (cx-110, cy+40),
    ]
    draw.polygon(side, fill=darker)
    
    # ===== TOE BOX (front bulge) =====
    toe_light = tuple(min(255, c + 25) for c in shoe_color)
    toe = [
        (cx-90, cy-65),
        (cx-55, cy-85),
        (cx+40, cy-88),
        (cx+35, cy-30),
        (cx-75, cy-25),
    ]
    draw.polygon(toe, fill=toe_light)
    
    # ===== COLLAR (opening at top) =====
    collar_dark = tuple(max(0, c - 50) for c in shoe_color)
    collar = [
        (cx-75, cy-55),
        (cx+35, cy-60),
        (cx+30, cy-35),
        (cx-70, cy-30),
    ]
    draw.polygon(collar, fill=collar_dark)
    
    # ===== ACCENT STRIPE (design) =====
    accent = [
        (cx-80, cy+5),
        (cx-25, cy-45),
        (cx+50, cy-55),
        (cx+80, cy-10),
    ]
    draw.polygon(accent, fill=accent_color)
    
    # ===== TONGUE =====
    tongue = [
        (cx-35, cy-70),
        (cx+10, cy-75),
        (cx+5, cy-20),
        (cx-30, cy-15),
    ]
    draw.polygon(tongue, fill=toe_light)
    
    # ===== SIMPLE SHINE (highlight) =====
    shine = [
        (cx-70, cy-65),
        (cx-25, cy-80),
        (cx-35, cy-50),
        (cx-80, cy-40),
    ]
    draw.polygon(shine, fill=(255, 255, 255, 150))
    
    # ===== LACES =====
    for i in range(3):
        lx = cx - 35 + i * 25
        draw.line([(lx, cy-60), (lx, cy-10)], fill=(210, 210, 210), width=3)
    
    for i in range(3):
        ly = cy - 55 + i * 18
        draw.line([(cx-35, ly), (cx+40, ly)], fill=(190, 190, 190), width=2)
    
    # ===== TREAD PATTERN ON SOLE =====
    for i in range(-2, 4):
        draw.line([(cx-90+i*32, cy+92), (cx-75+i*32, cy+100)], fill=(15, 15, 15), width=2)
    
    # ===== SUBTLE SHADOW =====
    draw.ellipse([cx-130, cy+105, cx+130, cy+118], fill=(0, 0, 0, 50))
    
    img.save(f'images/{filename}')
    print(f'✓ {filename} created')

# Create shoes with realistic colors and different backgrounds
shoes = [
    ('Shoe 1.jfif', (45, 105, 175), (255, 95, 80), (240, 250, 255)),      # Blue shoe, light blue bg
    ('Shoe 2.jfif', (95, 145, 95), (255, 175, 60), (240, 255, 240)),      # Green shoe, light green bg
    ('Shoe 3.jfif', (55, 55, 65), (200, 200, 220), (245, 245, 245)),      # Gray shoe, light gray bg
    ('Shoe 4.jfif', (45, 120, 185), (255, 205, 75), (240, 248, 255)),     # Cyan shoe, alice blue bg
    ('Shoe 6.avif', (115, 55, 115), (255, 135, 175), (255, 240, 245)),    # Purple shoe, light pink bg
    ('Shoe 7.avif', (135, 75, 95), (255, 235, 95), (255, 250, 240)),      # Wine shoe, floral white bg
    ('Shoe 8.avif', (75, 130, 200), (200, 225, 255), (240, 250, 255)),    # Light blue shoe, light cyan bg
]

print("Creating realistic shoe images with colored backgrounds...")
for filename, shoe_color, accent_color, bg_color in shoes:
    create_simple_shoe(filename, shoe_color, accent_color, bg_color)
print("✓ Done! Visit http://127.0.0.1:8080")

from PIL import Image, ImageDraw, ImageFilter
import os
import math

os.makedirs('images', exist_ok=True)

def create_realistic_shoe(filename, primary_color, secondary_color, accent_color):
    """Create realistic shoe images that look like actual shoes"""
    width, height = 500, 450
    
    # Create image with light background
    img = Image.new('RGB', (width, height), (245, 245, 245))
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Center position
    cx, cy = width // 2, height // 2 - 20
    
    # === SOLE (Bottom) ===
    sole_color = (80, 80, 90)  # Dark gray/black sole
    sole_shadow = (40, 40, 50)
    
    # Draw sole bottom
    draw.ellipse([cx - 120, cy + 100, cx + 120, cy + 130], fill=sole_shadow)
    
    # Main sole shape
    sole_points = [
        (cx - 100, cy + 80),
        (cx + 100, cy + 80),
        (cx + 110, cy + 90),
        (cx + 115, cy + 100),
        (cx - 115, cy + 100),
        (cx - 110, cy + 90),
    ]
    draw.polygon(sole_points, fill=sole_color)
    
    # === MIDSOLE (Cushioning layer) ===
    midsole_color = (220, 220, 220)
    midsole_points = [
        (cx - 100, cy + 60),
        (cx + 100, cy + 60),
        (cx + 110, cy + 75),
        (cx - 110, cy + 75),
    ]
    draw.polygon(midsole_points, fill=midsole_color)
    
    # Add midsole detail/pattern
    for i in range(5):
        x = cx - 80 + i * 40
        draw.line([(x, cy + 65), (x + 15, cy + 72)], fill=(200, 200, 200), width=2)
    
    # === UPPER BODY (Main shoe part) ===
    
    # Main upper shoe body - rounded at toe, taller at heel
    upper_points = [
        (cx - 95, cy + 55),       # heel side left
        (cx - 85, cy - 30),       # heel back top
        (cx - 50, cy - 45),       # heel top
        (cx - 20, cy - 55),       # mid top
        (cx + 30, cy - 50),       # toe area top
        (cx + 95, cy + 30),       # toe tip right
        (cx + 85, cy + 55),       # toe area bottom
        (cx + 95, cy + 60),       # right side bottom
        (cx - 95, cy + 60),       # left side bottom
    ]
    
    # Draw main body with gradient effect using multiple layers
    draw.polygon(upper_points, fill=primary_color)
    
    # Add shading for 3D effect on the left side
    shadow_points = [
        (cx - 95, cy + 55),
        (cx - 85, cy - 30),
        (cx - 50, cy - 45),
        (cx - 40, cy + 0),
        (cx - 70, cy + 50),
    ]
    shadow_color = tuple(max(0, int(c * 0.7)) for c in primary_color)
    draw.polygon(shadow_points, fill=(*shadow_color, 120))
    
    # === SHOE OPENING/COLLAR ===
    collar_points = [
        (cx - 60, cy - 35),
        (cx - 40, cy - 50),
        (cx + 20, cy - 48),
        (cx + 30, cy - 35),
        (cx + 10, cy - 25),
        (cx - 30, cy - 25),
    ]
    draw.polygon(collar_points, fill=(50, 50, 60))  # Dark inside
    
    # Collar rim highlight
    draw.arc([cx - 65, cy - 60, cx + 35, cy - 30], 0, 180, fill=(180, 180, 190), width=3)
    
    # === HEEL COUNTER (Back part) ===
    heel_points = [
        (cx - 95, cy - 20),
        (cx - 85, cy - 30),
        (cx - 75, cy - 25),
        (cx - 80, cy - 10),
    ]
    heel_color = tuple(max(0, int(c * 0.85)) for c in primary_color)
    draw.polygon(heel_points, fill=heel_color)
    
    # === ACCENT STRIPE (Side design) ===
    stripe_points = [
        (cx - 70, cy - 10),
        (cx - 30, cy - 20),
        (cx + 20, cy - 15),
        (cx + 15, cy + 5),
        (cx - 35, cy + 10),
    ]
    draw.polygon(stripe_points, fill=accent_color)
    
    # === TOE BOX DETAILS ===
    # Toe creasing for realism
    draw.line([(cx + 70, cy - 20), (cx + 85, cy + 20)], fill=secondary_color, width=2)
    
    # === LACES ===
    lace_color = (100, 100, 100)
    lace_y_start = cy - 30
    lace_spacing = 12
    
    # Draw lace holes and laces
    for i in range(4):
        y = lace_y_start + i * lace_spacing
        
        # Left side lace holes
        draw.ellipse([cx - 28, y - 2, cx - 18, y + 2], fill=(30, 30, 40))
        # Right side lace holes
        draw.ellipse([cx + 18, y - 2, cx + 28, y + 2], fill=(30, 30, 40))
        
        # Lace strings crossing
        if i < 3:
            draw.line([(cx - 23, y), (cx + 23, y + lace_spacing)], fill=lace_color, width=2)
            draw.line([(cx + 23, y), (cx - 23, y + lace_spacing)], fill=lace_color, width=2)
    
    # === HIGHLIGHTS (Shine/Reflection) ===
    # Main highlight on top
    highlight_points = [
        (cx - 50, cy - 40),
        (cx - 30, cy - 50),
        (cx - 10, cy - 45),
        (cx - 20, cy - 30),
    ]
    highlight_color = tuple(min(255, int(c * 1.3)) for c in primary_color)
    draw.polygon(highlight_points, fill=(*highlight_color, 150))
    
    # Shine on midsole
    draw.ellipse([cx - 40, cy + 65, cx - 20, cy + 80], fill=(255, 255, 255, 80))
    
    # === SHADOW UNDERNEATH ===
    shadow_y = cy + 120
    for i in range(120, 0, -5):
        alpha = int(80 * (i / 120))
        draw.ellipse(
            [cx - i//2, shadow_y, cx + i//2, shadow_y + 8],
            fill=(0, 0, 0, alpha)
        )
    
    # Apply slight blur for anti-aliasing
    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
    
    img.save(f'images/{filename}')
    print(f"Created {filename}")

# Create realistic shoes with variety of colors
shoes = [
    ('Shoe 1.jfif', (70, 120, 200), (100, 150, 220), (255, 150, 0)),         # Blue with orange accent
    ('Shoe 2.jfif', (200, 80, 120), (220, 120, 160), (255, 200, 0)),         # Pink/Magenta
    ('Shoe 3.jfif', (40, 40, 40), (80, 80, 90), (200, 150, 100)),            # Black
    ('Shoe 4.jfif', (150, 80, 50), (180, 120, 80), (255, 200, 150)),         # Brown/Tan
    ('Shoe 6.avif', (100, 150, 100), (140, 180, 140), (200, 255, 200)),      # Green
    ('Shoe 7.avif', (200, 100, 80), (230, 150, 120), (255, 180, 100)),       # Orange
    ('Shoe 8.avif', (100, 100, 200), (150, 150, 230), (0, 200, 255)),        # Purple/Blue
]

for filename, primary, secondary, accent in shoes:
    create_realistic_shoe(filename, primary, secondary, accent)

print("✅ All realistic shoe images created successfully!")

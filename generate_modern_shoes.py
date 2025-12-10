from PIL import Image, ImageDraw, ImageFilter
import os

os.makedirs('images', exist_ok=True)

def create_modern_shoe(filename, shoe_color, accent_color, bg_color):
    """Create modern stylized shoe images"""
    width, height = 400, 400
    
    # Create image with solid background
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Shoe position
    shoe_x = 100
    shoe_y = 120
    
    # Draw main shoe body (side view, stylized)
    shoe_main = [
        (shoe_x + 30, shoe_y + 120),      # heel bottom
        (shoe_x + 50, shoe_y + 80),       # heel top
        (shoe_x + 80, shoe_y + 50),       # mid upper
        (shoe_x + 150, shoe_y + 40),      # toe area upper
        (shoe_x + 180, shoe_y + 60),      # toe end
        (shoe_x + 170, shoe_y + 130),     # toe sole
        (shoe_x + 100, shoe_y + 140),     # sole
    ]
    draw.polygon(shoe_main, fill=shoe_color, outline=shoe_color)
    
    # Draw accent stripe (modern swoosh-like)
    accent_stripe = [
        (shoe_x + 60, shoe_y + 85),
        (shoe_x + 100, shoe_y + 70),
        (shoe_x + 140, shoe_y + 75),
        (shoe_x + 120, shoe_y + 95),
    ]
    draw.polygon(accent_stripe, fill=accent_color, outline=accent_color)
    
    # Draw shoe sole/bottom
    sole_color = tuple(min(c - 30, 255) for c in shoe_color)
    draw.rectangle([shoe_x + 30, shoe_y + 120, shoe_x + 170, shoe_y + 145], 
                   fill=sole_color, outline=sole_color)
    
    # Draw window/mesh area (modern design detail)
    window_color = tuple(min(c + 40, 255) for c in shoe_color)
    window_rects = [
        (shoe_x + 75, shoe_y + 65, shoe_x + 95, shoe_y + 85),
        (shoe_x + 100, shoe_y + 58, shoe_x + 120, shoe_y + 78),
        (shoe_x + 125, shoe_y + 62, shoe_x + 145, shoe_y + 82),
    ]
    for rect in window_rects:
        draw.rectangle(rect, fill=window_color, outline=window_color)
    
    # Draw laces (modern minimal design)
    lace_color = (255, 255, 255, 200)
    lace_positions = [(shoe_x + 85, shoe_y + 75), (shoe_x + 105, shoe_y + 68), (shoe_x + 125, shoe_y + 72)]
    for x, y in lace_positions:
        draw.ellipse([x - 5, y - 3, x + 5, y + 3], fill=lace_color)
    
    # Add highlight/shine effect
    highlight = [
        (shoe_x + 110, shoe_y + 50),
        (shoe_x + 130, shoe_y + 45),
        (shoe_x + 140, shoe_y + 65),
        (shoe_x + 120, shoe_y + 70),
    ]
    draw.polygon(highlight, fill=(255, 255, 255, 100))
    
    # Add shadow at bottom
    shadow_color = (0, 0, 0, 60)
    shadow_points = [
        (shoe_x + 40, shoe_y + 145),
        (shoe_x + 160, shoe_y + 145),
        (shoe_x + 155, shoe_y + 160),
        (shoe_x + 45, shoe_y + 160),
    ]
    draw.polygon(shadow_points, fill=shadow_color)
    
    img.save(f'images/{filename}')
    print(f"Created {filename}")

# Create modern shoe images with different colors
shoes = [
    ('Shoe 1.jfif', (138, 115, 200), (220, 180, 255), (245, 240, 250)),     # Purple
    ('Shoe 2.jfif', (200, 100, 150), (255, 180, 220), (250, 240, 245)),     # Pink
    ('Shoe 3.jfif', (100, 150, 220), (180, 210, 255), (240, 248, 255)),     # Blue
    ('Shoe 4.jfif', (220, 140, 80), (255, 200, 140), (255, 245, 235)),      # Orange
    ('Shoe 6.avif', (140, 200, 100), (200, 240, 150), (245, 252, 240)),     # Green
    ('Shoe 7.avif', (180, 100, 140), (230, 160, 190), (250, 240, 245)),     # Mauve
    ('Shoe 8.avif', (100, 180, 200), (170, 220, 240), (240, 250, 255)),     # Cyan
]

for filename, primary_color, accent_color, bg_color in shoes:
    create_modern_shoe(filename, primary_color, accent_color, bg_color)

print("✅ All modern shoe images created successfully!")

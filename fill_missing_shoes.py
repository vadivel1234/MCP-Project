from PIL import Image, ImageDraw, ImageFilter
import os

os.makedirs('images', exist_ok=True)

def create_professional_shoe(filename, shoe_name, primary_color, secondary_color):
    """Create a professional-looking shoe image"""
    width, height = 500, 500
    
    img = Image.new('RGB', (width, height), (250, 250, 250))
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Gradient background
    for y in range(height):
        ratio = y / height
        r = int(250 - (ratio * 15))
        g = int(250 - (ratio * 15))
        b = int(250 - (ratio * 10))
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    cx, cy = width // 2, height // 2 - 30
    
    # Shadow
    for i in range(100, 0, -3):
        alpha = int(50 * (1 - i/100))
        draw.ellipse([cx - i, cy + 200 + (100-i)//3, cx + i, cy + 215 + (100-i)//3], 
                    fill=(0, 0, 0, alpha))
    
    # Sole
    draw.polygon([
        (cx - 120, cy + 130),
        (cx + 120, cy + 130),
        (cx + 125, cy + 150),
        (cx - 125, cy + 150),
    ], fill=(35, 35, 40))
    
    # Tread
    for i in range(-5, 6):
        x = cx + i * 35
        draw.rectangle([x - 8, cy + 135, x + 8, cy + 142], fill=(15, 15, 20))
    
    # Midsole
    draw.polygon([
        (cx - 120, cy + 105),
        (cx + 120, cy + 105),
        (cx + 125, cy + 130),
        (cx - 125, cy + 130),
    ], fill=(240, 240, 245))
    
    # Main shoe upper
    upper_points = [
        (cx - 118, cy + 100),
        (cx - 105, cy + 20),
        (cx - 75, cy - 60),
        (cx - 30, cy - 75),
        (cx + 30, cy - 75),
        (cx + 75, cy - 60),
        (cx + 105, cy + 20),
        (cx + 118, cy + 100),
    ]
    draw.polygon(upper_points, fill=primary_color, outline=(0, 0, 0))
    
    # Accent stripe
    draw.polygon([
        (cx - 70, cy - 10),
        (cx - 20, cy - 40),
        (cx + 20, cy - 40),
        (cx + 70, cy - 10),
        (cx + 60, cy + 10),
        (cx - 60, cy + 10),
    ], fill=secondary_color)
    
    # Collar
    collar_points = [
        (cx - 80, cy - 15),
        (cx - 55, cy - 65),
        (cx + 55, cy - 65),
        (cx + 80, cy - 15),
        (cx + 65, cy - 5),
        (cx - 65, cy - 5),
    ]
    draw.polygon(collar_points, fill=(0, 0, 0))
    draw.arc([cx - 85, cy - 75, cx + 85, cy - 10], 0, 180, fill=(150, 150, 150), width=3)
    
    # Tongue
    tongue_color = tuple(max(0, int(c * 0.9)) for c in primary_color)
    draw.polygon([
        (cx - 45, cy - 10),
        (cx + 45, cy - 10),
        (cx + 50, cy + 30),
        (cx - 50, cy + 30),
    ], fill=tongue_color)
    
    # Laces
    for y_pos in [cy - 50, cy - 30, cy - 10, cy + 10]:
        draw.ellipse([cx - 38, y_pos - 2, cx - 28, y_pos + 2], fill=(20, 20, 20))
        draw.ellipse([cx + 28, y_pos - 2, cx + 38, y_pos + 2], fill=(20, 20, 20))
        if y_pos < cy + 5:
            next_y = y_pos + 20
            draw.line([(cx - 33, y_pos), (cx + 33, next_y)], fill=(100, 100, 100), width=2)
    
    # Heel
    heel_color = tuple(max(0, int(c * 0.8)) for c in primary_color)
    draw.polygon([
        (cx - 120, cy + 25),
        (cx - 108, cy + 25),
        (cx - 85, cy - 55),
        (cx - 110, cy - 55),
    ], fill=heel_color)
    
    # Shading
    shadow_color = tuple(max(0, int(c * 0.6)) for c in primary_color)
    draw.polygon([
        (cx - 120, cy + 100),
        (cx - 108, cy + 25),
        (cx - 80, cy - 15),
        (cx - 65, cy + 30),
        (cx - 95, cy + 95),
    ], fill=(*shadow_color, 130))
    
    # Highlights
    draw.polygon([
        (cx - 60, cy - 65),
        (cx - 20, cy - 72),
        (cx, cy - 60),
        (cx - 35, cy - 45),
    ], fill=(255, 255, 255, 160))
    
    draw.ellipse([cx - 60, cy + 110, cx - 25, cy + 130], fill=(255, 255, 255, 110))
    
    img = img.filter(ImageFilter.GaussianBlur(radius=0.3))
    img.save(f'images/{filename}', quality=95)
    print(f"✓ Created {filename}")

# Create professional images for missing shoes
create_professional_shoe('Shoe 1.jfif', 'Blue Running', (60, 110, 190), (255, 150, 0))
create_professional_shoe('Shoe 6.avif', 'Green Walking', (90, 140, 90), (160, 200, 140))

print("\n✅ Created professional shoe images for missing files!")

from PIL import Image, ImageDraw, ImageFilter
import os

os.makedirs('images', exist_ok=True)

def create_category_image(filename, category_name, primary_color, accent_color):
    """Create colorful category showcase images with shoe representations"""
    width, height = 800, 600
    
    # Create image with gradient background
    img = Image.new('RGB', (width, height), primary_color)
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Create gradient background
    for y in range(height):
        r = int(primary_color[0] + (accent_color[0] - primary_color[0]) * (y / height))
        g = int(primary_color[1] + (accent_color[1] - primary_color[1]) * (y / height))
        b = int(primary_color[2] + (accent_color[2] - primary_color[2]) * (y / height))
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Draw decorative circles and shapes
    draw.ellipse([50, 50, 200, 200], fill=(255, 255, 255, 100), outline=(255, 255, 255, 150), width=3)
    draw.ellipse([600, 400, 750, 550], fill=(255, 255, 255, 80), outline=(255, 255, 255, 120), width=2)
    
    # Draw abstract shoe shape
    shoe_y = 250
    shoe_x = 300
    
    # Shoe sole
    draw.rectangle([shoe_x, shoe_y + 150, shoe_x + 200, shoe_y + 180], fill=(255, 255, 255, 255))
    
    # Shoe upper part
    points_upper = [
        (shoe_x + 10, shoe_y + 150),
        (shoe_x + 30, shoe_y + 80),
        (shoe_x + 80, shoe_y + 40),
        (shoe_x + 150, shoe_y + 50),
        (shoe_x + 190, shoe_y + 120),
        (shoe_x + 200, shoe_y + 150)
    ]
    draw.polygon(points_upper, fill=(255, 255, 255, 255), outline=(255, 255, 255, 200))
    
    # Laces detail
    for i in range(4):
        y_offset = shoe_y + 80 + i * 20
        draw.line([shoe_x + 60, y_offset, shoe_x + 140, y_offset], fill=(200, 200, 200), width=3)
    
    # Category text
    try:
        # Try to use a bold font if available
        from PIL import ImageFont
        font_size = 72
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    # Draw category name with white text and shadow
    text = category_name.upper()
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (width - text_width) // 2
    text_y = 450
    
    # Shadow effect
    draw.text((text_x + 3, text_y + 3), text, font=font, fill=(0, 0, 0, 100))
    # Main text
    draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255, 255))
    
    img.save(f'images/{filename}')
    print(f"Created {filename}")

# Create category images with vibrant colors
categories = [
    ('category_casual.jpg', 'Casual', (255, 165, 0), (255, 105, 180)),      # Orange to Pink
    ('category_running.jpg', 'Running', (65, 105, 225), (0, 191, 255)),     # Blue to Cyan
    ('category_formal.jpg', 'Formal', (128, 0, 128), (220, 20, 60)),        # Purple to Crimson
    ('category_sports.jpg', 'Sports', (220, 20, 60), (255, 69, 0)),         # Red to Orange-Red
]

for filename, name, primary, accent in categories:
    create_category_image(filename, name, primary, accent)

print("✅ All category images created successfully!")

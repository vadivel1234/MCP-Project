from PIL import Image, ImageDraw, ImageFont
import os

os.makedirs('images', exist_ok=True)

def create_placeholder_shoe(filename, color_name, hex_color):
    """Create a professional product placeholder for missing shoes"""
    width, height = 500, 500
    
    # Create gradient background (professional)
    img = Image.new('RGB', (width, height), (245, 245, 245))
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Gradient background
    for y in range(height):
        ratio = y / height
        r = int(245 - (ratio * 20))
        g = int(245 - (ratio * 20))
        b = int(245 - (ratio * 15))
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Large centered circle representing shoe
    cx, cy = width // 2, height // 2
    circle_radius = 120
    
    # Convert hex color to RGB
    hex_color = hex_color.lstrip('#')
    rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    # Draw main shoe circle
    draw.ellipse([cx - circle_radius, cy - circle_radius, 
                  cx + circle_radius, cy + circle_radius], 
                 fill=rgb_color, outline=(0, 0, 0, 50))
    
    # Add shine/highlight
    highlight_radius = circle_radius // 3
    draw.ellipse([cx - highlight_radius - 40, cy - highlight_radius - 40,
                  cx + highlight_radius - 60, cy + highlight_radius - 60],
                 fill=(255, 255, 255, 150))
    
    # Add text
    text = f"{color_name} Shoe"
    try:
        font = ImageFont.truetype("arial.ttf", 28)
    except:
        font = ImageFont.load_default()
    
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (width - text_width) // 2
    
    draw.text((text_x, height - 80), text, fill=(100, 100, 100), font=font)
    
    img.save(f'images/{filename}', quality=95)
    print(f"✓ Created {filename}")

# Create placeholder shoes for missing images
shoes = [
    ('Shoe 4.jfif', 'Brown Casual', '#8B6F47'),
    ('Shoe 6.avif', 'Green Athletic', '#4A7C59'),
]

print("🔄 Creating professional shoe placeholders...\n")
for filename, name, color in shoes:
    create_placeholder_shoe(filename, name, color)

print("\n✅ Placeholder shoes created successfully!")

import urllib.request
import os
from PIL import Image, ImageDraw
from io import BytesIO

os.makedirs('images', exist_ok=True)

# Try alternative approach - use a different free image source
shoe_urls = [
    # From different sources that allow direct linking
    ("Shoe 1.jfif", "https://cdn.shopify.com/s/files/1/0579/2957/products/3_54bd24a0-6046-41fe-bafc-af4a1db38f1a.jpg?v=1568046063"),
    ("Shoe 2.jfif", "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500"),
    ("Shoe 3.jfif", "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=500"),
    ("Shoe 4.jfif", "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=500"),
    ("Shoe 6.avif", "https://images.unsplash.com/photo-1511556532299-8d2976dc026c?w=500"),
    ("Shoe 7.avif", "https://images.unsplash.com/photo-1491553895911-0055eca6402d?w=500"),
    ("Shoe 8.avif", "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=500"),
]

print("🔄 Attempting to download REAL shoe photos...\n")

success_count = 0
for filename, url in shoe_urls:
    try:
        print(f"⬇️  {filename}...", end=" ", flush=True)
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0'}
        )
        response = urllib.request.urlopen(req, timeout=10)
        img_data = response.read()
        
        # Open and process image
        img = Image.open(BytesIO(img_data))
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize to standard size
        img.thumbnail((500, 500), Image.Resampling.LANCZOS)
        
        # Create white background
        final_img = Image.new('RGB', (500, 500), (255, 255, 255))
        offset = ((500 - img.width) // 2, (500 - img.height) // 2)
        final_img.paste(img, offset)
        
        # Save
        final_img.save(f'images/{filename}', quality=95)
        print("✓")
        success_count += 1
    except Exception as e:
        print(f"✗")

print(f"\n✅ Downloaded {success_count}/7 REAL shoe photos!")
if success_count > 0:
    print("📸 Your website now has REAL shoe photographs!")

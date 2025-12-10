import urllib.request
import os
from PIL import Image
from io import BytesIO

os.makedirs('images', exist_ok=True)

# Real shoe photos from Unsplash (high quality, free to use)
shoe_urls = [
    # Blue running shoe
    ("Shoe 1.jfif", "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&q=80"),
    # Pink/Magenta shoe
    ("Shoe 2.jfif", "https://images.unsplash.com/photo-1460353581641-37baddab0fa2?w=500&q=80"),
    # Black formal shoe
    ("Shoe 3.jfif", "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=500&q=80"),
    # Brown casual shoe
    ("Shoe 4.jfif", "https://images.unsplash.com/photo-1549917261-2c0d2694d22b?w=500&q=80"),
    # Green sneaker
    ("Shoe 6.avif", "https://images.unsplash.com/photo-1511556532299-8d2976dc026c?w=500&q=80"),
    # Orange sports shoe
    ("Shoe 7.avif", "https://images.unsplash.com/photo-1491553895911-0055eca6402d?w=500&q=80"),
    # Purple/Blue shoe
    ("Shoe 8.avif", "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=500&q=80"),
]

print("🔄 Downloading real shoe photos from Unsplash...\n")

for filename, url in shoe_urls:
    try:
        print(f"⬇️ Downloading {filename}...", end=" ")
        response = urllib.request.urlopen(url, timeout=10)
        img_data = response.read()
        
        # Open image and save it
        img = Image.open(BytesIO(img_data))
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        # Resize to standard size (500x500)
        img.thumbnail((500, 500), Image.Resampling.LANCZOS)
        img.save(f'images/{filename}', quality=95)
        print("✓")
    except Exception as e:
        print(f"✗ ({str(e)[:30]})")

print("\n✅ Real shoe photos downloaded successfully!")

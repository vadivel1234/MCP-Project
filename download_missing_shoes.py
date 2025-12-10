import urllib.request
import os
from PIL import Image
from io import BytesIO

os.makedirs('images', exist_ok=True)

# Real shoe photos - alternative URLs for the failed ones
shoe_urls = [
    # Brown casual shoe
    ("Shoe 4.jfif", "https://images.unsplash.com/photo-1595777707802-221551139c35?w=500&q=80"),
    # Green sneaker
    ("Shoe 6.avif", "https://images.unsplash.com/photo-1516478179778-3c3e461e8e74?w=500&q=80"),
]

print("🔄 Downloading missing real shoe photos from Unsplash...\n")

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
        # Resize to standard size
        img.thumbnail((500, 500), Image.Resampling.LANCZOS)
        img.save(f'images/{filename}', quality=95)
        print("✓")
    except Exception as e:
        print(f"✗ ({str(e)[:30]})")

print("\n✅ Missing shoe photos downloaded successfully!")

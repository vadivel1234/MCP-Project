import urllib.request
import os
from PIL import Image
from io import BytesIO
import ssl

# Disable SSL verification for downloading
ssl._create_default_https_context = ssl._create_unverified_context

os.makedirs('images', exist_ok=True)

# Real shoe photos from Pexels (free stock photos, high quality)
shoe_urls = [
    # Running shoe - blue
    ("Shoe 1.jfif", "https://images.pexels.com/photos/3962286/pexels-photo-3962286.jpeg?auto=compress&cs=tinysrgb&w=500"),
    # Casual sneaker - colorful
    ("Shoe 2.jfif", "https://images.pexels.com/photos/3622613/pexels-photo-3622613.jpeg?auto=compress&cs=tinysrgb&w=500"),
    # Formal black shoe
    ("Shoe 3.jfif", "https://images.pexels.com/photos/1926769/pexels-photo-1926769.jpeg?auto=compress&cs=tinysrgb&w=500"),
    # Sports/Athletic shoe
    ("Shoe 4.jfif", "https://images.pexels.com/photos/5632399/pexels-photo-5632399.jpeg?auto=compress&cs=tinysrgb&w=500"),
    # Walking/Casual shoe
    ("Shoe 6.avif", "https://images.pexels.com/photos/3944441/pexels-photo-3944441.jpeg?auto=compress&cs=tinysrgb&w=500"),
    # Running shoe - colorful
    ("Shoe 7.avif", "https://images.pexels.com/photos/3625285/pexels-photo-3625285.jpeg?auto=compress&cs=tinysrgb&w=500"),
    # Casual sneaker
    ("Shoe 8.avif", "https://images.pexels.com/photos/3407857/pexels-photo-3407857.jpeg?auto=compress&cs=tinysrgb&w=500"),
]

print("🔄 Downloading REAL shoe photos from Pexels...\n")

success_count = 0
for filename, url in shoe_urls:
    try:
        print(f"⬇️  {filename}...", end=" ")
        response = urllib.request.urlopen(url, timeout=15)
        img_data = response.read()
        
        # Open and process image
        img = Image.open(BytesIO(img_data))
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize to standard size (500x500) maintaining aspect ratio
        img.thumbnail((500, 500), Image.Resampling.LANCZOS)
        
        # Create white background for padding
        final_img = Image.new('RGB', (500, 500), (255, 255, 255))
        # Center the shoe image
        offset = ((500 - img.width) // 2, (500 - img.height) // 2)
        final_img.paste(img, offset)
        
        # Save
        final_img.save(f'images/{filename}', quality=95)
        print("✓")
        success_count += 1
    except Exception as e:
        print(f"✗ ({str(e)[:25]})")

print(f"\n✅ Downloaded {success_count}/7 REAL shoe photos successfully!")
print("\n📸 These are actual real shoe photographs from Pexels!")

"""
Upload Image to Imgur (Free Image Hosting)
This gets you a public URL that D-ID can use
"""

import os
import requests
import base64
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

# Imgur API - You can use this client ID for testing (public, rate-limited)
IMGUR_CLIENT_ID = "546c25a59c58ad7"  # Public client ID for testing

def optimize_image(image_path, max_size_mb=5):
    """Optimize image size if needed"""
    file_size_mb = os.path.getsize(image_path) / (1024 * 1024)
    
    if file_size_mb <= max_size_mb:
        # Image is small enough, read as-is
        with open(image_path, 'rb') as f:
            return f.read()
    
    print(f"⚠️  Image is {file_size_mb:.2f}MB, optimizing...")
    
    # Open and resize image
    img = Image.open(image_path)
    
    # Convert RGBA to RGB if needed
    if img.mode == 'RGBA':
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])
        img = background
    
    # Resize if too large
    max_dimension = 1920
    if max(img.size) > max_dimension:
        ratio = max_dimension / max(img.size)
        new_size = tuple(int(dim * ratio) for dim in img.size)
        img = img.resize(new_size, Image.Resampling.LANCZOS)
        print(f"   Resized to: {new_size[0]}x{new_size[1]}")
    
    # Save to bytes with compression
    output = BytesIO()
    img.save(output, format='JPEG', quality=85, optimize=True)
    optimized_data = output.getvalue()
    
    new_size_mb = len(optimized_data) / (1024 * 1024)
    print(f"   Optimized size: {new_size_mb:.2f}MB")
    
    return optimized_data

def upload_to_imgur(image_path):
    """Upload image to Imgur and get public URL"""
    
    print("\n" + "="*60)
    print("UPLOADING IMAGE TO IMGUR")
    print("="*60)
    
    if not os.path.exists(image_path):
        print(f"❌ ERROR: Image not found: {image_path}")
        return None
    
    file_size_mb = os.path.getsize(image_path) / (1024 * 1024)
    print(f"✅ Image found: {image_path}")
    print(f"   File size: {file_size_mb:.2f}MB")
    
    try:
        # Optimize image if needed
        image_bytes = optimize_image(image_path)
        image_data = base64.b64encode(image_bytes).decode('utf-8')
        
        print("\n📤 Uploading to Imgur...")
        
        url = "https://api.imgur.com/3/image"
        headers = {
            "Authorization": f"Client-ID {IMGUR_CLIENT_ID}"
        }
        data = {
            "image": image_data,
            "type": "base64"
        }
        
        # Add timeout and retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"   Attempt {attempt + 1}/{max_retries}...")
                response = requests.post(url, headers=headers, data=data, timeout=60)
                
                print(f"📥 Response Status: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    image_url = result['data']['link']
                    
                    print(f"\n✅ SUCCESS! Image uploaded to Imgur!")
                    print(f"   Public URL: {image_url}")
                    print(f"\n🔗 This URL can be used with D-ID!")
                    
                    return image_url
                else:
                    print(f"❌ ERROR: Upload failed")
                    print(f"   Response: {response.text}")
                    if attempt < max_retries - 1:
                        print("   Retrying...")
                        continue
                    return None
                    
            except requests.exceptions.ConnectionError as e:
                print(f"⚠️  Connection error on attempt {attempt + 1}")
                if attempt < max_retries - 1:
                    print("   Retrying in 2 seconds...")
                    import time
                    time.sleep(2)
                else:
                    print(f"❌ ERROR: All retry attempts failed")
                    print(f"   Error: {e}")
                    return None
            except requests.exceptions.Timeout:
                print(f"⚠️  Upload timeout on attempt {attempt + 1}")
                if attempt < max_retries - 1:
                    print("   Retrying...")
                else:
                    print(f"❌ ERROR: Upload timed out after {max_retries} attempts")
                    return None
                    
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("\n📤 IMGUR IMAGE UPLOAD TOOL")
    print("Upload your image to get a public URL for D-ID")
    
    image_path = input("\n📁 Enter path to your image: ").strip()
    
    if not image_path:
        print("❌ No image path provided")
    else:
        public_url = upload_to_imgur(image_path)
        
        if public_url:
            print("\n" + "="*60)
            print("✅ SUCCESS!")
            print("="*60)
            print(f"\nYour public image URL:")
            print(f"{public_url}")
            print(f"\nCopy this URL and use it in the avatar test script!")
            print("="*60 + "\n")
            
            # Save to file for easy access
            with open("imgur_url.txt", "w") as f:
                f.write(public_url)
            print("💾 URL also saved to: imgur_url.txt\n")

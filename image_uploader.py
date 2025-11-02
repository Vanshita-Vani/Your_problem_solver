"""
Automatic Image Uploader Module
Uploads images to ImgBB and returns public URLs for D-ID
"""

import os
import requests
import base64
from PIL import Image
from io import BytesIO

# ImgBB API - Free tier, no account needed
IMGBB_API_KEY = "d134209c49f56da2b0a8cb0d64e62bb6"  # Public key for testing

def optimize_image(image_path, max_size_mb=5):
    """Optimize image size for faster upload"""
    try:
        file_size_mb = os.path.getsize(image_path) / (1024 * 1024)
        
        if file_size_mb <= max_size_mb:
            # Image is small enough
            with open(image_path, 'rb') as f:
                return f.read()
        
        print(f"   Optimizing image ({file_size_mb:.2f}MB)...")
        
        # Open and optimize
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
        
        # Save to bytes with compression
        output = BytesIO()
        img.save(output, format='JPEG', quality=85, optimize=True)
        return output.getvalue()
        
    except Exception as e:
        print(f"   Warning: Could not optimize image: {e}")
        # Return original if optimization fails
        with open(image_path, 'rb') as f:
            return f.read()

def upload_image_to_imgbb(image_path):
    """
    Upload image to ImgBB and return public URL
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Public URL string if successful, None if failed
    """
    
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        return None
    
    try:
        print(f"📤 Uploading image to ImgBB...")
        
        # Optimize and encode image
        image_bytes = optimize_image(image_path)
        image_data = base64.b64encode(image_bytes).decode('utf-8')
        
        # Upload to ImgBB
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": IMGBB_API_KEY,
            "image": image_data,
        }
        
        # Try upload with retries
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.post(url, data=payload, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get('success'):
                        image_url = result['data']['url']
                        print(f"✅ Image uploaded successfully!")
                        print(f"   URL: {image_url}")
                        return image_url
                    else:
                        error_msg = result.get('error', {}).get('message', 'Unknown error')
                        print(f"❌ Upload failed: {error_msg}")
                        return None
                else:
                    print(f"❌ Upload failed (HTTP {response.status_code})")
                    if attempt < max_retries - 1:
                        print(f"   Retrying... ({attempt + 2}/{max_retries})")
                        continue
                    return None
                    
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    print(f"   Connection error, retrying... ({attempt + 2}/{max_retries})")
                    import time
                    time.sleep(1)
                else:
                    print(f"❌ Upload failed after {max_retries} attempts: {e}")
                    return None
                    
    except Exception as e:
        print(f"❌ Error uploading image: {e}")
        return None

def get_public_image_url(image_path):
    """
    Main function to get a public URL for an image
    Tries to upload to ImgBB, returns None if fails
    
    Args:
        image_path: Path to local image file
        
    Returns:
        Public URL string or None
    """
    return upload_image_to_imgbb(image_path)

# Test function
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        image_path = input("Enter image path: ").strip()
    
    print("\n" + "="*60)
    print("IMAGE UPLOADER TEST")
    print("="*60)
    
    url = get_public_image_url(image_path)
    
    if url:
        print("\n" + "="*60)
        print("✅ SUCCESS!")
        print("="*60)
        print(f"\nPublic URL: {url}")
        print("\nThis URL can be used with D-ID!")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("❌ FAILED!")
        print("="*60)

"""
Simple Avatar Creation Test Script
Upload an image and test if D-ID creates a talking avatar successfully
"""

import os
import requests
import base64
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DID_API_KEY = os.getenv('DID_API_KEY')

def test_avatar_creation(image_file_path):
    """Test avatar creation with D-ID"""
    
    print("\n" + "="*60)
    print("AVATAR CREATION TEST")
    print("="*60)
    
    # Check API key
    if not DID_API_KEY:
        print("❌ ERROR: DID_API_KEY not found in .env file")
        return False
    
    print(f"✅ API Key found: {DID_API_KEY[:10]}...")
    
    # Check if image file exists
    if not os.path.exists(image_file_path):
        print(f"❌ ERROR: Image file not found: {image_file_path}")
        return False
    
    print(f"✅ Image file found: {image_file_path}")
    print(f"   File size: {os.path.getsize(image_file_path)} bytes")
    
    # Step 1: Read and encode image
    print("\n📤 Step 1: Reading and encoding image...")
    
    try:
        with open(image_file_path, 'rb') as img_file:
            image_data = base64.b64encode(img_file.read()).decode('utf-8')
            
        # Get file extension
        ext = image_file_path.split('.')[-1].lower()
        if ext == 'jpg':
            ext = 'jpeg'
        
        # IMPORTANT: D-ID doesn't accept base64 images directly
        # We need to use a publicly accessible URL
        print("⚠️  WARNING: D-ID requires publicly accessible image URLs")
        print("   Base64 images are NOT supported by D-ID API")
        print("\n💡 SOLUTION: You need to:")
        print("   1. Upload your image to a cloud service (S3, Cloudinary, Imgur, etc.)")
        print("   2. Get a public URL (must end with .jpg, .jpeg, or .png)")
        print("   3. Use that URL instead")
        
        # For testing, we'll use D-ID's default avatar
        print("\n🔄 Using D-ID's default avatar for testing...")
        image_url = "https://d-id-public-bucket.s3.amazonaws.com/alice.jpg"
        
    except Exception as e:
        print(f"❌ ERROR reading image: {e}")
        return False
    
    # Step 2: Create talking avatar
    print("\n📤 Step 2: Creating talking avatar with D-ID...")
    
    url = "https://api.d-id.com/talks"
    headers = {
        "Authorization": f"Basic {DID_API_KEY}",
        "Content-Type": "application/json",
        "accept": "application/json"
    }
    
    test_text = "Hello! This is a test of the D-ID avatar creation. I am speaking with a synthesized voice."
    
    payload = {
        "source_url": image_url,
        "script": {
            "type": "text",
            "input": test_text,
            "provider": {
                "type": "microsoft",
                "voice_id": "en-US-JennyNeural"
            }
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"📥 Response Status: {response.status_code}")
        
        if response.status_code in [200, 201]:
            talk_data = response.json()
            talk_id = talk_data.get('id')
            print(f"✅ SUCCESS! Avatar creation started!")
            print(f"   Talk ID: {talk_id}")
            
            # Step 3: Poll for completion
            print("\n⏳ Step 3: Waiting for avatar video to be ready...")
            
            poll_url = f"https://api.d-id.com/talks/{talk_id}"
            max_attempts = 30
            
            for attempt in range(max_attempts):
                time.sleep(2)
                poll_response = requests.get(poll_url, headers=headers)
                
                if poll_response.status_code == 200:
                    poll_data = poll_response.json()
                    status = poll_data.get('status')
                    
                    print(f"   Attempt {attempt + 1}/{max_attempts}: Status = {status}")
                    
                    if status == 'done':
                        video_url = poll_data.get('result_url')
                        print(f"\n✅ SUCCESS! Avatar video is ready!")
                        print(f"   Video URL: {video_url}")
                        print(f"\n🎬 Open this URL in your browser to see the avatar:")
                        print(f"   {video_url}")
                        
                        # Download the video
                        print("\n📥 Downloading video...")
                        video_response = requests.get(video_url)
                        output_file = "test_avatar_output.mp4"
                        
                        with open(output_file, 'wb') as f:
                            f.write(video_response.content)
                        
                        print(f"✅ Video saved to: {output_file}")
                        print(f"   File size: {len(video_response.content)} bytes")
                        
                        return True
                        
                    elif status == 'error':
                        error_msg = poll_data.get('error', {})
                        print(f"\n❌ ERROR: Avatar creation failed")
                        print(f"   Error: {error_msg}")
                        return False
                else:
                    print(f"❌ ERROR polling status: {poll_response.status_code}")
                    print(f"   Response: {poll_response.text}")
                    return False
            
            print("\n⏱️ TIMEOUT: Avatar creation took too long")
            return False
            
        else:
            print(f"❌ ERROR: Avatar creation failed")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text}")
            
            try:
                error_data = response.json()
                print(f"   Error details: {error_data}")
            except:
                pass
            
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n🎬 AVATAR CREATION TEST SCRIPT")
    print("This script tests if D-ID avatar creation works")
    print("\n⚠️  IMPORTANT: D-ID requires publicly accessible image URLs")
    print("   For this test, we'll use D-ID's default avatar")
    print("   To use YOUR image, upload it to a cloud service first")
    
    # Ask for image file path
    image_file = input("\n📁 Enter path to your image file (or press Enter to use default): ").strip()
    
    if not image_file:
        # Check if there's any image file in uploads folder
        if os.path.exists('uploads'):
            image_files = [f for f in os.listdir('uploads') if f.endswith(('.jpg', '.jpeg', '.png', '.gif'))]
            if image_files:
                image_file = os.path.join('uploads', image_files[0])
                print(f"Found: {image_file}")
                print("⚠️  Note: This will still use default avatar due to D-ID limitations")
            else:
                print("No image files found - will use default avatar")
                image_file = "default"
        else:
            print("Will use default avatar")
            image_file = "default"
    
    # Run the test
    success = test_avatar_creation(image_file)
    
    print("\n" + "="*60)
    if success:
        print("✅ AVATAR CREATION TEST PASSED!")
        print("D-ID can create talking avatars successfully.")
        print("\n📝 NOTE: To use YOUR custom image:")
        print("   1. Upload image to Imgur, Cloudinary, or S3")
        print("   2. Get the public URL")
        print("   3. Modify the script to use that URL")
    else:
        print("❌ AVATAR CREATION TEST FAILED!")
        print("Check the errors above.")
    print("="*60 + "\n")

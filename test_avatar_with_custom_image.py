"""
Test Avatar Creation with YOUR Custom Image
Uses a public image URL (from Imgur or other service)
"""

import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

DID_API_KEY = os.getenv('DID_API_KEY')

def test_avatar_with_url(image_url):
    """Test avatar creation with a public image URL"""
    
    print("\n" + "="*60)
    print("AVATAR CREATION TEST - CUSTOM IMAGE")
    print("="*60)
    
    # Check API key
    if not DID_API_KEY:
        print("❌ ERROR: DID_API_KEY not found in .env file")
        return False
    
    print(f"✅ API Key found: {DID_API_KEY[:10]}...")
    print(f"✅ Image URL: {image_url}")
    
    # Validate URL
    if not image_url.startswith('http'):
        print("❌ ERROR: Invalid URL (must start with http:// or https://)")
        return False
    
    if not any(image_url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png']):
        print("⚠️  WARNING: URL doesn't end with .jpg, .jpeg, or .png")
        print("   D-ID might reject this URL")
    
    # Create talking avatar
    print("\n📤 Creating talking avatar with YOUR image...")
    
    url = "https://api.d-id.com/talks"
    headers = {
        "Authorization": f"Basic {DID_API_KEY}",
        "Content-Type": "application/json",
        "accept": "application/json"
    }
    
    test_text = "Hello! This is me speaking as a digital avatar. This is a test of D-ID with my custom image."
    
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
            
            # Poll for completion
            print("\n⏳ Waiting for avatar video to be ready...")
            
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
                        print(f"\n✅ SUCCESS! Your custom avatar video is ready!")
                        print(f"   Video URL: {video_url}")
                        print(f"\n🎬 Open this URL in your browser to see YOUR avatar:")
                        print(f"   {video_url}")
                        
                        # Download the video
                        print("\n📥 Downloading video...")
                        video_response = requests.get(video_url)
                        output_file = "my_custom_avatar.mp4"
                        
                        with open(output_file, 'wb') as f:
                            f.write(video_response.content)
                        
                        print(f"✅ Video saved to: {output_file}")
                        print(f"   File size: {len(video_response.content)} bytes")
                        print(f"\n🎉 Play '{output_file}' to see YOUR talking avatar!")
                        
                        return True
                        
                    elif status == 'error':
                        error_msg = poll_data.get('error', {})
                        print(f"\n❌ ERROR: Avatar creation failed")
                        print(f"   Error: {error_msg}")
                        return False
                else:
                    print(f"❌ ERROR polling status: {poll_response.status_code}")
                    return False
            
            print("\n⏱️ TIMEOUT: Avatar creation took too long")
            return False
            
        else:
            print(f"❌ ERROR: Avatar creation failed")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text}")
            
            try:
                error_data = response.json()
                print(f"\n📋 Error details:")
                if 'details' in error_data:
                    for key, value in error_data['details'].items():
                        print(f"   {key}: {value}")
            except:
                pass
            
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n🎬 CUSTOM AVATAR TEST SCRIPT")
    print("Test D-ID with YOUR image (requires public URL)")
    
    # Check if we have a saved Imgur URL
    if os.path.exists("imgur_url.txt"):
        with open("imgur_url.txt", "r") as f:
            saved_url = f.read().strip()
        print(f"\n💾 Found saved URL from Imgur:")
        print(f"   {saved_url}")
        use_saved = input("\nUse this URL? (y/n): ").strip().lower()
        if use_saved == 'y':
            image_url = saved_url
        else:
            image_url = input("\n🔗 Enter your public image URL: ").strip()
    else:
        print("\n💡 TIP: First run 'python upload_image_to_imgur.py' to get a public URL")
        image_url = input("\n🔗 Enter your public image URL: ").strip()
    
    if not image_url:
        print("❌ No URL provided")
    else:
        success = test_avatar_with_url(image_url)
        
        print("\n" + "="*60)
        if success:
            print("✅ CUSTOM AVATAR TEST PASSED!")
            print("Your image works with D-ID!")
            print("You now have a talking avatar with YOUR face!")
        else:
            print("❌ CUSTOM AVATAR TEST FAILED!")
            print("Check the errors above.")
        print("="*60 + "\n")

"""
Simple Voice Cloning Test Script
Upload an audio file and test if ElevenLabs clones it successfully
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')

def test_voice_clone(audio_file_path):
    """Test voice cloning with ElevenLabs"""
    
    print("\n" + "="*60)
    print("VOICE CLONING TEST")
    print("="*60)
    
    # Check API key
    if not ELEVENLABS_API_KEY:
        print("❌ ERROR: ELEVENLABS_API_KEY not found in .env file")
        return False
    
    print(f"✅ API Key found: {ELEVENLABS_API_KEY[:10]}...")
    
    # Check if audio file exists
    if not os.path.exists(audio_file_path):
        print(f"❌ ERROR: Audio file not found: {audio_file_path}")
        return False
    
    print(f"✅ Audio file found: {audio_file_path}")
    print(f"   File size: {os.path.getsize(audio_file_path)} bytes")
    
    # Step 1: Clone the voice
    print("\n📤 Step 1: Cloning voice with ElevenLabs...")
    
    url = "https://api.elevenlabs.io/v1/voices/add"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY
    }
    
    try:
        with open(audio_file_path, 'rb') as audio_file:
            files = {
                'files': (os.path.basename(audio_file_path), audio_file, 'audio/mpeg')
            }
            data = {
                'name': 'Test_Voice_Clone',
                'description': 'Test voice cloning'
            }
            
            response = requests.post(url, headers=headers, files=files, data=data)
            
            print(f"📥 Response Status: {response.status_code}")
            
            if response.status_code == 200:
                voice_data = response.json()
                voice_id = voice_data.get('voice_id')
                print(f"✅ SUCCESS! Voice cloned!")
                print(f"   Voice ID: {voice_id}")
                
                # Step 2: Test the cloned voice
                print("\n📤 Step 2: Testing cloned voice with text-to-speech...")
                test_text = "Hello! This is a test of my cloned voice. Can you hear me clearly?"
                
                tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
                tts_data = {
                    "text": test_text,
                    "model_id": "eleven_monolingual_v1",
                    "voice_settings": {
                        "stability": 0.5,
                        "similarity_boost": 0.75
                    }
                }
                
                tts_response = requests.post(tts_url, headers=headers, json=tts_data)
                
                if tts_response.status_code == 200:
                    # Save the audio
                    output_file = "test_cloned_voice_output.mp3"
                    with open(output_file, 'wb') as f:
                        f.write(tts_response.content)
                    
                    print(f"✅ SUCCESS! Audio generated with cloned voice!")
                    print(f"   Saved to: {output_file}")
                    print(f"   File size: {len(tts_response.content)} bytes")
                    print(f"\n🔊 Play the file '{output_file}' to hear your cloned voice!")
                    
                    # Step 3: Cleanup (optional)
                    print("\n🗑️  Step 3: Cleanup - Deleting test voice...")
                    delete_url = f"https://api.elevenlabs.io/v1/voices/{voice_id}"
                    delete_response = requests.delete(delete_url, headers=headers)
                    
                    if delete_response.status_code == 200:
                        print("✅ Test voice deleted from ElevenLabs")
                    
                    return True
                else:
                    print(f"❌ ERROR: Text-to-speech failed")
                    print(f"   Status: {tts_response.status_code}")
                    print(f"   Response: {tts_response.text}")
                    return False
            else:
                print(f"❌ ERROR: Voice cloning failed")
                print(f"   Status: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n🎤 VOICE CLONING TEST SCRIPT")
    print("This script tests if ElevenLabs voice cloning works")
    print("\nUsage: python test_voice_clone.py")
    
    # Ask for audio file path
    audio_file = input("\n📁 Enter path to your audio file (or press Enter for default): ").strip()
    
    if not audio_file:
        # Check if there's any audio file in uploads folder
        if os.path.exists('uploads'):
            audio_files = [f for f in os.listdir('uploads') if f.endswith(('.mp3', '.wav', '.m4a', '.webm'))]
            if audio_files:
                audio_file = os.path.join('uploads', audio_files[0])
                print(f"Using: {audio_file}")
            else:
                print("❌ No audio files found in uploads folder")
                audio_file = input("Please enter full path to audio file: ").strip()
        else:
            audio_file = input("Please enter full path to audio file: ").strip()
    
    # Run the test
    success = test_voice_clone(audio_file)
    
    print("\n" + "="*60)
    if success:
        print("✅ VOICE CLONING TEST PASSED!")
        print("Your voice can be cloned successfully.")
    else:
        print("❌ VOICE CLONING TEST FAILED!")
        print("Check the errors above.")
    print("="*60 + "\n")

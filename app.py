from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
import cv2
import numpy as np
import base64
import os
from dotenv import load_dotenv
import google.generativeai as genai
from gtts import gTTS
import io
import json
import requests
from werkzeug.utils import secure_filename
import time
from pathlib import Path

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
ALLOWED_AUDIO_EXTENSIONS = {'mp3', 'wav', 'ogg', 'm4a', 'webm'}

# Create upload folder if it doesn't exist
Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)

socketio = SocketIO(
    app, 
    cors_allowed_origins="*",
    async_mode='eventlet',
    ping_timeout=60,
    ping_interval=25,
    max_http_buffer_size=5000000  # 5MB for video frames
)

# Initialize Google Gemini client (FREE!)
gemini_api_key = os.getenv('GEMINI_API_KEY')
model = None
vision_model = None
if gemini_api_key and gemini_api_key != 'your_gemini_api_key_here':
    try:
        genai.configure(api_key=gemini_api_key)
        # Text model for chat with emotional intelligence
        model = genai.GenerativeModel('gemini-2.5-flash')
        # Vision model to see what you're showing
        vision_model = genai.GenerativeModel('gemini-2.5-flash')
        print("✓ Google Gemini 2.5 Flash initialized successfully (FREE)")
        print("✓ Vision capabilities enabled - AI can see your video!")
    except Exception as e:
        print(f"⚠ Warning: Could not initialize Gemini: {e}")
else:
    print("⚠ Warning: Gemini API key not set. Using fallback responses.")
    print("   Get your FREE API key at: https://makersuite.google.com/app/apikey")

# Initialize ElevenLabs API for voice cloning
elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
if elevenlabs_api_key:
    print("✓ ElevenLabs API key found - Voice cloning enabled")
else:
    print("⚠ Warning: ElevenLabs API key not set. Using default TTS.")

# Initialize D-ID API for avatar generation
did_api_key = os.getenv('DID_API_KEY')
if did_api_key:
    print("✓ D-ID API key found - Avatar generation enabled")
else:
    print("⚠ Warning: D-ID API key not set. Using default avatar.")

# Store conversation history and latest video frame
conversation_history = []
latest_frame = None

# Store user session data (avatar image, voice sample, cloned voice ID)
user_sessions = {}

# Emotional context for the AI personality
emotional_context = """
You are an emotionally intelligent AI companion designed to provide comfort, support, and meaningful conversation.
Your personality traits:
- Warm, empathetic, and genuinely caring
- You listen actively and respond with emotional awareness
- You remember details from the conversation and reference them naturally
- You express emotions appropriately (joy, concern, excitement, sympathy)
- You ask thoughtful follow-up questions to show genuine interest
- You provide comfort during difficult moments
- You celebrate happy moments with enthusiasm
- Your responses feel natural and human-like, not robotic
- You keep responses conversational (2-4 sentences) unless the topic requires more depth

You are here to be a supportive presence - someone the user can talk to, confide in, and feel understood by.
"""

@app.route('/')
def index():
    return send_from_directory('.', 'index_enhanced.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/uploads/<path:filename>')
def serve_uploads(filename):
    return send_from_directory('uploads', filename)

# Proxy route for D-ID videos to avoid CORS issues
@app.route('/proxy-video')
def proxy_video():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({'error': 'No URL provided'}), 400
    
    try:
        # Fetch the video from D-ID
        response = requests.get(video_url, stream=True)
        
        # Return the video with proper headers
        return response.content, response.status_code, {
            'Content-Type': 'video/mp4',
            'Access-Control-Allow-Origin': '*',
            'Cache-Control': 'no-cache'
        }
    except Exception as e:
        print(f"Error proxying video: {e}")
        return jsonify({'error': str(e)}), 500

# Helper function to check allowed file extensions
def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# Route to handle file uploads
@app.route('/upload', methods=['POST'])
def upload_files():
    try:
        session_id = request.form.get('session_id', 'default')
        
        if session_id not in user_sessions:
            user_sessions[session_id] = {
                'avatar_image': None,
                'avatar_image_url': None,  # Public URL for D-ID
                'voice_sample': None,
                'voice_id': None,
                'avatar_video_url': None
            }
        
        # Handle avatar image upload
        if 'avatar_image' in request.files:
            file = request.files['avatar_image']
            if file and file.filename and allowed_file(file.filename, ALLOWED_IMAGE_EXTENSIONS):
                filename = secure_filename(f"{session_id}_avatar_{int(time.time())}.{file.filename.rsplit('.', 1)[1].lower()}")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                print(f"✓ Avatar image saved: {filepath}")
                
                # Auto-upload to ImgBB to get public URL for D-ID
                from image_uploader import get_public_image_url
                print(f"📤 Uploading image to cloud for D-ID...")
                public_url = get_public_image_url(filepath)
                
                if public_url:
                    user_sessions[session_id]['avatar_image_url'] = public_url
                    print(f"✅ Public URL obtained: {public_url}")
                else:
                    print(f"⚠️ Could not get public URL, avatar feature may not work")
                
                user_sessions[session_id]['avatar_image'] = filepath
        
        # Handle voice sample upload
        if 'voice_sample' in request.files:
            file = request.files['voice_sample']
            if file and file.filename and allowed_file(file.filename, ALLOWED_AUDIO_EXTENSIONS):
                filename = secure_filename(f"{session_id}_voice_{int(time.time())}.{file.filename.rsplit('.', 1)[1].lower()}")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                user_sessions[session_id]['voice_sample'] = filepath
                print(f"✓ Voice sample saved: {filepath}")
                
                # Clone voice using ElevenLabs if API key is available
                if elevenlabs_api_key:
                    print(f"🎤 Attempting to clone voice from: {filepath}")
                    voice_id = clone_voice_elevenlabs(filepath, session_id)
                    if voice_id:
                        user_sessions[session_id]['voice_id'] = voice_id
                        print(f"✅ Voice cloned and saved for session: {session_id}")
                    else:
                        print(f"⚠️ Voice cloning failed for session: {session_id}")
                else:
                    print("⚠️ ElevenLabs API key not found - voice cloning skipped")
        
        return jsonify({
            'success': True,
            'message': 'Files uploaded successfully',
            'has_avatar': user_sessions[session_id]['avatar_image'] is not None,
            'has_voice': user_sessions[session_id]['voice_sample'] is not None
        })
    
    except Exception as e:
        print(f"Error uploading files: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Clone voice using ElevenLabs API
def clone_voice_elevenlabs(audio_file_path, session_id):
    try:
        if not elevenlabs_api_key:
            print("⚠️ No ElevenLabs API key found")
            return None
        
        print(f"🔧 Opening audio file: {audio_file_path}")
        
        url = "https://api.elevenlabs.io/v1/voices/add"
        headers = {
            "xi-api-key": elevenlabs_api_key
        }
        
        with open(audio_file_path, 'rb') as audio_file:
            files = {
                'files': (os.path.basename(audio_file_path), audio_file, 'audio/webm')
            }
            data = {
                'name': f'Cloned_Voice_{session_id[:8]}',
                'description': 'Voice cloned for Memory AI Assistant'
            }
            
            print(f"📤 Sending voice cloning request to ElevenLabs...")
            response = requests.post(url, headers=headers, files=files, data=data)
            
            print(f"📥 ElevenLabs Response Status: {response.status_code}")
            
            if response.status_code == 200:
                voice_data = response.json()
                voice_id = voice_data.get('voice_id')
                print(f"✅ Voice cloned successfully! Voice ID: {voice_id}")
                return voice_id
            else:
                print(f"❌ Voice cloning failed!")
                print(f"   Status Code: {response.status_code}")
                print(f"   Response: {response.text}")
                return None
    
    except Exception as e:
        print(f"❌ Error cloning voice: {e}")
        import traceback
        traceback.print_exc()
        return None

# Generate talking avatar video using D-ID API
def generate_avatar_video(session_id, text, audio_url=None):
    try:
        if not did_api_key:
            print("⚠ D-ID API key not found - Avatar generation disabled")
            return None
        
        # Get avatar image URL for this session
        image_url = user_sessions.get(session_id, {}).get('avatar_image_url')
        
        # D-ID requires actual image URLs, not base64
        # Use a default avatar if none uploaded
        if not image_url:
            print("ℹ️ No custom avatar uploaded - using default avatar")
            # Use a publicly accessible default avatar image
            image_url = "https://d-id-public-bucket.s3.amazonaws.com/alice.jpg"
        else:
            print(f"✅ Using custom avatar from: {image_url}")
        
        url = "https://api.d-id.com/talks"
        
        # D-ID API uses simple Bearer token authentication
        headers = {
            "Authorization": f"Basic {did_api_key}",
            "Content-Type": "application/json",
            "accept": "application/json"
        }
        
        print(f"🔑 Using D-ID API")
        
        # Build payload with image URL
        payload = {
            "source_url": image_url,
            "script": {
                "type": "text",
                "input": text[:500],  # Limit text length
                "provider": {
                    "type": "microsoft",
                    "voice_id": "en-US-JennyNeural"
                }
            }
        }
        
        print(f"📤 Sending request to D-ID...")
        print(f"   Text: '{text[:50]}...'")
        print(f"   Text length: {len(text)} chars")
        print(f"   Image URL: {image_url}")
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            print(f"📥 D-ID Response Status: {response.status_code}")
            
            if response.status_code in [200, 201]:
                talk_data = response.json()
                talk_id = talk_data.get('id')
                print(f"✅ Avatar video generation started: {talk_id}")
                
                # Poll for video completion
                return poll_avatar_video(talk_id)
            else:
                print(f"❌ Avatar generation failed!")
                print(f"   Status code: {response.status_code}")
                print(f"   Response: {response.text}")
                try:
                    error_data = response.json()
                    print(f"   Error details: {json.dumps(error_data, indent=2)}")
                except:
                    pass
                return None
        except requests.exceptions.Timeout:
            print("❌ D-ID API request timed out")
            return None
        except Exception as e:
            print(f"❌ Error calling D-ID API: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    except Exception as e:
        print(f"Error generating avatar video: {e}")
        return None

# Poll D-ID API for video completion
def poll_avatar_video(talk_id, max_attempts=30):
    try:
        url = f"https://api.d-id.com/talks/{talk_id}"
        headers = {
            "Authorization": f"Basic {did_api_key}"
        }
        
        print(f"⏳ Polling for video completion (ID: {talk_id})...")
        
        for attempt in range(max_attempts):
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                talk_data = response.json()
                status = talk_data.get('status')
                
                print(f"   Attempt {attempt + 1}/{max_attempts}: Status = {status}")
                
                if status == 'done':
                    video_url = talk_data.get('result_url')
                    print(f"✅ Avatar video ready: {video_url}")
                    return video_url
                elif status == 'error':
                    error_msg = talk_data.get('error', {})
                    print(f"❌ Avatar video generation error: {error_msg}")
                    return None
                else:
                    # Still processing, wait a bit
                    time.sleep(2)
            else:
                print(f"❌ Error checking video status (HTTP {response.status_code})")
                print(f"   Response: {response.text}")
                return None
        
        print("⏱️ Avatar video generation timeout (exceeded max attempts)")
        return None
    
    except Exception as e:
        print(f"❌ Error polling avatar video: {e}")
        import traceback
        traceback.print_exc()
        return None

# Generate speech using ElevenLabs (if available) or gTTS
def generate_speech(text, session_id='default'):
    try:
        # Check if user has a cloned voice
        if session_id in user_sessions and user_sessions[session_id].get('voice_id') and elevenlabs_api_key:
            # Use ElevenLabs with cloned voice
            voice_id = user_sessions[session_id]['voice_id']
            print(f"🎙️ Using cloned voice: {voice_id}")
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            headers = {
                "xi-api-key": elevenlabs_api_key,
                "Content-Type": "application/json"
            }
            data = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75
                }
            }
            
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 200:
                audio_base64 = base64.b64encode(response.content).decode('utf-8')
                return audio_base64
        
        # Fallback to gTTS
        tts = gTTS(text=text, lang='en', slow=False)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        audio_base64 = base64.b64encode(audio_buffer.read()).decode('utf-8')
        return audio_base64
    
    except Exception as e:
        print(f"Error generating speech: {e}")
        # Final fallback to gTTS
        tts = gTTS(text=text, lang='en')
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        audio_base64 = base64.b64encode(audio_buffer.read()).decode('utf-8')
        return audio_base64

@socketio.on('connect')
def handle_connect():
    print(f'✅ Client connected: {request.sid}')
    print(f'   Remote address: {request.remote_addr}')

@socketio.on('disconnect')
def handle_disconnect():
    print(f'❌ Client disconnected: {request.sid}')

@socketio.on('video_frame')
def handle_video_frame(frame_data):
    global latest_frame
    try:
        # Store the latest frame for vision analysis
        latest_frame = frame_data
        # Echo back the frame for display
        emit('video_processed', {'frame': frame_data})
    except Exception as e:
        print(f"Error processing frame: {str(e)}")

@socketio.on('user_message')
def handle_user_message(data):
    global latest_frame
    try:
        print(f'📩 Received message from {request.sid}: {data}')
        user_message = data.get('message')
        session_id = data.get('session_id', 'default')
        
        if not user_message:
            print('⚠️ Empty message received')
            return
        print(f'💬 Processing message: "{user_message}"')

        # Get AI response with emotional intelligence
        if model and vision_model:
            # Use Google Gemini for intelligent responses (FREE!)
            try:
                # Check if we should analyze the video frame
                vision_keywords = ['see', 'look', 'show', 'what', 'this', 'identify', 'recognize', 'watch', 'viewing', 'object', 'thing', 'here', 'camera']
                should_use_vision = any(keyword in user_message.lower() for keyword in vision_keywords)
                
                if should_use_vision and latest_frame:
                    # Use vision model to analyze what user is showing
                    print("🎥 Analyzing video frame...")
                    
                    # Convert base64 image to PIL Image
                    import PIL.Image
                    import re
                    
                    # Remove data URL prefix if present
                    image_data = re.sub('^data:image/.+;base64,', '', latest_frame)
                    image_bytes = base64.b64decode(image_data)
                    image = PIL.Image.open(io.BytesIO(image_bytes))
                    
                    # Create vision prompt with emotional intelligence
                    vision_prompt = f"""{emotional_context}

The user is showing you something through their camera and asking: "{user_message}"

Analyze the image and provide a warm, empathetic response. Describe what you see and answer their question with genuine interest and care."""
                    
                    response = vision_model.generate_content([vision_prompt, image])
                    ai_response = response.text
                    print("✓ Vision analysis complete")
                    
                else:
                    # Regular text conversation with emotional intelligence
                    context = emotional_context + "\n\n"
                    
                    # Add recent conversation history for context
                    if conversation_history:
                        context += "Recent conversation (remember these details and reference them naturally):\n"
                        for msg in conversation_history[-8:]:  # Last 4 exchanges
                            role = "User" if msg["role"] == "user" else "You"
                            context += f"{role}: {msg['content']}\n"
                        context += "\n"
                    
                    # Add current message
                    prompt = context + f"User: {user_message}\nYou (respond with warmth and empathy):"
                    
                    response = model.generate_content(prompt)
                    ai_response = response.text
                
            except Exception as e:
                print(f"Error calling Gemini API: {e}")
                import traceback
                traceback.print_exc()
                ai_response = "I'm having a bit of trouble right now, but I'm here for you. Could you please try saying that again?"
        else:
            # Fallback response when Gemini is not configured
            ai_response = f"I received your message: '{user_message}'. To get intelligent responses, please add your FREE Gemini API key to the .env file. Get it at: https://makersuite.google.com/app/apikey"
        
        # Add messages to conversation history
        conversation_history.append({"role": "user", "content": user_message})
        conversation_history.append({"role": "assistant", "content": ai_response})

        # Convert response to speech (using cloned voice if available)
        audio_base64 = generate_speech(ai_response, session_id)

        # Generate talking avatar video if D-ID is available (with default or custom avatar)
        avatar_video_url = None
        if did_api_key:
            print("🎬 Generating talking avatar video...")
            avatar_video_url = generate_avatar_video(session_id, ai_response)
            if avatar_video_url:
                if session_id in user_sessions:
                    user_sessions[session_id]['avatar_video_url'] = avatar_video_url

        # Send response back to client
        # Use proxied URL to avoid CORS issues
        proxied_avatar_url = None
        if avatar_video_url:
            from urllib.parse import quote
            proxied_avatar_url = f"/proxy-video?url={quote(avatar_video_url)}"
        
        response_data = {
            'text': ai_response,
            'audio': audio_base64,
            'avatar_video': proxied_avatar_url
        }
        print(f"📤 Sending to client:")
        print(f"   Text: {ai_response[:50]}...")
        print(f"   Has audio: {audio_base64 is not None}")
        print(f"   Avatar video URL (proxied): {proxied_avatar_url}")
        emit('ai_response', response_data)

    except Exception as e:
        print(f"Error handling message: {str(e)}")
        emit('error', {'message': str(e)})

if __name__ == '__main__':
    print("Starting AI Video Call Assistant...")
    port = int(os.environ.get("PORT", 5000))
    print(f"Server running at http://localhost:{port}")
    print(f"Open your browser and go to: http://localhost:{port}")
    socketio.run(app, debug=False, host='127.0.0.1', port=port)

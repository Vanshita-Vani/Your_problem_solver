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

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(
    app, 
    cors_allowed_origins="*",
    async_mode='eventlet',
    ping_timeout=60,
    ping_interval=25,
    max_http_buffer_size=10000000  # 10MB for video frames
)

# Initialize Google Gemini client (FREE!)
gemini_api_key = os.getenv('GEMINI_API_KEY')
model = None
vision_model = None
if gemini_api_key and gemini_api_key != 'your_gemini_api_key_here':
    try:
        genai.configure(api_key=gemini_api_key)
        # Text model for chat
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

# Store conversation history and latest video frame
conversation_history = []
latest_frame = None

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

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
        user_message = data.get('message')
        if not user_message:
            return

        # Get AI response
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
                    
                    # Create vision prompt
                    vision_prompt = f"""You are an AI video call assistant. The user is showing you something through their camera and asking: "{user_message}"

Analyze the image and provide a helpful, concise response (2-3 sentences). Describe what you see and answer their question."""
                    
                    response = vision_model.generate_content([vision_prompt, image])
                    ai_response = response.text
                    print("✓ Vision analysis complete")
                    
                else:
                    # Regular text conversation
                    context = "You are a helpful AI video call assistant. You can see the user through their camera and help them with tasks, answer questions, and provide guidance. Be friendly, concise (2-3 sentences max), and helpful.\n\n"
                    
                    # Add recent conversation history for context
                    if conversation_history:
                        context += "Recent conversation:\n"
                        for msg in conversation_history[-6:]:  # Last 3 exchanges
                            role = "User" if msg["role"] == "user" else "Assistant"
                            context += f"{role}: {msg['content']}\n"
                        context += "\n"
                    
                    # Add current message
                    prompt = context + f"User: {user_message}\nAssistant:"
                    
                    response = model.generate_content(prompt)
                    ai_response = response.text
                
            except Exception as e:
                print(f"Error calling Gemini API: {e}")
                import traceback
                traceback.print_exc()
                ai_response = "I'm having trouble analyzing the video right now. Could you please try again?"
        else:
            # Fallback response when Gemini is not configured
            ai_response = f"I received your message: '{user_message}'. To get intelligent responses, please add your FREE Gemini API key to the .env file. Get it at: https://makersuite.google.com/app/apikey"
        
        # Add messages to conversation history
        conversation_history.append({"role": "user", "content": user_message})
        conversation_history.append({"role": "assistant", "content": ai_response})

        # Convert response to speech
        tts = gTTS(text=ai_response, lang='en')
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        audio_base64 = base64.b64encode(audio_buffer.read()).decode('utf-8')

        # Send response back to client
        emit('ai_response', {
            'text': ai_response,
            'audio': audio_base64
        })

    except Exception as e:
        print(f"Error handling message: {str(e)}")
        emit('error', {'message': str(e)})

if __name__ == '__main__':
    print("Starting AI Video Call Assistant...")
    print("Server running at http://localhost:5000")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)

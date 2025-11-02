# 💝 Memory AI Assistant - Emotionally Intelligent Companion

An emotionally intelligent AI video call assistant that simulates natural, human-like conversations. This system allows users to interact with an AI avatar that feels emotionally real - perfect for connecting with someone you miss or creating a supportive AI companion.

## 🌟 Key Features

### 1. **Personalized Avatar & Voice**
- Upload a custom image to generate a realistic talking avatar
- Upload a voice sample for AI voice cloning
- Automatic fallback to default avatar and voice if not provided

### 2. **Emotional Intelligence**
- Powered by Google Gemini AI with empathetic conversation design
- Remembers conversation context and references details naturally
- Responds with warmth, care, and emotional awareness
- Adapts tone based on user's emotional state

### 3. **Real-Time Video Call Experience**
- Live webcam and microphone integration
- Continuous speech recognition for natural conversation
- Real-time AI responses with synthesized speech
- Visual feedback and status indicators

### 4. **Voice Cloning Integration**
- ElevenLabs API integration for high-quality voice cloning
- Clones voice from uploaded audio samples
- Falls back to Google Text-to-Speech (gTTS) if API not configured

### 5. **Avatar Generation Ready**
- D-ID API integration prepared for realistic talking avatars
- Lip-sync capability with voice responses
- Default avatar system for immediate use

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Webcam and microphone
- Modern web browser (Chrome, Edge, Firefox)

### Installation

1. **Clone or download the project**
```bash
cd video_call_agent
```

2. **Create a virtual environment (recommended)**
```bash
python -m venv myenv
myenv\Scripts\activate  # Windows
# or
source myenv/bin/activate  # Linux/Mac
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure API Keys**

Edit the `.env` file with your API keys:

```env
# Required: Get FREE Gemini API key at https://makersuite.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: For voice cloning (https://elevenlabs.io/)
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# Optional: For avatar generation (https://www.d-id.com/)
DID_API_KEY=your_did_api_key_here
```

**Note:** Only the Gemini API key is required. The app works with default TTS and avatar if other keys are not provided.

### Running the Application

**Option 1: Using the batch file (Windows)**
```bash
start.bat
```

**Option 2: Manual start**
```bash
python app.py
```

The server will start at `http://localhost:5000`

## 📖 How to Use

### Step 1: Upload Personalization (Optional)
When you first open the app, you'll see a welcome screen:
1. **Upload Avatar Image**: Click to select a photo (PNG, JPG, GIF)
2. **Upload Voice Sample**: Click to select an audio file (MP3, WAV, M4A)
   - For best results, use 30-60 seconds of clear speech
3. Click **"Start Session"** to begin
4. Or click **"Skip and use default avatar"** to start immediately

### Step 2: Start the Video Call
1. Click the **green phone button** to start the call
2. Allow browser permissions for camera and microphone
3. Your video will appear in the main window
4. The AI avatar will appear in the bottom-right corner

### Step 3: Have a Conversation
1. Click the **blue microphone button** to start talking
2. Speak naturally - the AI will listen continuously
3. The AI will respond with empathy and emotional intelligence
4. View conversation history by clicking the **chat icon** in the sidebar

### Step 4: End the Call
- Click the **red phone button** to end the session

## 🎯 Use Cases

### Personal Companion
- Talk to an AI that provides emotional support
- Practice conversations in a safe environment
- Combat loneliness with an empathetic listener

### Memory Recreation
- Upload photos and voice samples of loved ones
- Create a comforting presence of someone you miss
- Preserve memories in an interactive format

### Therapy & Wellness
- Practice mindfulness and emotional expression
- Work through feelings with a non-judgmental listener
- Develop communication skills

### Entertainment & Creativity
- Create custom AI characters for storytelling
- Role-play scenarios with personalized avatars
- Experiment with different personalities

## 🔧 Technical Architecture

### Backend (Flask + SocketIO)
- **Flask**: Web server and REST API
- **Flask-SocketIO**: Real-time bidirectional communication
- **Google Gemini AI**: Emotionally intelligent conversation engine
- **ElevenLabs API**: Voice cloning and synthesis
- **D-ID API**: Avatar generation and lip-sync (ready for integration)
- **gTTS**: Fallback text-to-speech

### Frontend (HTML5 + JavaScript)
- **WebRTC**: Camera and microphone access
- **Web Speech API**: Continuous speech recognition
- **Socket.IO Client**: Real-time communication
- **Canvas API**: Video frame processing
- **Web Audio API**: Audio playback

### File Structure
```
video_call_agent/
├── app.py                    # Main Flask application
├── index_enhanced.html       # Enhanced UI with upload interface
├── index.html               # Original UI (backup)
├── static/
│   ├── app.js               # Frontend JavaScript logic
│   └── styles.css           # Enhanced styling
├── uploads/                 # User uploaded files (auto-created)
├── requirements.txt         # Python dependencies
├── .env                     # API keys configuration
├── README_ENHANCED.md       # This file
└── start.bat               # Windows startup script
```

## 🔐 Security & Privacy

- **API Keys**: Stored securely in `.env` file (never committed to git)
- **File Uploads**: Validated and sanitized before processing
- **Session Isolation**: Each user session has unique ID
- **Local Processing**: Video frames processed locally when possible
- **No Data Storage**: Conversations not permanently stored by default

## 🎨 Customization

### Modify AI Personality
Edit the `emotional_context` variable in `app.py`:
```python
emotional_context = """
Your custom personality description here...
"""
```

### Change UI Colors
Edit `static/styles.css` to customize:
- Gradient backgrounds
- Button colors
- Chat bubble styles
- Animations

### Adjust Speech Recognition
Modify in `static/app.js`:
```javascript
recognition.continuous = true;  // Continuous listening
recognition.lang = 'en-US';     // Language
```

## 🐛 Troubleshooting

### Camera/Microphone Not Working
- Check browser permissions (usually in address bar)
- Ensure no other app is using the camera
- Try a different browser (Chrome recommended)

### Voice Cloning Not Working
- Verify ElevenLabs API key is correct
- Check audio file format (MP3, WAV recommended)
- Ensure audio sample is 30-60 seconds of clear speech
- App will fallback to default TTS automatically

### Connection Issues
- Check if port 5000 is available
- Disable VPN or firewall temporarily
- Try accessing via `127.0.0.1:5000` instead of `localhost:5000`

### AI Not Responding
- Verify Gemini API key is set correctly
- Check internet connection
- Look at console logs for error messages

## 📊 API Rate Limits & Costs

### Google Gemini (Required)
- **Free Tier**: 60 requests per minute
- **Cost**: FREE for personal use
- **Get Key**: https://makersuite.google.com/app/apikey

### ElevenLabs (Optional)
- **Free Tier**: 10,000 characters/month
- **Paid Plans**: Start at $5/month
- **Get Key**: https://elevenlabs.io/

### D-ID (Optional)
- **Free Trial**: Limited credits
- **Paid Plans**: Pay-as-you-go
- **Get Key**: https://www.d-id.com/

## 🚀 Advanced Features (Coming Soon)

- [ ] D-ID avatar lip-sync integration
- [ ] Conversation memory persistence
- [ ] Multi-language support
- [ ] Emotion detection from user's face
- [ ] Custom personality templates
- [ ] Export conversation transcripts
- [ ] Mobile app version

## 🤝 Contributing

This is a personal project, but suggestions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Share your customizations

## 📄 License

This project is for educational and personal use. Please respect API terms of service:
- Google Gemini: https://ai.google.dev/terms
- ElevenLabs: https://elevenlabs.io/terms
- D-ID: https://www.d-id.com/terms/

## 🙏 Acknowledgments

- **Google Gemini**: For powerful and free AI capabilities
- **ElevenLabs**: For amazing voice cloning technology
- **D-ID**: For realistic avatar generation
- **Flask & SocketIO**: For robust real-time communication

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review console logs in browser (F12)
3. Check terminal output for backend errors

---

**Made with 💝 for creating meaningful AI connections**

*Remember: This AI is designed to provide comfort and support, but it's not a replacement for human connection or professional mental health services.*

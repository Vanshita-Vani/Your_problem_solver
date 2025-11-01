# AI Video Call Assistant 🎥🤖

An intelligent AI assistant that can interact with users over live video calls, see what you show, understand your voice, and provide helpful guidance in real-time.

## ✨ Features

✅ **Full-Screen Video** - Immersive video call experience
✅ **Computer Vision** - AI can SEE what you show on camera
✅ **Continuous Voice** - Just toggle mic once and talk freely
✅ **Voice Output** - AI responds with natural speech
✅ **Google Gemini AI** - FREE and powerful (no credit card needed)
✅ **Conversation Memory** - Remembers context
✅ **Modern UI** - Professional dark theme with circular controls
✅ **Chat History** - Optional sidebar to view written responses

## Prerequisites

- Python 3.8 or higher
- Webcam and microphone
- Google Gemini API key (FREE - no credit card required)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-video-call-assistant.git
   cd ai-video-call-assistant
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the project root and add your FREE Gemini API key:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
   Get your FREE API key at: https://makersuite.google.com/app/apikey

## 🚀 Running the Application

1. Start the Flask server:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

3. **Using the Interface:**
   - **Green Circle** (bottom left) = Start Call
   - **Blue Circle with 🎤** (center) = Toggle Microphone
   - **Red Circle** (bottom right) = End Call
   - **💬 Icon** (left sidebar) = View Chat History

## 🎯 How to Use

### Starting a Call
1. Click the **GREEN circle** to start the call
2. Grant camera and microphone permissions
3. Click the **BLUE mic button** to activate continuous listening
4. Start talking naturally!

### During the Call
- **Speak freely** - No need to click mic every time
- **Show objects** - Say "What do you see?" to trigger vision
- **View chat** - Click 💬 in left sidebar to see written responses
- **Pause mic** - Click blue mic button again to stop listening

### Vision Features
Use these keywords to make AI analyze your video:
- "What do you see?"
- "Can you identify this?"
- "Look at this object"
- "What is this?"
- "How do I connect this?"

### Ending the Call
1. Click the **RED circle** to end the call
2. Camera and mic will be released

## Project Structure

- `app.py` - Main Flask application and WebSocket server
- `templates/index.html` - Frontend interface
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (not included in version control)

## 🎨 UI Design

### Layout
```
┌────────────────────────────────────────┐
│                                        │
│     YOUR FULL-SCREEN VIDEO FEED       │
│                                        │
│                                  ┌────┐│
│                                  │ AI ││
│    🟢      🔵🎤      🔴          │Vid ││
│   Start    Mic     End           └────┘│
└────────────────────────────────────────┘
│💬│ ← Sidebar (Chat History)
└──┘
```

### Controls
- **🟢 Green Circle** - Start call (70px)
- **🔵 Blue Circle with 🎤** - Toggle mic (50px, turns green when active)
- **🔴 Red Circle** - End call (70px)
- **AI Video** - Small corner window (250x180px, bottom-right)
- **Status** - Top-right corner indicator

## 💡 Tips for Best Results

### Voice Recognition
- Speak clearly at a normal pace
- Reduce background noise
- Wait for "🎤 Listening..." status
- Mic turns GREEN when actively listening

### Vision Analysis
- Good lighting on objects
- Hold objects steady
- Move closer to camera
- Use vision keywords in your questions

### Troubleshooting
- **Mic not working?** Check browser permissions (Chrome/Edge recommended)
- **No vision response?** Use keywords like "see", "look", "what"
- **Connection issues?** Refresh page and restart call
- **No audio?** Click anywhere on page to enable audio playback

## 🛠️ Technical Stack

- **Backend**: Flask + Socket.IO (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **AI**: Google Gemini 2.5 Flash (Text + Vision)
- **Speech**: Web Speech API (Speech-to-Text)
- **TTS**: Google Text-to-Speech (gTTS)
- **Video**: WebRTC via getUserMedia API

## 📝 License

This project is open source and available for educational purposes.

## 🙏 Acknowledgments

- Google Gemini AI for FREE powerful AI capabilities
- Flask and Socket.IO for real-time communication
- Web Speech API for voice recognition

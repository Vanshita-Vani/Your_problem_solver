# 📡 API Reference - Memory AI Assistant

## HTTP Endpoints

### GET /
**Description**: Serves the main application interface

**Response**: HTML page (index_enhanced.html)

**Example**:
```
GET http://localhost:5000/
```

---

### GET /static/<filename>
**Description**: Serves static files (CSS, JavaScript)

**Parameters**:
- `filename` (path): Path to static file

**Response**: Static file content

**Examples**:
```
GET http://localhost:5000/static/app.js
GET http://localhost:5000/static/styles.css
```

---

### POST /upload
**Description**: Handles avatar image and voice sample uploads

**Content-Type**: `multipart/form-data`

**Form Parameters**:
- `session_id` (string, required): Unique session identifier
- `avatar_image` (file, optional): Avatar image file
  - Allowed: PNG, JPG, JPEG, GIF, WEBP
  - Max size: 16MB
- `voice_sample` (file, optional): Voice audio file
  - Allowed: MP3, WAV, OGG, M4A, WEBM
  - Max size: 16MB

**Response**:
```json
{
  "success": true,
  "message": "Files uploaded successfully",
  "has_avatar": true,
  "has_voice": true
}
```

**Error Response**:
```json
{
  "success": false,
  "error": "Error message here"
}
```

**Example (JavaScript)**:
```javascript
const formData = new FormData();
formData.append('session_id', 'session_123');
formData.append('avatar_image', imageFile);
formData.append('voice_sample', audioFile);

const response = await fetch('/upload', {
    method: 'POST',
    body: formData
});

const result = await response.json();
console.log(result);
```

---

## WebSocket Events (Socket.IO)

### Client → Server Events

#### connect
**Description**: Fired when client connects to server

**Payload**: None

**Server Response**: Logs connection with client ID

**Example**:
```javascript
socket.on('connect', () => {
    console.log('Connected to server');
});
```

---

#### disconnect
**Description**: Fired when client disconnects from server

**Payload**: None

**Server Response**: Logs disconnection

**Example**:
```javascript
socket.on('disconnect', () => {
    console.log('Disconnected from server');
});
```

---

#### video_frame
**Description**: Sends video frame to server for processing

**Payload**:
```javascript
{
  frame: "data:image/jpeg;base64,/9j/4AAQSkZJRg..." // Base64 encoded image
}
```

**Server Response**: Emits `video_processed` event

**Example**:
```javascript
const imageData = canvas.toDataURL('image/jpeg', 0.5);
socket.emit('video_frame', imageData);
```

---

#### user_message
**Description**: Sends user's spoken message to AI

**Payload**:
```javascript
{
  message: "Hello, how are you?",
  session_id: "session_123"
}
```

**Server Response**: Emits `ai_response` event

**Example**:
```javascript
socket.emit('user_message', {
    message: transcript,
    session_id: sessionId
});
```

---

### Server → Client Events

#### video_processed
**Description**: Returns processed video frame

**Payload**:
```javascript
{
  frame: "data:image/jpeg;base64,/9j/4AAQSkZJRg..." // Base64 encoded image
}
```

**Example**:
```javascript
socket.on('video_processed', (data) => {
    const img = new Image();
    img.src = data.frame;
    // Display image
});
```

---

#### ai_response
**Description**: Returns AI's text and audio response

**Payload**:
```javascript
{
  text: "I'm doing great! How can I help you today?",
  audio: "SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4Ljc2..." // Base64 encoded audio
}
```

**Example**:
```javascript
socket.on('ai_response', (data) => {
    console.log('AI said:', data.text);
    // Display text
    addMessage('ai', data.text);
    // Play audio
    playAudio(data.audio);
});
```

---

#### error
**Description**: Returns error message

**Payload**:
```javascript
{
  message: "Error description here"
}
```

**Example**:
```javascript
socket.on('error', (data) => {
    console.error('Server error:', data.message);
    alert('Error: ' + data.message);
});
```

---

## External API Integrations

### Google Gemini API

#### Configuration
```python
import google.generativeai as genai

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.5-flash')
```

#### Text Generation
```python
response = model.generate_content(prompt)
ai_response = response.text
```

#### Vision Analysis
```python
import PIL.Image

response = vision_model.generate_content([prompt, image])
ai_response = response.text
```

**Rate Limits**: 60 requests/minute (free tier)

**Documentation**: https://ai.google.dev/docs

---

### ElevenLabs API

#### Voice Cloning
**Endpoint**: `POST https://api.elevenlabs.io/v1/voices/add`

**Headers**:
```python
{
    "xi-api-key": "your_api_key_here"
}
```

**Request**:
```python
files = {
    'files': open(audio_file_path, 'rb')
}
data = {
    'name': 'Cloned_Voice_123',
    'description': 'Voice cloned for Memory AI Assistant'
}
```

**Response**:
```json
{
  "voice_id": "21m00Tcm4TlvDq8ikWAM",
  "name": "Cloned_Voice_123",
  "samples": [...],
  "category": "cloned"
}
```

---

#### Text-to-Speech
**Endpoint**: `POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}`

**Headers**:
```python
{
    "xi-api-key": "your_api_key_here",
    "Content-Type": "application/json"
}
```

**Request**:
```json
{
  "text": "Hello, how are you today?",
  "model_id": "eleven_monolingual_v1",
  "voice_settings": {
    "stability": 0.5,
    "similarity_boost": 0.75
  }
}
```

**Response**: Audio file (binary)

**Rate Limits**: 
- Free: 10,000 characters/month
- Paid: Varies by plan

**Documentation**: https://docs.elevenlabs.io/

---

### D-ID API (Ready for Integration)

#### Create Talking Avatar
**Endpoint**: `POST https://api.d-id.com/talks`

**Headers**:
```python
{
    "Authorization": "Basic your_api_key_here",
    "Content-Type": "application/json"
}
```

**Request**:
```json
{
  "source_url": "https://example.com/avatar.jpg",
  "script": {
    "type": "audio",
    "audio_url": "https://example.com/speech.mp3"
  },
  "config": {
    "fluent": true,
    "pad_audio": 0
  }
}
```

**Response**:
```json
{
  "id": "tlk_abc123",
  "created_at": "2024-01-01T00:00:00.000Z",
  "status": "created"
}
```

**Documentation**: https://docs.d-id.com/

---

## Frontend JavaScript API

### Session Management

#### Generate Session ID
```javascript
const sessionId = 'session_' + Date.now() + '_' + 
                  Math.random().toString(36).substr(2, 9);
```

---

### File Upload

#### Upload Files
```javascript
async function uploadFiles() {
    const formData = new FormData();
    formData.append('session_id', sessionId);
    
    if (avatarFile) {
        formData.append('avatar_image', avatarFile);
    }
    
    if (voiceFile) {
        formData.append('voice_sample', voiceFile);
    }
    
    const response = await fetch('/upload', {
        method: 'POST',
        body: formData
    });
    
    return await response.json();
}
```

---

### Video Streaming

#### Start Video Stream
```javascript
async function startVideo() {
    localStream = await navigator.mediaDevices.getUserMedia({
        video: true,
        audio: true
    });
    
    localVideo.srcObject = localStream;
}
```

#### Send Video Frame
```javascript
function sendVideoFrame() {
    ctx.drawImage(localVideo, 0, 0, canvas.width, canvas.height);
    const imageData = canvas.toDataURL('image/jpeg', 0.5);
    socket.emit('video_frame', imageData);
}
```

---

### Speech Recognition

#### Initialize Speech Recognition
```javascript
const SpeechRecognition = window.SpeechRecognition || 
                          window.webkitSpeechRecognition;
recognition = new SpeechRecognition();
recognition.continuous = true;
recognition.interimResults = false;
recognition.lang = 'en-US';
```

#### Handle Speech Result
```javascript
recognition.onresult = (event) => {
    const lastResult = event.results[event.results.length - 1];
    if (lastResult.isFinal) {
        const transcript = lastResult[0].transcript.trim();
        sendMessage(transcript);
    }
};
```

---

### Audio Playback

#### Play Audio from Base64
```javascript
async function playAudio(base64Data) {
    const binaryString = atob(base64Data);
    const bytes = new Uint8Array(binaryString.length);
    
    for (let i = 0; i < binaryString.length; i++) {
        bytes[i] = binaryString.charCodeAt(i);
    }
    
    const audioBuffer = await audioContext.decodeAudioData(bytes.buffer);
    
    const source = audioContext.createBufferSource();
    source.buffer = audioBuffer;
    source.connect(audioContext.destination);
    source.start();
}
```

---

## Error Codes

### HTTP Errors

| Code | Description | Solution |
|------|-------------|----------|
| 400 | Bad Request | Check request format |
| 404 | Not Found | Verify endpoint URL |
| 413 | Payload Too Large | Reduce file size (<16MB) |
| 500 | Internal Server Error | Check server logs |

### Socket.IO Errors

| Error | Description | Solution |
|-------|-------------|----------|
| `connect_error` | Connection failed | Check server is running |
| `connect_timeout` | Connection timeout | Check network/firewall |
| `disconnect` | Connection lost | Reconnect automatically |

### API Errors

#### Gemini API
- **INVALID_API_KEY**: Check `.env` file
- **QUOTA_EXCEEDED**: Wait or upgrade plan
- **RATE_LIMIT**: Slow down requests

#### ElevenLabs API
- **401 Unauthorized**: Invalid API key
- **402 Payment Required**: Quota exceeded
- **429 Too Many Requests**: Rate limit hit

---

## Rate Limiting

### Server-Side
Currently no rate limiting implemented. Consider adding:

```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=lambda: request.remote_addr,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/upload', methods=['POST'])
@limiter.limit("10 per minute")
def upload_files():
    # ...
```

### Client-Side
Video frames throttled to 1 frame per 2 seconds:
```javascript
const FRAME_INTERVAL = 2000; // milliseconds
```

---

## Testing the API

### Using cURL

#### Test Upload Endpoint
```bash
curl -X POST http://localhost:5000/upload \
  -F "session_id=test_123" \
  -F "avatar_image=@path/to/image.jpg" \
  -F "voice_sample=@path/to/audio.mp3"
```

### Using Python

#### Test Socket.IO Connection
```python
import socketio

sio = socketio.Client()

@sio.on('connect')
def on_connect():
    print('Connected!')

@sio.on('ai_response')
def on_response(data):
    print('AI:', data['text'])

sio.connect('http://localhost:5000')
sio.emit('user_message', {
    'message': 'Hello!',
    'session_id': 'test_123'
})
```

---

## Best Practices

### 1. Error Handling
Always wrap API calls in try-catch:
```javascript
try {
    const response = await fetch('/upload', {...});
    const result = await response.json();
} catch (error) {
    console.error('Upload failed:', error);
    // Show user-friendly error
}
```

### 2. Session Management
Store session ID consistently:
```javascript
const sessionId = sessionStorage.getItem('sessionId') || generateSessionId();
sessionStorage.setItem('sessionId', sessionId);
```

### 3. Resource Cleanup
Always clean up resources:
```javascript
function cleanup() {
    if (localStream) {
        localStream.getTracks().forEach(track => track.stop());
    }
    if (recognition) {
        recognition.stop();
    }
    socket.disconnect();
}
```

---

This API reference provides all the information needed to integrate with and extend the Memory AI Assistant!

// Generate unique session ID
const sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);

// File upload handling
let avatarFile = null;
let voiceFile = null;
let cameraStream = null;
let mediaRecorder = null;
let audioChunks = [];
let recordingStartTime = null;
let recordingInterval = null;

const avatarInput = document.getElementById('avatarInput');
const voiceInput = document.getElementById('voiceInput');
const avatarUploadBox = document.getElementById('avatarUploadBox');
const voiceUploadBox = document.getElementById('voiceUploadBox');
const btnStartSession = document.getElementById('btnStartSession');
const skipLink = document.getElementById('skipLink');
const welcomeScreen = document.getElementById('welcomeScreen');

// Camera modal elements
const cameraModal = document.getElementById('cameraModal');
const cameraPreview = document.getElementById('cameraPreview');
const captureCanvas = document.getElementById('captureCanvas');
const captureImageBtn = document.getElementById('captureImageBtn');
const takePictureBtn = document.getElementById('takePictureBtn');
const closeCameraBtn = document.getElementById('closeCameraBtn');

// Audio modal elements
const audioModal = document.getElementById('audioModal');
const recordAudioBtn = document.getElementById('recordAudioBtn');
const startRecordingBtn = document.getElementById('startRecordingBtn');
const stopRecordingBtn = document.getElementById('stopRecordingBtn');
const closeAudioBtn = document.getElementById('closeAudioBtn');
const recordingStatus = document.getElementById('recordingStatus');
const recordingTimer = document.getElementById('recordingTimer');

avatarInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        avatarFile = e.target.files[0];
        avatarUploadBox.classList.add('file-selected');
        avatarUploadBox.querySelector('.upload-text').textContent = '✓ ' + avatarFile.name;
    }
});

voiceInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        voiceFile = e.target.files[0];
        voiceUploadBox.classList.add('file-selected');
        voiceUploadBox.querySelector('.upload-text').textContent = '✓ ' + voiceFile.name;
    }
});

// Camera capture functionality
captureImageBtn.addEventListener('click', async () => {
    try {
        cameraModal.style.display = 'flex';
        cameraStream = await navigator.mediaDevices.getUserMedia({ video: true });
        cameraPreview.srcObject = cameraStream;
    } catch (error) {
        console.error('Error accessing camera:', error);
        alert('Could not access camera. Please check permissions.');
        cameraModal.style.display = 'none';
    }
});

takePictureBtn.addEventListener('click', () => {
    const context = captureCanvas.getContext('2d');
    captureCanvas.width = cameraPreview.videoWidth;
    captureCanvas.height = cameraPreview.videoHeight;
    context.drawImage(cameraPreview, 0, 0);
    
    captureCanvas.toBlob((blob) => {
        avatarFile = new File([blob], 'captured_image.jpg', { type: 'image/jpeg' });
        avatarUploadBox.classList.add('file-selected');
        avatarUploadBox.querySelector('.upload-text').textContent = '✓ Captured Image';
        closeCameraModal();
    }, 'image/jpeg', 0.9);
});

closeCameraBtn.addEventListener('click', closeCameraModal);

function closeCameraModal() {
    if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
        cameraStream = null;
    }
    cameraModal.style.display = 'none';
}

// Audio recording functionality
recordAudioBtn.addEventListener('click', async () => {
    try {
        audioModal.style.display = 'flex';
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];
        
        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };
        
        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            voiceFile = new File([audioBlob], 'recorded_audio.webm', { type: 'audio/webm' });
            voiceUploadBox.classList.add('file-selected');
            voiceUploadBox.querySelector('.upload-text').textContent = '✓ Recorded Audio';
            stream.getTracks().forEach(track => track.stop());
        };
    } catch (error) {
        console.error('Error accessing microphone:', error);
        alert('Could not access microphone. Please check permissions.');
        audioModal.style.display = 'none';
    }
});

startRecordingBtn.addEventListener('click', () => {
    if (mediaRecorder && mediaRecorder.state === 'inactive') {
        audioChunks = [];
        mediaRecorder.start();
        startRecordingBtn.style.display = 'none';
        stopRecordingBtn.style.display = 'inline-block';
        recordingStatus.querySelector('span').textContent = 'Recording...';
        recordingStatus.classList.add('recording');
        
        // Start timer
        recordingStartTime = Date.now();
        recordingInterval = setInterval(updateRecordingTimer, 1000);
    }
});

stopRecordingBtn.addEventListener('click', () => {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
        startRecordingBtn.style.display = 'inline-block';
        stopRecordingBtn.style.display = 'none';
        recordingStatus.querySelector('span').textContent = 'Recording saved!';
        recordingStatus.classList.remove('recording');
        
        // Stop timer
        clearInterval(recordingInterval);
        recordingTimer.textContent = '00:00';
        
        setTimeout(() => {
            closeAudioModal();
        }, 1000);
    }
});

closeAudioBtn.addEventListener('click', closeAudioModal);

function closeAudioModal() {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
    }
    if (mediaRecorder && mediaRecorder.stream) {
        mediaRecorder.stream.getTracks().forEach(track => track.stop());
    }
    audioModal.style.display = 'none';
    startRecordingBtn.style.display = 'inline-block';
    stopRecordingBtn.style.display = 'none';
    recordingStatus.querySelector('span').textContent = 'Ready to record';
    recordingStatus.classList.remove('recording');
    clearInterval(recordingInterval);
    recordingTimer.textContent = '00:00';
}

function updateRecordingTimer() {
    const elapsed = Math.floor((Date.now() - recordingStartTime) / 1000);
    const minutes = Math.floor(elapsed / 60).toString().padStart(2, '0');
    const seconds = (elapsed % 60).toString().padStart(2, '0');
    recordingTimer.textContent = `${minutes}:${seconds}`;
}

// Upload files to server
async function uploadFiles() {
    if (!avatarFile && !voiceFile) {
        return true;
    }
    
    const formData = new FormData();
    formData.append('session_id', sessionId);
    
    if (avatarFile) {
        formData.append('avatar_image', avatarFile);
    }
    
    if (voiceFile) {
        formData.append('voice_sample', voiceFile);
    }
    
    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            console.log('✓ Files uploaded successfully');
            return true;
        } else {
            console.error('Upload failed:', result.error);
            alert('Upload failed: ' + result.error);
            return false;
        }
    } catch (error) {
        console.error('Upload error:', error);
        alert('Upload error: ' + error.message);
        return false;
    }
}

// Start session
btnStartSession.addEventListener('click', async () => {
    btnStartSession.textContent = 'Uploading...';
    btnStartSession.disabled = true;
    
    const success = await uploadFiles();
    
    if (success) {
        welcomeScreen.classList.add('hidden');
        setTimeout(() => {
            welcomeScreen.style.display = 'none';
        }, 500);
    } else {
        btnStartSession.textContent = 'Start Session';
        btnStartSession.disabled = false;
    }
});

// Skip upload
skipLink.addEventListener('click', (e) => {
    e.preventDefault();
    welcomeScreen.classList.add('hidden');
    setTimeout(() => {
        welcomeScreen.style.display = 'none';
    }, 500);
});

// Connect to Socket.IO server
const socket = io({
    transports: ['polling'],
    upgrade: false,
    reconnection: true,
    reconnectionDelay: 2000,
    reconnectionAttempts: 5,
    timeout: 30000
});

// DOM elements
const localVideo = document.getElementById('localVideo');
const aiVideo = document.getElementById('aiVideo');
const startButton = document.getElementById('startButton');
const stopButton = document.getElementById('stopButton');
const micButton = document.getElementById('mic-button');
const chatMessages = document.getElementById('chat-messages');
const statusDiv = document.getElementById('status');
const chatPanel = document.getElementById('chatPanel');
const navChatbot = document.getElementById('nav-chatbot');
const closeChat = document.getElementById('closeChat');

// Speech recognition
let recognition = null;
let isMicActive = false;
let isListening = false;

// Audio context and elements
let audioContext;
let audioQueue = [];
let isPlaying = false;

// Stream and canvas setup
let localStream;
const canvas = document.createElement('canvas');
const ctx = canvas.getContext('2d');
const aiCtx = aiVideo.getContext('2d');
let lastFrameTime = 0;
const FRAME_INTERVAL = 2000;

// Set canvas dimensions
function setupCanvas() {
    const width = 320;
    const height = 240;
    
    canvas.width = width;
    canvas.height = height;
    aiVideo.width = width;
    aiVideo.height = height;
}

// Initialize audio context
function initAudio() {
    audioContext = new (window.AudioContext || window.webkitAudioContext)();
}

// Play audio from base64 data
async function playAudio(base64Data) {
    if (!audioContext) initAudio();
    
    try {
        audioQueue.push(base64Data);
        
        if (isPlaying) return;
        
        while (audioQueue.length > 0) {
            isPlaying = true;
            const audioData = audioQueue[0];
            
            const binaryString = atob(audioData);
            const len = binaryString.length;
            const bytes = new Uint8Array(len);
            for (let i = 0; i < len; i++) {
                bytes[i] = binaryString.charCodeAt(i);
            }
            
            const audioBuffer = await audioContext.decodeAudioData(bytes.buffer);
            
            const source = audioContext.createBufferSource();
            source.buffer = audioBuffer;
            source.connect(audioContext.destination);
            
            source.start();
            
            await new Promise(resolve => {
                source.onended = resolve;
            });
            
            audioQueue.shift();
        }
        
        isPlaying = false;
    } catch (error) {
        console.error('Error playing audio:', error);
        isPlaying = false;
    }
}

// Play avatar video from URL
function playAvatarVideo(videoUrl) {
    try {
        console.log('🎬 Playing avatar video in corner:', videoUrl);
        
        // Get the AI video corner container
        const aiVideoCorner = document.querySelector('.ai-video-corner');
        const aiCanvas = document.getElementById('aiVideo');
        
        if (!aiVideoCorner || !aiCanvas) {
            console.error('❌ AI video corner elements not found');
            return;
        }
        
        // Remove any existing avatar video
        const existingVideo = aiVideoCorner.querySelector('video');
        if (existingVideo) {
            existingVideo.remove();
        }
        
        // Create a video element for the avatar
        const avatarVideoElement = document.createElement('video');
        avatarVideoElement.src = videoUrl;
        // Remove crossOrigin to avoid CORS issues
        avatarVideoElement.autoplay = true;
        avatarVideoElement.playsInline = true; // Important for mobile
        avatarVideoElement.muted = false;
        avatarVideoElement.controls = false;
        avatarVideoElement.style.width = '100%';
        avatarVideoElement.style.height = '100%';
        avatarVideoElement.style.objectFit = 'cover';
        avatarVideoElement.style.position = 'absolute';
        avatarVideoElement.style.top = '0';
        avatarVideoElement.style.left = '0';
        avatarVideoElement.style.borderRadius = '20px';
        avatarVideoElement.style.zIndex = '10';
        
        // Hide the canvas and show the video
        aiCanvas.style.display = 'none';
        
        // Add avatar video to the corner container
        aiVideoCorner.appendChild(avatarVideoElement);
        
        // Try to play the video
        const playPromise = avatarVideoElement.play();
        if (playPromise !== undefined) {
            playPromise
                .then(() => {
                    console.log('✅ Avatar video playing successfully');
                })
                .catch(error => {
                    console.error('❌ Error auto-playing video:', error);
                    console.log('ℹ️ Trying with muted...');
                    avatarVideoElement.muted = true;
                    avatarVideoElement.play().catch(e => {
                        console.error('❌ Still failed to play:', e);
                    });
                });
        }
        
        // When avatar video ends, show canvas again
        avatarVideoElement.onended = () => {
            console.log('✅ Avatar video ended');
            avatarVideoElement.remove();
            aiCanvas.style.display = 'block';
        };
        
        // Handle video loading
        avatarVideoElement.onloadeddata = () => {
            console.log('✅ Avatar video loaded successfully');
        };
        
        // Handle video errors
        avatarVideoElement.onerror = (error) => {
            console.error('❌ Error loading avatar video:', error);
            console.error('   Video URL:', videoUrl);
            avatarVideoElement.remove();
            aiCanvas.style.display = 'block';
        };
        
        console.log('✅ Avatar video element created');
    } catch (error) {
        console.error('❌ Error playing avatar video:', error);
        console.error('   Stack:', error.stack);
    }
}

// Start video stream
async function startVideo() {
    try {
        localStream = await navigator.mediaDevices.getUserMedia({
            video: true,
            audio: true
        });
        
        localVideo.srcObject = localStream;
        startButton.disabled = true;
        stopButton.disabled = false;
        micButton.disabled = false;
        
        initSpeechRecognition();
        sendVideoFrame();
        initAudio();
        
        statusDiv.querySelector('span').textContent = 'Connected';
        statusDiv.classList.add('connected');
        
        socket.emit('call_started');
        
    } catch (error) {
        console.error('Error accessing media devices:', error);
        alert('Could not access camera or microphone. Please check permissions.');
    }
}

// Stop video stream
function stopVideo() {
    if (localStream) {
        localStream.getTracks().forEach(track => track.stop());
        localVideo.srcObject = null;
    }
    
    if (isMicActive && recognition) {
        recognition.stop();
        isMicActive = false;
    }
    
    startButton.disabled = false;
    stopButton.disabled = true;
    micButton.disabled = true;
    statusDiv.querySelector('span').textContent = 'Disconnected';
    statusDiv.classList.remove('connected', 'listening');
    
    socket.emit('call_ended');
}

// Send video frame to server
function sendVideoFrame() {
    if (!localStream) return;
    
    const currentTime = Date.now();
    
    if (currentTime - lastFrameTime >= FRAME_INTERVAL) {
        ctx.drawImage(localVideo, 0, 0, canvas.width, canvas.height);
        const imageData = canvas.toDataURL('image/jpeg', 0.5);
        socket.emit('video_frame', imageData);
        lastFrameTime = currentTime;
    }
    
    requestAnimationFrame(sendVideoFrame);
}

// Send message to server
function sendMessage(message) {
    if (!message || !message.trim()) return;
    
    console.log('📤 Sending message:', message);
    addMessage('user', message);
    socket.emit('user_message', { message, session_id: sessionId });
}

// Add message to chat
function addMessage(sender, text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    messageDiv.textContent = text;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Initialize speech recognition
function initSpeechRecognition() {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = false;
        recognition.lang = 'en-US';
        
        recognition.onstart = () => {
            isListening = true;
            statusDiv.querySelector('span').textContent = '🎤 Listening...';
            statusDiv.classList.add('listening');
        };
        
        recognition.onresult = (event) => {
            const lastResult = event.results[event.results.length - 1];
            if (lastResult.isFinal) {
                const transcript = lastResult[0].transcript.trim();
                console.log('Heard:', transcript);
                sendMessage(transcript);
            }
        };
        
        recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            if (event.error !== 'no-speech') {
                statusDiv.querySelector('span').textContent = '❌ Error: ' + event.error;
                statusDiv.classList.remove('listening');
            }
        };
        
        recognition.onend = () => {
            isListening = false;
            if (isMicActive) {
                setTimeout(() => {
                    if (isMicActive) {
                        recognition.start();
                    }
                }, 100);
            } else {
                statusDiv.querySelector('span').textContent = 'Connected';
                statusDiv.classList.remove('listening');
            }
        };
    } else {
        console.warn('Speech recognition not supported');
        micButton.style.display = 'none';
    }
}

// Toggle microphone
function toggleMic() {
    if (!recognition) return;
    
    isMicActive = !isMicActive;
    
    if (isMicActive) {
        micButton.classList.add('active');
        recognition.start();
    } else {
        micButton.classList.remove('active');
        recognition.stop();
        statusDiv.querySelector('span').textContent = 'Connected';
        statusDiv.classList.remove('listening');
    }
}

// Event listeners
startButton.addEventListener('click', startVideo);
stopButton.addEventListener('click', stopVideo);
micButton.addEventListener('click', toggleMic);

// Chat panel toggle
navChatbot.addEventListener('click', () => {
    chatPanel.classList.add('open');
    navChatbot.classList.add('active');
});

closeChat.addEventListener('click', () => {
    chatPanel.classList.remove('open');
    navChatbot.classList.remove('active');
});

// Socket.IO event listeners
socket.on('connect', () => {
    console.log('✅ Connected to server');
    console.log('Socket ID:', socket.id);
});

socket.on('connect_error', (error) => {
    console.error('❌ Connection error:', error);
    statusDiv.querySelector('span').textContent = 'Connection Error';
});

socket.on('disconnect', (reason) => {
    console.log('❌ Disconnected:', reason);
    statusDiv.querySelector('span').textContent = 'Disconnected';
});

socket.on('ai_response', (data) => {
    console.log('✅ Received AI response from server');
    console.log('   Response data:', {
        text: data.text ? data.text.substring(0, 50) + '...' : 'none',
        hasAudio: !!data.audio,
        avatarVideo: data.avatar_video || 'none'
    });
    
    addMessage('ai', data.text);
    
    // If we have an avatar video, display it
    if (data.avatar_video) {
        console.log('🎬 Avatar video URL received, calling playAvatarVideo()');
        playAvatarVideo(data.avatar_video);
    } else {
        console.log('⚠️ No avatar video in response');
        if (data.audio) {
            console.log('🔊 Playing audio only');
            playAudio(data.audio);
        }
    }
});

socket.on('video_processed', (data) => {
    const img = new Image();
    img.onload = () => {
        aiCtx.drawImage(img, 0, 0, aiVideo.width, aiVideo.height);
    };
    img.src = data.frame;
});

socket.on('error', (data) => {
    console.error('Server error:', data.message);
    addMessage('ai', `Error: ${data.message}`);
});

// Initialize the app
setupCanvas();

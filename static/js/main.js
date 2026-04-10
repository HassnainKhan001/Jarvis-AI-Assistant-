const orb = document.getElementById('orb');
const wave = document.getElementById('wave');
const voiceBtn = document.getElementById('voice-btn');
const sendBtn = document.getElementById('send-btn');
const userInput = document.getElementById('user-input');
const chatHistory = document.getElementById('chat-history');
let isProcessing = false;
let recognition = null;
let checkSpeakingInterval = null;

// Settings Elements
const settingsBtn = document.getElementById('settings-btn');
const settingsModal = document.getElementById('settings-modal');
const closeModalBtn = document.querySelector('.close-modal');
const alwaysOnToggle = document.getElementById('always-on-toggle');
const voiceToggle = document.getElementById('voice-toggle');
const desktopModeToggle = document.getElementById('desktop-mode-toggle');
const listenerStatus = document.querySelector('.module-list li:nth-child(2) .status-dot');

// Boot Sequence Logic
const bootScreen = document.getElementById('boot-screen');
const biometricScanner = document.getElementById('biometric-scanner');
const scanPercentage = document.getElementById('scan-percentage');
const scanProgress = document.getElementById('scan-progress');
const mainUi = document.getElementById('main-ui');
const logContentLeft = document.getElementById('log-content-left');
const logContentRight = document.getElementById('log-content-right');

// Authentication Trigger (Required for Voice to work in browsers)
const initBtn = document.getElementById('init-btn');
const systemStatus = document.getElementById('system-status');

initBtn.addEventListener('click', () => {
    initBtn.style.display = 'none';
    systemStatus.style.display = 'none';
    
    biometricScanner.style.display = 'flex';
    startBiometricScan();
});

function startBiometricScan() {
    let progress = 0;
    const duration = 3500;
    const intervalTime = 40;
    const increment = 100 / (duration / intervalTime);

    const logLeft = document.getElementById('log-content-left');
    const logRight = document.getElementById('log-content-right');
    const hexRows = [document.getElementById('data-hex-1'), document.getElementById('data-hex-2')];

    // Announce start of detection
    speak("Face is detecting");

    // Dual-sidebar log generation
    const updateLogs = setInterval(() => {
        hexRows.forEach(row => {
            if (row) row.innerText = '0x' + Math.floor(Math.random() * 0xFFFF).toString(16).toUpperCase().padStart(4, '0');
        });
        
        const logs = [
            "> ANALYZING...", "> RETINAL_MATCH", "> BYPASSING...", "> UPLOADING...", 
            "> SYNC_CORE", "> NEURAL_LINK", "> AUTH_REQ", "> HEX_PARSING"
        ];
        
        if (Math.random() > 0.6) {
            const pL = document.createElement('div');
            pL.innerText = logs[Math.floor(Math.random() * logs.length)];
            logLeft.appendChild(pL);
            if (logLeft.children.length > 20) logLeft.removeChild(logLeft.firstChild);

            const pR = document.createElement('div');
            pR.innerText = logs[Math.floor(Math.random() * logs.length)];
            logRight.appendChild(pR);
            if (logRight.children.length > 20) logRight.removeChild(logRight.firstChild);
        }
    }, 100);

    const scanInterval = setInterval(() => {
        progress += increment;
        if (progress >= 100) {
            progress = 100;
            clearInterval(scanInterval);
            clearInterval(updateLogs);
            completeScan();
        }
        scanPercentage.innerText = Math.floor(progress);
        scanProgress.style.width = progress + '%';
    }, intervalTime);

    function completeScan() {
        biometricScanner.classList.add('authorized');
        const statusMain = document.querySelector('.status-main');
        if (statusMain) {
            statusMain.innerText = 'IDENTITY VERIFIED';
            statusMain.style.color = '#00ff88';
        }
        
        speak("Face detected. Hello Hasnain.");

        setTimeout(() => {
            bootScreen.style.opacity = '0';
            setTimeout(() => {
                bootScreen.style.display = 'none';
                mainUi.style.display = 'flex';
                mainUi.classList.add('animate-in');
                document.getElementById('user-input').focus();
            }, 600);
        }, 800);
    }
}

// Speech Recognition Setup
window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let isAlwaysListening = false;
let isVoiceEnabled = true;

function restartRecognition() {
    if (checkSpeakingInterval) clearInterval(checkSpeakingInterval);
    
    if (!isAlwaysListening || !recognition) return;

    // Small delay to let the audio device settle
    setTimeout(() => {
        if (!window.speechSynthesis.speaking) {
            try { 
                recognition.stop(); // Ensure it's fully stopped
                setTimeout(() => recognition.start(), 200); 
            } catch(e) {
                try { recognition.start(); } catch(e2) {}
            }
        } else {
            console.log("System is speaking, waiting to restart recognition...");
            checkSpeakingInterval = setInterval(() => {
                if (!window.speechSynthesis.speaking) {
                    clearInterval(checkSpeakingInterval);
                    try { 
                        recognition.stop();
                        setTimeout(() => recognition.start(), 200);
                    } catch(e) {
                        try { recognition.start(); } catch(e2) {}
                    }
                }
            }, 500);
        }
    }, 400);
}

// Load Settings
function loadSettings() {
    const alwaysOn = localStorage.getItem('jarvis_always_on') === 'true';
    const voiceOn = localStorage.getItem('jarvis_voice_enabled') !== 'false';
    
    alwaysOnToggle.checked = alwaysOn;
    voiceToggle.checked = voiceOn;
    isAlwaysListening = alwaysOn;
    isVoiceEnabled = voiceOn;
    
    updateStatusIndicators();
    loadListenerStatus();
}

async function loadListenerStatus() {
    try {
        const response = await fetch('/api/listener/toggle');
        const data = await response.json();
        if (data.is_running) {
            desktopModeToggle.checked = true;
            updateStatusIndicators();
        }
    } catch (e) {}
}

function updateStatusIndicators() {
    const isDesktopActive = desktopModeToggle ? desktopModeToggle.checked : false;
    
    if (isAlwaysListening || isDesktopActive) {
        listenerStatus.className = 'status-dot green';
        if (isAlwaysListening && recognition) {
            restartRecognition();
        }
    } else {
        listenerStatus.className = 'status-dot'; // inactive
    }
}

// Modal Listeners
settingsBtn.addEventListener('click', () => settingsModal.classList.add('active'));
closeModalBtn.addEventListener('click', () => settingsModal.classList.remove('active'));
window.addEventListener('click', (e) => {
    if (e.target === settingsModal) settingsModal.classList.remove('active');
});

// Toggle Listeners
alwaysOnToggle.addEventListener('change', (e) => {
    isAlwaysListening = e.target.checked;
    localStorage.setItem('jarvis_always_on', isAlwaysListening);
    updateStatusIndicators();
    if (isAlwaysListening) {
        appendMessage("Background listening activated, sir. You can call me anytime.", 'bot-msg');
        speak("Background listening activated, sir.");
    }
});

voiceToggle.addEventListener('change', (e) => {
    isVoiceEnabled = e.target.checked;
    localStorage.setItem('jarvis_voice_enabled', isVoiceEnabled);
});

desktopModeToggle.addEventListener('change', async (e) => {
    const enable = e.target.checked;
    updateStatusIndicators();
    
    try {
        const response = await fetch('/api/listener/toggle', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ enable })
        });
        const data = await response.json();
        
        if (data.status === 'started' || data.status === 'already_running') {
            appendMessage("True Desktop Background Mode activated, sir.", 'bot-msg');
            speak("Desktop background mode activated.");
        } else if (data.status === 'stopped') {
            appendMessage("Desktop background mode deactivated.", 'bot-msg');
        }
    } catch (err) {
        appendMessage("⚠️ Error communicating with the background listener.", 'bot-msg');
        e.target.checked = !enable; // revert
        updateStatusIndicators();
    }
});

if (window.SpeechRecognition) {
    recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.interimResults = false;

    recognition.onstart = () => {
        orb.style.animation = "pulsate 0.5s infinite alternate";
        wave.classList.add('active');
        voiceBtn.style.background = '#ff4444';
    };

    recognition.onresult = (event) => {
        const transcript = event.results[event.results.length - 1][0].transcript.trim().toLowerCase();
        
        if (isAlwaysListening) {
            if (transcript.includes('jarvis')) {
                const parts = transcript.split('jarvis');
                const cmd = parts[parts.length - 1].trim();
                
                if (cmd) {
                    userInput.value = cmd;
                    handleSend();
                } else {
                    speak("Yes, sir?");
                }
            }
        } else {
            userInput.value = transcript;
            handleSend();
        }
    };

    recognition.onend = () => {
        orb.style.animation = "pulsate 2s infinite ease-in-out";
        wave.classList.remove('active');
        voiceBtn.style.background = '';
        if (isAlwaysListening) restartRecognition();
    };

    recognition.onerror = (e) => {
        console.error("Speech Recognition Error Type:", e.error);
        orb.style.animation = "pulsate 2s infinite ease-in-out";
        wave.classList.remove('active');
        voiceBtn.style.background = '';
        
        if (isAlwaysListening && (e.error !== 'not-allowed' && e.error !== 'service-not-allowed')) {
            console.log("Attempting recognition restart after error:", e.error);
            setTimeout(() => {
                if (isAlwaysListening) restartRecognition();
            }, 2000);
        } else if (e.error === 'not-allowed') {
            appendMessage("⚠️ Microphone permission denied. Please allow microphone access in your browser.", 'bot-msg');
            isAlwaysListening = false;
            updateStatusIndicators();
        }
    };
}

voiceBtn.addEventListener('click', () => {
    if (recognition) {
        try { recognition.start(); } catch(e) {}
    } else {
        appendMessage('Voice recognition is not supported in this browser. Please type your message instead.', 'bot-msg');
    }
});

sendBtn.addEventListener('click', handleSend);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleSend();
});

async function handleSend() {
    const text = userInput.value.trim();
    if (!text || isProcessing) return;

    isProcessing = true;
    sendBtn.disabled = true;

    appendMessage(text, 'user-msg');
    userInput.value = '';

    const thinkingEl = document.createElement('p');
    thinkingEl.className = 'bot-msg';
    thinkingEl.innerHTML = '⚡ Jarvis is thinking<span class="thinking-dots"></span>';
    thinkingEl.id = 'thinking';
    chatHistory.appendChild(thinkingEl);
    chatHistory.scrollTop = chatHistory.scrollHeight;

    orb.style.animation = "pulsate 0.6s infinite alternate";

    try {
        const response = await fetch('/api/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt: text }),
        });

        const data = await response.json();
        const thinkingMsg = document.getElementById('thinking');
        if (thinkingMsg) thinkingMsg.remove();

        if (data.response) {
            appendMessage(data.response, 'bot-msg');
            speak(data.response);
        } else if (data.error) {
            appendMessage("⚠️ " + data.error, 'bot-msg');
        }
    } catch (err) {
        console.error("API Error:", err);
        const thinkingMsg = document.getElementById('thinking');
        if (thinkingMsg) thinkingMsg.remove();
        appendMessage("⚠️ Connection error. Is the server running?", 'bot-msg');
    } finally {
        orb.style.animation = "pulsate 2s infinite ease-in-out";
        isProcessing = false;
        sendBtn.disabled = false;
        userInput.focus();
    }
}

function appendMessage(text, className) {
    const p = document.createElement('p');
    p.innerText = text;
    p.className = className;
    chatHistory.appendChild(p);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

function speak(text) {
    if (window.speechSynthesis && isVoiceEnabled) {
        const cleanText = text.replace(/Jarvis:/g, '').replace(/⚡|⚠️/g, '');
        const utterance = new SpeechSynthesisUtterance(cleanText);
        utterance.rate = 1.0;
        utterance.pitch = 0.9;
        window.speechSynthesis.speak(utterance);
    }
}

userInput.focus();
loadSettings();

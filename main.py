import os
import edge_tts
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, Response
from pydantic import BaseModel
from groq import Groq

load_dotenv()
groq_api_key = os.environ.get("GROQ_API_KEY")

app = FastAPI()

client = Groq(
    api_key=groq_api_key,
    timeout=30.0,
    max_retries=2
)

LIBRARY_KNOWLEDGE_BASE = """
[YOUTH LIBRARY KHAIRA KHURD]
Management & In-charge: Strictly Gram Panchayat Khaira Khurd. Kisi vyakti ka farzi naam mat lo.
Timings: Daily 7:00 AM to 10:00 PM (All 7 Days Open)
Monthly Fee: ₹300 only
Facilities: High-speed Wi-Fi, AC, RO purified water, individual charging slots on desks, comfortable study chairs, washroom, 24/7 CCTV surveillance.
Rules: Strict silence maintain karni hai, phones compulsory silent mode par, desk par discussion bilkul allow nahi hai.
Admission: Reception par direct visit karke ID proof ke sath admission ho jata hai.
"""

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[ChatMessage] 
    
@app.get("/manifest.json")
async def get_manifest():
    return {
        "name": "Youth Library Khaira Khurd",
        "short_name": "Library Khaira AI",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#fcfbf9",
        "theme_color": "#fcfbf9",
        "icons": [
            {
                "src": "https://raw.githubusercontent.com/kuldeepguleria/khairalibrary/main/app-icon.png",
                "sizes": "500x500",
                "type": "image/png"
            }
        ]
    }

@app.get("/tts")
async def text_to_speech(text: str):
    communicate = edge_tts.Communicate(text, "hi-IN-SwaraNeural")
    audio_data = bytearray()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data.extend(chunk["data"])
    return Response(content=bytes(audio_data), media_type="audio/mpeg")

@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <meta name="theme-color" content="#fcfbf9">
        <meta name="mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="default">
        <link rel="manifest" href="/manifest.json">
        <link rel="icon" type="image/png" href="https://raw.githubusercontent.com/kuldeepguleria/khairalibrary/main/app-icon.png">
        <link rel="apple-touch-icon" href="https://raw.githubusercontent.com/kuldeepguleria/khairalibrary/main/app-icon.png">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&family=Plus+Jakarta+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <title>Library Khaira AI</title>
        <style>
            :root {
                --bg: #fcfbf9;
                --surface: #f7f5f0;
                --text-primary: #171717;
                --text-secondary: #74726d;
                --gold-accent: #c5a059;
                --gold-light: #eedcb3;
                --gold-net: rgba(197, 160, 89, 0.22);
                --gold-border: rgba(197, 160, 89, 0.45);
            }

            * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
            body { 
                background: #ebe7df; 
                display: flex; 
                justify-content: center; 
                height: 100dvh; 
                margin: 0; 
                padding: 0; 
                overflow: hidden; 
            }
            
            /* Container with subtle micro woven texture */
            .chat-container {
                width: 100%;
                max-width: 480px;
                height: 100dvh;
                display: flex;
                flex-direction: column;
                background-color: var(--bg);
                background-image: 
                    radial-gradient(var(--gold-net) 0.75px, transparent 0.75px),
                    radial-gradient(rgba(23, 23, 23, 0.03) 0.75px, transparent 0.75px);
                background-size: 16px 16px, 8px 8px;
                background-position: 0 0, 4px 4px;
                position: relative;
                overflow: hidden;
                border-left: 1px solid rgba(197, 160, 89, 0.15);
                border-right: 1px solid rgba(197, 160, 89, 0.15);
            }

            /* 3D Background Canvas Layer */
            #webgl-canvas {
                position: absolute;
                inset: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
                z-index: 1;
                opacity: 0.55;
            }

            /* 40% Transparent Fluid Satin Wave Header Strip */
            .header {
                background: 
                    radial-gradient(circle at 85% -20%, rgba(238, 220, 179, 0.60) 0%, transparent 60%),
                    radial-gradient(circle at 15% 120%, rgba(197, 160, 89, 0.55) 0%, transparent 55%),
                    linear-gradient(105deg, 
                        rgba(255, 255, 255, 0.65) 0%, 
                        rgba(247, 243, 233, 0.58) 35%, 
                        rgba(225, 205, 165, 0.60) 70%, 
                        rgba(255, 255, 255, 0.62) 100%
                    ) !important;
                backdrop-filter: blur(6px);
                -webkit-backdrop-filter: blur(6px);
                color: var(--text-primary);
                padding: 10px 16px;
                display: flex;
                align-items: center;
                gap: 12px;
                border-bottom: 1.2px solid rgba(197, 160, 89, 0.45);
                box-shadow: 
                    0 1px 0 rgba(255, 255, 255, 0.7) inset,
                    0 6px 20px rgba(197, 160, 89, 0.08);
                position: sticky;
                top: 0;
                z-index: 100;
            }

            .header img {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                object-fit: cover;
                border: 1.5px solid var(--gold-accent);
                box-shadow: 0 2px 8px rgba(197, 160, 89, 0.3);
            }

            .header-info h2 { 
                font-family: 'Cormorant Garamond', serif;
                font-size: 19px; 
                font-weight: 600; 
                color: var(--text-primary);
                letter-spacing: 0.02em;
            }
            .header-info p { 
                font-size: 10.5px; 
                color: var(--text-secondary); 
                letter-spacing: 0.04em;
            }

            .messages, #chatBox {
                flex: 1;
                min-height: 0;
                padding: 16px 14px;
                overflow-y: auto;
                display: flex;
                flex-direction: column;
                gap: 12px;
                background: transparent;
                position: relative;
                z-index: 2;
            }

            /* Slim Aesthetic Message Bubbles with Golden Net Texture */
            .msg {
                max-width: 84%;
                padding: 6px 14px;
                font-size: 13.5px;
                line-height: 1.45;
                word-wrap: break-word;
                letter-spacing: 0.01em;
                position: relative;
                backdrop-filter: blur(8px);
                -webkit-backdrop-filter: blur(8px);
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
            }

            /* Bot Message: Slim Left Bubble with Left Arrow Pointer */
            .bot {
                align-self: flex-start;
                margin-left: 10px;
                border-radius: 2px 8px 8px 8px;
                border: 1px solid var(--gold-border);
                color: var(--text-primary);
                background: 
                    linear-gradient(rgba(255, 255, 255, 0.72), rgba(250, 248, 244, 0.65)),
                    repeating-linear-gradient(45deg, transparent, transparent 5px, rgba(197, 160, 89, 0.16) 5px, rgba(197, 160, 89, 0.16) 6px),
                    repeating-linear-gradient(-45deg, transparent, transparent 5px, rgba(197, 160, 89, 0.16) 5px, rgba(197, 160, 89, 0.16) 6px);
            }

            .bot::before {
                content: "";
                position: absolute;
                left: -9px;
                top: 0px;
                width: 0;
                height: 0;
                border-top: 0px solid transparent;
                border-right: 9px solid var(--gold-border);
                border-bottom: 9px solid transparent;
            }
            .bot::after {
                content: "";
                position: absolute;
                left: -7.5px;
                top: 1px;
                width: 0;
                height: 0;
                border-top: 0px solid transparent;
                border-right: 8px solid #fdfcfa;
                border-bottom: 8px solid transparent;
            }

            /* User Message: Slim Horizontal Bar with Sharp Needle Tail */
            .user {
                align-self: flex-end;
                margin-right: 14px;
                border-radius: 6px 2px 6px 6px;
                border: 1.2px solid var(--gold-accent);
                color: var(--text-primary);
                background: 
                    linear-gradient(rgba(247, 240, 226, 0.75), rgba(242, 232, 212, 0.65)),
                    repeating-linear-gradient(45deg, transparent, transparent 5px, rgba(197, 160, 89, 0.22) 5px, rgba(197, 160, 89, 0.22) 6px),
                    repeating-linear-gradient(-45deg, transparent, transparent 5px, rgba(197, 160, 89, 0.22) 5px, rgba(197, 160, 89, 0.22) 6px);
            }

            /* User Sharp Horizontal Pointed Tail */
            .user::before {
                content: "";
                position: absolute;
                right: -13px;
                top: 3px;
                width: 0;
                height: 0;
                border-top: 4px solid transparent;
                border-left: 13px solid var(--gold-accent);
                border-bottom: 5px solid transparent;
            }
            .user::after {
                content: "";
                position: absolute;
                right: -11px;
                top: 4px;
                width: 0;
                height: 0;
                border-top: 3px solid transparent;
                border-left: 11px solid #f6eedc;
                border-bottom: 4px solid transparent;
            }

            .quick-chips { 
                margin-top: auto;
                display: flex; 
                gap: 8px; 
                overflow-x: auto; 
                padding: 10px 14px; 
                background: rgba(252, 251, 249, 0.88); 
                backdrop-filter: blur(10px);
                border-top: 1px solid var(--gold-border); 
                scrollbar-width: none; 
                position: relative;
                z-index: 2;
            }
            .quick-chips::-webkit-scrollbar { display: none; }
            .chip { 
                background: rgba(255, 255, 255, 0.85); 
                border: 1px solid var(--gold-border); 
                color: #8c6e2d; 
                padding: 6px 14px; 
                border-radius: 20px; 
                font-size: 12px; 
                font-weight: 500;
                white-space: nowrap; 
                cursor: pointer; 
                transition: all 0.2s ease;
            }
            .chip:active { 
                background: var(--gold-accent); 
                color: #ffffff; 
            }

            .input-area { 
                display: flex; 
                padding-top: 10px;
                padding-left: 12px;
                padding-right: 12px;
                padding-bottom: max(28px, calc(14px + env(safe-area-inset-bottom, 20px))) !important; 
                background: rgba(252, 251, 249, 0.95); 
                backdrop-filter: blur(12px);
                gap: 10px; 
                align-items: center; 
                border-top: 1px solid var(--gold-border);
                box-sizing: border-box;
                z-index: 999;
                position: relative;
            }

            input { 
                flex: 1; 
                padding: 10px 16px; 
                background: #ffffff; 
                border: 1px solid var(--gold-border); 
                border-radius: 24px; 
                outline: none; 
                font-size: 14px; 
                color: var(--text-primary); 
                transition: border-color 0.3s;
            }
            input:focus {
                border-color: var(--gold-accent);
                box-shadow: 0 0 0 2px rgba(197, 160, 89, 0.2);
            }
            input::placeholder { color: #a29e96; }

            /* Modern Studio Mic Button */
            .mic-btn-modern {
                background: #ffffff;
                border: 1px solid var(--gold-border);
                width: 40px;
                height: 40px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                color: var(--text-secondary);
                transition: all 0.3s ease;
                flex-shrink: 0;
            }
            .mic-btn-modern svg {
                width: 19px;
                height: 19px;
                fill: currentColor;
                transition: transform 0.2s;
            }
            .mic-btn-modern:hover {
                color: var(--gold-accent);
                border-color: var(--gold-accent);
            }

            /* Modern Pulsing Red Button when Active */
            .mic-btn-modern.recording {
                background: #ef4444;
                border-color: #ef4444;
                color: #ffffff;
                animation: micPulse 1.4s infinite cubic-bezier(0.4, 0, 0.2, 1);
            }
            @keyframes micPulse {
                0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.45); }
                70% { box-shadow: 0 0 0 12px rgba(239, 68, 68, 0); }
                100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
            }

            button.send-btn { 
                background: var(--text-primary); 
                color: #fcfbf9; 
                border: 1px solid var(--text-primary); 
                width: 40px; 
                height: 40px; 
                border-radius: 50%; 
                cursor: pointer; 
                display: flex; 
                align-items: center; 
                justify-content: center; 
                font-size: 15px; 
                flex-shrink: 0;
                transition: all 0.3s ease;
            }
            button.send-btn:hover {
                background: var(--gold-accent);
                border-color: var(--gold-accent);
            }

            .branding { 
                font-size: 10.5px; 
                text-align: center; 
                color: var(--text-secondary); 
                padding: 6px; 
                background: var(--bg); 
                letter-spacing: 0.08em; 
                text-transform: uppercase;
                border-top: 1px solid rgba(197, 160, 89, 0.15);
                position: relative;
                z-index: 2;
            }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <!-- 3D Three.js Moving Torus & Gold Cage Canvas -->
            <canvas id="webgl-canvas"></canvas>

            <div id="regModal" style="display:none; position:fixed; inset:0; background:rgba(23, 23, 23, 0.55); backdrop-filter:blur(8px); z-index:999; justify-content:center; align-items:center; padding:20px;">
                <div style="background:#ffffff; width:100%; max-width:360px; border-radius:18px; padding:24px; text-align:center; border:1px solid rgba(197, 160, 89, 0.35); box-shadow:0 20px 40px rgba(0,0,0,0.12);">
                    <h3 style="font-family:'Cormorant Garamond', serif; font-size:24px; color:#171717; margin-bottom:6px;">Youth Library Khaira Khurd</h3>
                    <p style="color:#74726d; font-size:12.5px; margin-bottom:18px;">Please enter your Name and Mobile number:</p>
                    <input id="regName" placeholder="Your Name" style="width:100%; padding:11px 14px; margin-bottom:10px; background:#f7f5f0; border:1px solid rgba(197, 160, 89, 0.25); border-radius:8px; color:#171717; outline:none;" />
                    <input id="regPhone" type="tel" maxlength="10" placeholder="10-digit Mobile Number" style="width:100%; padding:11px 14px; margin-bottom:18px; background:#f7f5f0; border:1px solid rgba(197, 160, 89, 0.25); border-radius:8px; color:#171717; outline:none;" />
                    <button onclick="submitReg()" style="width:100%; padding:12px; background:#171717; color:#fff; border:none; border-radius:30px; font-weight:600; font-size:12px; letter-spacing:0.12em; text-transform:uppercase; cursor:pointer;">Start Chat</button>
                </div>
            </div>

            <div class="header">
                <img src="https://raw.githubusercontent.com/kuldeepguleria/khairalibrary/main/Logo.png" alt="Logo">
                <div class="header-info">
                    <h2>Youth Library Study Mentor</h2>
                    <p>Designed & Developed by Kuldeep Guleria • Khaira Khurd</p>
                </div>
            </div>

            <div class="messages" id="chatBox">
                <div class="msg bot"><span>Hey friend! 👋 Youth Library Khaira Khurd me aapka swagat hai. Aaj padhai me kis subject ya topic me guidance chahiye?</span> <button onclick="speakText(this.previousElementSibling.innerText)" style="background:transparent; border:none; cursor:pointer; font-size:14px; margin-left:8px; vertical-align:middle; opacity:0.75;">🔊</button></div>
            </div>
            
            <div class="quick-chips">
                <span class="chip" onclick="sendQuick('Library fees, timings aur desk rules kya hain?')">Library Rules & Fees</span>
                <span class="chip" onclick="sendQuick('Pichhle kuch dino se padhai me bilkul focus nahi ban raha')">Focus Problem</span>
                <span class="chip" onclick="sendQuick('Mock test me marks nahi badh rahe, kya karu?')">Mock Test Marks</span>
                <span class="chip" onclick="sendQuick('Maths ya Reasoning ka 1 tricky quiz sawaal pucho')">Subject Quiz</span>
            </div>

            <div class="input-area">
                <button id="micBtn" class="mic-btn-modern" onclick="toggleMic()" title="Voice Typing">
                    <svg viewBox="0 0 24 24">
                        <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/>
                        <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/>
                    </svg>
                </button>
                <input type="text" id="userInput" placeholder="Apna reply ya sawal likhein..." onkeypress="if(event.key==='Enter') sendMessage()" />
                <button class="send-btn" onclick="sendMessage()">➤</button>
            </div>

            <div class="branding">Designed & Developed by Kuldeep Guleria • Khaira Khurd</div>
        </div>

        <script>
        // --- 3D Background Three.js Animation ---
        const canvas = document.getElementById('webgl-canvas');
        const container = document.querySelector('.chat-container');
        const scene = new THREE.Scene();

        const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
        camera.position.z = 6.2;

        const renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

        const group = new THREE.Group();
        scene.add(group);

        const torusGeo = new THREE.TorusGeometry(1.4, 0.3, 32, 100);
        const matteWhiteMat = new THREE.MeshStandardMaterial({
            color: 0xfdfdfd,
            roughness: 0.25,
            metalness: 0.1
        });
        const mainTorus = new THREE.Mesh(torusGeo, matteWhiteMat);
        group.add(mainTorus);

        const cageGeo = new THREE.IcosahedronGeometry(1.9, 1);
        const goldMat = new THREE.MeshStandardMaterial({
            color: 0xc5a059,
            roughness: 0.3,
            metalness: 0.85,
            wireframe: true
        });
        const goldCage = new THREE.Mesh(cageGeo, goldMat);
        group.add(goldCage);

        const ambientLight = new THREE.AmbientLight(0xffffff, 0.85);
        scene.add(ambientLight);

        const pointLight = new THREE.PointLight(0xfff7e6, 1.2, 50);
        pointLight.position.set(5, 5, 5);
        scene.add(pointLight);

        const backLight = new THREE.PointLight(0xc5a059, 0.8, 50);
        backLight.position.set(-5, -5, -2);
        scene.add(backLight);

        let mouseX = 0, mouseY = 0, targetX = 0, targetY = 0;
        window.addEventListener('mousemove', (e) => {
            mouseX = (e.clientX - window.innerWidth / 2) * 0.001;
            mouseY = (e.clientY - window.innerHeight / 2) * 0.001;
        });

        window.addEventListener('resize', () => {
            if (!container) return;
            camera.aspect = container.clientWidth / container.clientHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(container.clientWidth, container.clientHeight);
        });

        function animate() {
            requestAnimationFrame(animate);
            mainTorus.rotation.x += 0.004;
            mainTorus.rotation.y += 0.006;
            goldCage.rotation.x -= 0.002;
            goldCage.rotation.y -= 0.003;

            targetX += (mouseX - targetX) * 0.05;
            targetY += (mouseY - targetY) * 0.05;

            group.rotation.y = targetX * 1.5;
            group.rotation.x = targetY * 1.5;

            renderer.render(scene, camera);
        }
        animate();

        // --- MIC (Voice to Text) ---
        let recognition;
        let isRecording = false;
        let isVoiceQuery = false;

        const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (SpeechRec) {
            recognition = new SpeechRec();
            recognition.lang = 'hi-IN';
            recognition.continuous = false;
            recognition.interimResults = false;

            recognition.onresult = (event) => {
                const text = event.results[0][0].transcript;
                document.getElementById("userInput").value = text;
                sendMessage();
            };

            recognition.onend = () => {
                isRecording = false;
                const mBtn = document.getElementById("micBtn");
                if (mBtn) mBtn.classList.remove("recording");
            };
        }

        function toggleMic() {
            if (!recognition) {
                alert("Aapke browser/phone me voice support uplabdh nahi hai.");
                return;
            }
            const mBtn = document.getElementById("micBtn");
            if (isRecording) {
                try { recognition.stop(); } catch(e) {}
                isRecording = false;
                if (mBtn) mBtn.classList.remove("recording");
            } else {
                isVoiceQuery = true;
                isRecording = true;
                if (mBtn) mBtn.classList.add("recording");
                try {
                    recognition.start();
                } catch(e) {
                    isRecording = false;
                    if (mBtn) mBtn.classList.remove("recording");
                    alert("Mic error: " + e.message);
                }
            }
        }

        // --- EDGE-TTS Natural Swara Voice Player ---
        let currentAudio = null;
        async function speakText(text) {
            try {
                if (currentAudio) {
                    currentAudio.pause();
                    currentAudio = null;
                }
                let clean = text.replace(/[*_#]/g, "");
                currentAudio = new Audio("/tts?text=" + encodeURIComponent(clean));
                currentAudio.play();
            } catch(e) {
                console.log("Audio playback error:", e);
            }
        }

        const SHEET_URL = "https://script.google.com/macros/s/AKfycbzNk_9fOCmXT7cSluwNvA7Ii5IT5DJmBb-Ak5QY4agrN6AbjRrFQRkR0SA5xuvgFLdh/exec";

        let studentName = localStorage.getItem("yl_name") || "";
        let studentPhone = localStorage.getItem("yl_phone") || "";

        window.addEventListener("DOMContentLoaded", () => {
            const modal = document.getElementById("regModal");
            if (!studentName || !studentPhone) {
                modal.style.display = "flex";
            } else {
                modal.style.display = "none";
            }
        });

        function submitReg() {
            const n = document.getElementById("regName");
            const p = document.getElementById("regPhone");
            const name = n ? n.value.trim() : "";
            const phone = p ? p.value.trim().replace(/\\D/g, '') : "";

            if (!name) {
                alert("Kripya apna naam enter karein.");
                return;
            }
            if (phone.length !== 10) {
                alert("Kripya 10-digit mobile number enter karein.");
                return;
            }

            const modal = document.getElementById("regModal");
            if (modal) modal.style.display = "none";

            localStorage.setItem("yl_name", name);
            localStorage.setItem("yl_phone", phone);
            studentName = name;
            studentPhone = phone;

            try {
                fetch(SHEET_URL, {
                    method: "POST",
                    mode: "no-cors",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ name: name, phone: phone })
                });
            } catch (err) {
                console.log("Sheet sync error:", err);
            }
        }

        let conversationHistory = [];

        function cleanFormat(text) {
            return text.replace(/\\\\/g, "").replace(/\\*/g, "");
        }

        async function sendMessage() {
            const input = document.getElementById("userInput");
            const text = input.value.trim();
            if (!text) return;
            
            appendMsg(text, "user");
            conversationHistory.push({ role: "user", content: text });
            input.value = "";
            
            const chatBox = document.getElementById("chatBox");
            const loadingDiv = document.createElement("div");
            loadingDiv.className = "msg bot";
            loadingDiv.innerText = "Soch raha hoon... 💭";
            chatBox.appendChild(loadingDiv);
            chatBox.scrollTop = chatBox.scrollHeight;

            try {
                const res = await fetch("/chat", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ messages: conversationHistory })
                });
                const data = await res.json();
                const replyTxt = cleanFormat(data.reply || "Lagta hai network slow hai, kripya dobara try karein.");
                loadingDiv.innerHTML = '<span>' + replyTxt + '</span> <button onclick="speakText(this.previousElementSibling.innerText)" style="background:transparent; border:none; cursor:pointer; font-size:14px; margin-left:8px; vertical-align:middle; opacity:0.75;">🔊</button>';
                conversationHistory.push({ role: "assistant", content: data.reply });
                if (isVoiceQuery) {
                    speakText(replyTxt);
                    isVoiceQuery = false;
                }
            } catch(err) {
                loadingDiv.innerText = "Server se contact nahi ho pa raha hai.";
            }
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        function appendMsg(text, sender) {
            const chatBox = document.getElementById("chatBox");
            const div = document.createElement("div");
            div.className = "msg " + sender;
            const cleaned = cleanFormat(text);
            if (sender === "bot") {
                div.innerHTML = `<span>${cleaned}</span> <button onclick="speakText(this.previousElementSibling.innerText)" style="background:transparent; border:none; cursor:pointer; font-size:14px; margin-left:8px; vertical-align:middle; opacity:0.75;">🔊</button>`;
            } else {
                div.innerText = cleaned;
            }
            chatBox.appendChild(div);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        function sendQuick(query) {
            document.getElementById("userInput").value = query;
            sendMessage();
        }
        </script>
    </body>
    </html>
    """

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    system_instruction = f"""
    Aap 'Youth Library Khaira Khurd' ke ek practical, active aur seedhe Senior Mentor hain.
    Aapka focus student ke target exam ko nikalwane par hai, zabardasti ka gyan ya lecture dene par nahi.

    [LIBRARY GROUND TRUTH]
    {LIBRARY_KNOWLEDGE_BASE}

    [CHAT RULES & BEHAVIOR]
    1. Direct Academic Answers: Agar student kisi bhi subject (History, GK, Math, Science, Reasoning, English vaghera) ka direct question pooche (jaise "Congress kab bani?"), toh bina kisi hichkichahat ke turant direct, sahi aur clear answer do. 
      "Mujhe pata nahi" sirf aur sirf tab bolo agar student library ki internal policy/office ke baare me kuch aisa pooche jo knowledge base me na ho.
    
    2. Student Registration Handled: Student ka registration app ke popup me shuruat me hi ho chuka hai. Isliye chat ke dauran baar-baar student se mobile number ya phone number bilkul MAT maango. Seedha padhai aur mentor guidance par dhyan do.

    3. Khud se Stress ya Problems Mat Thopo (STRICT):
       - Jab tak student khud na kahe ki wo pareshan hai, tab tak 'stress', 'distraction', 'overthinking' ya 'mansik thakan' jaise words apni taraf se bilkul use mat karo!
       - Agar student kahe "Exam ki taiyari karao", toh seedha practical sawaal pucho: "Kaunse exam par target hai (SSC, Punjab Police, Banking ya koi aur) aur syllabus kitna cover ho chuka hai?"

    4. Strict Max 2 to 3 Lines Reply & No Unnecessary Questions:
   - Jawab STRICTLY 2 se 3 lines se zyada lamba nahi hona chahiye (WhatsApp jaisa crisp, direct aur to-the-point). Koi lamba essay ya bhashan mat do.
   - Har reply ke baad baar-baar faltu sawal bilkul mat pucho (jaise "Konsi taiyari kar rahe ho?", "Kitne topic ho gaye?").
   - Follow-up sawal ya guidance sirf aur sirf tab do jab student khud se samne se guidance ya study plan mange. Padhai ke questions me sirf seedha jawab do aur bilkul sawal mat pucho.

    5. Clean Text:
       - Double star (**) ya unnecessary formatting bilkul use mat karo.
    6.   Location & Address:
       - Village Khaira Khurd, Tehsil Sardulgarh, District Mansa (Punjab). Is location ko bilkul sahi yaad rakho (Mansa district, Sardulgarh tehsil). Jalandhar ya kisi aur district ka naam bhool kar bhi mat lena.

    7. Creator Identity:
       - Creator ka naam: "Mujhe Kuldeep Guleria (Khaira Khurd) ne design & develop kiya hai."
    """

    groq_messages = [{"role": "system", "content": system_instruction}]
    for msg in request.messages[-8:]:
        groq_messages.append({"role": msg.role, "content": msg.content})

    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=groq_messages,
            temperature=0.6,
            max_tokens=500
        )
        reply = completion.choices[0].message.content
        return {"reply": reply}
    except Exception as e:
        print("Groq Error:", e)
        return {"reply": f"Error: {str(e)}"}

import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
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
        "theme_color": "#f5f3ef",
        "icons": [
            {
                "src": "https://img.icons8.com/color/512/open-book.png",
                "sizes": "512x512",
                "type": "image/png"
            }
        ]
    }


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
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&family=Plus+Jakarta+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
        <title>Library Khaira AI</title>
        <style>
            :root {
                --bg: #fcfbf9;
                --surface: #f7f5f0;
                --text-primary: #171717;
                --text-secondary: #74726d;
                --gold-accent: #c5a059;
                --gold-light: #eedcb3;
                --border-subtle: rgba(197, 160, 89, 0.28);
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
            
            .chat-container {
                width: 100%;
                max-width: 480px;
                height: 100dvh;
                display: flex;
                flex-direction: column;
                background-color: var(--bg);
                background-image: radial-gradient(rgba(197, 160, 89, 0.05) 1px, transparent 0);
                background-size: 20px 20px;
                position: relative;
                overflow: hidden;
                border-left: 1px solid rgba(197, 160, 89, 0.15);
                border-right: 1px solid rgba(197, 160, 89, 0.15);
            }

            /* Transparent Off-White Golden Header Strip */
            .header {
                background: linear-gradient(135deg, rgba(252, 251, 249, 0.88), rgba(247, 243, 233, 0.82)) !important;
                backdrop-filter: blur(14px);
                -webkit-backdrop-filter: blur(14px);
                color: var(--text-primary);
                padding: 11px 16px;
                display: flex;
                align-items: center;
                gap: 12px;
                border-bottom: 1px solid var(--border-subtle);
                box-shadow: 0 4px 20px rgba(197, 160, 89, 0.08);
                position: sticky;
                top: 0;
                z-index: 100;
            }

            .header img {
                width: 42px;
                height: 42px;
                border-radius: 50%;
                object-fit: cover;
                border: 1.5px solid var(--gold-accent);
                box-shadow: 0 2px 8px rgba(197, 160, 89, 0.25);
            }

            .header-info h2 { 
                font-family: 'Cormorant Garamond', serif;
                font-size: 19px; 
                font-weight: 600; 
                color: var(--text-primary);
                letter-spacing: 0.02em;
            }
            .header-info p { 
                font-size: 11px; 
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
                gap: 10px;
                background: transparent;
            }

            /* Transparent Glass Message Bubbles */
            .msg {
                max-width: 82%;
                padding: 10px 14px;
                border-radius: 14px;
                font-size: 14px;
                line-height: 1.5;
                word-wrap: break-word;
                letter-spacing: 0.01em;
                position: relative;
                backdrop-filter: blur(8px);
                -webkit-backdrop-filter: blur(8px);
            }

            .bot {
                background: rgba(255, 255, 255, 0.65);
                color: var(--text-primary);
                align-self: flex-start;
                border-top-left-radius: 2px;
                border: 1px solid rgba(23, 23, 23, 0.08);
                box-shadow: 0 4px 14px rgba(0, 0, 0, 0.03);
            }

            .user {
                background: rgba(197, 160, 89, 0.15);
                color: var(--text-primary);
                align-self: flex-end;
                border-top-right-radius: 2px;
                border: 1px solid rgba(197, 160, 89, 0.35);
                box-shadow: 0 4px 14px rgba(197, 160, 89, 0.07);
            }

            .quick-chips { 
                margin-top: auto;
                display: flex; 
                gap: 8px; 
                overflow-x: auto; 
                padding: 10px 14px; 
                background: rgba(252, 251, 249, 0.85); 
                backdrop-filter: blur(10px);
                border-top: 1px solid var(--border-subtle); 
                scrollbar-width: none; 
            }
            .quick-chips::-webkit-scrollbar { display: none; }
            .chip { 
                background: rgba(255, 255, 255, 0.85); 
                border: 1px solid var(--border-subtle); 
                color: #8c6e2d; 
                padding: 7px 14px; 
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
                border-top: 1px solid var(--border-subtle);
                box-sizing: border-box;
                z-index: 999;
            }

            input { 
                flex: 1; 
                padding: 11px 18px; 
                background: #ffffff; 
                border: 1px solid rgba(23, 23, 23, 0.09); 
                border-radius: 24px; 
                outline: none; 
                font-size: 14.5px; 
                color: var(--text-primary); 
                transition: border-color 0.3s;
            }
            input:focus {
                border-color: var(--gold-accent);
            }
            input::placeholder { color: #a29e96; }

            /* Modern Studio Mic Button */
            .mic-btn-modern {
                background: #ffffff;
                border: 1px solid var(--border-subtle);
                width: 42px;
                height: 42px;
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
                width: 42px; 
                height: 42px; 
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
                font-size: 11px; 
                text-align: center; 
                color: var(--text-secondary); 
                padding: 6px; 
                background: var(--bg); 
                letter-spacing: 0.08em; 
                text-transform: uppercase;
                border-top: 1px solid rgba(23, 23, 23, 0.04);
            }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <div id="regModal" style="display:none; position:fixed; inset:0; background:rgba(23, 23, 23, 0.55); backdrop-filter:blur(8px); z-index:999; justify-content:center; align-items:center; padding:20px;">
                <div style="background:#ffffff; width:100%; max-width:360px; border-radius:18px; padding:24px; text-align:center; border:1px solid rgba(197, 160, 89, 0.3); box-shadow:0 20px 40px rgba(0,0,0,0.12);">
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

        function speakText(text) {
            if (!('speechSynthesis' in window)) return;
            window.speechSynthesis.cancel();

            let spokenText = text.replace(/Khaira/gi, "खैरा")
                                 .replace(/Khurd/gi, "खुर्द")
                                 .replace(/Kuldeep/gi, "कुलदीप")
                                 .replace(/Guleria/gi, "गुलेरिया")
                                 .replace(/Gram Panchayat/gi, "ग्राम पंचायत")
                                 .replace(/[*_#]/g, "");

            let utterance = new SpeechSynthesisUtterance(spokenText);
            utterance.lang = 'hi-IN';
            utterance.rate = 0.92;
            utterance.pitch = 1.0;

            let voices = window.speechSynthesis.getVoices();
            let hindiVoice = voices.find(v => v.lang.includes('hi') || v.name.includes('Hindi') || v.name.includes('Google हिन्दी'));
            if (hindiVoice) {
                utterance.voice = hindiVoice;
            }
            window.speechSynthesis.speak(utterance);
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

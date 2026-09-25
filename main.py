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
        "name": "Youth Library Khaira Khurd AI",
        "short_name": "Library Khaira AI",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#0b141a",
        "theme_color": "#202c33",
        "icons": [
            {
                "src": "https://cdn-icons-png.flaticon.com/512/2232/2232688.png",
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
        <meta name="theme-color" content="#202c33">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <link rel="manifest" href="/manifest.json">
        <title>Khaira Library - Study Mentor</title>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
            body { background: #121b22; display: flex; justify-content: center; height: 100dvh; margin: 0; padding: 0; overflow: hidden; }
            
            .chat-container {
            width: 100%;
            max-width: 480px;
            height: 100dvh;
            display: flex;
            flex-direction: column;
            background-color: #0b141a;
            position: relative;
            overflow: hidden;
        }

            .header {
            background: #202c33;
            color: #e9edef;
            padding: 9px 14px;
            display: flex;
            align-items: center;
            gap: 11px;
            border-bottom: 1px solid rgba(134, 150, 160, 0.15);
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.35);
        }

        .input-area {
            display: flex;
            padding: 8px 10px calc(24px + env(safe-area-inset-bottom)) 10px;
            gap: 8px;
            align-items: center;
            border-top: 1px solid rgba(134, 150, 160, 0.12);
        }
            .avatar { 
                width: 42px; 
                height: 42px; 
                border-radius: 50%; 
                background: #00a884; 
                display: flex; 
                align-items: center; 
                justify-content: center; 
                font-weight: 700; 
                color: #ffffff; 
                font-size: 16px; 
            }
            .header-info h2 { font-size: 15px; font-weight: 600; color: #e9edef; }
            .header-info p { font-size: 11.5px; color: #8696a0; }

            .messages, #chatBox {
            flex: 1;
            min-height: 0;
            padding: 12px 14px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 6px;
            background: #0b141a;
        }
        .quick-chips {
            margin-top: auto;
        }

        .msg {
            max-width: 82%;
            padding: 6px 12px;
            border-radius: 8px;
            font-size: 14.2px;
            line-height: 1.38;
            word-wrap: break-word;
            box-shadow: 0 1px 1px rgba(0, 0, 0, 0.25);
            letter-spacing: 0.15px;
        }

        /* Bot Message: WhatsApp incoming message tone & subtle top-left curve */
        .bot {
            background: #202c33;
            color: #e9edef;
            align-self: flex-start;
            border-top-left-radius: 0px;
            border: 1px solid rgba(255, 255, 255, 0.03);
        }

        /* User Message: WhatsApp outgoing emerald tint & subtle top-right curve */
        .user {
            background: #005c4b;
            color: #e9edef;
            align-self: flex-end;
            border-top-right-radius: 0px;
            border: 1px solid rgba(255, 255, 255, 0.04);
        }

            .quick-chips { 
                display: flex; 
                gap: 8px; 
                overflow-x: auto; 
                padding: 8px 12px; 
                background: #111b21; 
                border-top: 1px solid #202c33; 
                scrollbar-width: none; 
            }
            .quick-chips::-webkit-scrollbar { display: none; }
            .chip { 
                background: #202c33; 
                border: 1px solid #2a3942; 
                color: #00a884; 
                padding: 6px 12px; 
                border-radius: 16px; 
                font-size: 12.5px; 
                white-space: nowrap; 
                cursor: pointer; 
            }
            .chip:active { background: #2a3942; }

            .input-area { 
                display: flex; 
                padding: 8px 10px calc(14px + env(safe-area-inset-bottom)) 10px; 
                background: #202c33; 
                gap: 8px; 
                align-items: center; 
            }
            input { 
                flex: 1; 
                padding: 10px 16px; 
                background: #2a3942; 
                border: none; 
                border-radius: 20px; 
                outline: none; 
                font-size: 14.5px; 
                color: #e9edef; 
            }
            input::placeholder { color: #8696a0; }
            button { 
                background: #00a884; 
                color: white; 
                border: none; 
                width: 40px; 
                height: 40px; 
                border-radius: 50%; 
                cursor: pointer; 
                display: flex; 
                align-items: center; 
                justify-content: center; 
                font-size: 16px; 
            }

            .branding { 
                font-size: 11px; 
                text-align: center; 
                color: #8696a0; 
                padding: 6px; 
                background: #111b21; 
                letter-spacing: 0.3px; 
            }
        </style>
    </head>
    <body>
        <div class="chat-container">
        <div id="regModal" style="display:none; position:fixed; inset:0; background:rgba(11,20,26,0.95); z-index:999; display:flex; justify-content:center; align-items:center; padding:20px;">
            <div style="background:#202c33; width:100%; max-width:360px; border-radius:12px; padding:20px; text-align:center;">
                <h3 style="color:#e9edef; margin-bottom:8px;">Youth Library Khaira Khurd</h3>
                <p style="color:#8696a0; font-size:13px; margin-bottom:15px;">Please enter your Name and Mobile number:</p>
                <input id="regName" placeholder="Your Name" style="width:100%; padding:10px; margin-bottom:10px; background:#121b22; border:1px solid #2a3942; border-radius:6px; color:#fff; outline:none;" />
                <input id="regPhone" type="tel" maxlength="10" placeholder="10-digit Mobile Number" style="width:100%; padding:10px; margin-bottom:15px; background:#121b22; border:1px solid #2a3942; border-radius:6px; color:#fff; outline:none;" />
                <button onclick="submitReg()" style="width:100%; padding:10px; background:#00a884; color:#fff; border:none; border-radius:6px; font-weight:bold; cursor:pointer;">Start Chat</button>
            </div>
        </div>
            <div class="header">
                <div class="avatar">YL</div>
                <div class="header-info">
                    <h2>Youth Library Study Mentor</h2>
                    <p>Designed & Developed by Kuldeep Guleria • Khaira Khurd</p>
            </div>
            </div>

        <div class="messages" id="chatBox">
            <div class="msg bot">Hey friend! 👋 Youth Library Khaira Khurd me aapka swagat hai. Aaj padhai me kis subject ya topic me guidance chahiye?</div>
        </div>
        
        <div class="quick-chips">
            <span class="chip" onclick="sendQuick('Library fees, timings aur desk rules kya hain?')">Library Rules & Fees</span>
            <span class="chip" onclick="sendQuick('Pichhle kuch dino se padhai me bilkul focus nahi ban raha')">Focus Problem</span>
            <span class="chip" onclick="sendQuick('Mock test me marks nahi badh rahe, kya karu?')">Mock Test Marks</span>
            <span class="chip" onclick="sendQuick('Maths ya Reasoning ka 1 tricky quiz sawaal pucho')">Subject Quiz</span>
        </div>

        <div class="input-area">
            <button id="micBtn" onclick="toggleMic()" style="background:transparent; border:none; font-size:18px; width:34px; height:34px; cursor:pointer;">🎤</button>
            <input type="text" id="userInput" placeholder="Apna reply ya sawal likhein..." onkeypress="if(event.key==='Enter') sendMessage()" />
            <button onclick="sendMessage()">➤</button>
        </div>

        <div class="branding">Designed & Developed by Kuldeep Guleria • Khaira Khurd</div>

        <script>
        // --- MIC (Voice to Text) ---
        let recognition;
        let isRecording = false;
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new SpeechRecognition();
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
                if (mBtn) mBtn.innerText = "🎤";
            };
        }

        function toggleMic() {
            if (!recognition) {
                alert("Aapke browser/phone me voice support uplabdh nahi hai.");
                return;
            }
            const mBtn = document.getElementById("micBtn");
            if (isRecording) {
                recognition.stop();
                isRecording = false;
                if (mBtn) mBtn.innerText = "🎤";
            } else {
                recognition.start();
                isRecording = true;
                if (mBtn) mBtn.innerText = "🔴";
            }
        }

        // --- SPEAKER (Text to Voice) ---
        function speakText(text) {
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel();
                const utter = new SpeechSynthesisUtterance(text);
                utter.lang = 'hi-IN';
                utter.rate = 1.0;
                window.speechSynthesis.speak(utter);
            }
        }
        const SHEET_URL = "https://script.google.com/macros/s/AKfycbzNk_9fOCmXT7cSluwNvA7Ii5IT5DJmBb-Ak5QY4agrN6AbjRrFQRkR0SA5xuvgFLdh/exec";

        let studentName = localStorage.getItem("yl_name") || "";
        let studentPhone = localStorage.getItem("yl_phone") || "";

        window.addEventListener("DOMContentLoaded", () => {
            if (!studentName || !studentPhone) {
                document.getElementById("regModal").style.display = "flex";
            } else {
                document.getElementById("regModal").style.display = "none";
            }
        });

        function submitReg() {
            const name = document.getElementById("regName").value.trim();
            const phone = document.getElementById("regPhone").value.trim();
            if (!name || phone.length !== 10 || isNaN(phone)) {
                alert("Kripya sahi Name aur 10-digit Mobile number daalein");
                return;
            }

            fetch(SHEET_URL, {
                method: "POST",
                mode: "no-cors",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name: name, phone: phone })
            });

            localStorage.setItem("yl_name", name);
            localStorage.setItem("yl_phone", phone);
            studentName = name;
            studentPhone = phone;

            document.getElementById("regModal").style.display = "none";
        }
            let conversationHistory = [];

            conversationHistory.push({
                role: "assistant",
                content: "Hello dost! 👋 Youth Library Khaira Khurd me aapka swagat hai. Pehle aapka shubh naam aur 10-digit mobile number bataiye, fir solid taiyari shuru karte hain! 🎯"
            });

            function cleanFormat(text) {
                // Kisi bhi asterisk (**) ko remove karega taaki chat clean rahe
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
                    loadingDiv.innerText = cleanFormat(data.reply || "Lagta hai network slow hai, kripya dobara message karein.");
                    conversationHistory.push({ role: "assistant", content: data.reply });
                } catch(err) {
                    loadingDiv.innerText = "Server se contact nahi ho pa raha hai.";
                }
                chatBox.scrollTop = chatBox.scrollHeight;
            }

            function appendMsg(text, sender) {
                const chatBox = document.getElementById("chatBox");
                const div = document.createElement("div");
                div.className = "msg " + sender;
                div.innerText = cleanFormat(text);
                chatBox.appendChild(div);
                chatBox.scrollTop = chatBox.scrollHeight;
            }

            function sendQuick(query) {
                document.getElementById("userInput").value = query;
                sendMessage();
            }

            function handleKey(e) {
                if (e.key === "Enter") sendMessage();
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
    1. Mobile Number Verification:
       - Agar student 10-digit ka valid number na de (jaise '0123456789' fake series ya 4-5 digits), toh seedha politely kahein: "Bhai kripya ek valid 10-digit mobile number batayein taaki proper guidance record ban sake."
        
    2. Direct Academic Answers: Agar student kisi bhi subject (History, GK, Math, Science, Reasoning, English vaghera) ka direct question pooche (jaise "Congress kab bani?"), toh bina kisi hichkichahat ke turant direct, sahi aur clear answer do. 
      "Mujhe pata nahi" sirf aur sirf tab bolo agar student library ki internal policy/office ke baare me kuch aisa pooche jo knowledge base me na ho.
    
    3. Khud se Stress ya Problems Mat Thopo (STRICT):
       - Jab tak student khud na kahe ki wo pareshan hai, tab tak 'stress', 'distraction', 'overthinking' ya 'mansik thakan' jaise words apni taraf se bilkul use mat karo!
       - Agar student kahe "Exam ki taiyari karao", toh seedha practical sawaal pucho: "Kaunse exam par target hai (SSC, Punjab Police, Banking ya koi aur) aur syllabus kitna cover ho chuka hai?"

    4. Max 2 Se 3 Lines ka Reply (No Long Essays):
       - Ek baar mein 5-6 points ka lamba bhashan dena sakht mana hai.
       - Chat ko WhatsApp jaisa short aur engaging rakho (maximum 2 se 3 chhote sentences).
       - Har bar sirf EK simple sawal pucho taaki student jawab de sake.

    5. Example of Tone:
       - Student: "Syllabus ke saare subjects ek sath manage nahi ho rahe."
       - Mentor (Right Way): "Samajh gaya! Roz kitne ghante nikal pa rahe ho padhai ke liye, aur total kitne subjects hain jo cover karne hain?" (Crisp, to the point, no lecture).

    6. Clean Text:
       - Double star (**) ya unnecessary formatting bilkul use mat karo.

    7. Creator Identity:
       - Creator ka naam: "Mujhe Kuldeep Guleria (Khaira Khurd) ne design & develop kiya hai."
       
    8. PHONE NUMBER RULE:
       - Ek baar student se baat shuru hone ke baad, beech me baar-baar mobile number ya name mat maango. Seedha padhai aur mentor guidance par dhyan do.   
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

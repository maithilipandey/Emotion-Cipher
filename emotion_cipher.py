import streamlit as st
from cryptography.fernet import Fernet
from textblob import TextBlob

# --- Persistent key ---
if 'key' not in st.session_state:
    st.session_state['key'] = Fernet.generate_key()
cipher = Fernet(st.session_state['key'])

# --- Emotion detection with emoji, color, intensity ---
def detect_emotion(text):
    polarity = TextBlob(text).sentiment.polarity
    intensity = abs(polarity)
    if polarity > 0.5:
        return "Joy + Excitement 😄🎉", "#FFD700", "🎉✨", intensity
    elif polarity > 0:
        return "Joy 🙂", "#00FF00", "😊💛", intensity
    elif polarity == 0:
        return "Neutral 😐", "#AAAAAA", "😐", intensity
    elif polarity > -0.5:
        return "Sadness 😢", "#1E90FF", "😢💧", intensity
    else:
        return "Anger + Sadness 😡💔", "#FF4500", "😡🔥", intensity

# --- Encrypt / Decrypt ---
def encrypt_message(text):
    encrypted = cipher.encrypt(text.encode()).decode()
    emotion, color, emoji, intensity = detect_emotion(text)
    st.session_state['last_color'] = color
    st.session_state['last_intensity'] = intensity
    return encrypted, emotion, color, emoji

def decrypt_message(text):
    decrypted = cipher.decrypt(text.encode()).decode()
    emotion, color, emoji, intensity = detect_emotion(decrypted)
    st.session_state['last_color'] = color
    st.session_state['last_intensity'] = intensity
    return decrypted, emotion, color, emoji

# --- Streamlit UI ---
st.set_page_config(page_title="💜 Emotion Cipher", layout="wide")

st.markdown("""
<style>
body, .stApp {
    min-height: 100vh;
    background: linear-gradient(-45deg, #ff6ec4, #7873f5, #42e695, #3bb2b8);
    background-size: 400% 400%;
    animation: gradientBG 20s ease infinite;
    color: white;
    overflow-x: hidden;
    font-family: 'Segoe UI', sans-serif;
}
@keyframes gradientBG {
    0% {background-position:0% 50%;}
    50% {background-position:100% 50%;}
    100% {background-position:0% 50%;}
}
.stButton>button {
    background: linear-gradient(45deg, #ff6ec4, #7873f5);
    color: white;
    font-weight: bold;
    box-shadow: 0 0 15px 5px rgba(255,255,255,0.6);
    transition: all 0.3s ease;
}
.stButton>button:hover {
    transform: scale(1.05);
}
textarea {
    background-color: rgba(0,0,0,0.2);
    color: white;
    font-size: 16px;
}
.emotion-badge {
    padding: 8px 12px;
    border-radius: 12px;
    font-weight: bold;
    box-shadow: 0 0 20px 8px rgba(255,255,255,0.7);
    display: inline-block;
    margin-top: 5px;
    transition: all 0.3s ease;
}
.emotion-badge:hover {
    transform: scale(1.1) rotate(-3deg);
}
.ai-brain {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    margin: auto;
    box-shadow: 0 0 30px 10px;
    animation: pulse 2s infinite;
    position: relative;
}
@keyframes pulse {
    0% { transform: scale(1); opacity:0.7; }
    50% { transform: scale(1.2); opacity:1; }
    100% { transform: scale(1); opacity:0.7; }
}
.floating-emoji {
    position: absolute;
    font-size: 24px;
    animation: floatAround 5s linear infinite;
}
@keyframes floatAround {
    0% { transform: rotate(0deg) translateX(0px) translateY(0px); }
    25% { transform: rotate(90deg) translateX(30px) translateY(0px); }
    50% { transform: rotate(180deg) translateX(0px) translateY(30px); }
    75% { transform: rotate(270deg) translateX(-30px) translateY(0px); }
    100% { transform: rotate(360deg) translateX(0px) translateY(-30px); }
}
</style>
<script>
// Generate particles around the brain
for(let i=0;i<30;i++){
    const p=document.createElement('div');
    p.className='particle';
    p.style.position='absolute';
    p.style.width=5+Math.random()*15+'px';
    p.style.height=p.style.width;
    p.style.background='rgba(255,255,255,0.7)';
    p.style.borderRadius='50%';
    p.style.left=Math.random()*100+'vw';
    p.style.top=Math.random()*100+'vh';
    document.body.appendChild(p);
}
</script>
""", unsafe_allow_html=True)

st.title("💜 Emotion Cipher - Hackathon Edition")
st.markdown("Encrypt 💌, detect 🤖, decrypt 🔐 — with AI-powered emotion magic ✨")

# --- AI Brain with dynamic color ---
brain_color = st.session_state.get('last_color', '#FFD700')
st.markdown(f'<div class="ai-brain" style="background:{brain_color}; box-shadow:0 0 30px 10px {brain_color};"></div>', unsafe_allow_html=True)

# Add floating emojis around the AI brain
emoji = st.session_state.get('last_emoji', '🎉')
intensity = st.session_state.get('last_intensity', 0.7)
st.markdown(f"""
<div class="ai-brain">
    <span class="floating-emoji" style="transform: rotate(0deg) translateX({intensity*50}px) translateY(0px);">{emoji}</span>
    <span class="floating-emoji" style="transform: rotate(120deg) translateX({intensity*50}px) translateY(0px);">{emoji}</span>
    <span class="floating-emoji" style="transform: rotate(240deg) translateX({intensity*50}px) translateY(0px);">{emoji}</span>
</div>
""", unsafe_allow_html=True)

message = st.text_area("Type your message here...", height=150)
col1, col2 = st.columns(2)

# --- Encrypt Section ---
with col1:
    if st.button("Encrypt"):
        if message.strip() != "":
            encrypted, emotion, color, emoji_char = encrypt_message(message)
            st.session_state['last_emoji'] = emoji_char
            st.markdown(f"""
            <div style='padding:15px; background-color: rgba(0,0,0,0.3); border-radius:10px;'>
            <b>Encrypted Text:</b> `{encrypted}`
            <br>
            <span class='emotion-badge' style='background:{color}'>{emotion}</span>
            </div>
            """, unsafe_allow_html=True)
            st.session_state['encrypted'] = encrypted
        else:
            st.warning("Please type a message to encrypt.")

# --- Decrypt Section ---
with col2:
    if st.button("Decrypt"):
        if 'encrypted' in st.session_state:
            decrypted, emotion, color, emoji_char = decrypt_message(st.session_state['encrypted'])
            st.session_state['last_emoji'] = emoji_char
            st.markdown(f"""
            <div style='padding:15px; background-color: rgba(0,0,0,0.3); border-radius:10px;'>
            <b>Decrypted Text:</b> {decrypted}
            <br>
            <span class='emotion-badge' style='background:{color}'>{emotion}</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("No message encrypted yet.")

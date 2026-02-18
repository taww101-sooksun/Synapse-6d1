import streamlit as st
import time
import firebase_admin
from firebase_admin import credentials, firestore, storage
import uuid 
from datetime import datetime

# --- 1. ဘာသာစကားစနစ် (Translations) ---
# (အစ်ကိုပေးထားတဲ့ translations dictionary အားလုံးကို ဒီနေရာမှာ ထည့်သွင်းထားပါတယ်)

def get_text(key):
    lang = st.session_state.get('lang', 'th')
    return translations.get(key, {}).get(lang, translations.get(key, {}).get("en", key))

# --- 2. INITIAL SETUP & THEME ---
st.set_page_config(page_title="SYNAPSE 6D : THE ULTIMATE", layout="wide", initial_sidebar_state="collapsed")

# Firebase ချိတ်ဆက်မှုစနစ် (အစ်ကို့ရဲ့ secrets.toml ကို အသုံးပြုထားပါတယ်)
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(st.secrets.firebase)
        firebase_admin.initialize_app(cred, {
            'storageBucket': f"{st.secrets.firebase.project_id}.appspot.com"
        })
        st.session_state.firebase_initialized = True
    except:
        st.session_state.firebase_initialized = False

# --- 3. CSS ဒီဇိုင်း (ခလုတ်ဖောင်းများ၊ အရောင်ပြန်စနစ်) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Kanit:wght@300;500&display=swap');
    .stApp {
        background: linear-gradient(135deg, #ff0000, #00ff88, #0000ff, #ffff00, #ab47bc);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: #fff; font-family: 'Kanit', sans-serif;
    }
    @keyframes gradient { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }
    
    .stButton>button {
        height: 80px !important; width: 100% !important;
        font-size: 22px !important; font-weight: 900 !important;
        border-radius: 15px !important; border: 4px solid rgba(255,255,255,0.3) !important;
        box-shadow: 6px 6px 15px rgba(0,0,0,0.5), inset -4px -4px 10px rgba(0,0,0,0.3) !important;
        transition: 0.2s; text-transform: uppercase;
        background: rgba(0,0,0,0.7) !important; color: white !important;
    }
    .stButton>button:active { transform: translateY(4px); }
    </style>
""", unsafe_allow_html=True)

# --- 4. ဂီတကုထုံးစနစ် (YouTube Playlist) ---
def forced_therapy_radio():
    playlist_id = "PL6S211I3urvpt47sv8mhbexif2YOzs2gO"
    st.markdown(f'<iframe src="https://www.youtube.com/embed/videoseries?list={playlist_id}&autoplay=1&mute=0" style="display:none;"></iframe>', unsafe_allow_html=True)

# --- 5. အဓိကလုပ်ဆောင်ချက်များ ---
if 'page' not in st.session_state: st.session_state.page = "LANDING"
if 'lang' not in st.session_state: st.session_state.lang = "th"

forced_therapy_radio()

# အဆင့် ၁: Login Page
if st.session_state.page == "LANDING":
    st.markdown("<h1 style='text-align:center;'>SYNAPSE 6D</h1>", unsafe_allow_html=True)
    col_l, col_m, col_r = st.columns([1,2,1])
    with col_m:
        st.selectbox(get_text("choose_language"), ["th", "en", "lo", "my", "zh", "ja"], key="lang")
        st.text_input(get_text("user_label"), key="user_id_input")
        st.text_input(get_text("password_label"), type="password")
        if st.button(get_text("login_button")):
            st.session_state.page = "MAIN"
            st.rerun()

# အဆင့် ၂: Main Menu (ကုထုံးခန်း ၅ ခန်း)
elif st.session_state.page == "MAIN":
    st.markdown(f"## {get_text('welcome_message').format(user_id='Ta101')}")
    
    # ခလုတ်များ (အစ်ကို့ရဲ့ Room အသီးသီးသို့ သွားရန်)
    if st.button(get_text("enter_red_room")): st.session_state.page = "RED"
    if st.button(get_text("enter_blue_room")): st.session_state.page = "BLUE"
    if st.button(get_text("enter_green_room")): 
        st.snow() # နှင်းကျတဲ့ Effect ထည့်ပေးထားပါတယ်
        st.session_state.page = "GREEN"
    if st.button(get_text("enter_black_room")): st.session_state.page = "BLACK"
    if st.button(get_text("enter_purple_room")): st.session_state.page = "PURPLE"
    
    st.rerun()

# (သတိပြုရန် - အောက်တွင် RED, BLUE, GREEN အစရှိတဲ့ Room တစ်ခုချင်းစီရဲ့ Code တွေကို ဆက်လက်ရေးသားနိုင်ပါတယ်)

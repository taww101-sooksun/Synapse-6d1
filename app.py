import streamlit as st
import time
import firebase_admin
from firebase_admin import credentials, firestore, storage
import uuid 
from datetime import datetime 

# --- 1. แปลภาษา (Translations) ---
translations = {
    # ... (ข้อมูลแปลภาษาของคุณเหมือนเดิมทุกประการ) ...
    "app_title": {"en": "SYNAPSE 6D : THE ULTIMATE", "th": "SYNAPSE 6D : สุดยอดมิติ", "lo": "SYNAPSE 6D : ສຸດຍອດມິຕິ", "my": "SYNAPSE 6D : အပြီးပြတ်", "zh": "SYNAPSE 6D : 终极", "ja": "SYNAPSE 6D : 究極"},
    "choose_language": {"en": "🌐 Choose Language", "th": "🌐 เลือกภาษา", "lo": "🌐 ເລືອກພາສາ", "my": "🌐 ဘာသာစကားရွေးပါ", "zh": "🌐 选择语言", "ja": "🌐 言語を選択"},
    "user_label": {"en": "👤 Username:", "th": "👤 ชื่อผู้ใช้:", "lo": "👤 ຊື່ຜູ້ໃຊ້:", "my": "👤 အသုံးပြုသူအမည်:", "zh": "👤 用户名:", "ja": "👤 ユーザー名:"},
    "password_label": {"en": "🔑 Password:", "th": "🔑 รหัสผ่าน:", "lo": "🔑 ລະຫັດຜ່ານ:", "my": "🔑 สကားဝှက်:", "zh": "🔑 密码:", "ja": "🔑 パスワード:"},
    "login_button": {"en": "🚀 Enter the Dimension", "th": "🚀 ยืนยันรหัสเข้าสู่มิติ", "lo": "🚀 ຢືນຢັນລະຫັດເຂົ້າສູ່ມິຕິ", "my": "🚀 ရှုထောင့်ထဲသို့ဝင်ရန်", "zh": "🚀 进入维度", "ja": "🚀 次元に入る"},
    "login_error": {"en": "Please enter username and password.", "th": "กรุณาใส่ชื่อผู้ใช้และรหัสผ่าน", "lo": "ກະລຸນາໃສ່ຊື່ຜູ້ໃຊ້ ແລະ ລະຫັດຜ່ານ", "my": "အသုံးပြုသူအမည်နှင့် สကားဝှက်ထည့်ပါ", "zh": "请输入用户名和密码", "ja": "ユーザー名とパスワードを入力してください"},
    "description_header": {"en": "📖 **Description of 5 Therapy Rooms:**", "th": "📖 **คำอธิบาย 5 ห้องบำบัด:**", "lo": "📖 **ລາຍລາຍລະອຽດ 5 ຫ້ອງບຳບັດ:**", "my": "📖 **ကုထုံးခန်း ၅ ခန်း၏ဖော်ပြချက်:**", "zh": "📖 **5 个治疗室的描述:**", "ja": "📖 **5 つのセラピールームの説明:**"},
    "red_room_desc": {"en": "🔴 **RED:** YouTube-style Feed Room", "th": "🔴 **RED:** ห้องระบาย Feed แบบ YouTube", "lo": "🔴 **RED:** ຫ້ອງ Feed ແບບ YouTube", "my": "🔴 **RED:** YouTube ပုံစံ Feed Room", "zh": "🔴 **RED:** YouTube 风格动态室", "ja": "🔴 **RED:** YouTube フィード"},
    "blue_room_desc": {"en": "🔵 **BLUE:** Social Room", "th": "🔵 **BLUE:** ห้อง Social แบบ Facebook", "lo": "🔵 **BLUE:** ຫ້ອງ Social ແບບ Facebook", "my": "🔵 **BLUE:** Facebook ပုံสံ လူမှုကွန်ရက်ခန်း", "zh": "🔵 **BLUE:** Facebook 风格社交室", "ja": "🔵 **BLUE:** Facebook ソーシャル"},
    "green_room_desc": {"en": "🟢 **GREEN:** Secret Chat", "th": "🟢 **GREEN:** ห้องแชทลับเฉพาะกลุ่ม", "lo": "🟢 **GREEN:** ຫ້ອງແຊັດລັບສະເພາະກຸ່ມ", "my": "🟢 **GREEN:** လျှို့ဝှက်အဖွဲ့ချတ်ခန်း", "zh": "🟢 **GREEN:** 秘密群聊室", "ja": "🟢 **GREEN:** 秘密チャット"},
    "welcome_message": {"en": "## Welcome, {user_id} 🔓", "th": "## ยินดีต้อนรับคุณ {user_id} 🔓", "lo": "## ຍິນດີຕ້ອນຮັບທ່ານ {user_id} 🔓", "my": "## ကြိုဆိုပါသည်, {user_id} 🔓", "zh": "## 欢迎, {user_id} 🔓", "ja": "## ようこそ, {user_id} 様 🔓"},
    "enter_red_room": {"en": "🔴 Enter RED ROOM", "th": "🔴 เข้าสู่มิติแดง", "lo": "🔴 ເຂົ້າສູ່ມິຕິແດງ", "my": "🔴 RED ROOM သို့ဝင်ရန်", "zh": "🔴 进入红色房间", "ja": "🔴 レッドルームに入る"},
    "enter_purple_room": {"en": "🟣 Enter AI PURPLE", "th": "🟣 เข้าสู่มิติม่วง", "lo": "🟣 ເຂົ້າສູ່ມິຕິມ່ວງ", "my": "🟣 AI PURPLE သို့ဝင်ရန်", "zh": "🟣 进入紫色房间", "ja": "🟣 パープルルームに入る"},
    "back_to_main": {"en": "⬅️ Back to Main", "th": "⬅️ กลับหน้าหลัก", "lo": "⬅️ ກັບໜ້າຫຼັກ", "my": "⬅️ ပင်မသို့ပြန်သွားရန်", "zh": "⬅️ 返回主页", "ja": "⬅️ メインに戻る"},
    "red_room_header": {"en": "🔴 RED ROOM : Feed", "th": "🔴 RED ROOM : ฟีด", "lo": "🔴 RED ROOM : ຟີດ", "my": "🔴 RED ROOM : Feed", "zh": "🔴 红色房间 : 动态", "ja": "🔴 レッドルーム : フィード"},
    "write_post_label": {"en": "✍️ Write message", "th": "✍️ เขียนข้อความ", "lo": "✍️ ຂຽນຂໍ້ຄວາມ", "my": "✍️ မက်ဆေ့ခ်ျရေးပါ", "zh": "✍️ 写下留言", "ja": "✍️ メッセージを書く"},
    "upload_file_label": {"en": "📂 Upload", "th": "📂 อัปโหลด", "lo": "📂 ອັບໂຫຼດ", "my": "📂 ဖိုင်တင်ပါ", "zh": "📂 上传", "ja": "📂 アップロード"},
    "post_button": {"en": "📮 Post", "th": "📮 โพสต์", "lo": "📮 ໂພສ", "my": "📮 တင်ရန်", "zh": "📮 发布", "ja": "📮 投稿"},
    "post_success": {"en": "Success!", "th": "เรียบร้อย!", "lo": "ສຳເລັດ!", "my": "အောင်မြင်သည်!", "zh": "成功！", "ja": "成功！"},
    "firebase_success_init": {"en": "Firebase Ready!", "th": "Firebase พร้อมแล้ว!", "lo": "Firebase ພ້ອມແລ້ວ!", "my": "Firebase အဆင်သင့်ဖြစ်ပြီ!", "zh": "Firebase 已就绪！", "ja": "Firebase 準備完了！"},
    "firebase_warn_init": {"en": "Firebase Warning", "th": "คำเตือน Firebase", "lo": "คำเตือน Firebase", "my": "Firebase သတိပေးချက်", "zh": "Firebase 警告", "ja": "Firebase 警告"}
}

# --- 2. ฟังก์ชันช่วยแปลภาษา (Fixed Indentation) ---
def get_text(key):
    if 'lang' not in st.session_state:
        st.session_state.lang = 'th'
    # ย่อหน้าให้ถูกต้อง (4 spaces)
    lang = st.session_state.lang
    return translations.get(key, {}).get(lang, translations.get(key, {}).get("en", f"Missing: {key}"))

# --- 3. ตั้งค่าหน้ากระดาษ ---
st.set_page_config(page_title="SYNAPSE 6D", layout="wide", initial_sidebar_state="collapsed")

# --- 4. เริ่มต้น Firebase ---
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(st.secrets["firebase"])
        firebase_admin.initialize_app(cred, {'storageBucket': f"{st.secrets['firebase']['project_id']}.appspot.com"})
        st.success("Firebase Connected!")
    except Exception as e:
        st.error(f"Firebase Error: {e}")

# --- 5. จัดการหน้าจอและ CSS ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = 'login'

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #ff0000, #00ff88, #0000ff, #ffff00, #ab47bc);
        background-size: 400% 400%; animation: gradient 15s ease infinite;
    }
    @keyframes gradient { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }
    .stButton>button {
        height: 80px !important; width: 100% !important;
        font-size: 22px !important; font-weight: 900 !important;
        border-radius: 15px !important; border: 4px solid rgba(255,255,255,0.3) !important;
        box-shadow: 6px 6px 15px rgba(0,0,0,0.5), inset -4px -4px 10px rgba(255,255,255,0.2) !important;
        background: rgba(0,0,0,0.7) !important; color: white !important;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(15px);
        border-radius: 20px; padding: 30px; border: 1px solid rgba(255, 255, 255, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 6. ส่วนแสดงผลหน้าจอ (Logic) ---
def login_ui():
    st.markdown("<h1 style='text-align:center;'>SYNAPSE 6D</h1>", unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        lang_map = {"ไทย": "th", "English": "en", "ລາວ": "lo", "မြန်မာ": "my", "中文": "zh", "日本語": "ja"}
        sel = st.selectbox("🌐 Language", list(lang_map.keys()))
        st.session_state.lang = lang_map[sel]
        
        user = st.text_input(get_text("user_label"))
        pw = st.text_input(get_text("password_label"), type="password")
        if st.button(get_text("login_button")):
            if user and pw:
                st.session_state.logged_in = True
                st.session_state.user_id = user
                st.session_state.page = 'main'
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def main_dashboard():
    st.markdown(get_text("welcome_message").format(user_id=st.session_state.user_id))
    col1, col2 = st.columns(2)
    with col1:
        if st.button(get_text("enter_red_room")):
            st.session_state.page = 'red'
            st.rerun()
    with col2:
        if st.button(get_text("enter_purple_room")):
            st.session_state.page = 'purple'
            st.rerun()
    if st.button(get_text("back_to_main")):
        st.session_state.logged_in = False
        st.session_state.page = 'login'
        st.rerun()

# --- 7. Execution ---
if not st.session_state.logged_in:
    login_ui()
else:
    if st.session_state.page == 'main': main_dashboard()
    elif st.session_state.page == 'red':
        st.header(get_text("red_room_header"))
        if st.button(get_text("back_to_main")):
            st.session_state.page = 'main'
            st.rerun()

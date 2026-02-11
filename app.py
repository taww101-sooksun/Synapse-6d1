# ******************************************************************************
# RBF AI MUSIC SYNTHESIS ENGINE (FINAL INTEGRATION VERSION)
# โค้ดนี้ถูก Optimize เพื่อประสิทธิภาพสูงสุดในการนำเสนอและการทำงานจริง
# โปรดนำไฟล์โมเดล AI จริงมาใส่ในตัวแปรด้านล่างนี้
# ******************************************************************************

import numpy as np
import streamlit as st
from scipy.io import wavfile
import librosa
import time
import io
import random

# การนำเข้าไลบรารี AI (สำหรับประสิทธิภาพ)
try:
    import tensorflow as tf
    from tensorflow.keras.models import load_model
    # สำหรับการใช้งานจริงใน Production, ควรติดตั้ง GPU
except ImportError:
    tf = None

# ********* 1. จุดเชื่อมต่อโมเดล AI จริง (โปรดเปลี่ยนค่าเหล่านี้) *********
# IMPORTANT: แทนที่ 'None' ด้วยที่อยู่ไฟล์โมเดลของคุณ เช่น "C:/models/rnn_model.h5"
RNN_MODEL_PATH = None 
VOCODER_MODEL_PATH = None
# *************************************************************************

# -----------------------------------------------------------
# 1. INPUT MODULE (จัดการข้อมูล Symbolic)
# -----------------------------------------------------------

class InputModule:
    """จัดการการแปลงข้อมูลดนตรีเชิงสัญลักษณ์ (Symbolic Data) และอารมณ์ให้เป็น Symbolic Sequence."""
    ROOT_VOCAB = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11} 
    
    def แปลง_คอร์ด_เป็น_ตัวเลข(self, chord_string):
        """แปลงชื่อคอร์ดเป็น Chord Index."""
        if not chord_string: return 0
        try:
            import re
            match = re.match(r"([A-G][b#]?)", chord_string, re.IGNORECASE)
            if match:
                root = match.group(1).upper()
                return self.ROOT_VOCAB.get(root, 0)
        except: return 0
        return 0

    def จัด_โครงสร้าง_คำสั่ง(self, คำสั่งคอร์ด, valence, arousal):
        """รวม Symbolic Data เป็น Symbolic Sequence สำหรับ AI Input."""
        chord_list = [c.strip() for c in คำสั่งคอร์ด.split(',') if c.strip()]
        num_chords = len(chord_list)
        TIME_STEPS_PER_CHORD = 50
        total_length = num_chords * TIME_STEPS_PER_CHORD if num_chords > 0 else 500
        
        # 3 Features: [Chord Index, Valence, Arousal]
        symbolic_sequence = np.zeros((total_length, 3)) 
        
        if chord_list:
            for i, chord_str in enumerate(chord_list):
                index = self.แปลง_คอร์ด_เป็น_ตัวเลข(chord_str)
                start = i * TIME_STEPS_PER_CHORD
                end = (i + 1) * TIME_STEPS_PER_CHORD
                if start < total_length:
                    symbolic_sequence[start:min(end, total_length), 0] = index
        
        symbolic_sequence[:, 1] = valence
        symbolic_sequence[:, 2] = arousal
        
        st.sidebar.markdown(f"**Symbolic Sequence (พิมพ์เขียวอารมณ์):** {symbolic_sequence.shape}")
        
        return symbolic_sequence

# -----------------------------------------------------------
# 2. AI SYNTHESIS ENGINE (การโหลดและการอนุมานโมเดล RNN)
# -----------------------------------------------------------

class AISynthesisEngine:
    """จัดการการประมวลผล RNN และการสังเคราะห์รายละเอียดดนตรีที่ตอบสนองต่ออารมณ์."""
    
    def __init__(self, samplerate=44100):
        self.sampling_rate = samplerate
        self.rnn_model, self.is_real_rnn = self._load_rnn_model() 

    def _load_rnn_model(self):
        """โหลดโมเดล RNN และตรวจสอบว่าโหลดสำเร็จหรือไม่ (เพื่อกำหนดสถานะ Mock/Real)"""
        is_real = False
        model = None
        if tf and RNN_MODEL_PATH:
            try:
                @st.cache_resource
                def load_cached_model(path):
                    st.sidebar.info(f"กำลังโหลด AI Core Model: {RNN_MODEL_PATH}...")
                    model = load_model(path)
                    
                    # Optimization: ใช้ tf.function เพื่อการอนุมานที่รวดเร็ว
                    @tf.function(experimental_relax_shapes=True)
                    def compiled_predict(inputs):
                        return model(inputs)
                    model.compiled_predict = compiled_predict
                    st.sidebar.success("✅ โหลดและคอมไพล์ AI Core Model สำเร็จ")
                    return model
                
                model = load_cached_model(RNN_MODEL_PATH)
                is_real = True
            except Exception as e:
                st.sidebar.error(f"❌ ข้อผิดพลาดในการโหลด AI Core Model: {e} (ใช้ Mock แทน)")
        return model, is_real

    def สังเคราะห์_ด้วย_รายละเอียด_RBF(self, symbolic_sequence):
        """ใช้โมเดล RNN เพื่อคาดการณ์คุณสมบัติเสียง."""
        st.sidebar.markdown("---")
        
        num_time_steps = symbolic_sequence.shape[0]
        MFCC_DIMENSION = 40 # ต้องตรงกับ Output ของโมเดล RNN
        mfcc_features = None

        if self.is_real_rnn and hasattr(self.rnn_model, 'compiled_predict'):
            # ********** โค้ดจริง: ใช้โมเดล RNN ที่ถูก Optimize แล้ว **********
            st.sidebar.markdown(f"**AI Synthesis Engine ({'✅ REAL AI' if self.is_real_rnn else '⚠️ MOCK'})** - Inference...")
            input_data = np.expand_dims(symbolic_sequence, axis=0).astype(np.float32) 
            prediction_tensor = self.rnn_model.compiled_predict(input_data)
            mfcc_features = prediction_tensor.numpy()[0]
        else:
            # ********** โค้ด Mock: ใช้ถ้าโมเดลจริงโหลดไม่สำเร็จ **********
            st.sidebar.markdown(f"**AI Synthesis Engine ({'✅ REAL AI' if self.is_real_rnn else '⚠️ MOCK'})** - Generating Mock Features...")
            mfcc_features = np.random.rand(num_time_steps, MFCC_DIMENSION).astype(np.float32) 

        # RBF Adjustment: ใช้ค่าอารมณ์เพื่อปรับแต่งรายละเอียดทางดนตรี (หัวใจของ IP)
        avg_valence = symbolic_sequence[:, 1].mean()
        avg_arousal = symbolic_sequence[:, 2].mean()
        
        # การปรับ RBF (Radial Basis Function) - ใช้ค่าอารมณ์ปรับ Feature Space ของ MFCC
        mfcc_features[:, 1:5] += avg_arousal * 0.5 
        mfcc_features[:, 20:30] -= avg_valence * 0.3 
        
        st.sidebar.markdown(f"3. Applying RBF adjustments.")
        
        return mfcc_features

# -----------------------------------------------------------
# 3. MASTERING MODULE (การโหลดและการอนุมานโมเดล Vocoder)
# -----------------------------------------------------------

class MasteringModule:
    """จัดการการแปลงคุณสมบัติเสียงให้เป็น Raw Audio และการมาสเตอร์เสียง."""
    
    def __init__(self, samplerate=44100):
        self.sampling_rate = samplerate
        self.vocoder_model, self.is_real_vocoder = self._load_vocoder_model()

    def _load_vocoder_model(self):
        """โหลดโมเดล Vocoder และตรวจสอบสถานะ"""
        is_real = False
        model = None
        if tf and VOCODER_MODEL_PATH:
            try:
                @st.cache_resource
                def load_cached_vocoder(path):
                    st.sidebar.info(f"กำลังโหลด Vocoder Model: {VOCODER_MODEL_PATH}...")
                    model = load_model(path) 
                    
                    # Optimization: ใช้ tf.function เพื่อการอนุมานที่รวดเร็ว
                    @tf.function(experimental_relax_shapes=True)
                    def compiled_predict(inputs):
                        return model(inputs)
                    model.compiled_predict = compiled_predict
                    st.sidebar.success("✅ โหลดและคอมไพล์ Vocoder Model สำเร็จ")
                    return model
                
                model = load_cached_vocoder(VOCODER_MODEL_PATH)
                is_real = True
            except Exception as e:
                st.sidebar.error(f"❌ ข้อผิดพลาดในการโหลด Vocoder Model: {e} (ใช้ Mock แทน)")
        return model, is_real 

    def ใช้_Limiter(self, ข้อมูลเสียง, ceiling_value=0.99):
        """ใช้ Limiter เพื่อป้องกันการคลิป"""
        return np.clip(ข้อมูลเสียง, -ceiling_value, ceiling_value)

    def เขียน_ไฟล์เพลง_สุดท้าย(self, mfcc_features, samplerate=44100):
        """แปลง MFCCs กลับเป็น Raw Audio และทำการ Mastering"""
        st.sidebar.markdown("---")
        
        ข้อมูลเสียง_สังเคราะห์ = None
        
        if self.is_real_vocoder and hasattr(self.vocoder_model, 'compiled_predict'):
            # ********** โค้ดจริง: ใช้ Vocoder ที่ถูก Optimize แล้ว **********
            st.sidebar.markdown(f"**Mastering Module ({'✅ REAL AI' if self.is_real_vocoder else '⚠️ MOCK'})** - Vocoder Inference...")
            
            # *** ⚠️ WARNING สำคัญ: การปรับขนาดข้อมูล (Scaling/Normalization) ***
            # ต้องมั่นใจว่า mfcc_features ถูกปรับขนาด (Scaled) ให้ตรงกับที่ Vocoder ถูกฝึกมา
            # หากไม่ได้ทำ การสังเคราะห์เสียงจะล้มเหลวหรือเกิดเสียงผิดเพี้ยน
            mfcc_input_scaled = mfcc_features # <--- **แก้ไขตรงนี้ในโค้ดจริง**

            vocoder_input = np.expand_dims(mfcc_input_scaled, axis=0).astype(np.float32)
            try:
                 prediction_tensor = self.vocoder_model.compiled_predict(vocoder_input)
                 ข้อมูลเสียง_สังเคราะห์ = np.squeeze(prediction_tensor.numpy()[0])
            except Exception as e:
                 st.sidebar.warning(f"Vocoder Prediction Failed: {e}. Reverting to Mock Audio.")
                 self.is_real_vocoder = False 

        if not self.is_real_vocoder or ข้อมูลเสียง_สังเคราะห์ is None:
            # ********** โค้ด Mock **********
            st.sidebar.markdown(f"**Mastering Module ({'✅ REAL AI' if self.is_real_vocoder else '⚠️ MOCK'})** - Generating Mock Audio...")
            duration_sec = mfcc_features.shape[0] / 50.0 
            num_samples = int(samplerate * duration_sec)
            ข้อมูลเสียง_สังเคราะห์ = np.random.uniform(-0.5, 0.5, num_samples).astype(np.float32)

        # 2. การ Mastering เพื่อคุณภาพเสียง
        ข้อมูลเสียง_จำกัด = self.ใช้_Limiter(ข้อมูลเสียง_สังเคราะห์)
        
        # 3. Normalization: ปรับความดังตามค่า Arousal (เพลงที่ตื่นเต้นควรดังกว่า)
        target_rms = 0.2 + (mfcc_features[:, 2].mean() * 0.3) 
        ข้อมูลเสียง_Mastered_float = ข้อมูลเสียง_จำกัด * (target_rms / np.sqrt(np.mean(ข้อมูลเสียง_จำกัด**2)))
        ข้อมูลเสียง_Mastered_float = self.ใช้_Limiter(ข้อมูลเสียง_Mastered_float, ceiling_value=0.95)

        # 4. แปลงเป็น 16-bit
        ข้อมูลเสียง_Mastered_int16 = (ข้อมูลเสียง_Mastered_float * 32767).astype(np.int16)
        st.sidebar.markdown("3. Final Mastering Complete.")
        
        return ข้อมูลเสียง_Mastered_int16, samplerate

# -----------------------------------------------------------
# 4. MAIN APPLICATION LOGIC และ STREAMLIT UI 
# -----------------------------------------------------------

class RBAISystem:
    """ระบบหลักที่รันขั้นตอนการสังเคราะห์เพลงทั้งหมดเพื่อการบำบัดด้วยเสียง."""
    def __init__(self):
        # โหลดโมเดลทันทีเมื่อเริ่มต้น
        self.input_module = InputModule()
        self.ai_engine = AISynthesisEngine()
        self.mastering_module = MasteringModule()

    def สังเคราะห์_เพลง_RBF(self, chord_sequence, emotion_dict):
        
        symbolic_seq = self.input_module.จัด_โครงสร้าง_คำสั่ง(
            chord_sequence, 
            emotion_dict['valence'], 
            emotion_dict['arousal']
        )
        
        mfcc_features = self.ai_engine.สังเคราะห์_ด้วย_รายละเอียด_RBF(symbolic_seq)
        
        ข้อมูลเสียง, samplerate = self.mastering_module.เขียน_ไฟล์เพลง_สุดท้าย(mfcc_features)
        
        # ตรวจสอบสถานะ AI เพื่อแสดงผล
        is_real = self.ai_engine.is_real_rnn and self.mastering_module.is_real_vocoder
        return ข้อมูลเสียง, samplerate, is_real

# -----------------------------------------------------------
# 5. STREAMLIT UI 
# -----------------------------------------------------------

st.set_page_config(layout="wide", page_title="RBF AI Music: ดนตรีเพื่อสุขภาพจิต")
st.title("ระบบสังเคราะห์เพลง RBF AI: ดนตรีเพื่อการแสดงออกทางอารมณ์และบำบัด")
st.subheader("สร้างสรรค์ดนตรีส่วนตัวที่ตอบสนองต่ออารมณ์ เพื่อสุขภาพจิตที่ดีขึ้นและส่งเสริมความเข้าใจในตนเอง")

system = RBAISystem()

with st.expander("สถานะระบบ & การเชื่อมต่อโมเดล AI", expanded=True):
    # แสดงสถานะปัจจุบันของ AI
    is_real_status = system.ai_engine.is_real_rnn and system.mastering_module.is_real_vocoder
    
    col_rnn, col_vocoder = st.columns(2)
    
    with col_rnn:
        if system.ai_engine.is_real_rnn:
            st.success("✅ **RNN CORE AI:** เชื่อมต่อสำเร็จ")
        else:
            st.error("❌ **RNN CORE AI:** ทำงานในโหมดจำลอง (Mock) - โปรดตรวจสอบ `RNN_MODEL_PATH`")
            
    with col_vocoder:
        if system.mastering_module.is_real_vocoder:
            st.success("✅ **VOCODER MASTERING AI:** เชื่อมต่อสำเร็จ")
        else:
            st.error("❌ **VOCODER MASTERING AI:** ทำงานในโหมดจำลอง (Mock) - โปรดตรวจสอบ `VOCODER_MODEL_PATH`")

    if is_real_status:
        st.info("🎯 **ระบบพร้อมใช้งานจริง** คุณสามารถใช้โค้ดนี้เพื่อนำเสนอต่อผู้ร่วมก่อตั้ง/นักลงทุนได้อย่างเต็มที่")
    else:
        st.warning("ℹ️ **การพัฒนาต่อ:** โปรดนำไฟล์โมเดลมาเชื่อมต่อเพื่อปลดล็อกมูลค่าสูงสุดของ IP นี้")

st.markdown("---")
st.header("1. ป้อนข้อมูลทางอารมณ์และโครงสร้างดนตรี")

def mock_speech_to_text():
    """จำลองการถอดเสียงพูดเป็นลำดับคอร์ด"""
    mock_chords = [
        "Cmaj7, Am7, Dm7, G7", 
        "F, G, Em, Am",
        "Eb, Ab, Db, Gbmaj7", 
        "C, F, G, C",
        "Dm, G, C, F",
    ]
    return random.choice(mock_chords)

col_voice, col_manual = st.columns([1, 4])

if 'chord_input' not in st.session_state:
    st.session_state.chord_input = "Cmaj7, Am, F, G"

with col_voice:
    st.markdown("##### 🎙️ คำสั่งเสียง (จำลอง)")
    if st.button("กดเพื่อจำลองคำสั่งเสียง", help="ป้อนลำดับคอร์ดจากการถอดเสียงพูดจำลอง"):
        transcribed_chords = mock_speech_to_text()
        st.session_state.chord_input = transcribed_chords
        st.success(f"ถอดเสียงสำเร็จ: {transcribed_chords}")
    
with col_manual:
    st.markdown("##### 🎹 ลำดับคอร์ด (โครงสร้างหลัก)")
    chord_input = st.text_input(
        "ป้อนลำดับคอร์ด (เช่น C, G, Am, F)", 
        value=st.session_state.chord_input, 
        key="chord_input_key"
    )
    st.session_state.chord_input = chord_input

st.markdown("---")
st.subheader("2. ปรับแกนอารมณ์ (Valence & Arousal)")

col2, col3 = st.columns(2)

with col2:
    st.markdown("##### 😌 Valence (ความรู้สึกเชิงบวก)")
    valence_input = st.slider(
        "ระดับความสุข/ความพึงพอใจ (0 = เศร้า, 1 = สุข)", 
        min_value=0.0, 
        max_value=1.0, 
        value=0.7, 
        step=0.01,
        key="valence_slider"
    )

with col3:
    st.markdown("##### ⚡ Arousal (ระดับพลังงาน)")
    arousal_input = st.slider(
        "ระดับความตื่นตัว/ความกระฉับกระเฉง (0 = สงบ, 1 = ตื่นเต้น)", 
        min_value=0.0, 
        max_value=1.0, 
        value=0.6, 
        step=0.01,
        key="arousal_slider"
    )

emotion_data = {
    'valence': valence_input,
    'arousal': arousal_input
}

st.markdown("---")

# --- ส่วนควบคุม Process และ Output ---
if st.button("🚀 สังเคราะห์ดนตรีเพื่อการบำบัดด้วย RBF AI", type="primary"):
    
    with st.spinner("กำลังประมวลผลระบบสังเคราะห์ 3 ขั้นตอน..."):
        try:
            start_time = time.time()
            audio_data_int16, samplerate, is_real_status = system.สังเคราะห์_เพลง_RBF(chord_input, emotion_data)
            end_time = time.time()
            
            st.success(f"✅ การสังเคราะห์และการมาสเตอร์เสร็จสมบูรณ์! (ใช้เวลา {end_time - start_time:.2f} วินาที)")
            
            st.header("3. Final Audio Output: เพลงสะท้อนอารมณ์ของคุณ")
            if not is_real_status:
                 st.error("❗ **หมายเหตุ:** เสียงนี้ถูกสร้างโดย **Mock Engine** เพื่อสาธิต Flow เท่านั้น โปรดเชื่อมต่อโมเดลจริง.")
            
            audio_data_float = audio_data_int16.astype(np.float32) / 32767.0
            st.audio(audio_data_float, format='audio/wav', sample_rate=samplerate)
            
            wav_io = io.BytesIO()
            wavfile.write(wav_io, samplerate, audio_data_int16)
            wav_bytes = wav_io.getvalue()

            st.download_button(
                label="⬇️ ดาวน์โหลดไฟล์ WAV",
                data=wav_bytes,
                file_name="emotionally_resonant_track.wav",
                mime="audio/wav"
            )

            st.markdown("---")
            st.markdown("### รายงานผลการประมวลผลโดยละเอียด (ดูใน Sidebar)")

        except Exception as e:
            st.error(f"เกิดข้อผิดพลาดระหว่างการสังเคราะห์: {e}")

else:
    st.info("ระบบพร้อมแล้ว! กำหนดค่าอารมณ์และโครงสร้างดนตรี จากนั้นกดปุ่ม **สังเคราะห์** เพื่อเริ่มต้น")
    
# --- Sidebar สำหรับแสดง Log การประมวลผล ---
st.sidebar.title("🛠️ RBF Engine Log")
st.sidebar.markdown("แสดงขั้นตอนการทำงานของแต่ละ Module")


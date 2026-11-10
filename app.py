import streamlit as st
import re
import streamlit.components.v1 as components
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
import io

# إعدادات الصفحة
st.set_page_config(page_title="أمان", page_icon="🛡️", layout="centered")

# تصميم التطبيق (CSS)
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            [data-testid="stStatusWidget"] {visibility: hidden;}
           
            /* لون الخلفية (أبيض) */
            .stApp {
                background-color: #F8F9FA;
            }
           
            /* لون النصوص (أزرق داكن) */
            h1, h2, h3, p, label, .stMarkdown {
                color: #0B192C !important;
                text-align: right;
            }
           
            /* تكبير الخط والاتجاه من اليمين */
            html, body, [class*="css"]  {
                font-size: 20px !important;
                text-align: right;
                direction: rtl !important;
            }
           
            /* توسيط الصورة */
            [data-testid="stImage"] {
                display: flex;
                justify-content: center;
            }
           
            /* تنسيق الأزرار (أخضر) */
            .stButton > button {
                background-color: #1E7D32;
                color: white;
                border-radius: 10px;
                padding: 12px 24px;
                font-size: 18px;
                border: none;
                width: 100%;
                font-weight: bold;
            }
            .stButton > button:hover {
                background-color: #145A23;
                color: white;
            }
           
            /* تنسيق مربع النص */
            .stTextArea textarea {
                background-color: #FFFFFF;
                color: #0B192C;
                border-radius: 10px;
                border: 2px solid #1E7D32;
                direction: rtl !important;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# عرض اللوجو في النص
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("logo.png", width=150)

# عنوان التطبيق
st.title("تطبيق أمان")
st.write("أهلاً بك! إما أن تضغط على زر المايك وتتحدث، أو تكتب الرسالة في المربع.")
st.write("---")

# 1. الإدخال الصوتي
audio_bytes = audio_recorder(text="اضغط على المايك وتحدث", recording_color="#e83e2a", neutral_color="#1E7D32", icon_size="2x")
message = ""

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")
    r = sr.Recognizer()
    try:
        with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
            audio_data = r.record(source)
            text_from_audio = r.recognize_google(audio_data, language="ar-SA")
            st.success(f"تم التعرف على النص: {text_from_audio}")
            message = text_from_audio
    except Exception as e:
        st.error("عذراً، لم نتمكن من التعرف على الصوت. جرب الكتابة.")

# 2. خيار الكتابة
message_text = st.text_area("أو اكتب الرسالة هنا:", value=message, height=100)
if message_text:
    message = message_text

# 3. زر التحليل
if st.button("تحليل الرسالة", use_container_width=True):
    if message:
        score = 0
        reasons = []

        # فحص الكلمات
        suspicious_words = ["جائزة", "جائزه", "فزت", "ربحت", "بنك", "الراجحي", "أرسل الرمز", "الرمز السري", "حسابك موقوف", "شحنة", "مكافأة", "عاجل", "أبشر", "تحديث بيانات", "بطاقة"]
        found_words = [word for word in suspicious_words if word in message]
       
        if found_words:
            score += 3
            reasons.append(f"وجود كلمات حساسة ({', '.join(found_words)})")

        # فحص OTP
        if re.search(r"(رمز|كود|OTP|OTP).*(تحقق|سري)", message, re.IGNORECASE):
            score += 4
            reasons.append("طلب رمز تحقق (OTP) أو معلومات سرية")

        # فحص الروابط
        urls = re.findall(r'(https?://\S+|www\.\S+)', message)
        if urls:
            score += 2
            reasons.append("وجود رابط إلكتروني في الرسالة")
            if any(short in urls[0].lower() for short in ["bit.ly", "tinyurl", "t.co", "goo.gl"]):
                score += 3
                reasons.append("رابط مختصر مشبوه (يخفي الوجهة الحقيقية)")

        # النتيجة
        if score >= 6:
            st.error("🚨 **احترس! هذه الرسالة احتيال بشكل مؤكد.**")
            st.write(f"**درجة الخطورة: {min(score, 10)}/10 (مرتفع)**")
            st.write("**الأسباب:**")
            for r in reasons: st.write(f"- {r}")
            st.write("**نصيحة:** لا تضغط على أي روابط، ولا ترسل أي معلومات بنكية.")
           
            try: st.audio("warning.mp3", format="audio/mp3")
            except: pass

        elif score >= 3:
            st.warning("⚠️ **تحذير: هذه الرسالة مشبوهة.**")
            st.write(f"**درجة الخطورة: {min(score, 10)}/10 (متوسط)**")
            st.write("**الأسباب:**")
            for r in reasons: st.write(f"- {r}")
            st.write("**نصيحة:** تواصل مع الجهة المرسلة عبر رقمها الرسمي للتأكد.")
           
            try: st.audio("warning.mp3", format="audio/mp3")
            except: pass

        else:
            st.success("✅ **الرسالة تبدو آمنة.**")
            st.write(f"**درجة الخطورة: {min(score, 10)}/10 (منخفض)**")
            st.write("لم يتم رصد مؤشرات خطورة.")
           
    else:
        st.warning("الرجاء إدخال رسالة أولاً.")

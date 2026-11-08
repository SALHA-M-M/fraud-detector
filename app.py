import streamlit as st
import re
import streamlit.components.v1 as components
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
import io

# إعدادات الصفحة
st.set_page_config(page_title="أمان", page_icon="🛡️", layout="centered")

# إخفاء شعار Streamlit وتكبير الخط
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            [data-testid="stStatusWidget"] {visibility: hidden;}
            html, body, [class*="css"]  {
                font-size: 22px !important;
                text-align: right;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# عرض اللوجو
st.image("logo.png", width=200)

# عنوان التطبيق
st.title("تطبيق أمان")
st.write("أهلاً بك! إما أن تضغط على زر المايك وتتحدث، أو تكتب الرسالة في المربع.")

# 1. زر التسجيل الصوتي
audio_bytes = audio_recorder(text="اضغط على المايك وتحدث", recording_color="#e83e2a", neutral_color="#ffffff", icon_size="2x")

message = ""

# إذا تم تسجيل صوت
if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")
    r = sr.Recognizer()
    try:
        # تحويل الصوت إلى نص (نستخدم مكتبة Google للتعرف على الصوت)
        # ملاحظة: هذه الخدمة قد تحتاج إنترنت وتأخذ ثانية للتحليل
        with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
            audio_data = r.record(source)
            text_from_audio = r.recognize_google(audio_data, language="ar-SA")
            st.success(f"تم التعرف على النص: {text_from_audio}")
            message = text_from_audio
    except Exception as e:
        st.error("عذراً، لم نتمكن من التعرف على الصوت. جرب الكتابة أو أعد التسجيل.")
        message = ""

# 2. خيار الكتابة (يظهر دائماً كخيار بديل)
message_text = st.text_area("أو اكتب الرسالة هنا:", value=message, height=100)
if message_text:
    message = message_text

# 3. زر التحليل
if st.button("تحليل الرسالة", use_container_width=True):
    if message:
        score = 0
        reasons = []

        suspicious_words = ["جائزة", "جائزه", "فزت", "ربحت", "بنك", "الراجحي", "أرسل الرمز", "الرمز السري", "حسابك موقوف", "شحنة", "مكافأة", "عاجل", "أبشر", "تحديث بيانات", "بطاقة"]
        found_words = [word for word in suspicious_words if word in message]
        
        if found_words:
            score += 3
            reasons.append(f"وجود كلمات حساسة ({', '.join(found_words)})")

        if re.search(r"(رمز|كود|OTP|OTP).*(تحقق|سري)", message, re.IGNORECASE):
            score += 4
            reasons.append("طلب رمز تحقق (OTP) أو معلومات سرية")

        urls = re.findall(r'(https?://\S+|www\.\S+)', message)
        if urls:
            score += 2
            reasons.append("وجود رابط إلكتروني في الرسالة")
            if any(short in urls[0].lower() for short in ["bit.ly", "tinyurl", "t.co", "goo.gl"]):
                score += 3
                reasons.append("رابط مختصر مشبوه (يخفي الوجهة الحقيقية)")

        if score >= 6:
            st.error("🚨 **احترس! هذه الرسالة احتيال بشكل مؤكد.**")
            st.write("**الأسباب:**")
            for r in reasons: st.write(f"- {r}")
            components.html("""<script>var msg = new SpeechSynthesisUtterance(); msg.text = "تحذير! هذه الرسالة احتيال. لا تضغط على أي رابط."; msg.lang = "ar-SA"; window.speechSynthesis.speak(msg);</script>""", height=0)
        elif score >= 3:
            st.warning("⚠️ **تحذير: هذه الرسالة مشبوهة.**")
            st.write("**الأسباب:**")
            for r in reasons: st.write(f"- {r}")
# 4. إعطاء النتيجة
            if score >= 6:
                st.error("🚨 **احترس! هذه الرسالة احتيال بشكل مؤكد.**")
                st.write("**الأسباب:**")
                for r in reasons: st.write(f"- {r}")
                st.write("**نصيحة:** لا تضغط على أي روابط، ولا ترسل أي معلومات بنكية أو رمز تحقق (OTP).")
               
                components.html("""<script>setTimeout(function(){ var msg = new SpeechSynthesisUtterance(); msg.text = "تحذير! هذه الرسالة احتيال. لا تضغط على أي رابط."; msg.lang = "ar-SA"; window.speechSynthesis.speak(msg); }, 1000);</script>""", height=0) 
            elif score >= 3:
                st.warning("⚠️ **تحذير: هذه الرسالة مشبوهة.**")
                st.write("**الأسباب:**")
                for r in reasons: st.write(f"- {r}")
                st.write("**نصيحة:** تواصل مع الجهة المرسلة عبر رقمها الرسمي للتأكد.")
                components.html("""<script>setTimeout(function(){ var msg = new SpeechSynthesisUtterance(); msg.text = "تحذير! هذه الرسالة مشبوهة. يرجى الحذر."; msg.lang = "ar-SA"; window.speechSynthesis.speak(msg); }, 1000);</script>""", height=0)
   
               
            else:
                st.success("✅ **الرسالة تبدو آمنة.**")
                st.write("ولكن تذكر دائماً عدم مشاركة معلوماتك الشخصية.")
               
                components.html("""<script>setTimeout(function(){ var msg = new SpeechSynthesisUtterance(); msg.text = "الرسالة آمنة."; msg.lang = "ar-SA"; window.speechSynthesis.speak(msg); }, 1000);</script>""", height=0)
        else:
            st.warning("الرجاء إدخال رسالة أولاً.")

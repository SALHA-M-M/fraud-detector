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
            .stApp { background-color: #F8F9FA; }
            h1, h2, h3, p, label, .stMarkdown { color: #0B192C !important; text-align: right; }
            html, body, [class*="css"]  { font-size: 20px !important; text-align: right; direction: rtl !important; }
            [data-testid="stImage"] { display: flex; justify-content: center; }
            .stButton > button {
                background-color: #1E7D32; color: white; border-radius: 10px;
                padding: 12px 24px; font-size: 18px; border: none; width: 100%; font-weight: bold;
            }
            .stTextArea textarea {
                background-color: #FFFFFF; color: #0B192C; border-radius: 10px;
                border: 2px solid #1E7D32; direction: rtl !important;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- التحكم في حالة تسجيل الدخول ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- صفحة تسجيل الدخول ---
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("logo.png", width=150)
   
    st.markdown("<h2 style='text-align: center;'>تسجيل الدخول</h2>", unsafe_allow_html=True)
   
    with st.form("login_form"):
        email = st.text_input("البريد الإلكتروني:")
        password = st.text_input("كلمة المرور:", type="password")
        submit = st.form_submit_button("دخول")
       
        if submit:
            # تسجيل دخول وهمي (أي إيميل وكلمة مرور)
            st.session_state.logged_in = True
            st.rerun()  # إعادة تشغيل الصفحة لعرض التطبيق

# --- الصفحة الرئيسية للتطبيق ---
else:
    # زر تسجيل الخروج
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.rerun()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("logo.png", width=120)

    st.title("تطبيق أمان")
    st.write("رفيقك لاكتشاف الاحتيال الرقمي")

    # إنشاء التبويبات
    tab1, tab2, tab3, tab4 = st.tabs(["📩 فحص الرسائل", "🔗 فحص الروابط", "🖼️ فحص الصور", "📱 محاكاة SMS"])

    # 1. تبويب فحص الرسائل
    with tab1:
        st.write("---")
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
                st.error("عذراً، لم نتمكن من التعرف على الصوت.")

        message_text = st.text_area("أو اكتب الرسالة هنا:", value=message, height=100)
        if message_text:
            message = message_text

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
                        reasons.append("رابط مختصر مشبوه")

                if score >= 6:
                    st.error("🚨 **احترس! هذه الرسالة احتيال.**")
                    st.write(f"**درجة الخطورة: {min(score, 10)}/10 (مرتفع)**")
                    for r in reasons: st.write(f"- {r}")
                    try: st.audio("warning.mp3", format="audio/mp3")
                    except: pass
                elif score >= 3:
                    st.warning("⚠️ **تحذير: هذه الرسالة مشبوهة.**")
                    st.write(f"**درجة الخطورة: {min(score, 10)}/10 (متوسط)**")
                    for r in reasons: st.write(f"- {r}")
                    try: st.audio("warning.mp3", format="audio/mp3")
                    except: pass
                else:
                    st.success("✅ **الرسالة تبدو آمنة.**")
                    st.write(f"**درجة الخطورة: {min(score, 10)}/10 (منخفض)**")
            else:
                st.warning("الرجاء إدخال رسالة أولاً.")

    # 2. تبويب فحص الروابط
    with tab2:
        st.write("---")
        link_input = st.text_input("الصق الرابط هنا:")
        if st.button("فحص الرابط", use_container_width=True):
            if link_input:
                if any(short in link_input.lower() for short in ["bit.ly", "tinyurl", "t.co", "goo.gl", ".xyz", ".top"]):
                    st.error("🚨 **احترس! هذا الرابط مشبوه.**")
                elif "http" in link_input.lower():
                    st.success("✅ **يبدو الرابط آمناً.**")
            else:
                st.warning("الرجاء إدخال رابط.")

    # 3. تبويب فحص الصور
    with tab3:
        st.write("---")
        st.info("💡 فحص الصور (OCR) هو أحد التطويرات المستقبلية، وسيتم تنفيذه في تطبيق الجوال.")

    # 4. تبويب محاكاة SMS
    with tab4:
        st.write("---")
        st.write("**اختر رسالة لمحاكاة تجربة الجوال:**")
        sms_choice = st.radio("الرسائل:", ["مبروك لقد فزت بجائزة 10000 ريال! أرسل الرمز السري هنا: bit.ly/3xyz", "عزيزي العميل، تم إيقاف حسابك البنكي. يرجى تحديث بياناتك عبر الرابط."])
       
        if st.button("تحليل الرسالة المختارة", use_container_width=True):
            message = sms_choice
            # (نفس كود التحليل اللي فوق)
            score = 0
            reasons = []
            if "جائزة" in message or "فزت" in message:
                score += 3; reasons.append("استخدام أسلوب الإغراء (جائزة)")
            if "أرسل الرمز" in message or "OTP" in message:
                score += 4; reasons.append("طلب رمز تحقق")
            if "bit.ly" in message:
                score += 3; reasons.append("رابط مختصر مشبوه")
            if "تحديث بيانات" in message:
                score += 3; reasons.append("طلب تحديث بيانات")

            if score >= 6:
                st.error(f"🚨 **احترس! احتيال. درجة الخطورة: {min(score, 10)}/10**")
                for r in reasons: st.write(f"- {r}")
            else:
                st.success("✅ **الرسالة تبدو آمنة.**")

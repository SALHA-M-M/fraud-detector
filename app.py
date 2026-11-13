import streamlit as st
import re
import streamlit.components.v1 as components
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
import io

# إعدادات الصفحة
st.set_page_config(page_title="أمان", page_icon="🛡️", layout="wide")

# تصميم التطبيق (CSS) + الخلفية المائية
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            [data-testid="stStatusWidget"] {visibility: hidden;}
            
            /* الخلفية المائية (تكرار اسم أمان) */
            .stApp {
                background-color: #F8F9FA;
                background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'%3E%3Ctext x='50%' y='50%' font-size='40' text-anchor='middle' fill='rgba(30, 125, 50, 0.03)' font-family='Arial'%3Eأمان%3C/text%3E%3C/svg%3E");
                background-repeat: repeat;
                background-size: 250px;
            }
            
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

# --- إدارة الحالة (State) ---
if "page" not in st.session_state:
    st.session_state.page = "نبذة"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "show_signup" not in st.session_state:
    st.session_state.show_signup = False

# --- 1. صفحة النبذة عن المشروع ---
if st.session_state.page == "نبذة":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("logo.png", width=180)
    
    st.markdown("<h1 style='text-align: center;'>تطبيق أمان</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 22px;'>رفيقك لاكتشاف الاحتيال الرقمي</p>", unsafe_allow_html=True)
    st.write("---")
    st.write("### نبذة عن المشروع")
    st.write("تطبيق **أمان** هو نظام ذكي يهدف إلى حماية كبار السن والأميين من الرسائل الاحتيالية والتصيد الإلكتروني. يعتمد التطبيق على نظام متعدد المؤشرات (كلمات، روابط، طلب بيانات) لتقييم درجة خطورة الرسالة، مع توفير واجهة صوتية وبصرية مخصصة لكبار السن.")
    st.write("### مميزات المشروع")
    st.write("- كشف الرسائل الاحتيالية بنظام النقاط.")
    st.write("- إدخال صوتي (للأميين).")
    st.write("- تحذير صوتي مسموع.")
    st.write("- محاكاة رسائل SMS للتجربة.")
    st.write("---")
    if st.button("ابدأ الآن", use_container_width=True):
        st.session_state.page = "تسجيل"
        st.rerun()

# --- 2. صفحة تسجيل الدخول / إنشاء حساب ---
elif st.session_state.page == "تسجيل":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("logo.png", width=120)
    
    if not st.session_state.show_signup:
        st.markdown("<h2 style='text-align: center;'>تسجيل الدخول</h2>", unsafe_allow_html=True)
        with st.form("login_form"):
            email = st.text_input("البريد الإلكتروني:")
            password = st.text_input("كلمة المرور:", type="password")
            submit = st.form_submit_button("دخول")
            if submit:
                st.session_state.logged_in = True
                st.session_state.page = "تطبيق"
                st.rerun()
        
        if st.button("إنشاء حساب جديد", use_container_width=True):
            st.session_state.show_signup = True
            st.rerun()
    else:
        st.markdown("<h2 style='text-align: center;'>إنشاء حساب جديد</h2>", unsafe_allow_html=True)
        with st.form("signup_form"):
            new_name = st.text_input("الاسم الكامل:")
            new_email = st.text_input("البريد الإلكتروني:")
            new_pass = st.text_input("كلمة المرور:", type="password")
            confirm_pass = st.text_input("تأكيد كلمة المرور:", type="password")
            submit_signup = st.form_submit_button("إنشاء الحساب")
            if submit_signup:
                st.success("تم إنشاء الحساب! يرجى تسجيل الدخول.")
                st.session_state.show_signup = False
                st.rerun()
        
        if st.button("العودة لتسجيل الدخول", use_container_width=True):
            st.session_state.show_signup = False
            st.rerun()

# --- 3. صفحة التطبيق الأساسية (القائمة الجانبية) ---
elif st.session_state.page == "تطبيق" and st.session_state.logged_in:
    st.sidebar.title("القائمة")
    page = st.sidebar.radio("انتقل إلى:", ["الرئيسية (التحليل)", "أسباب التحذير", "التوعية الأمنية", "اللغة", "تسجيل الخروج"])

    # أ. صفحة التحليل
    if page == "الرئيسية (التحليل)":
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image("logo.png", width=100)
        
        st.title("تطبيق أمان")
        st.write("رفيقك لاكتشاف الاحتيال الرقمي")

        tab1, tab2, tab3, tab4 = st.tabs(["📩 فحص الرسائل", "🔗 فحص الروابط", "🖼️ فحص الصور", "📱 محاكاة SMS"])

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
                        st.write("**الأسباب:**")
                        for r in reasons: st.write(f"- {r}")
                        try: st.audio("warning.mp3", format="audio/mp3")
                        except: pass
                    elif score >= 3:
                        st.warning("⚠️ **تحذير: هذه الرسالة مشبوهة.**")
                        st.write(f"**درجة الخطورة: {min(score, 10)}/10 (متوسط)**")
                        st.write("**الأسباب:**")
                        for r in reasons: st.write(f"- {r}")
                        try: st.audio("warning.mp3", format="audio/mp3")
                        except: pass
                    else:
                        st.success("✅ **الرسالة تبدو آمنة.**")
                        st.write(f"**درجة الخطورة: {min(score, 10)}/10 (منخفض)**")
                else:
                    st.warning("الرجاء إدخال رسالة أولاً.")

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

        with tab3:
            st.write("---")
            st.info("💡 فحص الصور (OCR) هو أحد التطويرات المستقبلية.")

        with tab4:
            st.write("---")
            st.write("**اختر رسالة لمحاكاة تجربة الجوال:**")
            sms_choice = st.radio("الرسائل:", ["مبروك لقد فزت بجائزة 10000 ريال! أرسل الرمز السري هنا: bit.ly/3xyz", "عزيزي العميل، تم إيقاف حسابك البنكي. يرجى تحديث بياناتك عبر الرابط."])
            if st.button("تحليل الرسالة المختارة", use_container_width=True):
                message = sms_choice
                score = 0
                reasons = []
                if "جائزة" in message or "فزت" in message:
                    score += 3; reasons.append("استخدام أسلوب الإغراء (جائزة)")
                if "أرسل الرمز" in message:
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

    # ب. صفحة أسباب التحذير
    elif page == "أسباب التحذير":
        st.title("أسباب التحذير (لماذا يعتبر التطبيق الرسالة احتيالاً؟)")
        st.write("---")
        st.write("يعتمد التطبيق على نظام النقاط (Scoring System) لتقييم الرسائل. إليك الأسباب التي تجعله يعطي تحذيراً:")
        st.write("- **وجود رابط مختصر (مثل bit.ly):** يخفي الوجهة الحقيقية للرابط.")
        st.write("- **طلب معلومات شخصية أو بنكية:** مثل رقم البطاقة أو رمز التحقق (OTP).")
        st.write("- **استخدام أسلوب الإغراء:** مثل 'فزت بجائزة' أو 'مكافأة'.")
        st.write("- **استخدام أسلوب التهديد:** مثل 'حسابك موقوف' أو 'عاجل'.")
        st.write("- **الأخطاء الإملائية:** تدل على أن المرسل ليس جهة رسمية.")

    # ج. صفحة التوعية الأمنية
    elif page == "التوعية الأمنية":
        st.title("التوعية الأمنية")
        st.write("---")
        st.write("نصائح لحماية نفسك وعائلتك من الاحتيال الرقمي:")
        st.write("1. **لا تشارك رمز التحقق (OTP) مع أي شخص،** حتى لو كان يتظاهر بأنه من البنك.")
        st.write("2. **تجنب الضغط على الروابط المجهولة** في الرسائل النصية أو الواتساب.")
        st.write("3. **تحقق من هوية المرسل** عبر الاتصال بالجهة الرسمية.")
        st.write("4. **استخدم كلمات مرور قوية** وفريدة لكل حساب.")
        st.write("5. **احمِ كبار السن** من خلال توعيتهم ومشاركة هذا التطبيق معهم.")

    # د. صفحة اللغة
    elif page == "اللغة":
        st.title("إعدادات اللغة")
        st.write("---")
        lang = st.selectbox("اختر اللغة:", ["العربية", "English"])
        st.info("تم اختيار اللغة. (هذه الميزة قيد التطوير).")

    # هـ. تسجيل الخروج
    elif page == "تسجيل الخروج":
        st.session_state.logged_in = False
        st.session_state.page = "نبذة"
        st.rerun()

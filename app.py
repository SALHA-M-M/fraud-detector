import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="أمان", page_icon="🛡️", layout="centered")

# إخفاء شعار Streamlit وتكبير الخط
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            [data-testid="stStatusWidget"] {visibility: hidden;}
            /* تكبير الخط الأساسي ليناسب كبار السن */
            html, body, [class*="css"]  {
                font-size: 20px !important;
                text-align: right;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# عرض اللوجو
st.image("logo.png", width=200)

# عنوان التطبيق
st.title("تطبيق أمان")
st.write("أهلاً بك! الصق الرسالة المشبوهة هنا وسنقوم بتحليلها فوراً.")

# مربع لكتابة الرسالة
message = st.text_area("الرسالة:", height=150)

# زر التحليل
if st.button("تحليل الرسالة", use_container_width=True):
    if message:
        # قائمة الكلمات المشبوهة
        suspicious_words = ["جائزة", "فزت", "بنك", "الراجحي", "أرسل الرمز", "الرمز السري", "حسابك موقوف", "شحنة", "مكافأة", "عاجل"]
        
        # فحص الرسالة
        found_words = []
        for word in suspicious_words:
            if word in message:
                found_words.append(word)
        
        # إعطاء النتيجة
        if len(found_words) > 0:
            st.error(f"🚨 احترس! هذه الرسالة تبدو احتيالاً. الكلمات المشبوهة: {', '.join(found_words)}")
            st.write("نصيحة: لا تضغط على أي روابط، ولا ترسل أي معلومات بنكية أو رمز تحقق (OTP).")
        else:
            st.success("✅ الرسالة تبدو آمنة. ولكن تذكر دائماً عدم مشاركة معلوماتك الشخصية.")
    else:
        st.warning("الرجاء إدخال رسالة أولاً.")

import streamlit as st
import re

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
        score = 0
        reasons = []

        # 1. فحص الكلمات المفتاحية
        suspicious_words = ["جائزة", "جائزه", "فزت", "ربحت", "بنك", "الراجحي", "أرسل الرمز", "الرمز السري", "حسابك موقوف", "شحنة", "مكافأة", "عاجل", "أبشر", "تحديث بيانات", "بطاقة"]
        found_words = [word for word in suspicious_words if word in message]
       
        if found_words:
            score += 3
            reasons.append(f"وجود كلمات حساسة ({', '.join(found_words)})")

        # 2. فحص طلب معلومات سرية (OTP)
        if re.search(r"(رمز|كود|OTP|OTP).*(تحقق|سري)", message, re.IGNORECASE):
            score += 4
            reasons.append("طلب رمز تحقق (OTP) أو معلومات سرية")

        # 3. فحص الروابط (URLs)
        # نبحث عن أي رابط يبدأ بـ http أو www
        urls = re.findall(r'(https?://\S+|www\.\S+)', message)
        if urls:
            score += 2
            reasons.append("وجود رابط إلكتروني في الرسالة")
            # إذا كان الرابط مختصر (مثل bit.ly) خطورته أعلى
            if any(short in urls[0].lower() for short in ["bit.ly", "tinyurl", "t.co", "goo.gl"]):
                score += 3
                reasons.append("رابط مختصر مشبوه (يخفي الوجهة الحقيقية)")

        # 4. إعطاء النتيجة بناءً على النقاط
        if score >= 6:
            st.error("🚨 **احترس! هذه الرسالة احتيال بشكل مؤكد.**")
            st.write("**الأسباب:**")
            for r in reasons: st.write(f"- {r}")
            st.write("**نصيحة:** لا تضغط على أي روابط، ولا ترسل أي معلومات بنكية أو رمز تحقق (OTP).")
        elif score >= 3:
            st.warning("⚠️ **تحذير: هذه الرسالة مشبوهة.**")
            st.write("**الأسباب:**")
            for r in reasons: st.write(f"- {r}")
            st.write("**نصيحة:** تواصل مع الجهة المرسلة عبر رقمها الرسمي للتأكد.")
        else:
            st.success("✅ **الرسالة تبدو آمنة.**")
            st.write("ولكن تذكر دائماً عدم مشاركة معلوماتك الشخصية.")
    else:
        st.warning("الرجاء إدخال رسالة أولاً.")

import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="أمان", page_icon="🛡️", layout="centered")

# إخفاء شعار Streamlit وتكبير الخط
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            /* تكبير الخط الأساسي ليناسب كبار السن */
            html, body, [class*="css"]  {
                font-size: 20px !important;
                text-align: right;
            }
[data-testid="stStatusWidget"] {visibility:hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# عرض اللوجو
# تأكدي أن الصورة مرفوعة بنفس الاسم logo.png
st.image("logo.png", width=200)

# عنوان التطبيق
st.title("تطبيق أمان")
st.write("أهلاً بك! الصق الرسالة المشبوهة هنا وسنقوم بتحليلها.")

# مربع لكتابة الرسالة
message = st.text_area("الرسالة:", height=150)

# زر التحليل
if st.button("تحليل الرسالة", use_container_width=True):
    if message:
        st.success("تم استلام الرسالة! (هذا مجرد اختبار لنجاح التشغيل)")
    else:
        st.warning("الرجاء إدخال رسالة أولاً.")

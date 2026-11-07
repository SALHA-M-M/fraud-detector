import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="امان", page_icon="🛡️")

st.title("🛡️تطبيق امان")
st.write("أهلاً بك! الصق الرسالة المشبوهة هنا وسنقوم بتحليلها.")

# مربع لكتابة الرسالة
message = st.text_area("الرسالة:", height=150)

# زر التحليل
if st.button("تحليل الرسالة"):
    if message:
        st.success("تم استلام الرسالة! (هذا مجرد اختبار لنجاح التشغيل)")
    else:
        st.warning("الرجاء إدخال رسالة أولاً.")

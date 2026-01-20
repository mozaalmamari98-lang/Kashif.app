import streamlit as st
import google.generativeai as genai
from PIL import Image

# إعداد واجهة التطبيق
st.set_page_config(page_title="كاشف الدواء الذكي", page_icon="💊")
st.title("💊 تطبيق كاشف الدواء الذكي")
st.write("ارفع صورة الدواء أو استخدم الكاميرا وسأعطيك معلومات عنها.")

# إعداد مفتاح API (استخدم مفتاح Gemini 1.5 Flash الخاص بك)
API_KEY = "ضـع_مفتاحك_هنا"
genai.configure(api_key=API_KEY)

# خيارات إدخال الصورة
source = st.camera_input("التقط صورة للدواء")

if source is not None:
    image = Image.open(source)
    if st.button('تحليل الدواء الآن'):
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = "تعرف على الدواء واذكر دواعي الاستعمال والجرعة المعتادة باختصار شديد باللغة العربية."
        
        with st.spinner('جاري التحليل...'):
            response = model.generate_content([prompt, image])
            st.success("النتيجة:")
            st.write(response.text)

st.caption("ملاحظة: هذا التطبيق تعليمي ولا يغني عن استشارة الطبيب.")

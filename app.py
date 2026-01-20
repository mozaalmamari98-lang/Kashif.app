import streamlit as st
import google.generativeai as genai
from PIL import Image

# إعدادات الصفحة لتشبه واجهة التطبيق
st.set_page_config(page_title="كاشف الدواء", layout="centered")

# تنسيق CSS لجعل الواجهة احترافية (الألوان والخطوط)
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #2e5bc0; color: white; height: 3em; font-weight: bold; }
    .welcome-card { background-color: #1e3a8a; color: white; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 20px; }
    .info-box { background-color: white; padding: 15px; border-radius: 10px; border-left: 5px solid #2e5bc0; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# الجزء العلوي (الترحيب)
st.markdown('<div class="welcome-card"><h1>مرحباً بك</h1><p>شريكك الصحي الذكي لضمان تناول أدويتك بأمان.</p></div>', unsafe_allow_html=True)

# أزرار الوظائف الإضافية
col1, col2 = st.columns(2)
with col1:
    st.button("📋 خطة الطبيب")
with col2:
    st.button("📁 السجل")

# محرك البحث
search = st.text_input("🔍 ابحث عن دواء بالاسم...")

# إعداد الذكاء الاصطناعي (ضع مفتاحك هنا)
API_KEY = "AIzaSyDb1X2IhoTJbPIT1qMne3Y-rW7J0MI0pOY"
genai.configure(api_key=API_KEY)

# خيارات التصوير والرفع
st.write("---")
source_option = st.radio("اختر طريقة الإدخال:", ("📸 التقط صورة", "🖼️ من الاستوديو"))

if source_option == "📸 التقط صورة":
    img_file = st.camera_input("التقط صورة واضحة للعبوة")
else:
    img_file = st.file_uploader("اختر صورة من الاستوديو", type=['png', 'jpg', 'jpeg'])

if img_file is not None:
    image = Image.open(img_file)
    st.image(image, caption="الصورة التي تم اختيارها", use_container_width=True)
    
    if st.button('ابدأ المسح الذكي'):
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = "أنت صيدلي خبير. تعرف على هذا الدواء من الصورة واذكر: 1- الاسم العلمي والتجاري 2- دواعي الاستعمال 3- الجرعة المعتادة 4- تحذيرات هامة. اجعل الإجابة منظمة جداً وباللغة العربية."
        
        with st.spinner('جاري المسح والتحليل...'):
            try:
                response = model.generate_content([prompt, image])
                st.markdown('<div class="info-box">', unsafe_allow_html=True)
                st.subheader("✅ نتيجة الفحص:")
                st.write(response.text)
                st.markdown('</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"حدث خطأ: تأكد من مفتاح API الخاص بك. {e}")

# التذييل
st.write("---")
st.caption("📍 الصيدلانية موزة المعمري | مركز وادي بني عمر الصحي")
st.warning("تنبيه: المعلومات ناتجة عن ذكاء اصطناعي. استشر الطبيب دائماً.")

import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="كاشف الدواء الذكي", layout="centered")

# 2. تنسيق الواجهة لتطابق AI Studio (الألوان والخطوط)
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    .header-box { background-color: #1e3a8a; color: white; padding: 1.5rem; border-radius: 15px; text-align: center; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .stButton>button { width: 100%; border-radius: 25px; background-color: #2563eb; color: white; font-weight: bold; border: none; transition: 0.3s; }
    .stButton>button:hover { background-color: #1e40af; border: none; }
    .info-card { background-color: white; padding: 20px; border-radius: 15px; border-right: 5px solid #2563eb; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 15px; direction: rtl; }
    .footer { text-align: center; color: #64748b; margin-top: 50px; border-top: 1px solid #e2e8f0; padding-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 3. واجهة المستخدم العلوية
st.markdown('<div class="header-box"><h1>مرحباً بك</h1><p>شريكك الصحي الذكي لضمان تناول أدويتك بأمان</p></div>', unsafe_allow_html=True)

# أزرار الوظائف الجانبية (مثل AI Studio)
col1, col2 = st.columns(2)
with col1:
    st.button("📋 خطة الطبيب")
with col2:
    st.button("📁 السجل")

# 4. إعداد الاتصال بالذكاء الاصطناعي
# ارفقي مفتاحك هنا بين علامات التنصيص
API_KEY = "AIzaSyDb1X2IhoTJbPIT1qMne3Y-rW7J0MI0pOY"
genai.configure(api_key=API_KEY)

# 5. منطقة رفع الصور والبحث
st.write("---")
search_query = st.text_input("🔍 ابحث عن دواء بالاسم...")

input_method = st.radio("اختر طريقة الفحص:", ("📸 تصوير عبوة الدواء", "🖼️ رفع صورة من الاستوديو"))

if input_method == "📸 تصوير عبوة الدواء":
    img_file = st.camera_input("التقط صورة واضحة")
else:
    img_file = st.file_uploader("اختر صورة الدواء من هاتفك", type=['png', 'jpg', 'jpeg'])

# 6. معالجة الصورة وإظهار النتائج
if img_file is not None:
    image = Image.open(img_file)
    st.image(image, caption="تم رفع الصورة بنجاح", use_container_width=True)
    
    if st.button('✨ ابدأ المسح الذكي'):
        # استخدام النسخة الأحدث والأسرع
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = """
        أنت صيدلي خبير ومساعد طبي ذكي. حلل هذه الصورة واستخرج المعلومات التالية بدقة وباللغة العربية:
        1. اسم الدواء (التجاري والعلمي).
        2. الاستخدامات الأساسية لهذا الدواء.
        3. الجرعة المعتادة (مع تنبيه بضرورة استشارة الطبيب).
        4. التحذيرات الهامة والآثار الجانبية الشائعة.
        نسق الإجابة في نقاط واضحة وجميلة.
        """
        
        with st.spinner('⏳ جاري تحليل مكونات الدواء...'):
            try:
                response = model.generate_content([prompt, image])
                st.markdown('<div class="info-card">', unsafe_allow_html=True)
                st.subheader("📝 تقرير فحص الدواء:")
                st.write(response.text)
                st.markdown('</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"عذراً، حدث خطأ أثناء الاتصال بالخادم. تأكد من جودة الصورة. الخطأ: {e}")

# 7. تذييل الصفحة (Footer)
st.markdown(f"""
    <div class="footer">
        <p>📍 تم التطوير بواسطة: <b>الصيدلانية موزة المعمري</b></p>
        <p>مركز وادي بني عمر الصحي</p>
        <p style='font-size: 0.8em; color: #ef4444;'>⚠️ إخلاء مسؤولية: هذا التطبيق تعليمي، استشر طبيبك دائماً قبل تناول أي دواء.</p>
    </div>
    """, unsafe_allow_html=True)
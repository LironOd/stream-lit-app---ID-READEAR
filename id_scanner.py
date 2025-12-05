import streamlit as st
from PIL import Image
import pytesseract
import re
import sys

# ------------------------------------------------------------------
# CONFIGURATION & SETUP
# ------------------------------------------------------------------
# Instructions:
# 1. Install Python libraries: pip install streamlit pytesseract pillow
# 2. Install Tesseract OCR Software:
#    - Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
#    - Mac: brew install tesseract
#    - Linux: sudo apt-get install tesseract-ocr
# 3. If Tesseract is not in your PATH, uncomment the line below and set the path:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# ------------------------------------------------------------------

st.set_page_config(page_title="Liron's ID Scanner", page_icon="🆔")

# 1. Greeting
st.title("Hi Liron 👋")
st.write("Ready to scan your document.")

# 2. Upload
st.divider()
st.header("Upload ID Photo")
uploaded_file = st.file_uploader("Choose an image file (JPG, PNG)...", type=["jpg", "jpeg", "png"])

# 3. Processing
if uploaded_file is not None:
    # Display the image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_container_width=True)

    st.divider()
    
    if st.button('🔍 Scan ID'):
        with st.spinner('Scanning image for text...'):
            try:
                # Perform OCR
                # Note: lang='eng' is default. For Hebrew, you need the Hebrew data pack 
                # installed and change this to lang='heb+eng'
                extracted_text = pytesseract.image_to_string(image, lang='eng')

                if not extracted_text.strip():
                    st.warning("Could not detect any clear text. Please try a clearer photo.")
                else:
                    st.success("Scan Complete!")
                    
                    # Create two columns for layout
                    col1, col2 = st.columns(2)

                    with col1:
                        st.subheader("📝 Raw Text")
                        st.text_area("Content", extracted_text, height=200)

                    with col2:
                        st.subheader("🆔 Detected Details")
                        
                        # --- Basic Extraction Logic ---
                        # 1. Try to find a 9-digit ID number (Common in Israel)
                        id_pattern = r'\b\d{9}\b'
                        id_match = re.search(id_pattern, extracted_text)
                        
                        # 2. Try to find dates (DD/MM/YYYY)
                        date_pattern = r'\d{2}[/.]\d{2}[/.]\d{4}'
                        dates_found = re.findall(date_pattern, extracted_text)

                        # Display findings
                        if id_match:
                            st.metric(label="ID Number", value=id_match.group(0))
                        else:
                            st.info("No 9-digit ID number found.")

                        if dates_found:
                            st.write("**Dates found:**")
                            for date in dates_found:
                                st.code(date)
                        else:
                            st.info("No dates detected.")

            except pytesseract.TesseractNotFoundError:
                st.error("❌ Tesseract OCR is not found on this computer.")
                st.info("Please install Tesseract OCR software to run the scan (see code comments).")
                if sys.platform.startswith('win'):
                    st.markdown("[Download Tesseract for Windows](https://github.com/UB-Mannheim/tesseract/wiki)")
            except Exception as e:
                st.error(f"An error occurred: {e}")

else:
    st.info("Please upload an image to begin.")
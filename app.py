from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai 
import fitz

genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))

#func to load gemini pro vision
model = genai.GenerativeModel('gemini-pro-vision')

def gemini_get_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])  # in gemini, it takes parameters in a list
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{'mime_type': uploaded_file.type, "data": bytes_data}]
        return image_parts
    else:
        raise FileNotFoundError("No File Uploaded")

st.set_page_config(page_title='MultiLanguage Invoice Extractor')
st.header('Gemini App')
input_prompt = st.text_input('Input Prompt', key='input')
uploaded_file = st.file_uploader('Choose an image or PDF of invoice...', type=["jpg", "jpeg", "png", "pdf"])
image = None  # Initialize the variable outside the conditional block

if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        # If the uploaded file is a PDF, convert it to an image
        pdf_file = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        page = pdf_file.load_page(0)
        pix = page.get_pixmap()
        image = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    else:
        # If the uploaded file is an image, open it directly
        image = Image.open(uploaded_file)

    st.image(image, caption='Uploaded Image.', use_column_width=True)

submit = st.button("Tell me about the Resume")
input_prompt = """
You are expert in understanding Resumes. We will uplaod an image as Resume and you have to answer any questions based on uploaded Resume image
"""

if submit:
    if image is not None:  # Check if the image is defined
        image_data = input_image_details(uploaded_file)
        response = gemini_get_response(input_prompt, image_data, input_prompt)
        st.subheader('The Response is')
        st.write(response)
    else:
        st.warning("Please upload a valid image or PDF file.")

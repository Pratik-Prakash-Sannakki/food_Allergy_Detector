from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai 
import fitz
from audio import record_audio
import time
from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr


# Button to trigger audio recording


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


def wav_to_text():
    # Initialize the recognizer
    recognizer = sr.Recognizer()
    # Path to the WAV file
    wav_path = "recording0.wav"

    # Load the audio file
    audio_file = sr.AudioFile(wav_path)

    with audio_file as source:
        # Adjust for ambient noise and record the audio
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.record(source)

        try:
            # Use Google Web Speech API to convert audio to text
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            print("Google Web Speech API could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Web Speech API; {e}")



def show_audio_player(mp3_path):

    # Use st.audio to display audio player controls
    st.audio(mp3_path, format="audio/mp3", start_time=0)
    time.sleep(7)
    st.success("speak")
    recording = record_audio()
    st.success("Audio recording completed successfully!")
 

# Path to the MP3 file in the same directory
mp3_path = "welcome.mp3"

# Call the function with the MP3 path
show_audio_player(mp3_path)


import speech_recognition as sr



# Convert WAV to text





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




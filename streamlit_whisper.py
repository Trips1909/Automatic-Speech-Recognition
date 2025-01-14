import streamlit as st
import speech_recognition as sr
import tempfile
import os
import whisper

st.title('Audio Transcription and Live Speech to Text')

# Initialize the recognizer
recognizer = sr.Recognizer()

# Function to save audio to a temporary file
def save_audio_to_file(audio):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
        temp_audio_file.write(audio.get_wav_data())
        return temp_audio_file.name

# Initialize Whisper model
whisper_model = whisper.load_model("base")

# Initialize variables for live speech-to-text
capturing = False
captured_audio = None
audio_file_path = None

# Streamlit UI
st.title("Whisper App")

# Upload audio file with Streamlit
audio_file = st.file_uploader("Upload Audio", type=["wav", "mp3", "m4a"])

# Streamlit function to get the file path
def get_audio_file_details(file):
    file_details = {"Filename": file.name, "FileType": file.type, "FileSize": file.size}
    return file_details

# Start/Stop button for live speech-to-text
if not capturing and st.button('Start Recording'):
    capturing = True
    st.write("Recording... Speak into the microphone.")
    with sr.Microphone() as source:
        captured_audio = recognizer.listen(source, timeout=None)
    st.write("Recording stopped.")
    audio_file_path = save_audio_to_file(captured_audio)

if audio_file_path:
    st.write("Audio captured and saved.")
    st.audio(audio_file_path)

    if capturing and st.button('Stop Recording'):
        capturing = False

if not capturing and audio_file_path:
    st.write("Recording complete. You can now convert to text or transcribe.")

    # Transcribe audio using Whisper
    if st.button('Transcribe Audio'):
        st.write("Transcribing audio...")
        transcription = whisper_model.transcribe(audio_file_path)
        st.success("Transcription Complete")
        st.text(transcription["text"])

    # Convert audio to text using live speech recognition
    if st.button('Convert to Text'):
        st.write("Converting audio to text...")
        try:
            with sr.AudioFile(audio_file_path) as audio_file:
                audio_data = recognizer.record(audio_file)
                language = st.selectbox("Select Language", ["en-US", "hi-IN", "fr-FR", "es-ES", "de-DE"])
                text = recognizer.recognize_google(audio_data, language=language, show_all=False)
                st.success("Text Result:")
                st.write(text)
        except sr.UnknownValueError:
            st.warning("No speech detected")
        except sr.RequestError as e:
            st.error("Error while requesting results: {0}".format(e))

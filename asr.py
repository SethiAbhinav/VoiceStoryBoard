import whisper
import speech_recognition as sr
import streamlit as st

@st.cache_resource()
def load_whisper():
    whisper_small = whisper.load_model("small")
    return whisper_small


def whisper_asr():
    model = load_whisper()
    result = model.transcribe('./voices/user_response.wav', fp16=False)
    transcribed_user_response = result['text']
    return transcribed_user_response
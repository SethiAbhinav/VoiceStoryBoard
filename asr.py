import speech_recognition as sr
import requests
import soundfile as sf
import whisper
import speech_recognition as sr
from utils import get_user_voice_input, generate_ai_response

import soundfile as sf

def whisper_asr(audio_file_path):
    model = whisper.load_model("base")
    result = model.transcribe('./voices/user_response.wav', fp16=False)
    transcribed_user_response = result['text']
    return transcribed_user_response


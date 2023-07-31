import whisper
import speech_recognition as sr

def whisper_asr():
    model = whisper.load_model("base")
    result = model.transcribe('./voices/user_response.wav', fp16=False)
    transcribed_user_response = result['text']
    return transcribed_user_response
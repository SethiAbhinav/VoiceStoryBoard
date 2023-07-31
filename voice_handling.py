from elevenlabs import generate, play, set_api_key, stream, save
from utils import format_output
# from pydub import AudioSegment
import json
import os
import streamlit as st

@st.cache_data(show_spinner=True)
def play_dialogues(story_metadata):
    character_voices = format_output(story_metadata)
    if len(story_metadata['Dialogues']) <= 1:
        try:
            dialogues = story_metadata['Dialogues'][0]
        except:
            dialogues = story_metadata['Dialogues']
    else:
        dialogues = story_metadata['Dialogues']

    audio_files = []
    print(dialogues)
    for idx, role in enumerate(dialogues):
        try:
            character = role['Character'].strip()
            dialogue = role['Dialogue'].strip()
        except:
            character = dialogues['Character']
            dialogue = dialogues['Dialogue']

        voice_path = f'voices/voice_{idx}_{character}.wav'
        voice = character_voices[character]
        audio = generate(text = dialogue, voice = voice)
        save(audio, voice_path)

        audio_files.append(voice_path)
    return audio_files, character_voices
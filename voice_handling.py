from elevenlabs import generate, play, set_api_key, stream, save
from utils import format_output
# from pydub import AudioSegment
import json
import os
import streamlit as st

@st.cache_data(show_spinner=True)
def play_dialogues(story_metadata):
    f = 0
    character_voices = format_output(story_metadata)
    # print(99)
    # print(story_metadata['Dialogues'])
    # print(type(story_metadata['Dialogues']))

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
        # print(role)
        # print(type(role))
        try:
            character = role['Character'].strip()
            dialogue = role['Dialogue'].strip()
        except:
            character = dialogues['Character']
            dialogue = dialogues['Dialogue']
            # f = 1


        voice_path = f'voices/voice_{idx}_{character}.wav'
        voice = character_voices[character]
        audio = generate(text = dialogue, voice = voice)
        save(audio, voice_path)

        audio_files.append(voice_path)
        # if f==1:
            # break

    # print(101)
    return audio_files, character_voices
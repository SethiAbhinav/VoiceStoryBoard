import json
import random
from elevenlabs import generate, play, set_api_key, stream
import speech_recognition as sr
import openai
import streamlit as st

# Load the voice data
with open('data/voice_data.json', 'r') as file:
    voice_data = json.load(file)

def is_dialogue_format(script):
    """
    Check if the script is already in dialogue format.
    """
    # Split the script into lines
    lines = script.split('\n')
    
    # Check each line
    for line in lines:
        # If the line doesn't contain a colon, it's not in dialogue format
        if line and (':' not in line):
            return False
    
    # If all lines are in dialogue format, return True
    return True

def extract_dialogues(script):
    # Split the script into lines
    lines = script.split('\n')
    
    # Initialize an output dictionary
    output = {"Characters": set(), "Dialogues": []}
    
    # Iterate over each line
    for line in lines:
        # Check if the line is in dialogue format
        if ':' in line:
            # Split the line into character and dialogue
            character, dialogue = line.split(':', maxsplit = 1)
            
            output['Characters'].add(character.strip())
            # Add the character and dialogue to the output
            output["Dialogues"].append({"Character": character.strip(), "Dialogue": dialogue.strip()})
    
    return output

# @st.cache_data()
def format_output(story_metadata):
    # Prepare a dictionary to store the voice assignment for each character
    character_voices = {}

    # Get the list of voice names
    voice_names = list(voice_data.keys())

    # Assign a unique voice to each character
    for character in story_metadata["Characters"].split(','):
        if character in character_voices:
            continue
        character = character.strip()
        f = 0
        while f==0:
            voice_name = random.choice(voice_names)
            try:
                audio = generate('Hi', voice = voice_name)
                f = 1
            except:
                continue
        character_voices[character] = voice_name
        # Remove the chosen voice from the list so it won't be used for another character
        voice_names.remove(voice_name)
        # st.write(f'**Update:** Voice {voice_name} removed from avaliable voices. {voice_name} attached with character {character}')
        st.markdown(f'**Voice has been added for _{character}_**.')
    
    for role in story_metadata['Dialogues']:
        try:
            character = role['Character']
        except:
            continue
        dialogue = role['Dialogue']

        # Split the line into character name and dialogue
        character = character.strip()
        dialogue = dialogue.strip()

        # Get the voice ID
        voice_id = voice_data[character_voices[character]]['id']

        # print('Character:', character, '| Voice ID:', voice_id, '| Dialogue:', dialogue)

        # # Generate the voice
        # voice = stream(generate(dialogue, voice=voice_id, stream = True, latency = 3)) # Could not pursue due to Streamlit issues with mpv.
        # st.write(f'{character}: {dialogue}')
        # play(voice)
    return character_voices

def get_user_voice_input():
    # Initialize recognizer class (for recognizing the speech)
    r = sr.Recognizer()

    # Use the microphone as source for input
    with sr.Microphone() as source:
        print("Listening...")
        # Read the audio data from the default microphone
        audio_data = r.record(source, duration=5)
        print("Recognizing...")
        # Convert speech to text
        # text = r.recognize_google(audio_data)
        return audio_data

def generate_ai_response(transcribed_input, key):
    openai.api_key = key
    assistant_message = {
        'role': 'assistant',
        'content': "What did you like about the story? What did you learn from it?"
    }

    user_message = {
        'role': 'user',
        'content': transcribed_input
    }
    
    system_message = {
        'role': 'system',
        'content': 'if you don\'t understand the query, just say "Hope you had a great time with me and my friends - AI, of course." Otherwise, based on the user\'s query, reply and suggest something though provoking and insightful in one sentence. End the conersation on a happy note, thank them for using your service. Don\'t mention that you didn\t understand their query or that you are an AI language model.'
    }

    # Query the model
    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages = [assistant_message, user_message, system_message ]
    )

    # Extract the response
    return response['choices'][0]['message']['content']

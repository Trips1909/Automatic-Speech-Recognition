import pyttsx3
import json

def text_to_speech(speech_text, language):
    # Print the language to check if it's being passed correctly
    print(f"Language: {language}")

    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Set the default voice ID for languages other than Tamil
    default_voice_id = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_DAVID_11.0'

    # Set the voice for Tamil
    tamil_voice_id = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\MSTTS_V110_taIN_ValluvarM'

    # If the language is Tamil, use the Tamil voice; otherwise, use the default voice
    if language.lower() == 'tamil':
        engine.setProperty('voice', tamil_voice_id)
    else:
        engine.setProperty('voice', default_voice_id)

    # Provide the text you want to convert to speech
    engine.say(speech_text)

    # Play the generated speech
    engine.runAndWait()

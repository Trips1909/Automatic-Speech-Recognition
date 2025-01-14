from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os
import subprocess
from .transcribe import transcribe_received_audio
import pyaudio
import json # Import the subprocess module for running FFmpeg commands
from .tts import text_to_speech  # Import the Python function from tts.py
from .translate import trans_main
from .models import ButtonState
from .loop import Iterator
from .translate import trans_main

loop_iterator = Iterator()
# Store the transcribed and translated text in a global variable
transcription_result = None
translate_result=None
transliterate_result=None

# ASR_app/views.py
def home(request):
    button_state = ButtonState.objects.first()
    return render(request, 'home.html', {'button_state': button_state})


@csrf_exempt
# View to start the loop

def start_loop(request):
    audio_path = loop_iterator.save_audio_to_wav()
    try:
        button_state = ButtonState.objects.get(pk=1)  # Get the existing ButtonState object
    except ButtonState.DoesNotExist:
        button_state = ButtonState.objects.create(pk=1)  # Create a new ButtonState object if it doesn't exist

    if not button_state.is_active:
        button_state.is_active = True
        button_state.save()
        loop_iterator.start_loop()
    return JsonResponse({'status': 'success', 'audio_path': audio_path})

# View to stop the loop
def stop_loop(request):
    audio_path = loop_iterator.save_audio_to_wav()

    try:
        button_state = ButtonState.objects.get(pk=1)  # Get the existing ButtonState object
    except ButtonState.DoesNotExist:
        button_state = ButtonState.objects.create(pk=1)  # Create a new ButtonState object if it doesn't exist

    if button_state.is_active:
        button_state.is_active = False
        button_state.save()
        loop_iterator.stop_loop()
    return JsonResponse({'status': 'success', 'audio_path': audio_path})

def get_latest_audio_path(request):
    latest_audio_path = r"C:\Users\TARUN\OneDrive\Desktop\ASR_app_test\ASR_app (1)_copy1\ASR_app (1)\ASR_app\ASR\media\recorded_audio.wav"

    # Create a JSON response with the latest audio file path
    response_data = {
        "latest_audio_path": latest_audio_path,
    }

    return JsonResponse(response_data)



# views.py
def transcribe_audio(request):
    global transcription_result
    if request.method == 'POST':
        audio_path = r"C:\Users\TARUN\OneDrive\Desktop\ASR_app_test\ASR_app (1)_copy1\ASR_app (1)\ASR_app\ASR\media\recorded_audio.wav"
        
        # Check if the audio file exists at the specified path
        if os.path.exists(audio_path):
            # Define a new file path for the converted WAV file
            converted_audio_path = os.path.splitext(audio_path)[0] + '_converted.wav'

            # Get the user-specified number of speakers from the request
            num_speakers = int(request.POST.get('num_speakers', 2))  # Default to 2 speakers if not specified

            # Call the transcribe_received_audio function with the converted WAV file and num_speakers
            result = transcribe_received_audio(audio_path, num_speakers)

            # Delete the temporary converted audio file (if it was created)
            if audio_path == converted_audio_path:
                os.remove(converted_audio_path)
            
            transcription_result=result
            return result  # Return the result of transcribe_received_audio

        else:
            return JsonResponse({'message': 'Audio file not found.'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method.'}, status=400)



from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
import os
import numpy as np
import scipy.io.wavfile as wavfile

def serve_audio(request, audio_filename):
    audio_path = os.path.join(settings.MEDIA_ROOT, audio_filename)
    response = FileResponse(open(audio_path, 'rb'))
    return response

@csrf_exempt
def play_audio(request):
    action = request.POST.get('action', None)
    percentage = int(request.POST.get('percentage', 0))

    # Define the audio file path
    audio_file_path = r"C:\Users\TARUN\OneDrive\Desktop\ASR_app_test\ASR_app (1)_copy1\ASR_app (1)\ASR_app\ASR\media\recorded_audio.wav"

    # Initialize PyAudio and open the audio stream
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    output=True)

    message = ''  # Initialize the message variable

    if action == 'play':
        # Play audio from the specified percentage
        audio_data = read_audio_from_percentage(audio_file_path, percentage)
        stream.write(audio_data.tobytes())
        message = 'Playing'
    elif action == 'pause':
        # Pause audio playback
        stream.stop_stream()
        message = 'Paused'
    elif action == 'seek':
        # Seek to the specified percentage
        audio_data = read_audio_from_percentage(audio_file_path, percentage)
        stream.stop_stream()
        stream.start_stream()
        stream.write(audio_data.tobytes())
        message = 'Seeking to ' + str(percentage) + '%'

    # Close the audio stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    return JsonResponse({'message': message})

#     return audio_data
def read_audio_from_percentage(audio_file_path, percentage):
    # Check if the provided percentage is within the valid range (0-100)
    if percentage < 0:
        percentage = 0
    elif percentage > 100:
        percentage = 100

    # Read the audio file
    sample_rate, audio_data = wavfile.read(audio_file_path)

    # Calculate the starting sample index based on the percentage
    start_sample = int((percentage / 100) * len(audio_data))

    # Define the duration you want to play from the starting sample (in seconds)
    duration_seconds = 10  # Adjust this as needed

    # Calculate the corresponding ending sample index
    end_sample = start_sample + int(duration_seconds * sample_rate)

    # Ensure that the end sample does not exceed the length of the audio data
    end_sample = min(end_sample, len(audio_data))

    # Extract the audio data for the specified duration
    audio_data_portion = audio_data[start_sample:end_sample]

    return audio_data_portion


def translate_text(request):
    global transcription_result
    global translate_result
    global transliterate_result
    if request.method == 'POST':
        audio_path = request.POST.get('audio_path', r"C:/Users/TARUN/OneDrive/Desktop/ASR_app_test/ASR_app (1)_copy1/ASR_app (1)/ASR_app/ASR/media/recorded_audio.wav")  
    
        # Check if the audio file exists at the specified path
        if os.path.exists(audio_path):
            # Define a new file path for the converted WAV file
            converted_audio_path = os.path.splitext(audio_path)[0] + '_converted.wav'

            # Call the transcribe_received_audio function with the converted WAV file
            result = transcription_result

            # Delete the temporary converted audio file (if it was created)
            if audio_path == converted_audio_path:
                os.remove(converted_audio_path)
        
            result = transcription_result
            # convert to dict
            ans_dict = json.loads(result.content.decode('utf-8'))
    
            # Remove the 'message' part
            ans_dict=ans_dict['message']
            
            # Convert the modified dictionary back to a JSON string
            desired_text = json.dumps(ans_dict)
            print(f"this is half part {desired_text}, this is its type {type(desired_text)} and this is whole text {result}")

            # Getting target language
            target_language= request.POST.get('target_language', 'en')  # Default to English ('en') if not specified
            language=target_language

            # Call your translation logic from translate.py
            translated_text, transliterate_text = trans_main(desired_text, language)
            translate_result=translated_text
            transliterate_result=transliterate_text

            # Create a JSON response
            response_data = {
                "translated_text": translated_text,
                "transliterate_text": transliterate_text,

            }

            return JsonResponse(response_data)
        else:
            return JsonResponse({'result': 'Audio file not found.'}, status=400)
    else:
        return JsonResponse({'result': 'Invalid request method.'}, status=400)

# views.py
def generate_audio(request):
    global translate_result
    global transliterate_result
    if request.method == 'POST':
        # Extract the target language from the request
        target_language = request.POST.get('targetLanguage', 'en')  # Default to 'en' if not specified

        # Ensure that the target_language received is correct by printing it
        print(f"Language: {target_language}")

        audio_path = r"C:\Users\TARUN\OneDrive\Desktop\ASR_app_test\ASR_app (1)_copy1\ASR_app (1)\ASR_app\ASR\media\recorded_audio.wav"

        # Check if the audio file exists at the specified path
        if os.path.exists(audio_path):
            # Define a new file path for the converted WAV file
            converted_audio_path = os.path.splitext(audio_path)[0] + '_converted.wav'

            # Delete the temporary converted audio file (if it was created)
            if audio_path == converted_audio_path:
                os.remove(converted_audio_path)

            try:
                # Call the text_to_speech function with the translated result and target language
                text_to_speech(transliterate_result, target_language)
                return JsonResponse({'result': converted_audio_path})
            except Exception as e:
                return JsonResponse({'result': str(e)}, status=500)

        else:
            return JsonResponse({'result': 'Audio file not found.'}, status=400)
    else:
        return JsonResponse({'result': 'Invalid request method.'}, status=400)

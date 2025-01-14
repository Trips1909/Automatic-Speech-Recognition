import whisper
import os
import torchaudio
import numpy as np
import soundfile as sf
from speechbrain.pretrained import EncoderClassifier
from sklearn.cluster import KMeans
from pyannote.audio.pipelines.speaker_verification import PretrainedSpeakerEmbedding
from pyannote.core import Segment
from django.http import JsonResponse

def transcribe_received_audio(audio_path, num_speakers=2):
    # Load the Whisper ASR model
    whisper_model_path = 'C:\\Users\\TARUN\\miniconda3\\Lib\\site-packages\\whisper\\model'
    model = whisper.load_model("small")

    # Transcribe the audio
    result = model.transcribe(audio_path)

    # Calculate the duration of the audio
    signal, sample_rate = torchaudio.load(audio_path)
    duration = signal.size(1) / sample_rate

    # Initialize a list for embeddings
    embeddings = []

    # Load the speaker embedding model
    classifier = EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb")

    # Define a function to calculate the segment embedding
    def segment_embedding(segment):
        start = segment["start"]
        # Whisper might overshoot the end timestamp in the last segment
        end = min(duration, segment["end"])
        clip = Segment(start, end)

        # Crop the audio segment using indexing
        start_frame = int(start * sample_rate)
        end_frame = int(end * sample_rate)
        segment_signal = signal[:, start_frame:end_frame]

        # Convert the signal to mono if it's stereo
        if segment_signal.shape[0] > 1:
            segment_signal = segment_signal.mean(dim=0, keepdim=True)

        # Encode the segment using the speaker embedding model
        segment_embedding = classifier.encode_batch(segment_signal)

        return segment_embedding[0].numpy()

    # Calculate embeddings for each segment
    for i, segment in enumerate(result['segments']):
        embeddings.append(segment_embedding(segment))

    # Flatten the embeddings
    flattened_embeddings = [emb.flatten() for emb in embeddings]

    # Perform K-means clustering for num_speakers
    kmeans = KMeans(n_clusters=num_speakers, random_state=0).fit(flattened_embeddings)
    labels = kmeans.labels_

    # Assign speakers based on clustering
    speakers = [f"Speaker {label + 1}" for label in labels]

    # Add speaker information to the result segments
    for i, segment in enumerate(result['segments']):
        segment["speaker"] = speakers[i]

    # Prepare the transcriptions with speaker information
    transcriptions = [{"speaker": speakers[i], "text": segment["text"]} for i, segment in enumerate(result['segments'])]
    print(f"transcription text is : {transcriptions}")

    # To convert according to app.json
    message = "\n".join([f"{item['speaker']}: {item['text']}" for item in transcriptions])

    # Create a dictionary to match the expected format in your JavaScript code
    response_data = {'message': message}
    print(f"This is JsonResponse of transcribed_received_audio {response_data}")
    return JsonResponse(response_data, safe=False)

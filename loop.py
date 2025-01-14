# # iterator.py

# import time

# class Iterator:
#     def __init__(self):
#         self.running = False

#     def start_loop(self):
#         self.running = True
#         while self.running:
#             print("Loop is running...")
#             time.sleep(1)

#     def stop_loop(self):
#         self.running = False
#         print("loop terminated")


import time
import pyaudio
import wave
from django.conf import settings
import os

class Iterator:
    def __init__(self):
        self.running = False
        self.audio_stream = None
        self.audio_frames = []
        self.audio_format = pyaudio.paInt16
        self.audio_channels = 1
        self.audio_rate = 44100
        self.audio_chunk = 1024

    def start_loop(self):
        self.running = True
        self.audio_frames = []  # Clear any previous audio frames
        self.audio_stream = self.initialize_audio_stream()

        while self.running:
            print("Recording...")
            audio_data = self.audio_stream.read(self.audio_chunk)
            self.audio_frames.append(audio_data)

    def stop_loop(self):
        if self.running:
            self.running = False
            print("Recording stopped...")
            self.audio_stream.stop_stream()
            self.audio_stream.close()

            # Save the recorded audio to a WAV file
            self.save_audio_to_wav()

    def initialize_audio_stream(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=self.audio_format,
                        channels=self.audio_channels,
                        rate=self.audio_rate,
                        input=True,
                        frames_per_buffer=self.audio_chunk)
        return stream

    # def save_audio_to_wav(self):
    #     if self.audio_frames:
    #         p = pyaudio.PyAudio()
    #         wf = wave.open("recorded_audio.wav", 'wb')
    #         wf.setnchannels(self.audio_channels)
    #         wf.setsampwidth(p.get_sample_size(self.audio_format))
    #         wf.setframerate(self.audio_rate)
    #         wf.writeframes(b''.join(self.audio_frames))
    #         wf.close()
    def save_audio_to_wav(self):
        if self.audio_frames:
            p = pyaudio.PyAudio()
            audio_filename = f"recorded_audio.wav"
            audio_path = os.path.join(settings.MEDIA_ROOT, audio_filename)
            wf = wave.open(audio_path, 'wb')
            wf.setnchannels(self.audio_channels)
            wf.setsampwidth(p.get_sample_size(self.audio_format))
            wf.setframerate(self.audio_rate)
            wf.writeframes(b''.join(self.audio_frames))
            wf.close()
            return audio_path  # Return the path to the saved audio file


if __name__ == "__main__":
    iterator = Iterator()
    iterator.start_loop()
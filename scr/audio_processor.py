# audio_processor.py
import speech_recognition as sr
from gtts import gTTS
import os

class AudioProcessor:
    def __init__(self):
        self.recognizer = sr.Recognizer()
    
    def process_audio(self, audio_file):
        with sr.AudioFile(audio_file) as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio_data = self.recognizer.record(source)
            return self.recognizer.recognize_google(audio_data)
            
        # Process audio file
        with sr.AudioFile(audio_path) as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio_data = self.recognizer.record(source)
            return self.recognizer.recognize_google(audio_data)
    
    def text_to_speech(self, text):
        tts = gTTS(text=text, lang='en')
        response_path = os.path.join('static', 'audio', 'response.mp3')
        tts.save(response_path)
        return '/static/audio/response.mp3'


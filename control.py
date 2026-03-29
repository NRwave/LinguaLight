import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
from langdetect import detect
from deep_translator import GoogleTranslator
import serial
import speech_recognition as sr
import time

import constants 
#from Catagorizing_Speech import detect_tone, keyword_indication
HIGH_THRESHOLD = 500
LOW_THRESHOLD = 150

LANGUAGES = ["en-US", "es-ES"]

INTERROGATIVE_KEYWORDS = ["who", "what", "when", "where", "why", "who", "is", "are", "do", "does", "can", "could", "would", "may"]
EXCLAMATORY_KEYWORDS = ["wow", "awesome", "amazing", "crazy", "unbelievable", "yay", "woohoo", "oops", "whoops", "oopsie", "uh oh", "oh no", "weee", "aw, man", "ouch", "owie", "mmm", "yum", "yuck", "ick", "ew", "woah", "cool"]
FILLER_WORDS = ["um", "like", "so", "uh", "you know", "you see"]
arduino = serial.Serial('COM3', 9600)  # Replace COM3 with your port
time.sleep(2)

def clean_text(text):
    lowercase_text = text.lower()
    lowercase_text = lowercase_text.strip()
    lowercase_text = lowercase_text.split()
    
    return lowercase_text

    
def keyword_indication(text):
    cleaned_text = clean_text(text)
    for word in cleaned_text:
        
        if word in EXCLAMATORY_KEYWORDS:
            return "Emotional"
    
    if(cleaned_text and cleaned_text[0] in INTERROGATIVE_KEYWORDS):
        return "Pondering"

    else:
        return "Neutral"
    
def detect_tone(recorded_input, sample_rate):
    
   
    frequency = np.fft.rfftfreq(len(recorded_input), 1/sample_rate)
    spectrum = np.abs(np.fft.rfft(recorded_input))
    dominant_frequency = frequency[np.argmax(spectrum)]
    print(f"Dominant Frequency: {dominant_frequency}")

    if dominant_frequency > HIGH_THRESHOLD:
        return "High"
    
    elif dominant_frequency < LOW_THRESHOLD:
        return "Low"
    
    else:
        return "Neutral"
    
duration = 3
sample_rate = 44100
channels = 1
r = sr.Recognizer()

while True:
    
    recorded_input = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels)
    
    sd.wait()
    
    if len(recorded_input.shape) > 1:
        recorded_input = recorded_input.mean(axis = 1)
        
    recorded_input = recorded_input /np.max(np.abs(recorded_input) + 1e-6)

    recording_int16 = np.int16(recorded_input * 32767)

    write("speech_test.wav",sample_rate , recording_int16)

    
    with sr.AudioFile("speech_test.wav") as source:
        audio = r.record(source)
    det_lang = ""
    text_en = ""
    text_es = ""
    try:
        catagory = ""
        try:
            text_en= r.recognize_google(audio, language="en-US")
        except sr.UnknownValueError:
            text_en = ""
        try:
            text_es= r.recognize_google(audio, language="es-ES")  
        except sr.UnknownValueError:
             text_es = ""
             
        if(text_es and not text_en):
            text = text_es
            det_lang = "es"
        elif(text_en and not text_es):
            text = text_en
            det_lang = "en"
        elif(len(text_es) > len(text_en)):
            text = text_es
            det_lang = "es"
        else:
            text = text_en
            det_lang = "en"

        if not text.strip():  
            print("No speech detected, skipping language detection")
            continue
       
       
        if text == "stop":
            break
        if(det_lang == "es"):
            text = GoogleTranslator(source = 'es', target = 'en').translate(text)
            
        print(f"Current Language: {det_lang}")
        #if(detected_language != "en"):
           # text = GoogleTranslator(source='auto', target='en').translate(text)
        tone = detect_tone(recorded_input, sample_rate)
        keywords = keyword_indication(text)
        evaluations = (tone, keywords)
        print(text)

        match evaluations:

            case ("High", "Emotional"):
                catagory = "Exclamation"
                arduino.write(b'E\n')
                
            case ("High", "Pondering"):
                catagory = "Question"
                arduino.write(b'Q\n')

            case ("High", "Neutral"):
                catagory = "Exclamation"
                arduino.write(b'E\n')

            case ("Low", "Emotional"):
                catagory = "Exclamation"
                arduino.write(b'E\n')

            case ("Low", "Pondering"):
                catagory = "Question"
                arduino.write(b'Q\n')

            case ("Low", "Neutral"):
                catagory = "Statement"
                arduino.write(b'S\n')

            case ("Neutral", "Emotional"):
                catagory = "Exclamation"
                arduino.write(b'E\n')

            case ("Neutral", "Pondering"):
                catagory = "Question"
                arduino.write(b'Q\n')
                
            case ("Neutral", "Neutral"):
                catagory = "Statement"
                arduino.write(b'S\n')
                
        message = f"{catagory} Tone: {tone} Keywords: {keywords}"
        print(message)
        
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results; check your internet connection")
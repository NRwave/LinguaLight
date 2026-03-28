import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

duration = 5  
fs = 44100   

print("Recording...")
recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
sd.wait()
print("Done recording!")

recording_int16 = np.int16(recording * 32767)

write("speech_test.wav", fs, recording_int16)
import speech_recognition as sr

r = sr.Recognizer()

with sr.AudioFile("speech_test.wav") as source:
    audio = r.record(source)

try:
    text = r.recognize_google(audio)
    print("You said:", text)
except sr.UnknownValueError:
    print("Could not understand audio")
except sr.RequestError as e:
    print("Could not request results; check your internet connection")
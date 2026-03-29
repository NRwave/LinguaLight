from constants import FILLER_WORDS, EXCLAMATORY_KEYWORDS, INTERROGATIVE_KEYWORDS
import sounddevice as sd
import numpy as np
import constants

def clean_text(text):
    lowercase_text = text.lower()
    lowercase_text = lowercase_text.strip()
    lowercase_text = lowercase_text.split()
    
    return lowercase_text
    
def keyword_indication(text):
    cleaned_text = clean_text(text)
    index = 0
    for words in EXCLAMATORY_KEYWORDS:
        
        if cleaned_text[index] == words:
            return "Emotional"
        index += 1
    
    if(cleaned_text and cleaned_text[0] in INTERROGATIVE_KEYWORDS):
        return "Pondering"

    else:
        return "Neutral"
    
def detect_tone(recorded_input, sample_rate):
    
   
    frequency = np.fft.rfftfreq(len(recorded_input), 1/sample_rate)
    spectrum = np.abs(np.fft.rfft(recorded_input))
    dominant_frequency = frequency[np.argmax(spectrum)]
    
    if dominant_frequency > constants.HIGH_THRESHOLD:
        return "High"
    
    elif dominant_frequency < constants.LOW_THRESHOLD:
        return "Low"
    
    else:
        return "Neutral"
    
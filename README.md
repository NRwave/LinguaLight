# LinguaLight

About: This device called lingua-light takes speech from a microphone in various languages and outputs a light corresponding to the type of sentence(exclaition, question, or statement) to cue users on understanding of the language even if they do not know the words. 

What you need: This project relies on Arduino and establing a connection between python and arduino using the python serial library. YOu also need to download the numpy, deeptranslator, scipy.io.wavfile, soundevice, speech_recogntiion,and the time libraries. On top of this, this device relies on an external mic connected to the laptop and the device plugged into the laptop. 

Features
 - Tone and pitch detection using FFT
 - Sends command signals to arduino
 - Real-time audio using sound-device
 - Multilingual speech recognition from both English and Spanish

Clone Repository
Install Dependencies Using Pip
Connect Arduino to the COM port
Run program called control.py

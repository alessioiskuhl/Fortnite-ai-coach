import tkinter as tk
import subprocess
import sys
import pyautogui
import cv2
import numpy as np
from gtts import gTTS
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import scipy.io.wavfile as wav
import sounddevice as sd
import soundfile as sf
import time
from vosk import Model, KaldiRecognizer
import vosk
import wave
import json
import pyttsx3



#-----Window for OS selection-----
class Windows10StyleWindow(QMainWindow):
  def __init__(self):
    super().__init__()

    #Create Window with the title "Please select a language"
    self.setWindowTitle("Please select a language")
    self.setGeometry(100, 100, 200, 50) #x, y, width, height

    #Remove native title bar for a windows 10 look
    self.setWindowFlags(Qt.FramelessWindowHint)
    self.setStyleSheet("background-color: #ffffff;") # White background

    #Title Bar
    self.title_bar = QLabel("Please select a language", self)
    self.title_bar.setStyleSheet("background-color: #0078d7; color: white; padding: 10px; font-size: 10px;")
    self.title_bar.setAlignment(Qt.AlignCenter)
    self.title_bar.setGeometry(0, 0, 200, 20)

    # Main Content
    self.deutsch_button = QPushButton("Deutsch", self)
    self.deutsch_button.setStyleSheet("""
        QPushButton {
            background-color: #ff4d4d;
            border: none;
            color: white;
            font-size: 12px;
            padding: 5px 10px;                              
        }
        QPushButton:hover {
            background-color: #e60000;
        }
    """)
    self.deutsch_button.setGeometry(0, 0, 100, 50)
    self.english_button = QPushButton("English", self)
    self.english_button.setStyleSheet("""
        QPushButton {
            background-color: #ff4d4d;
            border: none;
            color: white;
            font-size: 12px;
            padding: 5px 10px;                              
        }
        QPushButton:hover {
            background-color: #e60000;
        }
    """)
    self.english_button.setGeometry(100, 0, 100, 50)
      

def install_python():
    #URL to the python installer (Windows)
    python_installer_url = "https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe"
    installer_path = "python_installer.exe"

    #download the installer
    print("Downloading Python installer...")
    subprocess.run(["curl", "-o", installer_path, python_installer_url], 
                   check=True)

    #Run the installer silently
    print("Installing Python...")
    subprocess.run([installer_path, "/quiet", "InstallAllUsers=1", "PrependPath=1"], 
                   check=True)

    #Cleanup
    os.remove(installer_path)
    print("Python installed succsessfully!")

def check_python():
    try:
        subprocess.check_call([sys.executable, '-c', 'import sys'])
        print("Python is installed!")
    except subprocess.CalledProcessError:
        print("Python is not installed. Installing...")
        install_python()
        # Install Python using the appropriate method for your system
        # Example for Windows using the official installer:
        # subprocess.run(["powershell", "-Command", "Start-Process -FilePath 'https://www.python.org/ftp/python/3.10.9/python-3.10.9-amd64.exe' -ArgumentList '/quiet /norestart'"])
        # Note: You may need to adapt this for your specific system and Python version
        print("Python installation complete!")

# ---open the Terminal and execute commands---
def execute_in_terminal():
    #Open a command Prompt and execute a Python command
    commands = [
        'echo "Hello from the Terminal!"'
        'python --version'
    ]
    for command in commands:
        subprocess.run(f"cmd /k {command}", shell=True)
        subprocess.run(['pip', 'install', 'sounddevice', 'pysoundfile'], check=True)
        subprocess.run(['pip', 'install', 'pyttsx3'], check=True)
        subprocess.run(['pip', 'install', 'opencv-python'], check=True)
        subprocess.run(['pip', 'install', 'pyautogui', 'mss'], check=True)
        subprocess.run(['pip', 'install', 'PyQt5'], check=True)
        subprocess.run(['pip', 'install', 'vosk'], check=True)
        subprocess.run(['pip', 'install', 'gtts'], check=True)
        subprocess.run(['wget', 'https://alphacephei.com/vosk/models/vosk-model-small-de-0.15.zip'], check=True)

if __name__ == "__main__":
    execute_in_terminal()



def start_coaching():
    print("Starting coaching!")
    # Add code to start capturing screen and analyzing
    # You'll need to implement the screen capture and analysis logic here
    # using pyautogui and cv2

def stop_coaching():
    print("Stopping coaching!")
    # Add code to stop capturing screen and analyzing

def open_settings():
    print("Opening settings!")
    # Add code to open the settings window (e.g., using a new tk window)
    # Add code to select monitor, audio input/output here

def capture_screen():
    # Capture the entire screen
    screenshot = pyautogui.screenshot()
    # Convert the screenshot to OpenCV format
    image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2RGB)
    return image

def analyze_screen(image):
    # Add code here to analyze the image and detect objects
    # (e.g., using OpenCV or other computer vision techniques)
    # ...
    # Example: Detect walls (you'll need to find specific color ranges)
    lower_wall_color = np.array([100, 100, 100])
    upper_wall_color = np.array([150, 150, 150])
    mask = cv2.inRange(image, lower_wall_color, upper_wall_color)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        print("Walls detected!")
    else:
        print("No walls detected.")

#-----Record when speaking-----
#Parameters
samplerate = 44100 # Sampling rate
duration_check = 0.5 # Duration to capture audio in chunks (seconds)
silence_threshold = 500 # Silence threshold (lower values = more sensitive)
max_silence_duration = 2 # Max silence duration (seconds)

def is_speaking(audio_chunk):
    """Check if audio Chunk is below silence threshold"""
    return np.abs(audio_chunk).mean() > silence_threshold

def record_on_speech():
    start_time = time.time()
    audio_chunks = []
    recording = False
    silence_start = None # Track when silence starts

    while True:
        #Record small chunks of audio
        audio_chunk = sd.rec(
            int(duration_check * samplerate),
            samplerate=samplerate,
            channels=1,
            dtype="int16",
        )
        sd.wait()

        if is_speaking(audio_chunk):
            if not recording:
                recording = True # Start recording
            audio_chunks.append(audio_chunk) # Add audio chunk to the buffer
            silence_start = None # Reset silence timer
        else:
            if recording:
                if silence_start is None:
                    silence_start = time.time()
                elif time.time() - silence_start > max_silence_duration:
                    break

    # Combinie all audio chunks into a single array
    audio_data = np.concatenate(audio_chunks, axis=0) if audio_chunks else None
    # Process audio directly in memory (or return it for further processing)
    return audio_data
    
# Start recording
audio_data = record_on_speech()



#-----translate the recording into text-----
# Initialize the vosk model (The Filename of the currently used vosk model)
model = vosk.Model("vosk-model-small-de-0.15.zip")
# Open the audio data as a .wav file
wf = wave.open(audio_data, "rb")
# Create the recognizer
rec = vosk.KaldiRecognizer(model, wf.getframerate())
# Process the audio file
while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        result = rec.Result()
        Result = json.loads(result)["Text"]


    


window = tk.Tk()
window.title("Fortnite AI Coach")

start_button = tk.Button(window, text="Start Coaching", command=start_coaching)
start_button.pack()

stop_button = tk.Button(window, text="Stop Coaching", command=stop_coaching)
stop_button.pack()

settings_button = tk.Button(window, text="Settings", command=open_settings)
settings_button.pack()

window.mainloop()

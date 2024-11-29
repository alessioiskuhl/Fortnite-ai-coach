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
import sounddevice as sd
import soundfile as sf
import time
from vosk import Model, KaldiRecognizer
import wave
import json



#-----Window for OS selection-----
class Windows10StyleWindow(QMainWindow):
  def __init__(self):
    super().__init__()

    #Create Window with the title "Please select an operating system"
    self.setWindowTitle("Please select an operating system")
    self.setGeometry(100, 100, 200, 50) #x, y, width, height

    #Remove native title bar for a windows 10 look
    self.setWindowFlags(Qt.FramelessWindowHint)
      

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
        subprocess.run(['pip', 'install', 'PyQt5-tools'], check=True)
        subprocess.run(['pip', 'install', 'vosk'], check=True)

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

def speak_advice(advice):
    tts = gTTS(text=advice, lang='en')
    tts.save("advice.mp3")
    os.system("mpg321 advice.mp3")  # Or use a different audio player

def record_audio():
    # Code to record audio using PyAudio
    # ...

def listen_and_respond(audio_data):
    try:
        r = sr.Recognizer()
        text = r.recognize_google(audio_data)
         # Process the text input (e.g., answer questions)
        print(f"You said: {text}")
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

window = tk.Tk()
window.title("Fortnite AI Coach")

start_button = tk.Button(window, text="Start Coaching", command=start_coaching)
start_button.pack()

stop_button = tk.Button(window, text="Stop Coaching", command=stop_coaching)
stop_button.pack()

settings_button = tk.Button(window, text="Settings", command=open_settings)
settings_button.pack()

window.mainloop()

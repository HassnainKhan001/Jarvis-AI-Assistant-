import speech_recognition as sr
import pyttsx3
import requests
import time
import json
import os
import logging
from threading import Thread
from face_detection import FaceDetector

# Setup Logging
logging.basicConfig(
    filename='listener.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Initialize TTS
try:
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # You can change to voices[1].id for a female voice
    engine.setProperty('rate', 170)
except Exception as e:
    print(f"Error initializing TTS: {e}")
    engine = None

# Initialize Face Detector
face_detector = None

def face_detected_callback(message):
    """Callback function when face is detected"""
    speak(message)

def speak(text):
    if engine:
        clean_text = text.replace('Jarvis:', '').replace('⚡', '').replace('⚠️', '').strip()
        print(f"Speaking: {clean_text}")
        logging.info(f"Jarvis Output: {clean_text}")
        try:
            engine.say(clean_text)
            engine.runAndWait()
        except Exception as e:
            logging.error(f"TTS Error: {e}")
    else:
        print(f"TTS disabled. Output: {text}")

def listen_for_command():
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True
    recognizer.dynamic_energy_adjustment_damping = 0.15
    recognizer.dynamic_energy_ratio = 1.5
    recognizer.pause_threshold = 0.8
    recognizer.operation_timeout = 5
    
    last_calibration = time.time()
    
    with sr.Microphone() as source:
        print("\n[INITIALIZING-SOURCE] Calibrating...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
        while True:
            try:
                # Periodic re-calibration
                if time.time() - last_calibration > 300: 
                    print("\n[RE-CALIBRATING] Noise levels...")
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    last_calibration = time.time()
                
                # Keep energy threshold reasonable
                if recognizer.energy_threshold < 50:
                    recognizer.energy_threshold = 300
                if recognizer.energy_threshold > 3500:
                    recognizer.energy_threshold = 3500

                print(f"\nListening (Thresh: {int(recognizer.energy_threshold)})...")
                try:
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                except sr.WaitTimeoutError:
                    continue # Silent restart loop
                
                logging.info("Audio captured, starting recognition...")
                text = recognizer.recognize_google(audio).lower()
                print(f"You said: {text}")
                logging.info(f"User heard: {text}")
                
                if "jarvis" in text or "hey jarvis" in text:
                    command = text.split("jarvis", 1)[-1].strip()
                    if command:
                        print(f"Processing command: {command}")
                        process_command_via_api(command)
                    else:
                        speak("Yes, sir?")
                        # Follow-up without wake word
                        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                        command = recognizer.recognize_google(audio).lower()
                        process_command_via_api(command)
                        
            except sr.UnknownValueError:
                logging.info("Speech not understood.")
                continue 
            except sr.RequestError as e:
                print(f"Network error: {e}")
                time.sleep(2)
            except Exception as e:
                print(f"Loop error: {e}")
                logging.error(f"Error in main listen loop: {e}")
                time.sleep(1)

def process_command_via_api(command):
    if not command:
        return
        
    url = "http://127.0.0.1:8000/api/ask"
    headers = {"Content-Type": "application/json"}
    payload = {"prompt": command}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            reply = data.get("response", data.get("error", "Error connecting to Jarvis core."))
            speak(reply)
        else:
            speak(f"System returned error code {response.status_code}.")
    except requests.exceptions.ConnectionError:
        speak("I cannot connect to the server. Please ensure the Django server is running.")
    except Exception as e:
        print(f"API Error: {e}")
        speak("I encountered a critical error communicating with the main system.")

if __name__ == "__main__":
    print("=======================================")
    print("      Jarvis Background Listener       ")
    print("=======================================")
    
    # Initialize and start face detection
    try:
        face_detector = FaceDetector(callback=face_detected_callback)
        face_detector.start_detection()
        print("Face detection enabled.")
    except Exception as e:
        print(f"Face detection failed to start: {e}")
        logging.error(f"Face detection failed: {e}")
    
    speak("Background listener activated.")
    
    try:
        listen_for_command()
    except KeyboardInterrupt:
        print("\nShutting down...")
        if face_detector:
            face_detector.stop_detection()
        print("Jarvis listener stopped.")

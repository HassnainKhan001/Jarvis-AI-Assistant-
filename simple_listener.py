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

# Initialize Face Detector
face_detector = None

def face_detected_callback(message):
    """Callback function when face is detected"""
    print(message)
    logging.info(f"Face detection: {message}")

def speak(text):
    """Simple text output since we don't have TTS without PyAudio"""
    clean_text = text.replace('Jarvis:', '').replace('⚡', '').replace('⚠️', '').strip()
    print(f"Jarvis: {clean_text}")
    logging.info(f"Jarvis Output: {clean_text}")

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

def listen_for_text_commands():
    """Listen for text commands instead of voice commands"""
    print("\n" + "="*50)
    print("      Jarvis Text Command Interface       ")
    print("="*50)
    print("Type your commands below (or 'quit' to exit):")
    print("Examples:")
    print("  - open google")
    print("  - search google for tradingview software")
    print("  - open tradingview")
    print("  - open chrome")
    print("  - search for python tutorial on google")
    print("="*50 + "\n")
    
    while True:
        try:
            command = input("You: ").strip()
            
            if command.lower() in ['quit', 'exit', 'stop']:
                print("Goodbye!")
                break
                
            if not command:
                continue
                
            print(f"Processing command: {command}")
            process_command_via_api(command)
                        
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            logging.error(f"Error in main loop: {e}")
            time.sleep(1)

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
        listen_for_text_commands()
    except KeyboardInterrupt:
        print("\nShutting down...")
        if face_detector:
            face_detector.stop_detection()
        print("Jarvis listener stopped.")

import cv2
import time
import threading
import logging
from datetime import datetime

class FaceDetector:
    def __init__(self, callback=None):
        self.callback = callback
        self.running = False
        self.last_greeting_time = 0
        self.greeting_cooldown = 30  # Wait 30 seconds between greetings
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Setup logging
        logging.basicConfig(
            filename='face_detection.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    def start_detection(self):
        """Start face detection in a separate thread"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._detect_faces)
            self.thread.daemon = True
            self.thread.start()
            logging.info("Face detection started")
            print("Face detection started...")
            
    def stop_detection(self):
        """Stop face detection"""
        self.running = False
        if hasattr(self, 'thread'):
            self.thread.join()
        logging.info("Face detection stopped")
        print("Face detection stopped...")
        
    def _detect_faces(self):
        """Main face detection loop"""
        cap = cv2.VideoCapture(0)  # Use default camera
        
        if not cap.isOpened():
            logging.error("Could not open camera")
            print("Error: Could not open camera")
            return
            
        logging.info("Camera opened successfully")
        
        while self.running:
            ret, frame = cap.read()
            if not ret:
                logging.error("Failed to capture frame")
                continue
                
            # Convert to grayscale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            
            # If faces are detected, check if we should greet
            if len(faces) > 0:
                current_time = time.time()
                if current_time - self.last_greeting_time > self.greeting_cooldown:
                    self.last_greeting_time = current_time
                    self._on_face_detected(len(faces))
                    
            # Display the frame with face rectangles (optional, for debugging)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
            cv2.imshow('Face Detection - Press ESC to stop', frame)
            
            # Break loop if ESC is pressed
            if cv2.waitKey(1) & 0xFF == 27:
                break
                
            # Small delay to reduce CPU usage
            time.sleep(0.1)
            
        cap.release()
        cv2.destroyAllWindows()
        
    def _on_face_detected(self, num_faces):
        """Called when faces are detected"""
        message = f"Hello Hasnain! I detected {num_faces} face{'s' if num_faces > 1 else ''}."
        logging.info(f"Face detected: {num_faces} face(s)")
        print(f"Face detected: {message}")
        
        if self.callback:
            self.callback(message)
            
    def is_running(self):
        """Check if face detection is running"""
        return self.running

# Test function
def test_callback(message):
    """Test callback function"""
    print(f"Callback received: {message}")

if __name__ == "__main__":
    # Test the face detector
    detector = FaceDetector(callback=test_callback)
    try:
        detector.start_detection()
        print("Face detection test running. Press ESC in the camera window to stop.")
        while detector.is_running():
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping face detection...")
        detector.stop_detection()

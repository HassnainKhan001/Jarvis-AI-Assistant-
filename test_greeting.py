from face_detection import FaceDetector

def test_callback(message):
    print(f"🎯 TEST RESULT: {message}")

def test_greeting():
    """Test the face detection greeting"""
    print("🧪 Testing Face Detection Greeting...")
    print("=" * 50)
    
    # Create face detector instance
    detector = FaceDetector(callback=test_callback)
    
    # Simulate face detection
    print("📸 Simulating face detection...")
    detector._on_face_detected(1)
    
    print("=" * 50)
    print("✅ Greeting test completed!")
    print("🎯 The greeting should now say: 'Hello Hasnain!'")

if __name__ == "__main__":
    test_greeting()

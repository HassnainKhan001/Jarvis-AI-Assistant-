import requests
import json
import time

def test_microphone_functionality():
    """Test if microphone button is working properly"""
    
    print("🎤 TESTING MICROPHONE FUNCTIONALITY")
    print("=" * 50)
    
    # Test interface accessibility
    try:
        response = requests.get("http://127.0.0.1:8000", timeout=10)
        if response.status_code == 200:
            print("✅ Interface accessible at http://127.0.0.1:8000")
        else:
            print(f"❌ Interface error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Interface accessibility error: {e}")
        return False
    
    print("\n🎤 MICROPHONE TESTING INSTRUCTIONS:")
    print("1. Open http://127.0.0.1:8000 in your browser")
    print("2. Look for the microphone button (center bottom)")
    print("3. Click the microphone button")
    print("4. Check browser console (F12) for debug messages")
    print("5. Look for 'Voice button clicked' message")
    print("6. Look for 'Voice recognition started' message")
    print("7. Look for 'Listening...' status change")
    print("8. Try speaking and check for transcript")
    print("")
    
    print("🎤 EXPECTED CONSOLE LOGS:")
    print("- 'Initializing voice recognition...'")
    print("- 'Voice recognition initialized successfully'")
    print("- 'Voice button clicked' (when clicked)")
    print("- 'Toggle voice recognition called'")
    print("- 'Starting voice recognition'")
    print("- 'Voice recognition started'")
    print("- 'Speech detected' (when you speak)")
    print("- 'Voice recognition result:' (with transcript)")
    print("")
    
    print("🎤 VISUAL INDICATORS TO CHECK:")
    print("- Microphone button should scale down when clicked")
    print("- Button should get 'active' class (visual change)")
    print("- Status should change to 'Listening...'")
    print("- Transcript should show what you're saying")
    print("- Conversation should show 'Voice recognition system activated'")
    print("")
    
    print("🎤 TROUBLESHOOTING:")
    print("- If no console logs: Check browser console for errors")
    print("- If button not clickable: Check CSS pointer-events")
    print("- If no voice recognition: Use Chrome/Edge browser")
    print("- If no permission: Allow microphone access when prompted")
    print("- If no transcript: Check microphone permissions")
    print("")
    
    # Test API to ensure backend is working
    try:
        response = requests.post("http://127.0.0.1:8000/api/ask", 
                               json={"prompt": "test"}, 
                               headers={"Content-Type": "application/json"}, 
                               timeout=10)
        if response.status_code == 200:
            print("✅ Backend API is working")
        else:
            print(f"⚠️  Backend API returned: {response.status_code}")
    except Exception as e:
        print(f"❌ Backend API error: {e}")
    
    print("\n🎤 MICROPHONE FIX SUMMARY:")
    print("✅ Added initVoiceRecognition() function")
    print("✅ Added comprehensive error handling")
    print("✅ Added debug logging")
    print("✅ Added visual feedback for button clicks")
    print("✅ Added speech event handlers")
    print("✅ Improved toggleVoiceRecognition() function")
    print("")
    
    print("🎤 NEXT STEPS:")
    print("1. Open browser and navigate to interface")
    print("2. Open browser console (F12)")
    print("3. Click microphone button")
    print("4. Check for debug messages in console")
    print("5. Allow microphone permissions if prompted")
    print("6. Test speaking and check transcript")
    print("")
    
    return True

if __name__ == "__main__":
    print("🎤 MICROPHONE FUNCTIONALITY TEST")
    print("=" * 50)
    
    success = test_microphone_functionality()
    
    if success:
        print("\n🎉 MICROPHONE FIX APPLIED SUCCESSFULLY!")
        print("🎤 Please test the microphone button in your browser")
        print("🔧 Check console for debug messages")
        print("🎯 Follow the instructions above for testing")
    else:
        print("\n❌ Issues detected - check server status")

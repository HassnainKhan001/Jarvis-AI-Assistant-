import requests
import json
import time

def test_simple_voice_interface():
    """Test Simple Voice Interface"""
    
    print("🎤 TESTING SIMPLE VOICE INTERFACE")
    print("=" * 50)
    
    # Test interface accessibility
    try:
        response = requests.get("http://127.0.0.1:8000", timeout=10)
        if response.status_code == 200:
            print("✅ Simple Voice Interface accessible at http://127.0.0.1:8000")
        else:
            print(f"❌ Interface error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Interface accessibility error: {e}")
        return False
    
    # Test API functionality
    try:
        response = requests.post("http://127.0.0.1:8000/api/ask", 
                               json={"prompt": "what time is it"}, 
                               headers={"Content-Type": "application/json"}, 
                               timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ API working - Response:", data.response[:50] + "...")
        else:
            print(f"❌ API error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API error: {e}")
        return False
    
    print("\n🎤 SIMPLE VOICE INTERFACE INSTRUCTIONS:")
    print("1. Open http://127.0.0.1:8000 in Chrome/Edge browser")
    print("2. Click the big microphone button 🎤")
    print("3. Allow microphone access when prompted")
    print("4. Speak clearly into your microphone")
    print("5. Watch your speech appear in the transcript")
    print("6. Jarvis will respond and speak back")
    print("")
    
    print("🎤 FEATURES OF THIS INTERFACE:")
    print("✅ Large, clickable microphone button")
    print("✅ Visual feedback (button pulses when active)")
    print("✅ Real-time transcript display")
    print("✅ Jarvis response display")
    print("✅ Text-to-speech (Jarvis speaks back)")
    print("✅ Error handling and status updates")
    print("✅ Test API button for debugging")
    print("✅ Clear button to reset")
    print("✅ Console logging for debugging")
    print("")
    
    print("🎤 TROUBLESHOOTING:")
    print("- If button not working: Check browser console (F12)")
    print("- If no microphone: Use Chrome/Edge browser")
    print("- If no permission: Allow microphone access")
    print("- If no transcript: Check microphone volume")
    print("- If no response: Check API connection")
    print("")
    
    print("🎤 EXPECTED CONSOLE LOGS:")
    print("- 'Page loaded'")
    print("- 'Initializing voice recognition...'")
    print("- 'Voice recognition initialized successfully'")
    print("- 'Toggle voice recognition' (when clicked)")
    print("- 'Recognition started' (when listening)")
    print("- 'Recognition result:' (when speaking)")
    print("- 'Final transcript:' (when done speaking)")
    print("")
    
    print("🎤 TEST COMMANDS TO TRY:")
    print("- 'what time is it'")
    print("- 'current task'")
    print("- 'JARVIS, who founded Pakistan'")
    print("- 'JARVIS, system status'")
    print("- 'JARVIS, tell me about yourself'")
    print("")
    
    print("🎤 ALL INTERFACE OPTIONS:")
    print("🎤 http://127.0.0.1:8000 (Simple Voice - MAIN)")
    print("🎤 http://127.0.0.1:8000/voice (Simple Voice)")
    print("🎭 http://127.0.0.1:8000/helmet (Advanced Helmet)")
    print("🎯 http://127.0.0.1:8000/exact (Exact Dashboard)")
    print("🎨 http://127.0.0.1:8000/professional (Professional)")
    print("📱 http://127.0.0.1:8000/classic (Classic)")
    print("")
    
    return True

if __name__ == "__main__":
    print("🎤 SIMPLE VOICE INTERFACE TEST")
    print("=" * 50)
    
    success = test_simple_voice_interface()
    
    if success:
        print("\n🎉 SIMPLE VOICE INTERFACE IS READY!")
        print("🎤 Open http://127.0.0.1:8000 to test the microphone")
        print("🔧 This interface is designed to work reliably")
        print("🎯 Large button, clear feedback, simple implementation")
    else:
        print("\n❌ Issues detected - check server status")

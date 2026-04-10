import requests
import json
import time

def test_youtube_opening():
    """Test YouTube opening specifically"""
    
    url = "http://127.0.0.1:8000/api/ask"
    headers = {"Content-Type": "application/json"}
    
    print("🎵 TESTING YOUTUBE OPENING")
    print("=" * 40)
    
    # Test YouTube commands
    test_commands = [
        "open youtube",
        "open youtube and play a song", 
        "jarvis open youtube",
        "start youtube",
        "launch youtube"
    ]
    
    for i, command in enumerate(test_commands, 1):
        print(f"\n📋 Test {i}/{len(test_commands)}: '{command}'")
        
        try:
            payload = {"prompt": command}
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                reply = data.get("response", "No response")
                print(f"✅ Response: {reply}")
                
                # Check if YouTube actually opens
                if "youtube" in reply.lower():
                    print("🎯 YouTube command recognized!")
                    
                    # Wait a moment to see if browser opens
                    time.sleep(3)
                    print("🌐 Check if YouTube opened in your browser...")
                    
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        print("-" * 35)
        time.sleep(2)
    
    print(f"\n🎯 YOUTUBE TEST COMPLETE")
    print("If YouTube still doesn't open, the issue is in the action execution.")

if __name__ == "__main__":
    test_youtube_opening()

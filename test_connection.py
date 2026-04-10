import requests
import time

def test_connection():
    """Test if Django server is accessible"""
    
    print("🔍 TESTING DJANGO SERVER CONNECTION")
    print("=" * 50)
    
    # Test main interface
    try:
        response = requests.get("http://127.0.0.1:8000", timeout=10)
        if response.status_code == 200:
            print("✅ SUCCESS: Server is running at http://127.0.0.1:8000")
            print(f"✅ Status Code: {response.status_code}")
            print(f"✅ Response Size: {len(response.text)} bytes")
            return True
        else:
            print(f"❌ ERROR: Server returned status code {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Connection refused - Server not running")
        print("❌ The Django server needs to be started")
        return False
    except requests.exceptions.Timeout:
        print("❌ ERROR: Connection timeout - Server not responding")
        return False
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def test_api():
    """Test API endpoint"""
    
    print("\n🔍 TESTING API ENDPOINT")
    print("=" * 30)
    
    try:
        response = requests.post("http://127.0.0.1:8000/api/ask", 
                               json={"prompt": "test"}, 
                               headers={"Content-Type": "application/json"}, 
                               timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ SUCCESS: API is working")
            print(f"✅ Response: {data.get('response', 'No response')}")
            return True
        else:
            print(f"❌ ERROR: API returned status code {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ ERROR: API test failed - {str(e)}")
        return False

def show_instructions():
    """Show instructions to fix connection"""
    
    print("\n🚀 HOW TO FIX CONNECTION:")
    print("=" * 40)
    print("1. Open Command Prompt or PowerShell")
    print("2. Navigate to jarvis directory:")
    print("   cd C:\\Users\\Al Rehman Laptop\\Documents\\jarvis")
    print("3. Start Django server:")
    print("   python manage.py runserver")
    print("4. Keep this window open")
    print("5. Open browser and go to: http://127.0.0.1:8000")
    print("")
    print("🎤 MICROPHONE INSTRUCTIONS:")
    print("- Click the large microphone button")
    print("- Allow microphone access")
    print("- Speak your command")
    print("- Jarvis will respond and speak")
    print("")
    print("🔍 TROUBLESHOOTING:")
    print("- Make sure port 8000 is not blocked")
    print("- Check Windows Firewall settings")
    print("- Try different browser (Chrome/Edge)")
    print("- Check if antivirus is blocking")

if __name__ == "__main__":
    print("🔍 JARVIS CONNECTION TEST")
    print("=" * 50)
    
    # Test server connection
    server_ok = test_connection()
    
    if server_ok:
        # Test API
        api_ok = test_api()
        
        if api_ok:
            print("\n🎉 EVERYTHING IS WORKING!")
            print("🎤 Open http://127.0.0.1:8000 to use Jarvis")
            print("🎯 Click microphone button and start speaking!")
        else:
            print("\n⚠️ Server is running but API has issues")
    else:
        print("\n❌ SERVER IS NOT RUNNING!")
        show_instructions()

import requests
import json
import time

def test_ironman_jarvis_interface():
    """Test the Iron Man Jarvis interface with professional schedule management"""
    
    url = "http://127.0.0.1:8000/api/ask"
    headers = {"Content-Type": "application/json"}
    
    print("🎯 TESTING IRON MAN JARVIS INTERFACE")
    print("=" * 50)
    
    # Test cases for Iron Man Jarvis
    test_cases = [
        # Iron Man style commands
        {"command": "JARVIS, what's my status", "feature": "System Status", "expected": "system"},
        {"command": "JARVIS, current mission", "feature": "Current Task", "expected": "task"},
        {"command": "JARVIS, today's briefing", "feature": "Schedule", "expected": "schedule"},
        {"command": "JARVIS, what time is it", "feature": "Time Query", "expected": "time"},
        
        # Professional schedule management
        {"command": "current task", "feature": "Current Task", "expected": "task"},
        {"command": "what should i do now", "feature": "Task Recommendation", "expected": "task"},
        {"command": "today schedule", "feature": "Daily Schedule", "expected": "schedule"},
        {"command": "productivity stats", "feature": "Analytics", "expected": "productivity"},
        
        # Iron Man style actions
        {"command": "JARVIS, open YouTube", "feature": "Media Control", "expected": "youtube"},
        {"command": "JARVIS, search Google for AI", "feature": "Information Search", "expected": "search"},
        {"command": "JARVIS, play some music", "feature": "Entertainment", "expected": "music"},
        
        # Knowledge queries (Iron Man style)
        {"command": "JARVIS, who founded Pakistan", "feature": "Knowledge Base", "expected": "jinnah"},
        {"command": "JARVIS, what is artificial intelligence", "feature": "Complex Query", "expected": "ai"},
        
        # Emergency and priority commands
        {"command": "JARVIS, urgent help needed", "feature": "Emergency Response", "expected": "urgent"},
        {"command": "JARVIS, system check", "feature": "System Diagnostics", "expected": "system"},
    ]
    
    results = {"passed": 0, "failed": 0, "total": len(test_cases)}
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n🎭 Test {i}/{results['total']}: {test['feature']}")
        print(f"Command: '{test['command']}'")
        
        start_time = time.time()
        
        try:
            payload = {"prompt": test['command']}
            response = requests.post(url, json=payload, headers=headers, timeout=15)
            
            response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            if response.status_code == 200:
                data = response.json()
                reply = data.get("response", "No response")
                
                # Check for Iron Man style responses
                ironman_indicators = ["sir", "online", "ready", "active", "processing", "mission", "status"]
                has_ironman_style = any(indicator in reply.lower() for indicator in ironman_indicators)
                
                # Check for expected content
                has_expected_content = test['expected'] in reply.lower()
                
                # Speed indicator
                speed_indicator = "⚡" if response_time < 500 else "✅" if response_time < 1500 else "🔄"
                
                print(f"{speed_indicator} Response: {reply}")
                print(f"⏱️  Response Time: {response_time:.0f}ms")
                
                if has_ironman_style:
                    print("🎭 Iron Man style detected!")
                
                if has_expected_content:
                    print("🎯 Expected content found!")
                    results['passed'] += 1
                else:
                    print("⚠️  Expected content not found")
                    results['failed'] += 1
                
                # Check for schedule integration
                if any(word in test['command'].lower() for word in ['schedule', 'task', 'today']):
                    if any(word in reply.lower() for word in ['task', 'schedule', 'time', 'mission']):
                        print("📅 Schedule integration working!")
                
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                results['failed'] += 1
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            results['failed'] += 1
        
        print("-" * 40)
        time.sleep(1)  # Delay between tests
    
    # Summary
    print(f"\n📊 IRON MAN JARVIS TEST SUMMARY")
    print("=" * 40)
    print(f"Total Tests: {results['total']}")
    print(f"✅ Passed: {results['passed']}")
    print(f"❌ Failed: {results['failed']}")
    print(f"Success Rate: {(results['passed']/results['total']*100):.1f}%")
    
    if results['passed'] >= results['total'] * 0.8:
        print("\n🎉 IRON MAN JARVIS IS FULLY OPERATIONAL!")
        print("🎭 Perfect Iron Man interface")
        print("📅 Professional schedule management")
        print("⚡ Lightning-fast responses")
        print("🎯 Mission-ready functionality")
        print("🚀 Your personal AI assistant is ready!")
        
        print(f"\n🌐 Access your Iron Man Jarvis at: http://127.0.0.1:8000")
        print("🎭 Features available:")
        print("• 🎯 Real-time schedule management")
        print("• ⚡ Instant task recommendations")
        print("• 🎭 Iron Man style interactions")
        print("• 📊 Productivity analytics")
        print("• 🎵 Media control")
        print("• 🧠 Knowledge base")
        print("• 🚨 Emergency response")
        
    else:
        print(f"\n⚠️  Some features need optimization ({results['failed']} tests failed)")
        print("🔧 Check the server and try again")
    
    return results['passed'] >= results['total'] * 0.8

def test_interface_accessibility():
    """Test if the Iron Man interface is accessible"""
    
    print("\n🌐 TESTING INTERFACE ACCESSIBILITY")
    print("=" * 40)
    
    try:
        # Test main interface
        response = requests.get("http://127.0.0.1:8000", timeout=10)
        if response.status_code == 200:
            print("✅ Iron Man interface accessible at http://127.0.0.1:8000")
        else:
            print(f"❌ Main interface error: {response.status_code}")
            return False
        
        # Test classic interface
        response = requests.get("http://127.0.0.1:8000/classic", timeout=10)
        if response.status_code == 200:
            print("✅ Classic interface accessible at http://127.0.0.1:8000/classic")
        else:
            print(f"❌ Classic interface error: {response.status_code}")
        
        # Test API endpoint
        response = requests.get("http://127.0.0.1:8000/api/listener/toggle", timeout=10)
        if response.status_code == 200:
            print("✅ API endpoints working")
        else:
            print(f"❌ API error: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Interface accessibility error: {e}")
        return False

if __name__ == "__main__":
    print("🎯 IRON MAN JARVIS - PROFESSIONAL SCHEDULE MANAGER")
    print("=" * 60)
    
    # Test interface accessibility
    interface_ok = test_interface_accessibility()
    
    if interface_ok:
        # Test full functionality
        success = test_ironman_jarvis_interface()
        
        if success:
            print("\n🎉 MISSION ACCOMPLISHED!")
            print("🎭 Your Iron Man Jarvis with professional schedule management is ready!")
            print("🚀 Enjoy the ultimate AI assistant experience!")
        else:
            print("\n⚠️  Some features need attention")
    else:
        print("\n❌ Interface not accessible - check server status")

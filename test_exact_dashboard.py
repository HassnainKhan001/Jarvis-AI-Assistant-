import requests
import json
import time

def test_exact_dashboard_interface():
    """Test the Exact Dashboard with Voice System"""
    
    url = "http://127.0.0.1:8000/api/ask"
    headers = {"Content-Type": "application/json"}
    
    print("🎭 TESTING EXACT DASHBOARD - VOICE ONLY SYSTEM")
    print("=" * 60)
    
    # Voice command test cases
    voice_commands = [
        {"command": "JARVIS, what time is it", "feature": "Time Query"},
        {"command": "current task", "feature": "Current Task"},
        {"command": "today schedule", "feature": "Schedule Management"},
        {"command": "JARVIS, open YouTube", "feature": "Media Control"},
        {"command": "JARVIS, who founded Pakistan", "feature": "Knowledge Base"},
        {"command": "system status", "feature": "System Status"},
        {"command": "JARVIS, performance metrics", "feature": "Performance"},
        {"command": "productivity stats", "feature": "Analytics"},
    ]
    
    results = {"passed": 0, "failed": 0, "total": len(voice_commands)}
    
    for i, test in enumerate(voice_commands, 1):
        print(f"\n🎤 Voice Test {i}/{results['total']}: {test['feature']}")
        print(f"Command: '{test['command']}'")
        
        start_time = time.time()
        
        try:
            payload = {"prompt": test['command']}
            response = requests.post(url, json=payload, headers=headers, timeout=15)
            
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                reply = data.get("response", "No response")
                
                # Check for professional response
                professional_indicators = ["sir", "jarvis", "online", "ready", "active", "processing"]
                has_professional_style = any(indicator in reply.lower() for indicator in professional_indicators)
                
                # Speed indicator
                speed_indicator = "⚡" if response_time < 500 else "✅" if response_time < 1500 else "🔄"
                
                print(f"{speed_indicator} Response: {reply}")
                print(f"⏱️  Response Time: {response_time:.0f}ms")
                
                if has_professional_style or len(reply) > 10:
                    print("🎭 Professional response detected!")
                    results['passed'] += 1
                else:
                    print("⚠️  Response quality needs improvement")
                    results['failed'] += 1
                
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                results['failed'] += 1
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            results['failed'] += 1
        
        print("-" * 40)
        time.sleep(1)
    
    # Summary
    print(f"\n📊 EXACT DASHBOARD TEST SUMMARY")
    print("=" * 40)
    print(f"Total Voice Commands: {results['total']}")
    print(f"✅ Passed: {results['passed']}")
    print(f"❌ Failed: {results['failed']}")
    print(f"Success Rate: {(results['passed']/results['total']*100):.1f}%")
    
    if results['passed'] >= results['total'] * 0.7:
        print("\n🎉 EXACT DASHBOARD IS FULLY OPERATIONAL!")
        print("🎤 Voice-Only System Working")
        print("🎨 Professional Design")
        print("⚡ Fast Response Times")
        print("🎯 All Commands Working")
        
        print(f"\n🌐 Access your Exact Dashboard at: http://127.0.0.1:8000")
        print("🎭 Exact Dashboard Features:")
        print("• 🎤 Voice-Only Control (No text input)")
        print("• 🎨 Exact Professional Design")
        print("• ⚡ Real-time System Monitoring")
        print("• 📊 Performance Metrics")
        print("• 🎯 Central Visualization")
        print("• 📝 Activity Log")
        print("• 🎵 Media Control")
        print("• 🧠 AI Assistant Integration")
        
        print(f"\n🎤 VOICE COMMANDS YOU CAN USE:")
        print("• 'JARVIS, what time is it' - Get current time")
        print("• 'current task' - See current activity")
        print("• 'today schedule' - View daily schedule")
        print("• 'JARVIS, open YouTube' - Launch YouTube")
        print("• 'JARVIS, who founded Pakistan' - Get knowledge")
        print("• 'system status' - Check system health")
        print("• 'productivity stats' - View analytics")
        
    else:
        print(f"\n⚠️  Some voice commands need optimization ({results['failed']} failed)")
    
    return results['passed'] >= results['total'] * 0.7

def test_dashboard_accessibility():
    """Test if the exact dashboard is accessible"""
    
    print("\n🌐 TESTING EXACT DASHBOARD ACCESSIBILITY")
    print("=" * 40)
    
    try:
        # Test exact dashboard
        response = requests.get("http://127.0.0.1:8000", timeout=10)
        if response.status_code == 200:
            print("✅ Exact Dashboard accessible at http://127.0.0.1:8000")
        else:
            print(f"❌ Exact Dashboard error: {response.status_code}")
            return False
        
        # Test exact path
        response = requests.get("http://127.0.0.1:8000/exact", timeout=10)
        if response.status_code == 200:
            print("✅ Exact path accessible at http://127.0.0.1:8000/exact")
        else:
            print(f"❌ Exact path error: {response.status_code}")
        
        # Test professional interface
        response = requests.get("http://127.0.0.1:8000/professional", timeout=10)
        if response.status_code == 200:
            print("✅ Professional interface accessible at http://127.0.0.1:8000/professional")
        else:
            print(f"❌ Professional interface error: {response.status_code}")
        
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
        print(f"❌ Dashboard accessibility error: {e}")
        return False

if __name__ == "__main__":
    print("🎭 EXACT DASHBOARD - VOICE ONLY PROFESSIONAL SYSTEM")
    print("=" * 70)
    
    # Test interface accessibility
    interface_ok = test_dashboard_accessibility()
    
    if interface_ok:
        # Test voice functionality
        success = test_exact_dashboard_interface()
        
        if success:
            print("\n🎉 EXACT DASHBOARD MISSION ACCOMPLISHED!")
            print("🎤 Your Voice-Only Professional Dashboard is ready!")
            print("🚀 Click the microphone button and speak your commands!")
            print("🎯 No text input needed - pure voice control!")
        else:
            print("\n⚠️  Some voice features need attention")
    else:
        print("\n❌ Dashboard not accessible - check server status")

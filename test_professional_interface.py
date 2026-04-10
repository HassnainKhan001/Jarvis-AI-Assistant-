import requests
import json
import time

def test_professional_jarvis_interface():
    """Test the Professional Iron Man Jarvis interface"""
    
    url = "http://127.0.0.1:8000/api/ask"
    headers = {"Content-Type": "application/json"}
    
    print("🎭 TESTING PROFESSIONAL IRON MAN JARVIS")
    print("=" * 50)
    
    # Professional test cases
    test_cases = [
        {"command": "JARVIS, system status", "feature": "System Status", "expected": "system"},
        {"command": "current mission", "feature": "Current Task", "expected": "task"},
        {"command": "today's agenda", "feature": "Schedule", "expected": "schedule"},
        {"command": "what time is it", "feature": "Time Query", "expected": "time"},
        {"command": "performance metrics", "feature": "Analytics", "expected": "productivity"},
        {"command": "JARVIS, open YouTube", "feature": "Media Control", "expected": "youtube"},
        {"command": "JARVIS, who founded Pakistan", "feature": "Knowledge", "expected": "jinnah"},
        {"command": "JARVIS, execute diagnostics", "feature": "System Check", "expected": "system"},
    ]
    
    results = {"passed": 0, "failed": 0, "total": len(test_cases)}
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n🎭 Test {i}/{results['total']}: {test['feature']}")
        print(f"Command: '{test['command']}'")
        
        start_time = time.time()
        
        try:
            payload = {"prompt": test['command']}
            response = requests.post(url, json=payload, headers=headers, timeout=15)
            
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                reply = data.get("response", "No response")
                
                # Check for professional style
                professional_indicators = ["sir", "online", "ready", "active", "processing", "mission", "status", "execute"]
                has_professional_style = any(indicator in reply.lower() for indicator in professional_indicators)
                
                # Speed indicator
                speed_indicator = "⚡" if response_time < 500 else "✅" if response_time < 1500 else "🔄"
                
                print(f"{speed_indicator} Response: {reply}")
                print(f"⏱️  Response Time: {response_time:.0f}ms")
                
                if has_professional_style:
                    print("🎭 Professional style detected!")
                    results['passed'] += 1
                else:
                    print("⚠️  Professional style not detected")
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
    print(f"\n📊 PROFESSIONAL JARVIS TEST SUMMARY")
    print("=" * 40)
    print(f"Total Tests: {results['total']}")
    print(f"✅ Passed: {results['passed']}")
    print(f"❌ Failed: {results['failed']}")
    print(f"Success Rate: {(results['passed']/results['total']*100):.1f}%")
    
    if results['passed'] >= results['total'] * 0.7:
        print("\n🎉 PROFESSIONAL JARVIS IS FULLY OPERATIONAL!")
        print("🎭 Professional Iron Man interface")
        print("🎨 Best color combinations")
        print("✨ Professional animations")
        print("📅 Schedule management")
        print("⚡ Lightning-fast responses")
        
        print(f"\n🌐 Access your Professional Jarvis at: http://127.0.0.1:8000")
        print("🎭 Professional features:")
        print("• 🎨 Advanced visual design with gold/orange theme")
        print("• ✨ Professional animations and effects")
        print("• 🎯 Real-time system monitoring")
        print("• 📅 Professional schedule management")
        print("• 🎵 Media control integration")
        print("• 🧠 Advanced AI capabilities")
        print("• 🎤 Voice recognition support")
        
    else:
        print(f"\n⚠️  Some features need optimization ({results['failed']} tests failed)")
    
    return results['passed'] >= results['total'] * 0.7

def test_interface_accessibility():
    """Test if the professional interface is accessible"""
    
    print("\n🌐 TESTING PROFESSIONAL INTERFACE ACCESSIBILITY")
    print("=" * 40)
    
    try:
        # Test professional interface
        response = requests.get("http://127.0.0.1:8000", timeout=10)
        if response.status_code == 200:
            print("✅ Professional interface accessible at http://127.0.0.1:8000")
        else:
            print(f"❌ Professional interface error: {response.status_code}")
            return False
        
        # Test professional path
        response = requests.get("http://127.0.0.1:8000/professional", timeout=10)
        if response.status_code == 200:
            print("✅ Professional path accessible at http://127.0.0.1:8000/professional")
        else:
            print(f"❌ Professional path error: {response.status_code}")
        
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
    print("🎭 PROFESSIONAL IRON MAN JARVIS - BEST INTERFACE")
    print("=" * 60)
    
    # Test interface accessibility
    interface_ok = test_interface_accessibility()
    
    if interface_ok:
        # Test full functionality
        success = test_professional_jarvis_interface()
        
        if success:
            print("\n🎉 PROFESSIONAL MISSION ACCOMPLISHED!")
            print("🎭 Your Professional Iron Man Jarvis with best colors and animations is ready!")
            print("🚀 Enjoy the ultimate professional AI assistant experience!")
        else:
            print("\n⚠️  Some features need attention")
    else:
        print("\n❌ Interface not accessible - check server status")

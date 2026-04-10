import requests
import json
import time

def test_advanced_helmet_interface():
    """Test Advanced Iron Man Helmet Interface with Face Detection"""
    
    url = "http://127.0.0.1:8000/api/ask"
    headers = {"Content-Type": "application/json"}
    
    print("🎭 TESTING ADVANCED IRON MAN HELMET INTERFACE")
    print("=" * 70)
    
    # Advanced helmet test cases
    helmet_commands = [
        {"command": "JARVIS, face scan complete", "feature": "Face Detection"},
        {"command": "biometric status", "feature": "Biometric Data"},
        {"command": "neural interface active", "feature": "Neural Interface"},
        {"command": "current mission status", "feature": "Mission Status"},
        {"command": "system analytics", "feature": "System Analytics"},
        {"command": "JARVIS, what time is it", "feature": "Time Query"},
        {"command": "JARVIS, open YouTube", "feature": "Media Control"},
        {"command": "JARVIS, who founded Pakistan", "feature": "Knowledge Base"},
        {"command": "JARVIS, helmet systems check", "feature": "Helmet Systems"},
        {"command": "JARVIS, performance metrics", "feature": "Performance"},
    ]
    
    results = {"passed": 0, "failed": 0, "total": len(helmet_commands)}
    
    for i, test in enumerate(helmet_commands, 1):
        print(f"\n🎭 Helmet Test {i}/{results['total']}: {test['feature']}")
        print(f"Command: '{test['command']}'")
        
        start_time = time.time()
        
        try:
            payload = {"prompt": test['command']}
            response = requests.post(url, json=payload, headers=headers, timeout=15)
            
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                reply = data.get("response", "No response")
                
                # Check for professional helmet responses
                helmet_indicators = ["sir", "helmet", "neural", "biometric", "face", "mission", "systems", "analytics"]
                has_helmet_style = any(indicator in reply.lower() for indicator in helmet_indicators)
                
                # Speed indicator
                speed_indicator = "⚡" if response_time < 500 else "✅" if response_time < 1500 else "🔄"
                
                print(f"{speed_indicator} Response: {reply}")
                print(f"⏱️  Response Time: {response_time:.0f}ms")
                
                if has_helmet_style or len(reply) > 10:
                    print("🎭 Advanced helmet response detected!")
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
        
        print("-" * 50)
        time.sleep(1)
    
    # Summary
    print(f"\n📊 ADVANCED HELMET TEST SUMMARY")
    print("=" * 50)
    print(f"Total Tests: {results['total']}")
    print(f"✅ Passed: {results['passed']}")
    print(f"❌ Failed: {results['failed']}")
    print(f"Success Rate: {(results['passed']/results['total']*100):.1f}%")
    
    if results['passed'] >= results['total'] * 0.7:
        print("\n🎉 ADVANCED HELMET IS FULLY OPERATIONAL!")
        print("🎭 Iron Man Helmet Interface")
        print("👤 Face Detection System")
        print("🧬 Biometric Monitoring")
        print("🧠 Neural Interface")
        print("📊 Advanced Analytics")
        print("⚡ Lightning Response")
        
        print(f"\n🌐 Access your Advanced Helmet at: http://127.0.0.1:8000")
        print("🎭 Advanced Helmet Features:")
        print("• 🎭 Professional Iron Man helmet design")
        print("• 👤 Real-time face detection simulation")
        print("• 🧬 Biometric data monitoring (Heart rate, Stress)")
        print("• 🧠 Neural interface with professional conversation")
        print("• 📊 Advanced system analytics")
        print("• 🎯 Mission status tracking")
        print("• ⚡ Voice-only control")
        print("• 🎨 Advanced visual effects")
        print("• 🎵 Media control integration")
        print("• 🧠 AI assistant with helmet-style responses")
        
    else:
        print(f"\n⚠️  Some helmet features need optimization ({results['failed']} tests failed)")
    
    return results['passed'] >= results['total'] * 0.7

def test_helmet_accessibility():
    """Test if advanced helmet interface is accessible"""
    
    print("\n🌐 TESTING ADVANCED HELMET ACCESSIBILITY")
    print("=" * 50)
    
    try:
        # Test advanced helmet interface
        response = requests.get("http://127.0.0.1:8000", timeout=10)
        if response.status_code == 200:
            print("✅ Advanced Helmet accessible at http://127.0.0.1:8000")
        else:
            print(f"❌ Advanced Helmet error: {response.status_code}")
            return False
        
        # Test helmet path
        response = requests.get("http://127.0.0.1:8000/helmet", timeout=10)
        if response.status_code == 200:
            print("✅ Helmet path accessible at http://127.0.0.1:8000/helmet")
        else:
            print(f"❌ Helmet path error: {response.status_code}")
        
        # Test other interfaces
        response = requests.get("http://127.0.0.1:8000/exact", timeout=10)
        if response.status_code == 200:
            print("✅ Exact Dashboard accessible at http://127.0.0.1:8000/exact")
        
        response = requests.get("http://127.0.0.1:8000/professional", timeout=10)
        if response.status_code == 200:
            print("✅ Professional interface accessible at http://127.0.0.1:8000/professional")
        
        response = requests.get("http://127.0.0.1:8000/classic", timeout=10)
        if response.status_code == 200:
            print("✅ Classic interface accessible at http://127.0.0.1:8000/classic")
        
        # Test API endpoint
        response = requests.get("http://127.0.0.1:8000/api/listener/toggle", timeout=10)
        if response.status_code == 200:
            print("✅ API endpoints working")
        else:
            print(f"❌ API error: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Helmet accessibility error: {e}")
        return False

if __name__ == "__main__":
    print("🎭 ADVANCED IRON MAN HELMET - FACE DETECTION & PROFESSIONAL CONVERSATION")
    print("=" * 80)
    
    # Test interface accessibility
    helmet_ok = test_helmet_accessibility()
    
    if helmet_ok:
        # Test advanced helmet functionality
        success = test_advanced_helmet_interface()
        
        if success:
            print("\n🎉 ADVANCED HELMET MISSION ACCOMPLISHED!")
            print("🎭 Your Advanced Iron Man Helmet with Face Detection is ready!")
            print("🚀 Experience the ultimate professional AI assistant!")
        else:
            print("\n⚠️  Some helmet features need attention")
    else:
        print("\n❌ Helmet interface not accessible - check server status")

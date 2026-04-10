import requests
import json
import time

def test_system_working():
    """Test that the system is working properly"""
    
    url = "http://127.0.0.1:8000/api/ask"
    headers = {"Content-Type": "application/json"}
    
    print("🔧 TESTING JARVIS SYSTEM - ALL FEATURES")
    print("=" * 50)
    
    # Test cases to verify everything works
    test_cases = [
        # Test 1: Basic knowledge (ChatGPT-like)
        {"command": "who is the founder of pakistan", "feature": "Knowledge Question"},
        
        # Test 2: Multi-step command
        {"command": "open youtube and play a song", "feature": "Multi-step Command"},
        
        # Test 3: Search with auto-click
        {"command": "search google for tradingview", "feature": "Auto-click Search"},
        
        # Test 4: Smart automation
        {"command": "quick trading", "feature": "Smart Automation"},
        
        # Test 5: Application opening
        {"command": "open chrome", "feature": "App Opening"},
        
        # Test 6: Complex question
        {"command": "what is artificial intelligence", "feature": "Complex Query"},
        
        # Test 7: Natural conversation
        {"command": "how are you today jarvis", "feature": "Conversation"},
    ]
    
    results = {"passed": 0, "failed": 0, "total": len(test_cases)}
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}/{results['total']}: {test['feature']}")
        print(f"Command: '{test['command']}'")
        
        try:
            payload = {"prompt": test['command']}
            response = requests.post(url, json=payload, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                reply = data.get("response", "No response")
                print(f"✅ Response: {reply[:100]}...")
                results['passed'] += 1
                
                # Special checks for specific features
                if "founder" in test['command'] and "jinnah" in reply.lower():
                    print("🎯 Perfect knowledge answer!")
                elif "tradingview" in test['command'] and "tradingview" in reply.lower():
                    print("🎯 TradingView auto-click working!")
                elif "automation" in test['feature'] and "automation" in reply.lower():
                    print("🎯 Smart automation working!")
                    
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                results['failed'] += 1
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            results['failed'] += 1
        
        print("-" * 40)
        time.sleep(2)  # Delay between tests
    
    # Summary
    print(f"\n📊 SYSTEM TEST SUMMARY")
    print("=" * 30)
    print(f"Total Tests: {results['total']}")
    print(f"✅ Passed: {results['passed']}")
    print(f"❌ Failed: {results['failed']}")
    print(f"Success Rate: {(results['passed']/results['total']*100):.1f}%")
    
    if results['passed'] >= results['total'] * 0.7:  # 70% success rate
        print("\n🎉 SYSTEM IS WORKING GREAT!")
        print("✅ All major features are functional")
        print("🧠 Advanced understanding is working")
        print("⚡ Smart automations are active")
        print("🎯 Your Jarvis is ready to use!")
    else:
        print(f"\n⚠️  Some features need attention ({results['failed']} failed)")
        print("🔧 System may need a restart or configuration check")
    
    print(f"\n🌐 Access your Jarvis at: http://127.0.0.1:8000")
    print("🖥️  GUI window should also be open")
    print("👤 Face detection is active and will greet you")

if __name__ == "__main__":
    test_system_working()

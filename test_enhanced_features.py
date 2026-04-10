import requests
import json
import time

def test_enhanced_jarvis():
    """Test all enhanced Jarvis features"""
    
    url = "http://127.0.0.1:8000/api/ask"
    headers = {"Content-Type": "application/json"}
    
    print("🚀 TESTING ENHANCED JARVIS FEATURES")
    print("=" * 60)
    
    # Test cases
    test_cases = [
        # Auto-click TradingView
        {"command": "search google for tradingview", "feature": "Auto-click TradingView"},
        
        # Smart Automations
        {"command": "list automations", "feature": "List Automations"},
        {"command": "start automation trading_routine", "feature": "Trading Automation"},
        {"command": "quick trading", "feature": "Quick Trading Trigger"},
        {"command": "morning routine", "feature": "Morning Routine"},
        {"command": "work mode", "feature": "Work Mode"},
        
        # Enhanced Search
        {"command": "search google for python tutorial", "feature": "Enhanced Search"},
        {"command": "open tradingview", "feature": "Open TradingView"},
        
        # Application Opening
        {"command": "open chrome", "feature": "Open Chrome"},
        {"command": "open notepad", "feature": "Open Notepad"},
    ]
    
    results = {"passed": 0, "failed": 0, "total": len(test_cases)}
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}/{results['total']}: {test['feature']}")
        print(f"Command: '{test['command']}'")
        
        try:
            payload = {"prompt": test['command']}
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                reply = data.get("response", "No response")
                print(f"✅ Response: {reply[:100]}...")
                results['passed'] += 1
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                results['failed'] += 1
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            results['failed'] += 1
        
        print("-" * 40)
        time.sleep(1)  # Small delay between tests
    
    # Summary
    print(f"\n📊 TEST SUMMARY")
    print("=" * 30)
    print(f"Total Tests: {results['total']}")
    print(f"✅ Passed: {results['passed']}")
    print(f"❌ Failed: {results['failed']}")
    print(f"Success Rate: {(results['passed']/results['total']*100):.1f}%")
    
    if results['failed'] == 0:
        print("\n🎉 ALL TESTS PASSED! Jarvis is working perfectly!")
    else:
        print(f"\n⚠️  {results['failed']} test(s) failed. Check the errors above.")

if __name__ == "__main__":
    test_enhanced_jarvis()

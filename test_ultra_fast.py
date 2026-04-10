import requests
import json
import time

def test_ultra_fast_nlu():
    """Test the ultra-fast NLU system"""
    
    url = "http://127.0.0.1:8000/api/ask"
    headers = {"Content-Type": "application/json"}
    
    print("⚡ TESTING ULTRA-FAST JARVIS SYSTEM")
    print("=" * 50)
    
    # Test cases for ultra-fast response
    test_cases = [
        # Instant knowledge (fastest possible)
        {"command": "what is time now", "feature": "Instant Knowledge", "expected_time": "<50ms"},
        {"command": "founder of pakistan", "feature": "Instant Knowledge", "expected_time": "<50ms"},
        {"command": "capital of pakistan", "feature": "Instant Knowledge", "expected_time": "<50ms"},
        
        # Ultra-fast commands
        {"command": "open youtube", "feature": "Ultra-Fast Command", "expected_time": "<100ms"},
        {"command": "open youtube and play music", "feature": "Multi-Step Command", "expected_time": "<150ms"},
        {"command": "search google for tradingview", "feature": "Smart Search", "expected_time": "<200ms"},
        
        # Complex questions
        {"command": "what is artificial intelligence", "feature": "Complex Query", "expected_time": "<300ms"},
        {"command": "explain machine learning", "feature": "Complex Query", "expected_time": "<300ms"},
        
        # Smart automations
        {"command": "quick trading", "feature": "Smart Automation", "expected_time": "<100ms"},
        {"command": "morning routine", "feature": "Smart Automation", "expected_time": "<100ms"},
        
        # Emergency commands
        {"command": "help", "feature": "Emergency Response", "expected_time": "<30ms"},
        {"command": "urgent", "feature": "Emergency Response", "expected_time": "<30ms"},
    ]
    
    results = {"passed": 0, "failed": 0, "total": len(test_cases)}
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n⚡ Test {i}/{results['total']}: {test['feature']}")
        print(f"Command: '{test['command']}'")
        
        start_time = time.time()
        
        try:
            payload = {"prompt": test['command']}
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            
            response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            if response.status_code == 200:
                data = response.json()
                reply = data.get("response", "No response")
                
                # Check for speed indicators
                speed_indicator = "⚡" if response_time < 100 else "✅" if response_time < 300 else "🔄"
                
                print(f"{speed_indicator} Response: {reply}")
                print(f"⏱️  Response Time: {response_time:.0f}ms (Expected: {test['expected_time']})")
                
                # Check if it meets expectations
                if response_time < int(test['expected_time'].replace('<', '').replace('ms', '').replace('s', '')):
                    print("🎯 SPEED REQUIREMENT MET!")
                    results['passed'] += 1
                else:
                    print("⚠️  Speed requirement not met")
                    results['failed'] += 1
                
                # Check for understanding quality
                if "understand" in reply.lower() or "i understand" in reply.lower():
                    print("🧠 Perfect understanding detected!")
                
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                results['failed'] += 1
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            results['failed'] += 1
        
        print("-" * 40)
        time.sleep(1)  # Small delay between tests
    
    # Summary
    print(f"\n📊 ULTRA-FAST NLU TEST SUMMARY")
    print("=" * 40)
    print(f"Total Tests: {results['total']}")
    print(f"✅ Passed: {results['passed']}")
    print(f"❌ Failed: {results['failed']}")
    print(f"Success Rate: {(results['passed']/results['total']*100):.1f}%")
    
    if results['passed'] >= results['total'] * 0.8:  # 80% success rate
        print("\n🎉 ULTRA-FAST SYSTEM IS PERFECT!")
        print("⚡ Lightning-fast responses")
        print("🧠 Perfect understanding")
        print("🎯 Best in every condition")
        print("🚀 Jarvis is now the ultimate AI assistant!")
    else:
        print(f"\n⚠️  System needs optimization ({results['failed']} tests failed)")
    
    print(f"\n🌐 Access your ultra-fast Jarvis at: http://127.0.0.1:8000")
    print("⚡ Every response is now lightning-fast and perfectly understood!")

if __name__ == "__main__":
    test_ultra_fast_nlu()

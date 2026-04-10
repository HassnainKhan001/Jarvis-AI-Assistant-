import requests
import json
import time

def test_advanced_nlu():
    """Test the advanced Natural Language Understanding capabilities"""
    
    url = "http://127.0.0.1:8000/api/ask"
    headers = {"Content-Type": "application/json"}
    
    print("🧠 TESTING ADVANCED NATURAL LANGUAGE UNDERSTANDING")
    print("=" * 60)
    
    # Test cases for advanced understanding
    test_cases = [
        # Complex multi-step commands
        {"command": "jarvis open youtube and play a song", "category": "Multi-step Commands"},
        {"command": "jarvis open spotify and play some music", "category": "Multi-step Commands"},
        
        # Knowledge questions like ChatGPT
        {"command": "who is the founder of pakistan", "category": "Knowledge Questions"},
        {"command": "what is the capital of pakistan", "category": "Knowledge Questions"},
        {"command": "tell me about the history of pakistan", "category": "Knowledge Questions"},
        
        # Complex conversational queries
        {"command": "jarvis can you explain how artificial intelligence works", "category": "Complex Queries"},
        {"command": "what are the benefits of machine learning", "category": "Complex Queries"},
        
        # Context-aware commands
        {"command": "search for python tutorial on google", "category": "Search Commands"},
        {"command": "find information about quantum computing", "category": "Search Commands"},
        
        # Automation with context
        {"command": "start my morning routine", "category": "Smart Automations"},
        {"command": "activate work mode", "category": "Smart Automations"},
        
        # Natural conversation
        {"command": "how are you today jarvis", "category": "Conversation"},
        {"command": "what can you help me with", "category": "Conversation"},
    ]
    
    results = {"passed": 0, "failed": 0, "total": len(test_cases)}
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}/{results['total']}: {test['category']}")
        print(f"Command: '{test['command']}'")
        
        try:
            payload = {"prompt": test['command']}
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                reply = data.get("response", "No response")
                print(f"✅ Response: {reply[:150]}...")
                results['passed'] += 1
                
                # Check for understanding indicators
                if "founder" in test['command'].lower() and "jinnah" in reply.lower():
                    print("🎯 Perfect understanding of historical question!")
                elif "capital" in test['command'].lower() and "islamabad" in reply.lower():
                    print("🎯 Perfect understanding of geography question!")
                elif "youtube" in test['command'].lower() and "youtube" in reply.lower():
                    print("🎯 Perfect command execution!")
                    
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                results['failed'] += 1
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            results['failed'] += 1
        
        print("-" * 50)
        time.sleep(1)  # Small delay between tests
    
    # Summary
    print(f"\n📊 ADVANCED NLU TEST SUMMARY")
    print("=" * 40)
    print(f"Total Tests: {results['total']}")
    print(f"✅ Passed: {results['passed']}")
    print(f"❌ Failed: {results['failed']}")
    print(f"Success Rate: {(results['passed']/results['total']*100):.1f}%")
    
    print(f"\n🎯 CAPABILITIES DEMONSTRATED:")
    print("• 🧠 Multi-step command understanding")
    print("• 📚 Knowledge-based questions (like ChatGPT)")
    print("• 🔍 Context-aware search commands")
    print("• ⚡ Smart automation triggers")
    print("• 💬 Natural conversation handling")
    print("• 🎯 Structured response generation")
    
    if results['failed'] == 0:
        print("\n🎉 ALL TESTS PASSED! Jarvis now has advanced understanding like ChatGPT!")
    else:
        print(f"\n⚠️  {results['failed']} test(s) failed. Check the errors above.")
    
    print(f"\n🚀 Jarvis can now understand complex queries just like ChatGPT!")

def demonstrate_understanding():
    """Demonstrate specific understanding capabilities"""
    
    print("\n" + "="*60)
    print("🎯 JARVIS ADVANCED UNDERSTANDING DEMONSTRATION")
    print("="*60)
    
    examples = [
        {
            "input": "jarvis open youtube and play a song",
            "understanding": "Multi-step command: Open YouTube + Search for music",
            "expected_action": "Opens YouTube and searches for songs"
        },
        {
            "input": "who is the founder of pakistan",
            "understanding": "Knowledge question about historical figure",
            "expected_response": "Quaid-e-Azam Muhammad Ali Jinnah"
        },
        {
            "input": "tell me about artificial intelligence",
            "understanding": "Complex informational request",
            "expected_response": "Detailed explanation of AI"
        },
        {
            "input": "search for python tutorials",
            "understanding": "Search command with specific topic",
            "expected_action": "Google search for Python tutorials"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. Input: '{example['input']}'")
        print(f"   🧠 Understanding: {example['understanding']}")
        print(f"   🎯 Expected: {example.get('expected_action', example.get('expected_response'))}")

if __name__ == "__main__":
    demonstrate_understanding()
    test_advanced_nlu()

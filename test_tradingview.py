import requests
import json

def test_tradingview_search():
    """Test if Jarvis can search for TradingView on Google"""
    
    # Test different command variations
    test_commands = [
        "search google for tradingview",
        "search google for tradingview software", 
        "open tradingview",
        "search for tradingview on google"
    ]
    
    url = "http://127.0.0.1:8000/api/ask"
    headers = {"Content-Type": "application/json"}
    
    print("Testing TradingView search functionality...")
    print("=" * 50)
    
    for command in test_commands:
        payload = {"prompt": command}
        
        try:
            print(f"\nTesting command: '{command}'")
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                reply = data.get("response", "No response")
                print(f"Jarvis Response: {reply}")
                
                # Check if the response indicates successful action
                if "searching" in reply.lower() or "opening" in reply.lower():
                    print("✅ Command processed successfully!")
                else:
                    print("⚠️  Command may not have worked as expected")
            else:
                print(f"❌ Error: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 30)

if __name__ == "__main__":
    test_tradingview_search()

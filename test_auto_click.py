import requests
import json

def test_tradingview_auto_click():
    """Test if Jarvis can search for TradingView and auto-click to open it"""
    
    # Test TradingView commands with auto-click
    test_commands = [
        "search google for tradingview",
        "search google for tradingview software", 
        "open tradingview",
        "tradingview search",
        "find tradingview"
    ]
    
    url = "http://127.0.0.1:8000/api/ask"
    headers = {"Content-Type": "application/json"}
    
    print("Testing TradingView Auto-Click functionality...")
    print("=" * 60)
    print("⚠️  WARNING: This will auto-click and open TradingView in your browser!")
    print("=" * 60)
    
    for command in test_commands:
        payload = {"prompt": command}
        
        try:
            print(f"\n🧪 Testing command: '{command}'")
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                reply = data.get("response", "No response")
                print(f"🤖 Jarvis Response: {reply}")
                
                # Check if the response indicates auto-click functionality
                if "opening the first result" in reply.lower():
                    print("✅ Auto-click activated! Will open TradingView automatically.")
                elif "tradingview application" in reply.lower():
                    print("✅ Trying to open local TradingView app.")
                else:
                    print("ℹ️  Standard search (no auto-click)")
            else:
                print(f"❌ Error: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 40)
        
        # Add delay between tests to avoid overwhelming the system
        import time
        time.sleep(2)

if __name__ == "__main__":
    test_tradingview_auto_click()

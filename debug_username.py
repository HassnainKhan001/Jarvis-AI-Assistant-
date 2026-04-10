import os
import getpass
import platform

def debug_username():
    """Debug where the username is coming from"""
    
    print("🔍 DEBUGGING USERNAME ISSUE")
    print("=" * 40)
    
    # Check various username sources
    print(f"1. os.getlogin(): {os.getlogin()}")
    print(f"2. getpass.getuser(): {getpass.getuser()}")
    print(f"3. os.getenv('USERNAME'): {os.getenv('USERNAME')}")
    print(f"4. os.getenv('USER'): {os.getenv('USER')}")
    print(f"5. platform.node(): {platform.node()}")
    
    # Check if there are any environment variables with the name
    env_vars = [k for k in os.environ.keys() if 'USER' in k.upper() or 'NAME' in k.upper()]
    print(f"6. Relevant env vars: {env_vars}")
    for var in env_vars:
        print(f"   {var}: {os.getenv(var)}")
    
    # Test face detection directly
    print("\n🧪 Testing Face Detection:")
    from face_detection import FaceDetector
    
    def test_callback(message):
        print(f"   📢 Face Detection Output: {message}")
    
    detector = FaceDetector(callback=test_callback)
    detector._on_face_detected(1)
    
    print("\n🎯 CONCLUSION:")
    print("If you still see 'Muhammad Makki' above, the issue might be:")
    print("1. Browser cache (refresh with Ctrl+F5)")
    print("2. System-level username being accessed somewhere")
    print("3. Another file we haven't found yet")

if __name__ == "__main__":
    debug_username()

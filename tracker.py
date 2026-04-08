import time
import requests
import ctypes

user32 = ctypes.windll.user32

def get_active_window_title():
    """Accesses the native Windows API to securely find out the exact name of the active foreground window."""
    hwnd = user32.GetForegroundWindow()
    length = user32.GetWindowTextLengthW(hwnd)
    buf = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buf, length + 1)
    return buf.value

def classify_activity(window_title: str) -> str:
    """Translates the active window text into the strict hackathon action space format."""
    title = window_title.lower()
    
    # Dopamine Traps
    distractions = ["youtube", "instagram", "facebook", "twitter", "reddit", "tiktok", "netflix", "whatsapp", "movies"]
    if any(site in title for site in distractions):
        return "scroll_social_media"
        
    # High Focus Workflow
    deep_work = ["visual studio", "vscode", "pycharm", "spyder", "cursor", "cmd", "powershell", "terminal", "github", "stack overflow"]
    if any(site in title for site in deep_work):
        return "deep_work"
        
    # Low Energy Admin tasks
    light_work = ["word", "excel", "gmail", "outlook", "slack", "teams", "zoom"]
    if any(site in title for site in light_work):
        return "light_work"
        
    # Unknown windows usually involve rapid task switching or breaks
    return "take_break"

def main():
    print("🚀 FocusFlow Autonomous OS Tracker Started!")
    print("Monitoring active Windows dynamically... Press Ctrl+C to stop.\n")
    print("Ensure you have another terminal running `python app.py` to view the UI live.\n")
    
    url = "http://127.0.0.1:7860/step"
    
    try:
        while True:
            time.sleep(15)  # Polls every 15 seconds safely in background
            
            title = get_active_window_title()
            
            if not title or title.strip() == "":
                action = "take_break" # Assumes they stepped away
                title = "[System Idle]"
            else:
                action = classify_activity(title)
                
            print(f"👁️ Active Window: '{title}'")
            print(f"🎯 Mapped Action: {action}")
            
            # Broadcast the action invisibly to our dashboard
            try:
                requests.post(url, json={"action_type": action}, timeout=2)
                print("✅ Broadcast Success.")
            except Exception:
                print("❌ Failed to reach local API. Make sure `python app.py` is running on another terminal!")
                
            print("-" * 50)
            
    except KeyboardInterrupt:
        print("\nTracker gracefully shut down.")

if __name__ == "__main__":
    main()

import time
import platform
import subprocess
import threading
import tkinter as tk
from tkinter import messagebox
import pyautogui # pip install pyautogui
from auth.locker import lock_windows
from auth.unlocker import unlock_windows

# --- CONFIGURATION ---
PHONE_IP = "192.168.1.4"    # Check your IP!
PING_INTERVAL = 5           # Check WiFi every 5s
MISSING_LIMIT = 3           # Strikes before warning
POPUP_TIMEOUT = 10          # Seconds to click "Cancel" before lock

# --- STATE ---
missed_pings = 0
is_locked_by_script = False
popup_open = False
stop_lock_event = None      # Event to signal "Don't Lock!"

def ping_phone(ip):
    """Returns True if phone responds."""
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    try:
        # Run ping silently
        res = subprocess.run(['ping', param, '1', '-w', '1000', ip], 
                             stdout=subprocess.DEVNULL, 
                             stderr=subprocess.DEVNULL)
        return res.returncode == 0
    except:
        return False

def show_warning_popup():
    """
    Shows a warning window. Returns TRUE if user clicked CANCEL (Stop Lock).
    Returns FALSE if timeout reached (Proceed to Lock).
    """
    global popup_open, stop_lock_event
    popup_open = True
    stop_lock_event = threading.Event()
    
    # Create a simple hidden root window
    root = tk.Tk()
    root.withdraw() # Hide the main ugly window
    root.attributes("-topmost", True) # Force on top
    
    # Custom Function to handle "Cancel" click
    def on_cancel():
        stop_lock_event.set() # Signal to stop locking
        root.destroy()
    
    # Auto-close after timeout
    def on_timeout():
        root.destroy()
        
    # Show the specific Yes/No dialog
    # We use a custom dialog logic via simple Messagebox for simplicity
    # Ideally, we build a custom window, but let's use a "Hack" to make it non-blocking
    
    # Better approach: Custom small window
    warn = tk.Toplevel(root)
    warn.title("Security Check")
    warn.geometry("300x150")
    warn.attributes("-topmost", True)
    
    lbl = tk.Label(warn, text=f"Phone Signal Lost!\nLocking in {POPUP_TIMEOUT} seconds...", font=("Arial", 12))
    lbl.pack(pady=20)
    
    btn = tk.Button(warn, text="I'M HERE! (CANCEL)", bg="red", fg="white", command=on_cancel)
    btn.pack(pady=10)
    
    # Timer loop to update UI and close
    for i in range(POPUP_TIMEOUT):
        if stop_lock_event.is_set():
            return True # User cancelled!
        
        lbl.config(text=f"Phone Signal Lost!\nLocking in {POPUP_TIMEOUT - i} seconds...")
        warn.update()
        time.sleep(1)
        
    warn.destroy()
    root.destroy()
    
    # Return True if user clicked cancel, False if timed out
    return stop_lock_event.is_set()

def monitor_wifi():
    global missed_pings, is_locked_by_script, popup_open

    print(f"📡 Smart WiFi Monitor Active: {PHONE_IP}")

    while True:
        alive = ping_phone(PHONE_IP)

        if alive:
            # --- PHONE FOUND ---
            missed_pings = 0
            
            # If we previously locked it, we unlock it now.
            # But we ONLY unlock if the script was the one that locked it (safety).
            if is_locked_by_script:
                print("🟢 Welcome back! Unlocking...")
                unlock_windows()
                is_locked_by_script = False
            
            # If computer is just normally locked by user, we can try to unlock too
            # (Optional: check if screen is locked, but 'unlock_windows' is safe to spam once)
            
        else:
            # --- PHONE MISSING ---
            missed_pings += 1
            print(f"⚠️ Ping Missed ({missed_pings}/{MISSING_LIMIT})")
            
            # ... inside monitor_wifi loop ...

            if missed_pings >= MISSING_LIMIT and not is_locked_by_script:
                # Trigger the Warning Popup
                print("⚠️ Triggering Warning Popup...")
                
                user_cancelled = show_warning_popup()
                
                if user_cancelled:
                    print("✅ User cancelled lock. Resetting counter.")
                    missed_pings = 0 
                else:
                    # --- NEW LOGIC HERE ---
                    print("🔒 Timeout reached. Locking System.")
                    lock_windows()
                    is_locked_by_script = True
                    
                    # Wait 15 seconds before killing the screen
                    time.sleep(15)
                    
                    # Turn off monitor
                    subprocess.run(["powershell", "(Add-Type '[DllImport(\"user32.dll\")]^public static extern int SendMessage(int hWnd, int hMsg, int wParam, int lParam);' -Name a -Pas)::SendMessage(-1,0x0112,0xF170,2)"])



        time.sleep(PING_INTERVAL)

if __name__ == "__main__":
    monitor_wifi()

import ctypes
import time

# Define hex code for SHIFT key
VK_SHIFT = 0x10
KEYEVENTF_KEYUP = 0x0002

def unlock_windows():
    """
    Wakes the screen by simulating a Shift key press.
    (Windows does not allow programmatically bypassing the login screen for security)
    """
    print("🔓 Waking up screen...")
    user32 = ctypes.windll.user32
    
    # Press Shift
    user32.keybd_event(VK_SHIFT, 0, 0, 0)
    # Release Shift
    user32.keybd_event(VK_SHIFT, 0, KEYEVENTF_KEYUP, 0)

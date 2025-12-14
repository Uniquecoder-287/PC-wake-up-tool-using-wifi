import asyncio
import json
from bleak import BleakScanner
from auth.proximity import is_near
from auth.locker import lock_windows
from auth.unlocker import unlock_windows

# --- LOAD CONFIGURATION ---
try:
    with open("config/device.json") as f:
        config = json.load(f)
        
    TARGET_MAC = config["mac"]
    UNLOCK_RSSI = config["unlock_rssi"] # e.g., -65 (Must be close)
    LOCK_RSSI = config["lock_rssi"]     # e.g., -80 (Must be far)
except Exception as e:
    print(f"❌ Error loading config: {e}")
    TARGET_MAC = ""
    UNLOCK_RSSI = -65
    LOCK_RSSI = -85

# --- SETTINGS ---
# How many times the phone must be "MISSING" or "FAR" before we lock.
# This prevents locking just because of one bad bluetooth scan.
CONSECUTIVE_LIMIT = 3 

# --- STATE VARIABLES ---
missed_scans = 0  # Counter for missing/far device
is_unlocked = False

async def monitor():
    global is_unlocked, missed_scans
    print(f"📡 Scanning for device: {TARGET_MAC}")
    print(f"   Unlock at > {UNLOCK_RSSI} dBm")
    print(f"   Lock at   < {LOCK_RSSI} dBm")

    while True:
        try:
            # 1. SCAN FOR DEVICES
            devices = await BleakScanner.discover(timeout=10.0)
            phone = next((d for d in devices if d.address == TARGET_MAC), None)
            
            if phone:
                current_rssi = phone.rssi
                print(f"📡 Phone Found! RSSI: {current_rssi} dBm")
                
                # --- LOGIC BRANCH 1: UNLOCKING ---
                # If phone is NEAR (Strong Signal)
                if is_near(current_rssi, UNLOCK_RSSI):
                    missed_scans = 0 # Reset "missing" counter because phone is definitely here
                    
                    if not is_unlocked:
                        print("🟢 Signal Strong! Unlocking...")
                        unlock_windows()
                        is_unlocked = True
                        print("🔓 Laptop Unlocked")
                
                # --- LOGIC BRANCH 2: MAINTAINING ---
                # If phone is in "MIDDLE ZONE" (e.g. -70 to -79)
                # It's not close enough to UNLOCK, but not far enough to LOCK.
                # We do NOT increment missed_scans here. We just relax.
                elif current_rssi >= LOCK_RSSI:
                     missed_scans = 0 # Still reset counter, because phone is present
                     # Do nothing else. Keep current state.
                     
                # --- LOGIC BRANCH 3: WEAK SIGNAL ---
                # Phone is found, but signal is very weak (Far away)
                else:
                    missed_scans += 1
                    print(f"⚠️ Signal Weak ({current_rssi} dBm). Strike {missed_scans}/{CONSECUTIVE_LIMIT}")

            else:
                # --- LOGIC BRANCH 4: PHONE NOT FOUND ---
                missed_scans += 1
                print(f"❌ Phone NOT found. Strike {missed_scans}/{CONSECUTIVE_LIMIT}")


            # --- LOCKING ACTION ---
            # If we have missed the phone (or signal was weak) for too many scans in a row:
            if missed_scans >= CONSECUTIVE_LIMIT:
                if is_unlocked:
                    print("🔒 Confirmed Away. Locking Windows...")
                    lock_windows()
                    is_unlocked = False
                    print("🔒 Laptop Locked")
                
                # Cap the counter so it doesn't grow to infinity
                missed_scans = CONSECUTIVE_LIMIT 

        except Exception as e:
            print(f"⚠️ Error during scan loop: {e}")

        # Wait a bit before next scan to save CPU/Battery
        await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(monitor())

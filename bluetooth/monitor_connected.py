import asyncio
from winsdk.windows.devices.bluetooth import BluetoothLEDevice
from winsdk.windows.devices.enumeration import DeviceInformation

# YOUR MAC ADDRESS (Keep standard format)
TARGET_MAC = "50:e7:b7:07:36:8b" 

async def monitor_connection():
    # Convert MAC to integer for Windows
    mac_int = int(TARGET_MAC.replace(":", ""), 16)
    
    print(f"🔍 Looking for paired device: {TARGET_MAC}...")

    # METHOD: We try to get the device directly. 
    # If this returns None, it means Windows hasn't "cached" the handle yet for this session.
    device = await BluetoothLEDevice.from_bluetooth_address_async(mac_int)
    
    if device is None:
        print("⚠️ Direct connection failed. Trying to force refresh...")
        # If direct fail, we just need to wait a second or ask user to toggle.
        # But usually, if it's paired, it should return an object (even if disconnected).
        print("❌ Error: Windows returned 'None'.")
        print("👉 Action: Open 'Bluetooth & Devices' settings window and keep it open.")
        return

    print(f"✅ FOUND DEVICE: {device.name}")
    print("------------------------------------------------")
    
    while True:
        # Check connection status
        status = device.connection_status.name # 'CONNECTED' or 'DISCONNECTED'
        
        # Try to read RSSI (only works if connected)
        rssi = "N/A"
        if status == "CONNECTED":
            try:
                 # We query the property directly
                 props = await device.get_device_information_async()
                 # Note: RSSI is often cached or unavailable for paired devices on some drivers
                 # We rely mostly on "CONNECTED" status for reliability
                 rssi = props.properties.lookup("System.Devices.Aep.SignalStrength")
            except:
                pass

        print(f"📡 Status: {status} | RSSI: {rssi}")

        if status == "DISCONNECTED":
            print("   ⚠️  (You are AWAY)")
        else:
             print("   🟢  (You are NEAR)")

        await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(monitor_connection())

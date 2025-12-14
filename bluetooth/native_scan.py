import asyncio

# Import native Windows Runtime (WinRT) APIs
from winsdk.windows.devices.bluetooth.advertisement import (
    BluetoothLEAdvertisementWatcher,
    BluetoothLEScanningMode
)

def on_advertisement_received(watcher, event_args):
    # This function runs every time a signal is heard
    rssi = event_args.raw_signal_strength_in_d_bm
    address = event_args.bluetooth_address
    
    # Convert address from number to Hex (MAC format)
    mac = ":".join(f"{b:02x}" for b in address.to_bytes(6, 'big'))
    
    # Get the name (local name)
    name = event_args.advertisement.local_name
    
    print(f"📡 Found: {mac} | RSSI: {rssi} | Name: {name}")

async def run_scan():
    print("🔍 Starting Native Windows Scan...")
    
    watcher = BluetoothLEAdvertisementWatcher()
    watcher.scanning_mode = BluetoothLEScanningMode.ACTIVE
    
    # Hook up the event listener
    watcher.add_received(on_advertisement_received)
    
    # Start scanning
    watcher.start()
    print("✅ Scanner started! Listening for 10 seconds...")
    
    await asyncio.sleep(10)
    
    watcher.stop()
    print("🛑 Scan finished.")

if __name__ == "__main__":
    asyncio.run(run_scan())

import asyncio
from bleak import BleakScanner

async def scan_with_uuids():
    print("Scanning for 10 seconds...")
    devices = await BleakScanner.discover(timeout=10, return_adv=True)
    
    for d, adv in devices.values():
        print(f"\n📱 Name: {d.name or 'Unknown'}")
        print(f"   MAC: {d.address}")
        print(f"   RSSI: {d.rssi}")
        print(f"   UUIDs: {adv.service_uuids}") # <--- This shows the UUIDs

asyncio.run(scan_with_uuids())

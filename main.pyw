import asyncio
from core.controller import monitor

if __name__ == "__main__":
    print("🚀 Starting Wake Up Buddy...")
    asyncio.run(monitor())

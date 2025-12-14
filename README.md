# ⚡ Wake Up Buddy (Windows Only)

Wake Up Buddy is a smart automation tool for **Windows** that automatically locks your PC when you walk away and wakes the screen when you return.  
It uses **WiFi presence detection** (pinging your phone's static IP) to decide whether you are near your computer.

> ❗ This tool is designed **only for Windows 10/11**.  
> It will not work on Linux or macOS.

---

## 🚀 Features

- **Auto-Unlock**: Detects your phone on the local WiFi network and wakes the screen when you come back.
- **Smart Auto-Lock**: Locks the workstation after your phone disappears from the network for a few checks.
- **Safety Popup**: Before locking, a warning popup appears and gives you a few seconds to cancel if you are still at the PC.
- **Power Saving**: After locking, the tool turns off the monitor using a Windows system command.
- **Background Mode**: Can run as a `.pyw` script with no console window visible.
- **Windows-Native**: Uses Windows APIs under the hood, built specifically for Windows 10/11.

---

## ⚙️ Requirements (Windows)

- **Operating System**:  
  - Windows 10 or Windows 11 (64-bit recommended)  
  - Not supported on Linux or macOS.

- **Python**:  
  - Python **3.10+** installed from the Microsoft Store or python.org.  
  - `py` launcher available in PATH (default on Windows).

- **Network**:  
  - PC and phone must be on the **same WiFi network**.  
  - Your phone should have a **static IP** on the router.

- **Libraries / Dependencies**:  
  - Uses only the Python standard library plus built-in Windows components:
    - `ctypes`, `subprocess`, `time`, `os`, `tkinter`  
  - No extra `pip install` is required for the basic functionality.

---

## 📁 Project Structure

A simple recommended layout:

WakeUpBuddy/
├─ wifi_unlocker.pyw # Main script (background mode)
├─ wifi_unlocker.py # Same script but with console (for debugging)
└─ README.md # Project documentation

text

You can keep only `wifi_unlocker.pyw` and `README.md` if you do not need console logs.

---

## 🛠️ Setup on Windows

### 1. Install Python (if not already installed)

1. Download Python 3.10 or newer from:
   - https://www.python.org/downloads/
2. During installation:
   - Check **"Add Python to PATH"**.
   - Complete the setup.

Verify Python is installed:

py --version

text

You should see something like:

Python 3.10.x

text

---

### 2. Get the Project Files

If using Git and GitHub:

cd %USERPROFILE%\Desktop
git clone https://github.com/YOUR_USERNAME/WakeUpBuddy.git
cd WakeUpBuddy

text

If not using Git:

1. Create a folder, for example: `C:\Users\YourName\Desktop\WakeUpBuddy`
2. Save `wifi_unlocker.pyw` and `README.md` inside that folder.

---

## 📡 Configure Your Phone IP (Static IP)

For Wake Up Buddy to work reliably, your phone’s IP address on WiFi must stay the same.

### Step 1: Reserve / Set Static IP on Router

On most routers:

1. Open your router admin page in a browser (usually `192.168.1.1` or `192.168.0.1`).
2. Log in with your router username and password.
3. Look for:
   - **DHCP Reservation**
   - **Static DHCP**
   - **Address Reservation**
4. Find your phone in the connected devices list.
5. Reserve a fixed IP for your phone, for example: `192.168.1.50`.

(Exact screens depend on your router brand/interface.)

### Step 2: Update the Script

Open `wifi_unlocker.pyw` (or `.py`) in a text editor and find the line:

PHONE_IP = "192.168.1.50" # Replace with your phone's static IP

text

Change it to the static IP you set for your phone.

Save the file.

---

## 🧪 How to Run (Testing Mode)

For testing with logs in a terminal:

1. Open **Command Prompt** or **PowerShell**.
2. Go to the folder where the script is:

cd C:\Users\YourName\Desktop\WakeUpBuddy

text

3. Run the script using Python (showing console):

py -3.10 wifi_unlocker.py

text

You should see log output like:

📡 WiFi Monitor Started. Watching 192.168.1.50...
🔴 Phone NOT found. Missed pings: 1/4
🟢 Phone found! PC is now considered UNLOCKED.
🔒 Locking workstation...

text

Use this mode to confirm that:

- When your phone WiFi is **on and connected**, the script sees it.
- When you **turn off WiFi on your phone** or walk away, the script eventually locks the PC.
- The safety popup appears before locking and lets you cancel.

---

## 🟢 Daily Use (Background Mode, No Console)

Once it works correctly in testing mode, use the background mode:

1. Make sure the main file is named:

wifi_unlocker.pyw

text

2. Double-click `wifi_unlocker.pyw` in File Explorer.  
   - No console window will appear.  
   - The script runs silently in the background.

You can stop it by:

- Logging out or shutting down, or
- Killing the Python process from **Task Manager** if needed.

---

## 🚀 Auto-Start on Login (Task Scheduler, Windows Only)

To make Wake Up Buddy start automatically every time you log in:

1. Press `Win + R`, type:

taskschd.msc

text

and press Enter. This opens **Task Scheduler**.

2. In the right panel, click **Create Task...** (not Basic Task).

3. **General** tab:
   - Name: `Wake Up Buddy`
   - Check: **Run with highest privileges**
   - Configure for: `Windows 10` or `Windows 11`

4. **Triggers** tab:
   - Click **New...**
   - Begin the task: `At log on`
   - Settings: `Any user` (or just your user)
   - Click **OK**

5. **Actions** tab:
   - Click **New...**
   - Action: `Start a program`
   - Program/script:
     - Either `pyw` (if in PATH), or the full path to `pythonw.exe`, e.g.:
       - `C:\Users\YourName\AppData\Local\Programs\Python\Python310\pythonw.exe`
   - Add arguments:
     - Full path to your script, for example:
       - `"C:\Users\YourName\Desktop\WakeUpBuddy\wifi_unlocker.pyw"`
   - Start in:
     - Folder where the script is:
       - `C:\Users\YourName\Desktop\WakeUpBuddy`
   - Click **OK**

6. **Conditions** tab:
   - Uncheck: **Start the task only if the computer is on AC power** (for laptops).

7. **Settings** tab:
   - Optional: Check **Run task as soon as possible after a scheduled start is missed**.

8. Click **OK** to save the task.

To test:

- Right-click the `Wake Up Buddy` task > **Run**.  
- Confirm that it runs without any visible console and reacts to your phone being present or absent.

---

## 🔧 Troubleshooting

| Problem | Possible Cause | Fix |
|--------|----------------|-----|
| Script always says phone not found | Wrong IP or phone not actually connected to WiFi | Double-check the static IP in router and in `PHONE_IP`. Ensure the phone is connected to the same WiFi. |
| PC locks while I am using it | Temporary WiFi drop or phone moved out of range | Increase the number of allowed missed pings or the warning timeout in the script. |
| Screen does not wake when I return | Phone reconnects slowly or PC already active | Give it a few extra seconds. Confirm Windows power settings are not too aggressive. |
| Nothing happens at all | Task Scheduler misconfigured or Python path wrong | Run manually from terminal first. Check you used the correct path to `pythonw.exe` and the script in Task Scheduler. |

---

## 📜 Notes and Limitations

- This tool is meant for **personal convenience**, not high-security environments.
- It assumes that your phone being near the PC is a good enough signal that you are present.
- Windows-only:
  - Uses Windows APIs via `ctypes`.
  - Uses PowerShell to turn off the monitor.
  - Designed specifically for Windows 10 and Windows 11.

---

## 📄 License

This project is intended for personal use and experimentation.  
You may modify it for your own setups or contribute improvements.

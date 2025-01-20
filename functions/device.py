from pynput.keyboard import Key, Controller
import subprocess
import platform
import time

keyboard = Controller()

def LockScreen():
    if platform.system() == "Linux":
        subprocess.run(["systemctl", "suspend", "-i"])
    else:
        raise NotImplementedError("Screen Locking has not been implemented on Windows yet")
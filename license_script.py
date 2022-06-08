import subprocess
from time import sleep
import uuid
import re
import requests
import os

def auth():
    serial_file = "key.txt"
    serial = ''
    if os.path.isfile(serial_file):
        with open(serial_file) as f:
            serial = f.read().strip()

    if serial == "":
        return False

    adress = str(get_windows_uuid())

    is_auth = check_user(adress, serial)

    if is_auth:
        return True
    else:
        return False


def check_user(adress, serial):
    data = requests.post("http://185.246.66.186:5050/check_user", json={"mac_adr": adress, "serial": serial}).json()
    return data["approved"]

def get_windows_uuid():
    try:
        # Ask Windows for the device's permanent UUID. Throws if command missing/fails.
        txt = subprocess.check_output("wmic csproduct get uuid").decode()

        # Attempt to extract the UUID from the command's result.
        match = re.search(r"\bUUID\b[\s\r\n]+([^\s\r\n]+)", txt)
        if match is not None:
            txt = match.group(1)
            if txt is not None:
                # Remove the surrounding whitespace (newlines, space, etc)
                # and useless dashes etc, by only keeping hex (0-9 A-F) chars.
                txt = re.sub(r"[^0-9A-Fa-f]+", "", txt)

                # Ensure we have exactly 32 characters (16 bytes).
                if len(txt) == 32:
                    return uuid.UUID(txt)
    except:
        pass # Silence subprocess exception.

    return None

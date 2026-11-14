import sys
import urllib.request
from pathlib import Path

OFFICE_IP_FILE = Path(__file__).with_name("office_ip.txt")


def get_public_ip():
    with urllib.request.urlopen("https://api.ipify.org", timeout=10) as response:
        return response.read().decode().strip()


try:
    current_ip = get_public_ip()
except OSError as error:
    print("Could not get the public IP:", error)
    sys.exit(1)

if not OFFICE_IP_FILE.exists():
    try:
        answer = input("Save the current public IP as the OFFICE network? (y/n) ")
    except EOFError:
        print("No answer received (not an interactive terminal). Nothing saved.")
        sys.exit(1)

    if answer.strip().lower() == "y":
        OFFICE_IP_FILE.write_text(current_ip)
        print("Saved as the OFFICE network.")
    else:
        print("Not saved.")
    sys.exit(0)

office_ip = OFFICE_IP_FILE.read_text().strip()

if current_ip == office_ip:
    print("INSIDE office network - monitoring OFF")
else:
    print("OUTSIDE office network - monitoring allowed")

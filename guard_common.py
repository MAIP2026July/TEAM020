import ipaddress
import json
import tkinter as tk
import urllib.request
from pathlib import Path

CONSENT_TEXT = (
    "To protect sensitive data, this app uses your webcam to detect phones "
    "and to check that you are at your desk during this session. "
    "No images or video are stored. Do you agree?"
)


def ask_consent():
    agreed = False

    def on_agree():
        nonlocal agreed
        agreed = True
        root.destroy()

    root = tk.Tk()
    root.title("Screen Privacy Guard")
    root.resizable(False, False)
    root.protocol("WM_DELETE_WINDOW", root.destroy)

    tk.Label(root, text=CONSENT_TEXT, wraplength=360, justify="left", padx=20, pady=20).pack()
    buttons = tk.Frame(root, pady=10)
    buttons.pack()
    tk.Button(buttons, text="Agree", width=12, command=on_agree).pack(side="left", padx=10)
    tk.Button(buttons, text="Decline", width=12, command=root.destroy).pack(side="left", padx=10)

    root.update_idletasks()
    x = (root.winfo_screenwidth() - root.winfo_width()) // 2
    y = (root.winfo_screenheight() - root.winfo_height()) // 2
    root.geometry(f"+{x}+{y}")
    root.attributes("-topmost", True)
    root.mainloop()
    return agreed


CONFIG_PATH = Path(__file__).with_name("config.json")

STATUS_CHECKING = "checking"
STATUS_INSIDE = "inside"
STATUS_OUTSIDE = "outside"
STATUS_UNKNOWN = "unknown"


def get_public_ip():
    with urllib.request.urlopen("https://api.ipify.org", timeout=10) as response:
        ip = response.read().decode().strip()
    ipaddress.ip_address(ip)
    return ip


def check_network():
    try:
        config = json.loads(CONFIG_PATH.read_text())
    except FileNotFoundError:
        return STATUS_UNKNOWN, "config.json is missing - monitoring OFF"
    except (OSError, ValueError):
        return STATUS_UNKNOWN, "config.json is unreadable or invalid - monitoring OFF"

    office_ips = config.get("office_public_ips") if isinstance(config, dict) else None
    if not isinstance(office_ips, list) or not any(isinstance(ip, str) and ip.strip() for ip in office_ips):
        return STATUS_UNKNOWN, "config.json has no office IPs - monitoring OFF"
    office_ips = {ip.strip() for ip in office_ips if isinstance(ip, str)}

    try:
        current_ip = get_public_ip()
    except (OSError, ValueError):
        return STATUS_UNKNOWN, "Could not check the network (no internet?) - monitoring OFF"

    if current_ip in office_ips:
        return STATUS_INSIDE, "Inside office network - monitoring OFF"
    return STATUS_OUTSIDE, "Outside office network - monitoring ON"

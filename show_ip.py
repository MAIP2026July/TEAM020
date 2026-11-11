import socket
import urllib.request


def get_private_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]


def get_public_ip():
    with urllib.request.urlopen("https://api.ipify.org", timeout=10) as response:
        return response.read().decode().strip()


try:
    print("Private IP:", get_private_ip())
except OSError as error:
    print("Private IP: could not be determined:", error)

try:
    print("Public IP: ", get_public_ip())
except OSError as error:
    print("Public IP:  could not be determined:", error)

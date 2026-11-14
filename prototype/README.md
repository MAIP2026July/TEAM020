# Prototype – SessionGuard V1.1 (`v1.1-privacy-fix`; first release `v1.0-first-release`)

Windows, Python 3.11.9, one webcam. Tested on one laptop with: ultralytics 8.4.142, opencv-python 5.0.0.93, pillow 12.3.0, torch 2.14.0, torchvision 0.29.0, numpy 2.4.6. `requirements.txt` pins only the first three; numpy, torch and torchvision come with ultralytics and may be a different version on another PC.

## Files
| File | Role |
|---|---|
| `guard.py` | Entry point. Reads the office IP list, asks consent, starts SecureDesk, runs detection and the absence lock, stops everything cleanly |
| `guard_common.py` | Consent window and `check_network` (public IP from `https://api.ipify.org`, 10 s timeout, compared with `config.json`) |
| `detection.py` | `PhoneDetector` class (YOLO, background thread) and webcam opening |
| `screen_cover.py` | Full-screen blurred cover made from an in-memory screenshot |
| `securedesk.py` | Demo protected application: a fake card-operations desk with a login screen and no real data |
| `view_log.py` | Read-only Employee log screen ("My Privacy Log") |
| `network_check.py` | Old stand-alone IP script with its own `office_ip.txt`. The guard does not use it; the guard uses `check_network` in `guard_common.py` |
| `show_ip.py` | Prints the local and public IP so IT can fill the list. Opens a UDP socket to `8.8.8.8:80` only to read the local address (nothing is sent) and calls `https://api.ipify.org` |
| `app.py` | Older stand-alone version of the phone guard with its own window, used during tuning |
| `test_webcam.py`, `test_detection.py` | The first camera and detection tests |
| `config.example.json` | Sample settings. Copy to `config.json` and edit |

Files kept out of Git (listed in `.gitignore` at the top of the repository): `config.json` (real office IP list), `session_log.txt` (incident lines), `office_ip.txt`, `venv/`, and the `.pt` model files.

## Set up
1. Install Python 3.11 and make a virtual environment in the project folder.
2. Install the packages in `requirements.txt`.
3. Copy `config.example.json` to `config.json`.
4. Run `show_ip.py` and put your current public IP into `office_public_ips` to simulate being inside the office. Leave the list without your IP to simulate being outside.
5. Place the model file `yolo11s.pt` next to `detection.py`. From V1.1 the library runs offline (`YOLO_OFFLINE=1`) and cannot download it. If you do not have the file, download it once on any machine and copy it in. It is not in Git.
6. Start with `guard.py`.

## Settings (`config.json`)
| Key | Meaning |
|---|---|
| `office_public_ips` | Public IP addresses of the office, set by the IT Administrator |
| `absence_lock_seconds` | Seconds with no person seen before the protected application closes and Windows locks. Sample file: 30. Demo value used by the team: 10 |

## What to expect
- **Inside:** SecureDesk opens alone. No consent window, no camera.
- **Outside:** consent window. Decline: nothing opens. Agree: SecureDesk opens and a small camera window appears at the bottom-right corner.
- **Phone:** a blurred full-screen cover appears when the rules confirm a phone and clears 2 seconds after the phone is gone.
- **Absence:** SecureDesk closes, the camera is released and Windows locks. Sign in again and restart through the guard.
- **Log:** `session_log.txt` receives incident lines only. View them with `view_log.py`.

## Limits
Simulated office check (a failed lookup is treated as outside); stand-in application; one monitor; Windows only; the guard protects only what it starts; the guard can be ended in Task Manager; phone detection is probabilistic.

## Network use
The guard calls only `https://api.ipify.org`, once at start. The helper `show_ip.py` also reads the local address through a UDP socket to `8.8.8.8:80` without sending data. The detection library did DNS lookups and sent anonymous usage statistics (no images) in v1.0. V1.1 sets `YOLO_OFFLINE=1` in `detection.py` before the library is imported. A probe that blocked and recorded Python-level network attempts saw none over 62 real predictions. Real network traffic was not captured. The model file `yolo11s.pt` must already be present. Details: `../04_Data_Privacy_Ethics_Risk.md`.

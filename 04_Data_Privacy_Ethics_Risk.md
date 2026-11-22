# 04 – Data, Privacy, Ethics and Risk
Team 020 – SessionGuard | Members: see `README.md`

## 1. Data held, exactly
| Data | Kept? | Where | How long | Why |
|---|---|---|---|---|
| Webcam frames | No. Read in memory, discarded | RAM only | Under 1 second | To see a phone or a person |
| Screenshot behind the cover | No. Built in memory, dropped when the cover goes | RAM only | Seconds | Needed to draw the blurred cover |
| Public IP address | No. Compared, never written | RAM only | Under 1 second | Office check |
| Log line (time + incident words) | Yes | `session_log.txt` on the Employee laptop | Append-only; no automatic deletion in V1. Proposed policy: 90 days, enforced in V2 | So the Employee and the Security Reviewer can see what happened |
| Face, identity, voice, screen content | Never collected | – | – | – |
| Protected application name | Not written to the log | – | – | Avoids leaking what was open |
| Office or home IP address | Not written to the log | – | – | The log says only inside or outside where needed, never the address |

**Log lines the product writes (the full list):**
1. `YYYY-MM-DD HH:MM:SS | Phone detected - screen covered`
2. `YYYY-MM-DD HH:MM:SS | Screen cover removed` (also written for a cancelled false alarm, and at shutdown if a cover was still up)
3. `YYYY-MM-DD HH:MM:SS | No person detected for N seconds - SecureDesk closed and workstation locked`
4. `YYYY-MM-DD HH:MM:SS | No person detected for N seconds - SecureDesk closed; workstation lock FAILED` (if Windows refuses the lock)

Only `view_log.py` reads the log. Write errors are ignored so logging can never crash the guard or leave the screen covered.

**What leaves the laptop.** Our code writes no image or video to disk and sends no image, video or log content anywhere. This was checked by searching every project file for image and video writing and for network calls. The only network call the guard makes is the public-IP lookup (`https://api.ipify.org`, 10 s timeout, once at start). Two helper scripts the guard never runs also touch the network: `show_ip.py` calls the same service and opens a UDP socket to `8.8.8.8:80` only to read the laptop's own address (no data is sent; this comes from how UDP sockets work, not from captured traffic), and the old `network_check.py` calls the same service. The detection library (Ultralytics 8.4.142) did more in the first release (v1.0), as found by reading its installed source:
| Library behaviour | Detail | Effect |
|---|---|---|
| DNS lookups | Looks up two public host names each time it loads | Shows that the laptop is online |
| Anonymous usage statistics | On by default in v1.0. After predictions it sends a small report, at most once every 30 seconds, to Google Analytics. Content: library, Python and torch versions, CPU name, model file name, device, speed figures, random session ids | No image, no webcam data, no log content; the connection itself shows the laptop IP to Google |
| When it can run | The model loads and runs one warm-up prediction while the consent window is open, so a report can go out even if the Employee clicks Decline | "Nothing is sent if you decline" was not true in v1.0 |
| Inside the office | The detection code is not loaded | None of this happens |
| Error reporting | Cannot run; the required package is not installed | None |
Live network traffic was not captured; this comes from reading the source.

**V1.1 fix (done, commit `540f846`, tag `v1.1-privacy-fix`).** `detection.py` sets the environment variable `YOLO_OFFLINE=1` before the library is imported. In the library source this makes both of its online checks return false, and the usage report only runs when the library is online. The model file is already present, so no download is needed. The library's own sync setting was not used: it has no environment override, and changing it means editing a settings file in the user folder, which is different on every PC.

How it was checked: a probe recorded every network attempt made from Python and blocked them all.
| Run | Result |
|---|---|
| Plain library (baseline) | A DNS lookup and a usage report to Google Analytics were attempted |
| Through `detection.py` | Zero network attempts over 29 real predictions |
| Through the guard's own start-up | Zero network attempts over 33 real predictions |

What this does not prove: the probe sees Python-level attempts only, and real network traffic was still not captured. Other machines and other library versions were not checked. The old hand-run `test_detection.py` imports the library directly, so it is not covered. Without the weights file the library can no longer download it, which is not a problem here because `yolo11s.pt` is present. The first release (v1.0) still has the statistics on.

`config.json` (holds the real office IP list) and `session_log.txt` are excluded from Git.

## 1a. How a Bank can check that SessionGuard is not the thief
A security product has to earn trust itself. Everything below can be checked by a Bank’s security reviewer from the source code in `prototype/`. We did these checks ourselves on the V1.1 code (tag `v1.1-privacy-fix`).

| What we claim | How to check it | What we found |
|---|---|---|
| **It stores no image or video** | Search the code for image and video writing (`imwrite`, `VideoWriter`, `.save(`) | None. The only file the guard writes is the text log, in `guard.py`. The screenshot behind the cover is taken in memory in `screen_cover.py`, shrunk, blurred and closed. It is never saved |
| **It sends nothing out** | Search the code for network use (`urllib`, `requests`, `socket`, `http`) | The guard makes one call: the public-IP lookup to `api.ipify.org`, once at start, with a 10-second timeout (`guard_common.py`). Two helper scripts that the guard never runs also use the network (`show_ip.py`, `network_check.py`) |
| **The detection library stays offline** | Check `detection.py` for the offline switch, then run the product and watch the network | `YOLO_OFFLINE=1` is set before the library loads. A probe that blocked and recorded Python-level network attempts saw none in 62 real predictions (29 through `detection.py`, 33 through the guard’s own start-up) |
| **It does not read keystrokes or the mouse** | Search the code for keyboard and mouse hooks (`pynput`, `keyboard`, `GetAsyncKeyState`, `SetWindowsHook`) | None |
| **The log holds only a time and an event** | Read the four log sentences in section 1 and the logging code in `guard.py` | Only those four sentences are written, one line each. No IP address, application name or image |
| **The camera opens only after consent** | Click Decline and watch the camera light | The light stays off (informal test; see `05_Model_and_Evaluation.md`, T5) |
| **A Bank can review exactly what runs** | Pin to a tagged version | The tags `v1.0-first-release` and `v1.1-privacy-fix` are in this repository |

**What we do not have yet.** We want the Bank to know where our checks stop:
- No independent security review of the code, and no signed builds. Both are planned for V2.
- The network probe sees Python-level attempts only. A packet capture, run by the Bank’s own security team behind its firewall, is the stronger proof. It should show one connection: the IP lookup.
- Most of the code that runs is not ours: the detection library, the vision library and the machine-learning framework. A Bank would review those as part of its supply chain checks. `requirements.txt` pins three packages; the versions of the others are listed in `05_Model_and_Evaluation.md`.
- Windows only, and tested on one laptop.

## 2. Consent
- A consent window appears every time the camera is about to open.
- Decline: the camera is never opened and the protected application does not run.
- Consent is per session and is not stored.
- The exact consent text (V1.1 wording, which names both the phone check and the presence check) is in `03_UX_and_Trust_Design.md`.

## 3. Data decisions the team made as owners of the product
| Temptation | Decision | What we accept |
|---|---|---|
| Keep a photo of the phone as proof | No | A Security Reviewer cannot see a picture afterwards |
| Log every event (consent, network, start, stop) | No. Logging was first designed wide, then cut to incidents only | Less audit detail, much less data to defend |
| Identify who is holding the phone | No | The product cannot say who |
| Measure idle time or productivity | No | The product cannot be used to rank Employees |
| Admin dashboard with Employee names | No | No central view in V1. A V3 mock-up and its storage design are in `12_Security_Reviewer_View_V3_Concept.md`; it would require a new consent text and Compliance Officer sign-off |

The first logging design recorded consent, network and start/stop events. During review the team asked for "minimal, only blur incidents" and the design was cut back. This is a worked example of minimisation by decision, not by statement.

## 4. Regulator view
- **Banking:** the Reserve Bank of India's information-security and outsourcing expectations apply to the bank. This product is one technical control inside that framework.
- **Personal data:** the Digital Personal Data Protection Act, 2023 applies to personal data of Employees. Our position: no personal data is retained (no image, no face, no identity). The retained log holds a time and an event label, on the Employee laptop.
- **To defend to a regulator:** the camera is needed only to see a phone and presence; we keep nothing that identifies a person; the Employee consents every session and can read every line kept.
- This is not legal advice. The bank's legal and compliance team verifies it before any pilot.

## 5. Fairness, privacy and interpretability in this product
| Word | Meaning here | Check |
|---|---|---|
| Fairness | The detector looks for an object and a presence, not for a type of person. It must not cover or lock more often for one Employee than another | 3 Employees repeat the phone test in the same lighting; difference in catch rate ≤ 10 percentage points (test T8) |
| Privacy | No image saved, no identity read | Search project and temp folders after tests: 0 image files (test T6) |
| Interpretability | The Employee can see why the screen was covered | Corner window shows HIGH RISK; the cover carries a message; the log line says what happened |

## 6. Risks and controls
| Risk | Control | Remaining risk |
|---|---|---|
| Phone missed (angle, light) | Rule windows, confidence 0.25, image size 512; limit is stated | Not a guarantee |
| A phone, camera or recording device outside the webcam’s view (side angle, another position, a CCTV camera in the room) | Not detected. Stated as a limit. SessionGuard is an extra layer next to VDI, privacy filters and the Bank’s own policies | Not covered. A privacy filter narrows the side angle |
| Capture devices other than phones (tablet, camera, smart glasses) | V1 detects phones only. Other devices are planned for V2 and need a model trained on labelled images of them | Not covered in V1 |
| Look-alike object covers the screen | 3-of-5 trigger, 10-frame confirm, 2 s release | Small annoyance |
| Office check uses public IP (a simulation) | Unknown or unreadable IP is treated as outside | Wrong list gives wrong mode |
| Employee ends the guard in Task Manager | Not blocked in V1 | Known gap; V3 would use a protected service |
| Application opened directly, skipping the guard | The shortcut is the supported path | Known gap; bank VDI policy would enforce |
| Hand-over applications (helper process then exit) | Documented; guard stops only what it started | Known gap |
| One monitor only | Documented | Known gap |
| Camera fails | Application closes with a popup | Lost work time |
| Absence lock closes the application | SecureDesk stores nothing in the demo; a real application could lose unsaved work | Needs design with the bank in V2 |
| Library sent anonymous usage statistics and did DNS lookups, even on Decline (v1.0) | Fixed in V1.1 (`YOLO_OFFLINE=1`); zero network attempts seen by a Python-level probe | Real network traffic not captured; v1.0 and `test_detection.py` still have it on |
| Consent text named phones only; the camera also checks presence (v1.0) | Fixed in V1.1; text names both | Compliance Officer still approves final wording |
| A camera read that hangs forever is not caught | Documented | Guard could stay up with a stuck camera |
| Absence lock force-closes the application with no save prompt | The demo application stores nothing; a real application needs design with the Bank | Unsaved work could be lost |
| Employees feel watched | Consent each session, text-only log, no productivity data, readable log | Trust must be earned in the pilot |
| Open-source licence | The detector is free under AGPL-3.0 only if we publish our source; a closed product needs a paid Enterprise License, price not public (`06` section 2a). Check before any sale | Legal check and a vendor quote needed |

## 7. Launch checklist
| Check | Threshold to start the pilot |
|---|---|
| Phone catch rate | ≥ 90 % in 20 trials |
| False cover | ≤ 1 per 10 minutes |
| Images stored | 0 |
| Decline test | Camera off in 5 of 5 |
| Absence lock | Locks within timer + 2 s in 5 of 5 |
| Consent text | Signed off by the Compliance Officer |
| Known gaps above | Written to the Employee and the Bank before the pilot |
If any threshold fails: stop, fix, re-measure. Do not pilot.

## 8. When the product abstains or escalates
- Camera cannot open or stops: close the protected application, show a popup.
- IP cannot be read: treat as outside.
- A cover cannot be overridden by the Employee in V1; it clears by itself 2 seconds after the last phone frame, and the incident is logged.

## 9. Shadow review
In the pilot, the Security Reviewer reads incident counts weekly and compares them with Employee feedback. Rising false covers trigger a model tuning round. The review uses the log only, never images.

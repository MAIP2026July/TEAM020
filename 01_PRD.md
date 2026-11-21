# 01 – Product Requirements Document (PRD)
Team 020 – SessionGuard | Members: see `README.md`

## 1. Business problem
Bank Employees sometimes work on sensitive screens from outside the office. A phone camera pointed at the screen can copy account-holder data. No one sees it and no record exists. Today the control is a policy document with no technical check.

## 2. Product in one paragraph
SessionGuard starts a protected application only after the Employee gives consent. Outside the office network, it watches the webcam. If a phone is confirmed, it covers the whole screen with a blurred image. If no person is seen for the lock timer, it closes the protected application, stops the camera and locks Windows. It stores no image and no video. It writes short text lines that the Employee can read on a log screen.

## 3. Roles
| Role | What they do with the product |
|---|---|
| Employee | Starts the protected application through the guard, gives consent, reads the log screen |
| IT Administrator | Sets the office public IP list and the lock timer in `config.json` |
| Security Reviewer | Reads incident lines after an event |
| Compliance Officer | Approves consent text, scope and retention |
| Bank (buyer) | Owns the risk and approves the pilot |

## 4. AI role and why AI
- **AI task:** real-time object detection on webcam frames. A pretrained YOLO model (`yolo11s`) finds the class "cell phone". The same detector reports whether a person is present.
- **Why not a rule:** a rule cannot see a phone. Only vision can.
- **Why not a human watcher:** a person cannot watch every Employee, and watching Employees is itself a privacy and culture problem.
- **Split:** detection is probabilistic (AI). Consent, network check, timers, cover, lock, log are deterministic rules.

## 5. Scope
**In scope (V1, built and demonstrated):**
1. **Guard wrapper** (`guard.py`): starts the protected application and stops everything when it closes.
2. **Consent window** every time the camera is to open. Decline keeps the camera off and the application closed.
3. **Office check:** public IP (looked up from `https://api.ipify.org`, 10-second timeout) compared with an IT-set list in `config.json`. Only an exact match skips monitoring. A missing `config.json`, a broken file, an empty list or a failed lookup are all treated as outside: consent, then camera.
4. **Phone detection:** when a phone appears in 3 of the last 5 detector results, the cover goes up at once (trigger). The next 10 results then confirm (at least 3 show a phone) or cancel (fewer than 3: false alarm, cover removed). Release comes 2 seconds after the last phone result; each new phone result restarts the 2 seconds.
5. **Real screen cover:** a borderless, always-on-top, full-screen window showing a blurred in-memory screenshot and a short message. Removed on release, on exit and on crash.
6. **Absence lock:** if no person is seen for `absence_lock_seconds` in a row, close the protected application (a forced close with no save prompt), release the webcam, remove any cover, lock Windows, exit. No auto unlock. If Windows refuses the lock, a separate log line says so.
7. **Minimal log** (`session_log.txt`, append-only): incident lines only.
8. **Employee log screen** (`view_log.py`): read-only table, three counters, a demo-data switch clearly marked as sample data.
9. **Small camera window** in the bottom-right corner showing HIGH RISK or No risk.
10. **Failure handling:** webcam cannot open, or more than 30 reads in a row fail (0.05 s apart, about 1.5 seconds), or the code crashes: the protected application is closed and a short popup explains why. No silent unmonitored work.

**Out of scope (V1):**
- Real mainframe or VDI integration. SecureDesk is a stand-in.
- Real network detection with IT. The IP list simulates it.
- Face recognition, identity, recording, any stored image.
- Multi-monitor, Mac, Linux, mobile.
- Central dashboard for managers. (A mock-up screen exists only as a V3 concept: see `12_Security_Reviewer_View_V3_Concept.md`. It is not part of the product.)
- IT-selectable protected application (built, tested and reverted; moved to V2).
- Hand-over applications that start a helper process and exit (some browsers, store apps).
- A camera read that hangs instead of failing (not caught in V1).
- Detection-library network traffic and statistics: switched off in V1.1 (see `04_Data_Privacy_Ethics_Risk.md`). Real network traffic was not captured, so this is checked at Python level only.

## 6. Configurable or fixed
| Item | Configurable? | Where |
|---|---|---|
| Office public IP list | Yes | `config.json`, key `office_public_ips` (IT Administrator) |
| Absence lock timer | Yes | `config.json`, key `absence_lock_seconds` (demo value 10, default 30) |
| Model file | Replaceable file | `yolo11s.pt` |
| Confidence 0.25, image size 512 | Code constants | `detection.py` |
| Result rules (3 of 5, 3 of next 10, 2 s), person confidence 0.5 | Code constants | `detection.py` |
| Consent text | Code constant | consent window |
| Protected application | Fixed to SecureDesk in V1 | `guard.py` (V2: configurable) |

## 7. Defined terms (no vague words)
| Term | Meaning in this product |
|---|---|
| Detector result | One output of the detector. The detector runs on its own thread, so 5 results take roughly half a second to a second. All rules below count results, not camera frames |
| Phone detected (trigger) | Model class "cell phone" at confidence ≥ 0.25 in at least 3 of the last 5 results. The cover goes up |
| Phone confirmed | At least 3 of the next 10 results also show "cell phone". Otherwise the cover is removed as a false alarm (a "covered" and a "removed" line are still logged) |
| Cover | Full-screen blurred window over the main screen |
| Release | Cover removed 2 seconds after the last frame that shows a phone |
| Outside office | Public IP not in the IT list, or the IP cannot be read (fail-safe) |
| Absence | No "person" detected with confidence ≥ 0.5 for `absence_lock_seconds` in a row, counted from the later of monitoring start and the last person result |
| Incident | A confirmed phone cover or an absence lock |
| Consent | The Employee clicks Agree on the consent window in the current session |

## 8. Success metrics
| Metric | How measured | Target | Measured |
|---|---|---|---|
| Phone catch rate | 20 trials, phone held toward the screen at about 50 cm; count covers | ≥ 90 % (18 of 20) | Informal: about 30 trials, all covered; formal count pending |
| False cover rate | 10 minutes at the desk, normal objects, no phone; count covers | ≤ 1 per 10 min | Informal: TV remote covered in about 5 of 30 trials; formal count pending |
| Time to cover | Stopwatch from phone appearing to screen covered; 5 runs | ≤ 3 s average | Informal: usually 1 to 2 s; not timed |
| Release time | Phone removed to screen clear; 5 runs | 2 s ± 1 s | Informal: about 1 s; not timed |
| Images stored | Search project and temp folders after all tests | 0 | Checked 14 Nov: the product writes no image or video; code search and folder search agree |
| Decline test | Click Decline 5 times; check camera light | Camera off 5 of 5 | Informal: camera light never came on; count not logged |
| Startup (Agree to camera ready) | Stopwatch | ≤ 10 s on the pilot laptop | Slow on the CPU-only development laptop; faster on a better one; not timed |
| Absence lock | Walk away; stopwatch | Locks within timer + 2 s | Informal: worked every time; not timed |

Engineering facts that are already recorded (per-frame time, rule logic checks, lifecycle checks) are in `05_Model_and_Evaluation.md`.

## 9. Prototype
Python 3.11, Tkinter, OpenCV, Ultralytics YOLO. Files and set-up: `prototype/README.md`. Releases: `v1.0-first-release` and `v1.1-privacy-fix` (current).

## 10. Human in the loop
| Point | Human role |
|---|---|
| Consent | Employee decides to Agree or Decline each session |
| False cover | Employee waits for the 2-second release; the incident is logged |
| Log review | Security Reviewer reads the lines after an incident |
| Setup | IT Administrator owns the IP list and the timer |
| Policy | Compliance Officer owns consent text and retention |
| After a lock | Employee signs in to Windows and restarts the application through the guard; consent is asked again |

## 11. Roadmap
**V1 – first pilot. Timeline: 8 weeks to a decision (plan).**
| Phase | Weeks | Outcome |
|---|---|---|
| 0 Define | 1 | PRD and consent text approved by the Compliance Officer |
| 1 Build | 2–4 | Guard, detection, cover, lock, log (prototype done) |
| 2 Measure | 5 | Metrics table run on 3 laptops |
| 3 Pilot | 6–7 | 10 Employees, one team, outside-office use |
| 4 Decide | 8 | Go / no-go against section 12 |

**V2 (sketch):** IT-selectable protected application; hand-over application handling; multi-monitor; log retention enforced by code; model tuning on pilot laptops.
**V3 (sketch):** VDI integration; real network detection with the bank's network team; counts-only report for the Security Reviewer (mock-up and storage design in `12_Security_Reviewer_View_V3_Concept.md`); optional offer to other banks.

## 12. Go / no-go for the pilot
Go if all hold: catch rate ≥ 90 %, false cover ≤ 1 per 10 minutes, images stored = 0, decline test 5 of 5, Compliance Officer signs the consent text. Otherwise: fix, re-measure. The results so far (section 8) are informal observations, so the first step of the pilot is the formal measurement. The look-alike TV remote and the start-up time on a laptop without a graphics card are the two points to watch.

# 05 – Model and Evaluation
Team 020 – SessionGuard | Members: see `README.md`

## 1. Model choice
| Model tried | Result for this product | Outcome |
|---|---|---|
| YOLOv8n (nano) | Fast, detects many classes, but weak on look-alike objects; the team judged it correct roughly 60–70 % of the time on its own informal tests | Replaced |
| YOLOv8s | Better at telling objects apart | Replaced |
| YOLO11s | Same speed class as v8s, better accuracy | **Chosen** |
| YOLO11m | More accurate but too slow on a CPU-only laptop | Rejected, rolled back to YOLO11s |
| YOLO11s + CLIP second check | Fewer look-alike covers but broke detection of rotated phones and slowed startup | Rejected and removed |

The full story of each step is in `08_Detection_Tuning_Log.md`.

## 2. Final detector settings
| Setting | Value | Why |
|---|---|---|
| Model | `yolo11s.pt` | Best balance of speed and accuracy found |
| Confidence | 0.25 | 0.15 flagged a mouse; 0.35 together with size 416 led to missed phones |
| Image size | 512 | 416 lowered catches (with 0.35); 640 was slower |
| Classes read | cell phone (class 67); person (class 0, confidence ≥ 0.5, for the absence lock) | Narrow task |
| Rules | 3 of 5 trigger; 3 of next 10 confirm; 2 s sliding release. These count detector results, not camera frames (5 results ≈ 0.5–1 s) | Cuts one-frame errors |
| Threading | Detector in a background thread | Keeps the video smooth |

## 3. Facts already recorded
These were observed during the build on the development laptop (Windows, CPU only, no graphics card).
| Fact | Value | Note |
|---|---|---|
| Time per frame at size 640 | about 146 ms (about 7 frames per second) | Before the speed work |
| Time per check at size 416 | about 81 ms | Used briefly; it lowered the catch rate |
| Cost of blurring a full frame | about 70 ms | Fixed by blurring a shrunken copy and scaling back up |
| Detection logic checks | 16 scripted checks against the written rules, using scripted detections and a fake clock | All passed |
| Start and stop flow checks | 10 scenarios with a fake camera and a fake protected application: inside office, decline, close application, `q`, window close, failed webcam, crash | All passed |
| Process shutdown | Ending the protected application through the guard leaves no process behind | Passed |
| Run without console | Detector loads and runs under `pythonw.exe`, which the desktop shortcut uses | Passed |
| V1.1 regression checks (14 Nov) | Detection rules, 11 cover and lifecycle scenarios, logging, 18 absence-lock scenarios, guard with real SecureDesk, log screen data and window, network-switching simulation, new consent-window test | All passed after the V1.1 change. The corner-window suite failed once in a full run and passed on four reruns (it depends on live screen and keyboard focus) |
| Network probe (14 Nov) | Python-level network attempts recorded and blocked: 29 predictions via `detection.py`, 33 via the guard start-up | Zero attempts; the plain library showed a DNS lookup and a usage report |

## 4. Why the 3-of-5 rule makes tuning sensitive
If a single frame catches the phone with probability p, the chance that the trigger fires (at least 3 of 5 frames) is:
| p, single-frame catch rate | Chance of 3 of 5 |
|---|---|
| 0.7 | 83.7 % |
| 0.5 | 50.0 % |
| 0.4 | 31.7 % |
| 0.3 | 16.3 % |

A modest drop in single-frame accuracy becomes a large drop in catches. This is the reason confidence 0.35 and size 416 were reverted.

## 5. Test plan and results
The Result column holds what the team saw on the demo laptop on 14 Nov 2026. "Informal" means manual observation by the team without a stopwatch or a written trial log, so counts are approximate. These are not formal measurements against the protocol in the Test column. The formal run (20 logged trials for T1, stopwatch for T3, T4, T9 and T10) is the first step of the pilot.
| # | Test | Method | Pass line | Result |
|---|---|---|---|---|
| T1 | Phone catch rate | Hold a phone toward the screen 20 times at about 50 cm | ≥ 18 of 20 covered | Informal: about 30 trials, a phone covered every time; some covers were slow (CPU only). Exact count and distance not logged |
| T2 | False cover | 10 minutes at the desk with mouse, charger, cup, notebook, no phone | ≤ 1 cover | Informal: a TV remote was covered as a phone in about 5 of 30 trials. Other desk objects: no false cover seen. Minutes at desk not logged |
| T3 | Time to cover | Stopwatch, 5 runs | ≤ 3 s average | Informal: usually 1 to 2 s. No stopwatch |
| T4 | Release time | Remove phone, stopwatch, 5 runs | 2 s ± 1 s | Informal: about 1 s. No stopwatch |
| T5 | Decline | Click Decline 5 times; check camera light | Off in 5 of 5 | Informal: Decline clicked several times (count not logged); the camera light never came on |
| T6 | No images | Search project and temp folders after T1–T5 | 0 files | Checked 14 Nov: no image or video file written by the product. The code writes only log text (and the old `network_check.py` writes `office_ip.txt`). A search of the project and temp folders found only window screenshots saved by the coding agent's own test scripts, none by the guard or the webcam |
| T7 | Dim light | Repeat T1, 10 trials | Report rate | Informal: no visible change in dim light; tries not counted |
| T8 | Different Employees | 3 people, 10 trials each | Gap ≤ 10 percentage points | 2 people tried; no numbers recorded |
| T9 | Absence lock | Walk away; stopwatch | Lock within timer + 2 s | Informal: worked every time; seconds not timed |
| T10 | Startup | Agree to camera ready | ≤ 10 s on pilot laptop | Slow on the development laptop (CPU only, no graphics card); faster on a teammate's better laptop. Seconds not timed, target not confirmed |
| T11 | Log screen | Open "My Privacy Log" after T1 and T9 | Counters match the events | Informal: counters matched the events made |

## 6. Observed behaviour, as reported by the team during testing
These are qualitative observations from live tests, not measurements.
- A computer-mouse underside with a light was sometimes taken for a phone at low confidence.
- Phone-shaped chargers and some toys were sometimes taken for a phone.
- A phone held straight toward the screen was caught best; steep or rotating angles were caught less reliably.
- On the development laptop the camera is slow to open (model load). The team plans to re-check on a faster laptop.
- A TV remote that looks like an old phone was covered in about 5 of 30 informal trials. It is the main false-cover case seen.
- Detection is sometimes slow on the CPU-only development laptop, but the phone was still caught in the end.
- Results are from two people in total (T8); no gap between them was measured.

## 7. Tested software versions
Python 3.11.9; ultralytics 8.4.142; opencv-python 5.0.0.93; pillow 12.3.0; torch 2.14.0; numpy 2.4.6.

## 8. Known limits
- Detection is probabilistic; misses and look-alike covers happen.
- No custom model was trained (needs labelled phone images and time; out of V1).
- Results come from one laptop and one camera.
- The office check is a simulation.

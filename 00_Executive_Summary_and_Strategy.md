# 00 – Executive Summary and Strategy
Team 020 – SessionGuard | Members: see `README.md`

## 1. Executive summary
Banks let some Employees work on sensitive screens from outside the office. Those screens can show account-holder data, for example a mainframe session. A phone camera pointed at the screen can copy that data in two seconds. Nobody sees it and nothing is recorded. Today the control is a written policy.

SessionGuard is a small desktop guard for the Employee laptop. It starts the protected application only after the Employee agrees to camera monitoring. Outside the office network, the webcam looks for a phone. If one is seen, a blurred full-screen cover hides the screen at once. If the Employee leaves the seat, the application closes and Windows locks.

Three design choices define the product:
1. **Nothing is stored.** No frame, no screenshot, no face, no identity. A short text log holds only the time of an incident.
2. **Consent every time.** The camera never opens without an Agree click in that session.
3. **Narrow and session-bound.** The camera runs only while the protected application is open and the laptop is outside the office. It does not measure work, keystrokes or idle time.

The working prototype was built and tuned by the team across many test rounds. The record of every change, every rollback and every decision is in `07_Build_Journey_and_Iterations.md` and `08_Detection_Tuning_Log.md`.

## 2. The problem in numbers we can defend
| Statement | Status |
|---|---|
| A phone photo of a screen takes about 2 seconds | Common knowledge, easy to test |
| A policy page cannot prove that photos were not taken | True by definition |
| Leak rate and cost of one leak | Planning assumptions in `06_Business_Case_and_Economics.md`, marked (A) |

## 3. Jobs to be done
| Role | The job they hire the product for |
|---|---|
| Bank — Information Security head | "When Employees work from home on sensitive screens, give me a technical control I can show to an auditor, without recording them." |
| Service Company (buyer) | "Give me a tool I can show the Bank to earn its trust and win projects, and let me offer work from home to Employees on critical projects so they stay." |
| Employee | "Let me finish my work from home without being watched all day, and tell me clearly when and why my screen was hidden." |
| IT Administrator | "Let me set the office network and timers once, in one file, without code changes." |
| Security Reviewer | "After an incident, show me what happened and when, in one line." |
| Compliance Officer | "Let me defend every piece of data kept, to a regulator, in one page." |

## 4. Strategy
**Positioning.** A security control for the Employees of a Service Company who work on a Bank’s data. The Service Company buys it to show the Bank a working control. It is not a monitoring product and not a productivity product.

**Place in the stack.** SessionGuard is an **extra layer on top of** VDI, privacy filters and office policy, not a replacement for them. It is for the case where Employees must work from home and office-only work is too costly. It cannot see anything outside the webcam’s view, including a CCTV or other camera in the room, and V1 detects phones only. Competitors and alternatives: `06_Business_Case_and_Economics.md` section 11.

**Wedge.** One threat only: a phone camera pointed at the screen. One more rule that comes from the same camera view: an empty seat locks the session. Everything else is out of scope for V1.

**Why this wedge.**
- It is a threat that file-based controls cannot see.
- It needs no integration with the bank's systems to demonstrate.
- It forces a clear privacy answer (store nothing), which makes approval easier.

**What we chose not to do, and why.**
| Option | Decision | Reason |
|---|---|---|
| Record images as evidence | No | Creates a new thing to protect and to defend to a regulator |
| Face recognition or identity check | No | Not needed to see a phone; raises privacy risk |
| Monitor all the time | No | Camera runs only in the risky state |
| Add size or shape filters to the detector | No | Tested idea; risked missing real phones (see `08_Detection_Tuning_Log.md`) |
| Second-stage image check (CLIP) | No | Tested; it broke detection of rotated phones and slowed startup |
| Open documents inside our own window | No | Breaks the business purpose: the real application must stay the real application |
| IT-selectable protected application | Not in V1 | Built, tested and reverted for time and risk; kept as V2 |

## 5. Build, buy or API
| Option | View |
|---|---|
| Build on an open-source pretrained model (chosen) | No licence fee in the prototype; runs on the laptop; no image leaves the machine |
| Buy a general data-loss-prevention suite | Such suites mostly watch files, clipboards and printing. Camera-based phone detection is a gap to confirm by market research |
| Cloud vision API | Sends images off the laptop and breaks the no-storage promise |

**AI role.** Computer vision: real-time object detection (YOLO). Everything around it is fixed logic: consent, network check, timers, lock, log. This split is deliberate: the probabilistic part is small and visible, the rest is deterministic and testable.

## 6. Standalone or embedded
V1 is a standalone wrapper that starts the protected application. V3 would embed it inside the bank's VDI client, where the protected session is already controlled.

## 7. Success evidence and decision
Go to a 10-seat pilot only if the targets in `01_PRD.md` section 8 are met on the pilot laptops, and the Compliance Officer signs off the consent text and the retention rule.

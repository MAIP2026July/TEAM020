# 03 – UX and Trust Design
Team 020 – SessionGuard | Members: see `README.md`

Principle: the Employee should always know three things: **what is being watched, why the screen was hidden, and what happens next.**

## 1. Screens and messages
| # | Moment | What the Employee sees | Trust purpose |
|---|---|---|---|
| 1 | Start inside the office | SecureDesk opens alone. No consent window. No camera window | Shows the camera is not used where it is not needed |
| 2 | Start outside the office | Consent window with Agree and Decline | Consent is asked every time the camera is to open |
| 3 | Decline | Nothing opens. The camera light stays off | A real choice with no penalty on the camera side |
| 4 | Agree | SecureDesk opens, then a small camera window appears at the bottom-right corner | Shows exactly what the camera sees |
| 5 | No phone | Camera window text: No risk (green) | Live status, never hidden |
| 6 | Phone triggered | Full-screen blurred cover with the message "Phone detected - screen hidden for data protection"; camera window text: HIGH RISK (red). The cover appears at the trigger and stays only if the next results confirm a phone | Says why, in plain words |
| 7 | Phone removed | Cover is removed after 2 seconds | Predictable, not punishing |
| 8 | Camera fails | Popup that explains the camera problem; protected application closes | Never silent |
| 9 | Absence lock | Application closes; Windows lock screen; the Employee signs in again with the normal password | Uses the normal sign-in; the product has no unlock of its own |
| 10 | Log screen ("My Privacy Log") | Read-only table of incident lines, three counters (phone incidents, absence locks, time of last incident), top note that no image or personal data is stored | Lets the Employee see everything the product kept |

## 2. Exact texts the Employee sees
**Consent window** (title "Screen Privacy Guard"; buttons Agree and Decline; the window's X counts as Decline):
> To protect sensitive data, this app uses your webcam to detect phones and to check that you are at your desk during this session. No images or video are stored. Do you agree?

This is the V1.1 text (commit `540f846`, 14 Nov 2026). The first release (v1.0) said "detect phones during this session" and did not mention the presence check. The window shows the full text on three lines with both buttons visible.

**Cover message:** Phone detected - screen hidden for data protection

**Popups** (title "Screen Privacy Guard"):
| Situation | Text |
|---|---|
| Webcam cannot open | The webcam could not be opened, so SecureDesk was closed. Monitoring is required outside the office network. |
| Webcam stops | The webcam stopped working, so SecureDesk was closed. Monitoring is required outside the office network. |
| Monitoring could not be prepared | Monitoring could not be prepared, so SecureDesk was not started. (then the error text) |
| Unexpected stop | The guard stopped unexpectedly. (then the error text) |

**Log screen note:** This log records only the time a phone was detected and the screen was covered, and absence locks. No images or personal data are stored.

**Why the text changed:** the camera also checks that a person is present (for the absence lock). The v1.0 text named phones only, so informed consent was weaker. V1.1 names both. The Compliance Officer still approves the final wording before any pilot.

## 3. How uncertainty is shown
| Uncertain thing | How the Employee is told |
|---|---|
| The detector might be wrong | Status text is shown live in the corner window. A cover always carries a message and clears by itself |
| A cover may be a false alarm | Release after 2 seconds; one log line records it |
| The product cannot see everything | Known limits are listed in `README.md` and `04_Data_Privacy_Ethics_Risk.md` |

## 4. Trust rules built into the design
1. The camera opens only after Agree, only outside the office, only while the protected application is open.
2. Nothing the camera sees is saved.
3. The log never contains the IP address, the application name or any image.
4. The product has no override that disables it quietly. If it cannot do its job (camera fails), it closes the application instead of continuing unwatched.
5. The product never measures work: no keystrokes, no idle time, no screen content.

## 5. What we deliberately did not build into the screens
- No sound alarms, no popups to managers, no photos of the phone.
- No "report" button or hidden remote view.
- No admin screen with Employee names. An admin view was considered and dropped to protect trust.

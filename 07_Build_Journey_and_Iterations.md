# 07 – Build Journey and Iterations
Team 020 – SessionGuard | Members: see `README.md`

This is the real history of the build. Each step followed the same loop: **the AI proposed, the team member tested on a real laptop, reviewed the result, and decided.** Many steps were rejected or rolled back. The rejected steps are part of the evidence of product judgement.

## 1. Method
1. State the next small capability in plain words.
2. Write a precise prompt for the coding agent, with "do not change X" lines to protect what already worked.
3. Run it on the Windows laptop. Test by hand with a real phone and real objects.
4. Report what was seen: missed phone, false cover, slow start, wrong behaviour.
5. Decide: keep, tune, or roll back. Save good states with Git tags.

Tools: Claude (chat) for planning and prompts; Claude Code on Windows for building and testing; Git for save points; the Claude Code checkpoint "Rewind" for going back.

## 2. Timeline at a glance
| Phase | When | What happened | Outcome |
|---|---|---|---|
| 0 Idea | Before the restart | Ideas weighed; webcam screen-guard chosen as the smallest honest project | Direction set |
| 1 First detection | Before the restart | Webcam test, YOLO test, blur and risk rules | Working but weak |
| 2 Tuning rounds | Before the restart | 13 experiments on thresholds, models, rules, CLIP | `yolo11s`, 3-of-5, confirm, 2 s release |
| 3 Restart and speed | 7 Nov | Background thread, speed vs accuracy | Reverted to conf 0.25, size 512 |
| 4 Consent and office check | 10 Nov | Consent window, IP list in `config.json` | Fail-safe office check |
| 5 Protected application | 10 Nov | Fake VDI application SecureDesk and the guard wrapper | Guard starts and stops everything |
| 6 Real screen cover | 10–11 Nov | In-memory blurred full-screen cover | Real cover, not only a camera blur |
| 7 Logging | 11 Nov | Log designed wide, then cut to incidents only | Minimal log |
| 8 Corner camera | 12 Nov | Small camera window bottom-right | Demo-ready |
| 9 Absence lock | 13 Nov | Close, release, lock | Done; timer 10 s for demo |
| 10 Employee log screen | 13 Nov | Read-only screen, three counters | Done |
| 11 Configurable application | 13 Nov | Built, tested, then reverted | Moved to V2 |
| 12 First release | 13 Nov | Freeze | Tag `v1.0-first-release`, commit `fd19c04` |
| 13 Privacy fix | 14 Nov | Statistics off, consent text names presence check | Tag `v1.1-privacy-fix`, commit `540f846` |

## 3. Phase 0 – Choosing the idea
Several ideas were weighed and dropped before this one: explainer-style tools, API-triggered ideas, and a BFSI migration idea. The team member wanted something real-time, small enough for about eight working days, and honest about what a non-coding MBA team can build. The webcam screen-guard won because it uses computer vision, runs offline, and has a clear privacy answer.

Rules agreed early: **store no data; do not monitor work culture; ask consent; run only in the risky state.** The "risky state" was later defined as outside the office network with a protected application open.

## 4. Phase 1 – First detection
- A webcam test script confirmed the camera works with OpenCV.
- A detection test script ran YOLOv8n live and printed what it saw. It found a person constantly and also phone, laptop, remote, book, scissors, TV and others. The team's own estimate was that it was right about 60–70 % of the time.
- A first guard built the risk rule: a phone means HIGH, more than one person means MEDIUM. The first blur only blurred the camera picture, not the real screen.
- Early feedback from testing: blur and no-blur flickered; the blur hit the webcam preview instead of the desktop.

## 5. Phase 2 – Tuning rounds
Thirteen experiments are logged one by one in `08_Detection_Tuning_Log.md`. In short:
- Confidence 0.15 caught more angles but flagged a mouse as a phone; it was dialled back.
- The sliding 2-second window (every phone frame resets the timer) was confirmed to work: the cover no longer dropped while a phone stayed in view.
- A single-frame decision was too jumpy; a multi-frame rule was introduced (first 6 of 10, then cut to 3 of 5 because it reacted too slowly).
- A confirm step was added: after the trigger, watch the next 10 frames and drop the cover if fewer than 3 show a phone.
- Model steps: YOLOv8n → YOLOv8s → YOLO11s; YOLO11m tried and rolled back for speed.
- Size and shape filters were suggested and **rejected** by the team member to avoid disturbing the model.
- A second-stage lens check with CLIP was tried: it reduced look-alike covers but broke rotated phones. A multi-frame version was proposed; the team member then chose to remove CLIP and return to the YOLO-only version.

## 6. The CLIP rollback, in detail
1. The team member's idea: rectangular look-alikes have no camera lens, so check for a lens.
2. A web search was run for other approaches; CLIP image-text matching was chosen to test.
3. Result: fewer false covers, but a phone rotated like a clock hand from 12 to 3 o'clock was no longer covered, and startup was slow.
4. The cause was a single snapshot checked at the trigger moment. A five-frame vote was proposed.
5. The team member decided to go back to the version that had worked before CLIP.
6. A clean rewrite from the written specification (yolo11s, 3 of 5, 10-frame confirm, 2 s grace) did not reproduce the old behaviour: detection was slow. The Claude Code checkpoint feature, Rewind, was then used and restored the version that worked. The team member also asked why a patch could not simply be removed, and concluded: "so this is why we use version control."
7. Lesson recorded: **save a Git tag after every good state.** From this point every working step was saved with a tag.

## 7. Phase 3 – Restart and speed (7 Nov)
- The project was restarted after a gap. The first step was a revision of what existed and a live run.
- Complaints: slow response and normal objects causing covers.
- Measured: about 146 ms per frame at size 640 on CPU.
- Change tried: detector in a background thread, size 416, confidence 0.35, phone class only (about 81 ms per check).
- Result on 10 Nov: phones were missed often. An investigation (no code changes allowed) found the likely cause: the 0.35 and 416 changes lowered the chance per frame, and the 3-of-5 rule magnified that (table in `05_Model_and_Evaluation.md`).
- Fix: confidence back to 0.25, size 512, keep the background thread, blur a shrunken copy of the frame to cut the 70 ms blur cost.
- A startup-time measurement was requested (import, model load, camera open, first frame). The team member decided to accept the slow start on this laptop and re-check on a faster one.

## 8. Phase 4 – Consent and the office check (10 Nov)
Ideas tried in order:
1. Two simulated tick boxes: "outside office" and "critical screen". Proposed first as the safe simulation.
2. The team member asked for Wi-Fi name detection and a link to a real desktop application.
3. The team member then asked whether an IP-address solution was possible. **Public IP comparison** was chosen, because an IT team can know and fix the office public IP, and the team can build it without network expertise.
4. First design asked for the IP at start. The team member replied: "better to predefine this IP and store it somewhere rather than the system asking." Result: `config.json` with `office_public_ips`, owned by the IT Administrator.
5. Consent was made to appear **every time the camera is to open**, including when switching from office network to mobile network.

## 9. Phase 5 – The protected application (10 Nov)
- First idea: trigger monitoring when a specific PDF opens. Rejected: opening the document inside our own window "completely breaks our business intention".
- Second idea: watch for the document in other windows. Rejected: monitoring which files are open breaks the no-monitoring rule.
- Third idea: a simulated VDI-like secure desk. Accepted. **SecureDesk** was built: a small fake card-operations application with a login screen and no real data.
- A **guard wrapper** (`guard.py`) now starts SecureDesk and everything else. Detection code was moved to `detection.py` unchanged.
- Windows detail tested first: a virtual-environment `python.exe` is a launcher that starts the real Python as a child, so stopping the launcher alone could leave SecureDesk running unmonitored. A heartbeat test confirmed that the guard ends the whole process tree.
- 10 start/stop scenarios and 16 logic checks passed.

## 10. Phase 6 – Real screen cover (10–11 Nov)
The team member pointed out that blurring the camera picture was not the product. The real cover was built: one in-memory screenshot, strongly blurred, shown borderless, full-screen and always on top. It never touches disk. It is removed on release, on exit, on `q`, on window close and on a crash.
Related find on 11 Nov: monitoring started on the home network because the home public IP had changed. The IP list is now understood as IT-managed; a real office IP is fixed. The fail-safe (unknown means monitor) is kept.

## 11. Phase 7 – Logging (11 Nov)
Save points: tag `v1-detection` on the tuned detection commit, then `v2-guard-screen-blur`. A first wide log design (consent, network, start, stop, incidents) was written. The team member then said: "logging should be minimal, it should not overwrite, it will write only the blur incidents." The log was cut to two lines for a cover and later one line for an absence lock. Tag `v3-logging`.

## 12. Phase 8 – Corner camera (12 Nov)
The camera window had appeared large in the middle. The team member asked for a small window at the bottom-right. Tag `v4-corner-preview`. Also on 12 Nov the team member prepared a live demo for teammates.

## 13. Phase 9 – Absence lock (13 Nov)
Idea first raised on 12 Nov as an idea and put on hold, then built on 13 Nov. Rules written:
- Only while monitoring is on (outside the office, application open, consent given).
- No person seen for N seconds in a row: close SecureDesk, release the camera, remove any cover, lock Windows, exit.
- No auto unlock. The Employee signs in to Windows and restarts through the guard, so consent is asked again.
- The close is forced, with no save prompt (safe for SecureDesk, which stores nothing).
- N is a setting; demo value 10 seconds.
Tested with a fake IP and a short timer.

## 14. Phase 10 – Employee log screen (13 Nov)
The team member asked for a log screen with analytics for both Employee and admin, then narrowed it: **Employee screen only**. Built read-only with three counters, a top note about what is not stored, and a clearly marked sample-data switch for demos that never touches the real log.

## 15. Phase 11 – Configurable protected application (13 Nov) – built and reverted
Idea: let IT pick the protected application in a setup window. Claude Code built a setup screen and a hand-over rule. In testing, the behaviour was not what the team member wanted (a guarded shortcut per application) and it carried risk: hand-over applications cannot be tracked, and an application closed by the absence lock could lose work. The decision: "no, lets not mess this, lets revert … I don't have that much time … will add these in the future." A safety save (`v5-before-revert`) was made first. The configurable parts were removed by hand, keeping the absence lock, logging, corner window, consent and detection. Moved to V2.

## 16. Phase 12 – First release (13 Nov)
Final check: all expected files present, features present, config checked, no real IP or email in the commit. Commit `fd19c04`, tag `v1.0-first-release`.

## 17. Phase 13 – Privacy fix (14 Nov)
The audit showed two gaps. The library sent anonymous statistics, and the consent text did not name the presence check. The coding agent was asked for two small changes and told not to touch the detection rules, thresholds, model, absence lock, logging, cover or SecureDesk. It set `YOLO_OFFLINE=1` before the library import and changed the consent text. It did not use the library's sync setting, because that edits a per-PC settings file. A probe that recorded and blocked Python-level network attempts saw zero attempts over 62 real predictions (the plain library showed a DNS lookup and a usage report). The existing checks passed. One corner-window test failed once in a full run and passed on four reruns; it reads live screen and keyboard focus, and the code it tests was not changed. Commit `540f846`, tag `v1.1-privacy-fix`, nothing pushed.

## 18. Save points
| Commit | Date (2026) | Message | Tag |
|---|---|---|---|
| `540f846` | 14 Nov | V1.1: statistics off, consent text names presence check | `v1.1-privacy-fix` |
| `fd19c04` | 13 Nov 23:31 | First release: guard, SecureDesk, logging, absence lock, employee log screen | `v1.0-first-release` |
| `5f25e6a` | 13 Nov 23:15 | Safety save before removing configurable application | `v5-before-revert` |
| `e5b631b` | 12 Nov 00:35 | Small camera preview in corner | `v4-corner-preview` |
| `e582278` | 12 Nov 00:01 | Minimal blur-incident logging added | `v3-logging` |
| `5eba3d0` | 11 Nov 23:45 | Guard, SecureDesk, real screen blur working | `v2-guard-screen-blur` |
| `4b45581` | 10 Nov 14:32 | Detection tuned, good enough for MVP | `v1-detection` |

## 19. Final audit (14 Nov)
Before submission the documents were checked against the code. The coding agent was asked, in read-only mode, to answer 11 questions from the actual files and Git history. It found differences, and each was corrected in these files: the cover goes up at the trigger, not after confirmation; consent is also asked when the IP cannot be checked; the consent text mentions phones only; the detection library sends anonymous usage statistics and does DNS lookups (both fixed in V1.1, phase 13); `network_check.py` is an old unused script (the guard uses `check_network` in `guard_common.py`); the absence lock force-closes the application; a second log wording exists for a failed lock. Details: `09_AI_Collaboration_Log.md` section 8.

## 20. What this journey shows
1. **Small steps with protection:** each prompt said what must not change.
2. **Real testing:** every claim came from a real phone and real objects on a real laptop.
3. **Willingness to reverse:** CLIP, speed tuning and configurable application were all removed when the evidence said so.
4. **Product decisions over technical ones:** consent every time, no storage, minimal log, Employee screen only.
5. **Honest limits:** listed in `README.md`.

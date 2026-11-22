# Team 020 – SessionGuard (Screen Privacy Guard)

**Course:** MBAZG583 Management of AI Products (S1-26), BITS Pilani WILP
**Professor:** Prof. Vinaya Sathyanarayana
**Product type:** security control for Employees of a Service Company working on a Bank’s data (computer vision)
**Prototype status:** working. First release: Git tag `v1.0-first-release` (commit `fd19c04`, 13 Nov 2026). Current: tag `v1.1-privacy-fix` (commit `540f846`, 14 Nov 2026)

## Team
| Name | Roll number | Role | GitHub ID | Phone |
|---|---|---|---|---|
| Gottumukkala Chandra Sekhar Varma | 2025MB26041 | Product Lead and Prototype/AI Engineer | [chandrasekharvarmag1-dev](https://github.com/chandrasekharvarmag1-dev) | 8143466458 |
| Sneha Mupparthi | 2025MB26183 | Evaluation and Quality Lead | [snehamupparthi](https://github.com/snehamupparthi) | 8885256685 |
| Durgesh Kumar Nirvan | 2025MB26073 | Business and Documentation Lead | [2025mb26073](https://github.com/2025mb26073) | 9782090475 |
| Gitika Sharma | 2025MB26069 | UX and Consent Lead | [gitikasharma](https://github.com/gitikasharma) | 8076109578 |
| MD Abdul Samadkhan | 2025MB26192 | Data, Privacy and Regulator Lead | 2025MB26192 | 8217355052 |

## What it is, in three lines
A bank Employee working on a sensitive screen outside the office is watched by the laptop webcam. If a phone is pointed at the screen, the whole screen is covered by a blurred image within seconds. If the Employee walks away, the protected application closes and Windows locks. No image or video is ever stored. Only short text lines are logged.

## Reading order
| # | File | What you will find |
|---|---|---|
| 00 | `00_Executive_Summary_and_Strategy.md` | Problem, jobs to be done, strategy, why this wedge, build vs buy |
| 01 | `01_PRD.md` | Scope, defined terms, configurable vs fixed, metrics table, roadmap V1/V2/V3, go/no-go |
| 02 | `02_Workflow_and_Architecture.md` | Swimlane workflow, control loops, C4 level 1 and level 2 (Mermaid) |
| 03 | `03_UX_and_Trust_Design.md` | Every screen and message the Employee sees, how uncertainty is shown |
| 04 | `04_Data_Privacy_Ethics_Risk.md` | Exact data held, consent, retention, regulator view, risks, launch checklist |
| 05 | `05_Model_and_Evaluation.md` | Model choice, measured facts, test plan and results table |
| 06 | `06_Business_Case_and_Economics.md` | Who pays, cost, model licence, value, pricing at 3 to 4 times the customer's gain, stress test, 100-seat view, competitors, go to market and volume |
| 06a | `06a_Economics_Workbook.xlsx` | The same numbers as a two-sheet workbook with live formulas: the customer’s case and our profitability |
| 07 | `07_Build_Journey_and_Iterations.md` | How the product was built, step by step, with every rollback |
| 08 | `08_Detection_Tuning_Log.md` | Every detection experiment: change, observation, decision |
| 09 | `09_AI_Collaboration_Log.md` | How AI was used, real prompts, where the team overruled the AI |
| 10 | `10_Contribution_Disclosure.md` | Who did what |
| 11 | `11_Pitch_Slides.md` | The 10-minute pitch |
| 11a | `11a_Pitch_Deck.pptx` | The final pitch deck: 17 main slides and 6 backup slides, with speaker notes |
| 12 | `12_Security_Reviewer_View_V3_Concept.md` | A V3 mock-up screen (not part of the product) and how its data could be stored; files in `demo_manager_view/` |
| – | `reflections/` | Individual reflections, one file per member (see `10_Contribution_Disclosure.md`) |
| 05a | `05a_Formal_Test_Log_TEMPLATE.md` | Plan and blank log for the formal measurement run (planned for the pilot, not yet run) |
| – | `prototype/` | Source description, setup steps, sample configuration |

## Where each required part of the assignment package lives
| Required part | File |
|---|---|
| Executive summary | `00_Executive_Summary_and_Strategy.md` |
| Strategy | `00_Executive_Summary_and_Strategy.md` |
| Product management artifact pack (PRD, workflow, roadmap, metrics) | `01_PRD.md`, `02_Workflow_and_Architecture.md` |
| UX and trust design | `03_UX_and_Trust_Design.md` |
| Data, model and evaluation | `05_Model_and_Evaluation.md`, `08_Detection_Tuning_Log.md` |
| Business and economics | `06_Business_Case_and_Economics.md` |
| Ethics and risk | `04_Data_Privacy_Ethics_Risk.md` |
| Prototype | `prototype/`, `07_Build_Journey_and_Iterations.md` |
| AI collaboration log | `09_AI_Collaboration_Log.md` |
| Contribution disclosure | `10_Contribution_Disclosure.md` |

## Quick look without a webcam or the model file
The full guard needs Windows, a webcam and `yolo11s.pt` (see `prototype/README.md`). Without them you can still see two parts of the product:
- **Employee log screen:** run `python prototype/view_log.py` and tick "Show sample data (demo only)". It uses only the Python standard library.
- **V3 mock-up screen:** open `demo_manager_view/manager_view.html` by double-click. It needs no internet. See `12_Security_Reviewer_View_V3_Concept.md`.

## Naming of people
People are always named by role: **Employee**, **IT Administrator**, **Security Reviewer**, **Compliance Officer**, **Bank**, **Service Company (buyer)**. Generic labels for people are not used anywhere in these files.

## Honest limits, in one place
1. The "office network" check compares the public IP address with a list set by IT. It simulates a real network check.
2. SecureDesk is a stand-in application. It holds no real data.
3. Phone detection is probabilistic. It can miss a phone and can blur for a look-alike object: a TV remote was covered in about 5 of 30 informal trials.
4. The guard protects only the application it starts. A directly opened application is not covered.
5. One monitor, Windows only, tested on one laptop.
6. An Employee with enough rights can end the guard in Task Manager.
7. The detection library (Ultralytics) did DNS lookups and sent anonymous usage statistics (no images, no log content) in v1.0. V1.1 switches this off. This was checked with a probe that sees Python-level network attempts only; real network traffic was not captured. See `04_Data_Privacy_Ethics_Risk.md`.
8. The old stand-alone files `app.py` and `test_detection.py` are not part of the guard. `app.py` has no absence lock, and `test_detection.py` imports the library directly, so the switch-off does not cover it.
9. The webcam sees only what is in its view. A phone outside the frame, a photo taken from a side angle, or a camera in the room (for example a CCTV camera) is not detected.
10. V1 detects phones only. Other capture devices (tablets, cameras, smart glasses) are not detected; they are planned for V2.
11. SessionGuard is an extra layer, not a replacement. It adds to VDI, privacy filters and office policy. See `06_Business_Case_and_Economics.md` section 11.
Details and controls: `04_Data_Privacy_Ethics_Risk.md`.

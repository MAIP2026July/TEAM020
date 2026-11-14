# 08 – Detection Tuning Log
Team 020 – SessionGuard | Members: see `README.md`

Every experiment on phone detection, in order. Observations are what the team member saw in live tests with a real phone and everyday objects. Thresholds and model names are exact. Percentages quoted are the team's own informal estimates, not measurements.

Note: "frames" in the rules below means detector results. The detector runs on its own thread, so 5 results take roughly half a second to a second.

Test objects used in these rounds: a phone held straight, a phone at angles, a phone rotated like a clock hand (12 to 3 o'clock), a computer mouse (underside has a light), a phone-shaped charger, toys, and other rectangular objects.

## Experiment table
| # | Change | Why we tried it | What we saw | Decision |
|---|---|---|---|---|
| E1 | Baseline: YOLOv8n, default confidence, decide on one frame | Simplest possible version | Detected many classes. Missed or mislabelled some objects; team estimate 60–70 % correct. Blur flickered | Keep as base; improve |
| E2 | Sliding 2-second window: every phone frame resets the timer | Cover dropped after 2 s even with the phone still in view | Confirmed working. A held phone keeps the cover on | **Kept** |
| E3 | Confidence 0.15 | Catch phones at more angles | Caught more, but the mouse underside was taken for a phone | Rejected: false covers destroy trust |
| E4 | Confidence 0.22 (middle value) | Balance of E3 and default | Still reacted to objects pointed quickly and to the mouse underside | Rejected as the only fix |
| E5 | YOLOv8s model, confidence back to 0.25, trigger needs 6 of the last 10 frames | A better model plus "seen consistently" | Fewer random-object covers, but a few seconds to react | Kept the model and the multi-frame idea; trigger too slow |
| E6 | Size and shape filters on detections | Remove rectangular look-alikes by box size or shape | Team member rejected it before testing: "I don't want to disturb the model" | **Rejected by the product owner** |
| E7 | Trigger cut from 6 of 10 to 3 of 5, plus a confirm step: watch the next 10 frames; drop the cover if fewer than 3 show a phone | The team member wanted faster response but still wanted to remove the cover if it was not a phone | Better response. A phone-shaped charger had been a problem at the previous step; the confirm step was designed to release such covers | **Kept** |
| E8 | YOLO11s in place of YOLOv8s | Newer generation, same speed class | Worked better, but some rectangular objects that are not phones were still taken for one. The team member called this "one major test we need to pass" | **Kept** |
| E9 | YOLO11m | The most accurate option within reach | Slow on a CPU-only laptop, and detection was still not good enough to justify the delay | Rolled back to YOLO11s |
| E10 | CLIP second check (lens idea): at trigger time, crop the detection and compare it with 5 text descriptions; keep the cover only if "a smartphone" wins | Rectangular objects have no lens; check for what a phone looks like | Fewer false covers, but a phone rotated 12 to 3 o'clock was no longer covered; first run downloaded a model of about 350 MB and startup got slow | Rejected |
| E11 | CLIP vote over five frames instead of one | The one-snapshot check landed on awkward angles | The team member chose to stop adding layers and go back to the version that worked | CLIP removed completely; return to YOLO-only |
| E12 | Speed work: detector in a background thread, image size 416, confidence 0.35, phone class only | The screen felt slow and normal objects were still covering | Video smoother (about 81 ms per check vs about 146 ms), but phones were missed often | Partly rejected |
| E13 | Back to confidence 0.25 and image size 512; keep the background thread; blur a shrunken copy of the frame | Single-frame catch rate matters because of 3-of-5 | Better catches; camera still slow to open on this laptop | **Final settings** |

## Why E12 failed, with arithmetic
With the trigger needing 3 of the last 5 frames, a small drop in single-frame accuracy becomes a large drop in catches.
| p, single-frame catch rate | Chance of 3 of 5 |
|---|---|
| 0.7 | 83.7 % |
| 0.5 | 50.0 % |
| 0.4 | 31.7 % |
| 0.3 | 16.3 % |
The formula is the sum of the binomial terms for 3, 4 and 5 hits out of 5.

## What was investigated before any code change
At E12 the team member asked the coding agent to investigate before changing anything: whether the consent screen change or the speed changes caused the misses, and whether the model's class filter had been mis-set. The finding pointed to the two accuracy-lowering settings (0.35 and 416) rather than to the consent screen.

## What we learned
1. **One threshold cannot satisfy every case.** Lower confidence catches more angles and also catches more look-alikes.
2. **Rules over frames beat a single number.** The frame windows removed most one-frame errors.
3. **More layers are not always better.** CLIP and the larger model each solved one problem and created another.
4. **Speed and accuracy trade directly,** and the 3-of-5 rule amplifies accuracy loss.
5. **Save points matter.** A good state must be tagged before an experiment starts.
6. **Know when to stop.** The team chose to accept limits and document them, because tuning could have consumed the whole project.

## Open items for V2
- Tune on a faster laptop and with the pilot cameras.
- If look-alike covers remain a problem, collect labelled phone images and train a small custom model. This needs time and data and is out of V1.
- Measure T1–T4 in `05_Model_and_Evaluation.md` on three laptops.

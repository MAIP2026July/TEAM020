# 11 – Pitch (10 minutes, 4 slides)
Team 020 – SessionGuard | Members: see `README.md`

Framing: an internal security tool for a bank. The ask is a funded pilot, and the value is the Bank's avoided loss.

## Slide 1 – The problem (2 min)
- Bank Employees work on sensitive screens from outside the office.
- A phone camera copies a screen in 2 seconds. Nothing is seen. Nothing is recorded.
- Today's control is a policy page. No auditor can test it.

## Slide 2 – The product and the demo (3 min)
- SessionGuard starts the protected application only after consent.
- Outside the office, the webcam looks for a phone.
- Phone confirmed: the whole screen is covered. Employee leaves: the application closes and Windows locks.
- **Nothing stored.** One text line per incident.
- **Live demo, in this order:**
  1. Inside the office: application opens alone, no camera.
  2. Outside, Decline: nothing opens, camera light off.
  3. Outside, Agree: hold a phone; the screen is covered; remove it; the cover clears.
  4. Walk away: the application closes and Windows locks.
  5. Open "My Privacy Log": the lines kept, and nothing else.

## Slide 3 – Proof, trust and honest limits (2 min)
- Built in small steps and tested on a real laptop with a real phone. Thirteen detection experiments, two features built and then removed (a CLIP check and a configurable application), every working state tagged in Git.
- Targets: catch rate ≥ 90 %, false cover ≤ 1 per 10 minutes, images stored 0 (say clearly that results so far are informal observations from about 30 trials, listed in `05_Model_and_Evaluation.md`, and that the formal measurement is the first pilot step).
- What we chose not to collect: images, faces, identity, productivity.
- Limits, said openly: office check by IP list, one monitor, can be ended in Task Manager, probabilistic detection, and the detection library's anonymous statistics, which V1.1 switched off (checked at Python level; real traffic not captured).

## Slide 4 – The business (3 min)
- Who pays: the Service Company, which can show the Bank a working control and offer work from home to Employees on critical projects. The Bank asks for it.
- Price: ₹ 500 per seat per month. The customer gains about ₹ 1,875 per seat per month (threat about 56 %, retention about 44 %). That is about 3.75 times what it pays (assumptions, to be measured in the pilot).
- 100 seats: the customer gains about ₹ 22.5 lakh a year and pays ₹ 6 lakh. We earn about ₹ 4.8 lakh a year after running costs and recover the ₹ 1.5 lakh build cost in about 4 months.
- No cloud or token cost: runs on the laptop.
- V1: 8 weeks to a go/no-go. V2: protected application chosen by IT, multi-monitor. V3: Bank VDI integration, sale to more Service Companies.
- **Ask:** approval and budget for a 10-seat pilot.

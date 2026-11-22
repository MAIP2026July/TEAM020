# 11 – Pitch (about 12 minutes: 17 main slides and 6 backup slides)
Team 020 – SessionGuard | Members: see `README.md`

Framing: a security control that a **Service Company** buys to prove trust to its **Bank** client and to let Employees on critical projects work from home. The first value is stopping phone-camera theft (fines, loss, lost trust). The second value is keeping people. The ask is a funded 10-seat pilot.

The deck is shared as a PowerPoint or PDF export with the submission. This file is its outline and the speaker plan.

## Main slides
| # | Slide | The one message | Speaker (suggested) |
|---|---|---|---|
| 1 | Title | SessionGuard, Team 020 | Chandra Sekhar Varma |
| 2 | The problem | One phone photo of a sensitive screen can mean a huge fine, a loss and lost trust. Second effect: Employees on critical projects are kept in the office and some leave | Chandra Sekhar Varma |
| 3 | Who it serves | Service Company (buyer), Bank (data owner and client), Employee (user). First value: stop the theft. Second value: keep the people | Durgesh Kumar Nirvan |
| 4 | The product and the demo | Consent, phone cover, walk-away lock, "My Privacy Log". Nothing stored | Chandra Sekhar Varma |
| 5 | AI in three places | AI for the documents, AI to build the product, AI inside the product (a pretrained detector). AI detects, fixed rules decide | Chandra Sekhar Varma |
| 6 | How it works | AI1 phone detection and AI2 person present, with the human gates marked | Chandra Sekhar Varma |
| 7 | If the AI gets it wrong | A wrong call is small, visible and recoverable | Sneha Mupparthi |
| 8 | Trust by design | What we chose not to collect, and the privacy fix found in our own audit | MD Abdul Samadkhan, Gitika Sharma |
| 9 | Evidence and honest limits | Informal tests, 13 tuning experiments, and the limits: phones only, the webcam’s view only, one laptop | Sneha Mupparthi |
| 10 | Competitors and alternatives | An extra layer on top of VDI, privacy filters and office policy, not a replacement | Durgesh Kumar Nirvan |
| 11 | Value and price | Threat ₹1,042 and retention ₹833 per seat per month, ₹1,875 in total; price ₹500; 3.75 times | Durgesh Kumar Nirvan |
| 12 | Economics 1: the Service Company | Pays ₹6 lakh, gains ₹22.5 lakh a year for 100 seats | Durgesh Kumar Nirvan |
| 13 | Economics 2: SessionGuard | Build ₹4 lakh, contribution ₹4.8 lakh a year, build cost earned back in about 10 months | Durgesh Kumar Nirvan |
| 14 | Stress test and fit | Where the numbers hold, and who the product does not fit | Durgesh Kumar Nirvan |
| 15 | Go to market and volume | Three routes, start direct; 1, 3 and 6 customers as a planning guess | Durgesh Kumar Nirvan |
| 16 | Roadmap | V1 now (phones only), V2 next (other capture devices), V3 later | Chandra Sekhar Varma |
| 17 | The pilot and the ask | 10 seats in 8 weeks; the pilot measures catch rate, thefts and attrition | Chandra Sekhar Varma |

## Backup slides, for questions
Every assumption and how the pilot checks it; the full stress test; the model licence as an unknown cost; how a Bank can check our product is not the thief; the V3 Security Reviewer view and its data storage; what we learned.

## If the slot is 10 minutes
Move slides 14 and 15 to the backup, and keep the rest.

## Live demo, in this order
1. Inside the office: the application opens alone, no camera.
2. Outside, Decline: nothing opens, camera light off.
3. Outside, Agree: hold a phone; the screen is covered; remove it; the cover clears.
4. Walk away: the application closes and Windows locks.
5. Open "My Privacy Log": the lines kept, and nothing else.

## What to say about the evidence
Say clearly that the results so far are informal observations from about 30 trials with Samsung phones, an iPhone and basic phones, listed in `05_Model_and_Evaluation.md`, and that the formal measurement (`05a_Formal_Test_Log_TEMPLATE.md`) is the first pilot step. Say "YOLO11s", the model we chose.

## What to say about the numbers
The cost, price, theft rate and retention figures are team assumptions, marked (A) in `06_Business_Case_and_Economics.md`, and the pilot replaces them with measured numbers. The model licence cost is not yet known. The same numbers are in `06a_Economics_Workbook.xlsx`.

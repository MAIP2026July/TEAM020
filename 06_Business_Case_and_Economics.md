# 06 – Business Case and Economics
Team 020 – SessionGuard | Members: see `README.md`

Figures marked **(A)** are team planning assumptions, not measured facts. The pilot is meant to replace them with the Bank's own numbers.

## 1. Framing
SessionGuard is an **internal security tool** for a bank. The primary case is internal: what it costs the Bank to run, and what loss it avoids. An optional second case shows how the same product could be offered to other banks (V3).

## 2. Who decides and what they get
- **Decision maker:** the Bank's Information Security head, with the Compliance Officer.
- **What they get:** a technical, auditable control against phone-camera copying of sensitive screens, without recording staff.
- **What they use today:** a policy document. Cost near zero. Effect that cannot be checked.

## 3. Internal value case (per protected seat)
| Line | Value | Basis |
|---|---|---|
| Chance of a screen-photo leak per seat per year | 1 in 500 (A) | Planning assumption |
| Cost of one leak (fine, investigation, trust loss) | ₹ 50,00,000 (A) | Planning assumption |
| Expected loss per seat per year | ₹ 10,000 | 50,00,000 ÷ 500 |
| Share of such leaks the tool stops | 50 % (A) | Planning assumption; to be tested in the pilot |
| Expected loss avoided per seat per year | ₹ 5,000 | 10,000 × 50 % |
| Expected loss avoided per seat per month | ₹ 417 | 5,000 ÷ 12 |

## 4. Cost to the Bank (per seat per month)
| Item | Value | Basis |
|---|---|---|
| Build effort, one time | ₹ 2,00,000 (A) | 200 hours × ₹ 1,000 per hour |
| Build cost spread over 100 seats and 24 months | ₹ 83 | 2,00,000 ÷ (100 × 24) |
| Support and updates | ₹ 100 (A) | Planning assumption |
| Model licence | ₹ 0 | Open-source model; licence terms to be checked |
| Cloud, API or token cost | ₹ 0 | Everything runs on the laptop |
| **Total cost per seat per month** | **₹ 183** | 83 + 100 |

## 5. Result
| Measure | Value |
|---|---|
| Value avoided per seat per month | ₹ 417 |
| Cost per seat per month | ₹ 183 |
| Net benefit per seat per month | ₹ 234 |
| Benefit-to-cost ratio | 2.3 |

**What this says:** under these assumptions the Bank gains more than it spends. **What would break it:** if the leak rate or the cost of a leak is a tenth of what we assumed, the ratio falls below 1. The pilot and the Bank's own incident data decide this. This is the weakest part of the case and we say so.

## 6. Contribution by workflow
| Workflow | Cost per use | Note |
|---|---|---|
| Start inside the office | About zero | Camera and model are not loaded |
| Monitoring outside the office | No cloud cost; laptop CPU only | Weak laptops start slowly |
| Log review | About zero | Local text file |
| Absence lock | About zero | Uses the same camera view |

Inference cost per month: ₹ 0 (no cloud inference).

## 7. Option: offering the product to other banks (V3)
| Item | Value |
|---|---|
| Possible list price | ₹ 400 per seat per month (A) |
| Variable cost (support share) | ₹ 100 (A) |
| Contribution per seat per month | ₹ 300 (75 %) |
| Build cost recovered at | 2,00,000 ÷ 300 ≈ 667 seat-months (about 7 months at 100 seats) |

Price is checked against value: the value avoided per seat per year is ₹ 5,000 and the price is ₹ 4,800 per year. This is close to the value, so the buyer has a thin reason to pay. We would test willingness to pay in the pilot before any price is set. Target-cost thinking applies: the price must sit below the value and above the cost.

## 8. Positioning and competition
- AI is the core of the product, not an add-on.
- Standalone in V1; embedded in the Bank's VDI client in V3.
- General data-loss-prevention suites mostly watch files, clipboards and printing. A camera-based phone check is a gap to confirm by market research before any sale.

## 9. Risks to the numbers
- Leak rate and leak cost are guesses; only the Bank's data can settle them.
- The Bank may build this itself. Our edge is speed and the no-storage design.
- Open-source model licence may limit commercial resale; check before offering to other banks.
- Support cost per seat may rise if laptops are weak or varied.

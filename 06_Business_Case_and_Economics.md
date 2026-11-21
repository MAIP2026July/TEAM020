# 06 – Business Case and Economics
Team 020 – SessionGuard | Members: see `README.md`

Figures marked **(A)** are team planning assumptions, not measured facts. The pilot is meant to replace every (A) figure with measured numbers. All amounts are in rupees. One **seat** is one Employee laptop protected by SessionGuard. We count everything per seat, per month.

## 1. Who pays, and why
SessionGuard is a security control that a **Service Company** (an IT services firm working on a Bank's critical projects) buys for its Employees.

| Role | What they get |
|---|---|
| **Service Company (buyer)** | A tool it can show to the Bank to earn the Bank's trust and win or keep projects. A way to offer work from home to Employees on critical projects, which is often not allowed today, and so keep them |
| **Bank** | A technical, auditable control against phone-camera copying of sensitive screens, without recording Employees. The Bank asks for it and approves the pilot |
| **Employee** | The option to work from home on critical projects, so better well-being. Consent every session, and a log screen to see everything kept |

**Main value: the threat.** Phone-camera theft of account-holder data. **Secondary value: retention** of Employees who would otherwise leave. **Extra benefit, not counted in the price:** a Service Company that can show the Bank a working control has about a **5 % better chance of winning projects from financial institutions** (team estimate (A), to be checked in the pilot through feedback from the Bank). We do not put a rupee value on it, because we cannot defend a figure yet. It is extra headroom on top of the numbers below.

## 2. What it costs us
| Kind | Meaning | Figure |
|---|---|---|
| One-time cost (build) | Paid once, however many customers we have. A production-quality version: better detection models, formal testing and more effort than the prototype | **₹4,00,000 (A)** |
| Running cost | Paid again for every seat each month: support and updates | **₹100 per seat per month (A)** |
| Cloud, API, tokens | Everything runs on the laptop | ₹0 |

We keep the two kinds apart. The ₹100 is the least we need from every seat. The ₹4,00,000 is earned back from what is left over.

## 3. What a seat is worth to the customer
| Gain | Working | Per seat per year | Per seat per month |
|---|---|---|---|
| **Threat (main)** | 1 theft in 200 seats a year (A) × ₹50,00,000 per theft (A) = ₹25,000 expected loss; the tool stops half (A) | ₹12,500 | **₹1,042** |
| **Retention (secondary)** | 2 of every 40 Employees stay (A) × ₹2,00,000 for rehiring and training one person (A) = ₹10,000 | ₹10,000 | **₹833** |
| **Total** | | ₹22,500 | **₹1,875** |

Threat is 56 % of the value and retention 44 %. Not counted in rupees: a better chance of winning projects (about 5 %), trust with the Bank, Employee well-being.

## 4. The price
**Price = the customer's value ÷ 3 to 4.** Value is ₹1,875, so the range is ₹469 to ₹625.

**List price: ₹500 per seat per month** (₹6,000 per seat per year). The customer gains ₹1,875 for every ₹500 it pays: **3.75 times**.

## 5. The customer's view, 100 seats, per year
| | Amount |
|---|---|
| Expected thefts: 100 ÷ 200 | 0.5 a year |
| Theft loss avoided: 0.5 × ₹50,00,000 × 50 % | ₹12,50,000 |
| Retention: 5 people stay (2 of every 40) × ₹2,00,000 | ₹10,00,000 |
| **Total gain** | **₹22,50,000** |
| Customer pays: 100 × ₹500 × 12 | ₹6,00,000 |
| **Multiple** | **3.75×** |
| Customer's net gain | ₹16,50,000 |

One avoided ₹50,00,000 incident equals about 8 years of the price for 100 seats.

**Honest note.** With 100 seats the model expects half a theft a year, so most years nothing happens. The product works like insurance: it is valuable because of a rare, costly event. A customer who sees no theft may ask why it pays. Retention is the second reason.

## 6. Our view, 100 seats, per year
| | Per year |
|---|---|
| Revenue: 100 × ₹500 × 12 | ₹6,00,000 |
| Running cost: 100 × ₹100 × 12 | ₹1,20,000 |
| **Contribution** | **₹4,80,000** (₹40,000 a month) |
| Less build cost, one time | ₹4,00,000 |
| **Year 1 result** | **₹80,000** |

- The build cost is earned back in about **10 months** (₹4,00,000 ÷ ₹40,000 a month), inside one year.
- With renewal, three years give about ₹10,40,000 after the build cost.
- This is **contribution, not profit.** It leaves out selling effort, legal and compliance work, any central server for a Security Reviewer view, tax and the team's own time.

## 7. Stress test, 100 seats
The price stays at ₹500, so the customer pays ₹6,00,000 a year in every row. One assumption changes at a time.

| What changes | Customer's gain per year | Customer's multiple at ₹500 | Price that still gives 3 times | Our yearly contribution at that price | Build cost earned back after |
|---|---|---|---|---|---|
| Base case | ₹22,50,000 | 3.75× | ₹625 | ₹4,80,000 (at ₹500) | 10 months |
| Only 1 of every 40 retained | ₹17,50,000 | 2.9× | ₹486 | ₹4,63,200 | 10.4 months |
| Retention worth nothing (threat only) | ₹12,50,000 | 2.1× | ₹347 | ₹2,96,400 | 16.2 months |
| Theft only 1 in 500 | ₹15,00,000 | 2.5× | ₹417 | ₹3,80,400 | 12.6 months |
| Tool stops only 25 % of thefts | ₹16,25,000 | 2.7× | ₹451 | ₹4,21,200 | 11.4 months |
| Theft 1 in 500 **and** 1 of 40 retained | ₹10,00,000 | 1.7× | ₹278 | ₹2,13,600 | 22.5 months |

**What this says.** The weakest assumption is the theft rate. At 1 in 500 the customer's multiple falls below 3, and the price would have to come down to about ₹417. If retention is worth nothing the product still stands on threat alone at about ₹347. In the worst row we still keep more than the ₹100 running cost per seat, but the build cost takes about 22 months to earn back. Several rows take longer than one year.

## 8. By number of seats (price ₹500, contribution ₹400 per seat per month)
| Seats | Contribution per year | Build cost earned back after |
|---|---|---|
| 20 | ₹96,000 | about 50 months |
| 50 | ₹2,40,000 | about 20 months |
| **100** | **₹4,80,000** | **about 10 months** |
| 200 | ₹9,60,000 | about 5 months |

The customer's multiple does not change with the number of seats. Only our earnings do. About 84 seats are needed to earn the build cost back within one year. A pilot of 10 seats alone would take about 8 years, so the plan depends on the pilot leading to larger contracts.

## 9. Where it does not make sense
| Segment | Why it is weak |
|---|---|
| Small teams (under about 50 seats) | Build cost takes more than 20 months to earn back |
| Teams where attrition is already low or work from home is not an issue | The retention value (44 % of the total) falls away; only threat remains |
| Work with no sensitive screens | No theft risk to avoid |
| Environments that do not allow a webcam | The product cannot work |
| Laptops without Windows or with several monitors | Not supported in V1 |

This table is our reasoning, not market data.

## 10. Cost per use, by workflow
| Workflow | Cost per use | Note |
|---|---|---|
| Start inside the office | About zero | Camera and model are not loaded |
| Monitoring outside the office | No cloud cost; laptop CPU only | Weak laptops start slowly |
| Log review | About zero | Local text file |
| Absence lock | About zero | Uses the same camera view |

Inference cost per month: ₹0 (no cloud inference).

## 11. Positioning and competition
- AI is the core of the product, not an add-on.
- Standalone in V1; embedded in the Bank's VDI client in V3.
- General data-loss-prevention suites mostly watch files, clipboards and printing. A camera-based phone check is a gap to confirm by market research before any sale.
- Our edge for the Service Company is that it can show the Bank a working control, and that nothing is stored.

## 12. Risks to the numbers, and what the pilot must measure
| Assumption (A) | Why it is weak | How the pilot measures it |
|---|---|---|
| 1 theft in 200 seats a year | A guess; the Bank's own incident data is the right source | The Bank's incident history; covers and incidents logged |
| The tool stops half of thefts | Detection is probabilistic; the catch rate so far is informal (`05_Model_and_Evaluation.md`) | The formal test (`05a_Formal_Test_Log_TEMPLATE.md`) |
| 2 of every 40 Employees retained | Work-from-home flexibility is only one reason people stay; not yet tested | Attrition before and after, on the same teams |
| ₹2,00,000 to rehire and train one person | Varies by role and company | The Service Company's own hiring figures |
| ₹4,00,000 build and ₹100 per seat running cost | An estimate for a production-quality version; support load not yet seen | Actual build effort and support hours in the pilot |

Other risks: the Bank may build this itself; the open-source model licence may limit resale and must be checked before any sale; support cost may rise if laptops are weak or varied.

## 13. What changed from the earlier version
| Item | Earlier | Now | Reason |
|---|---|---|---|
| Buyer | The Bank | The Service Company, with the Bank asking for it | The Service Company needs a trust tool to win projects and a way to keep Employees |
| Value counted | Leak loss only (₹417) | Threat plus retention (₹1,875) | Retention is a second, separate benefit |
| Theft chance | 1 in 500 | 1 in 200 | Team assumption; tested at 1 in 500 in section 7 |
| Build cost | ₹2,00,000 | ₹4,00,000 | A production-quality version with better detection models and formal testing, not only the prototype |
| Running cost | ₹100 | ₹100 | Unchanged |
| Price | ₹400 to other banks | ₹500 to Service Companies | Set from the 3 to 4 times rule |
| Result | Ratio 2.3 | Ratio 3.75 | |

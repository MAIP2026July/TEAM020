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

## 11. Competitors, alternatives and positioning
The problem of data leaving through a screen is more than 20 years old, so a buyer already has ways to deal with it. This section lists them, what each costs, and what each leaves open. We position SessionGuard as an **extra layer on top of these controls, not a replacement for them**: it is for the case where Employees must work from home and the usual answer ("come to the office") is too costly.

Prices below come from public web pages found in November 2026. They are third-party snapshots, not official quotes, and must be re-checked before any pitch to a customer. Where a price is not public, the table says so.

### 11a. Alternatives and what each leaves open
| # | Alternative | What it does | What it costs (public information) | What it leaves open |
|---|---|---|---|---|
| 1 | **Office-only work, no phones on the floor** (the customer's manual alternative) | Keeps people and phones in a controlled area | No licence fee. The cost is lost flexibility, people leaving, and office space | No work from home. Critical-project people look for other jobs |
| 2 | **VDI or DaaS** (Citrix, Microsoft Azure Virtual Desktop, VMware Horizon) | Keeps data on servers and blocks copy, paste and file download | Citrix: no official price list. Third-party sources give about $10 to $40 per user per month depending on edition and volume (one source: $13, $20 and $23 for three DaaS editions, one-year term, about 500 users). Azure Virtual Desktop: access is included with eligible Microsoft 365 plans, and Azure infrastructure is charged on top | Cannot see a phone camera pointed at the screen |
| 3 | **Privacy filters and built-in privacy screens** (3M filters, HP Sure View) | Narrow the viewing angle so a person beside you cannot read the screen | 3M laptop filters: about $40 to $85 each in retailer listings; cheaper magnetic filters about $15 to $20. HP Sure View: HP estimated about $75 extra when launched in 2016; the current premium was not found | A camera directly in front of the screen still reads it. No log |
| 4 | **Onlooker or presence detection built into laptops and services** (Dell Intelligent Privacy, Lenovo, HCLTech Onlooker Detection) | Uses the webcam to spot a person looking over your shoulder, then blurs or dims the screen | Bundled with supported hardware or sold as a service. Price not public | Detects a person looking, not a phone camera. Some features need specific hardware. The closest technology to ours |
| 5 | **Data-loss-prevention suites** (Microsoft Purview and similar) | Watches files, email, clipboards and endpoints | Microsoft Purview Suite is listed at $12 per user per month (requires Microsoft 365 E3). Microsoft 365 E5, which includes it, is listed at about $60 on one regional page | Cannot see a photo of the screen taken by a phone |
| 6 | **Dynamic screen watermarking** (Fasoo Smart Screen, Curtain MonGuard) | Shows the user’s name or ID over the screen so a leaked photo can be traced; Fasoo also logs capture attempts | Curtain MonGuard paid version: $10 per PC per year. Fasoo: price not public | Deters and traces after the photo is taken. It does not stop it |
| 7 | **Employee-monitoring tools** (Teramind) | Records screens and user activity, with data-loss features | One review lists $12, $25 and $30 per user per month by plan; newer listings show lower annual rates. Sources conflict | Records Employees’ screens, which raises consent and privacy problems. Does not look for phone cameras |
| 8 | **Patents and research** (a Dell patent for detecting an outside camera with the laptop camera; the ScreenAvoider research prototype) | Show that the webcam idea is possible | Not products | Our search found no widely used product built on this idea. This is a search result, not a full market study |

### 11b. Market size and share
We found **no reliable share figure** for the alternatives above, so we do not claim one. The signals we found are:
- Gartner expects spending on desktop as a service to grow from $4.3 billion in 2025 to $6.0 billion in 2029, about 7.9 % a year.
- On the review site PeerSpot, in October 2025, Citrix DaaS had 13.7 % of mindshare in the VDI category, Horizon Cloud 2.0 % and Oracle VDI 0.9 %. This measures attention on a review site, not sales.

### 11c. Our closest competitors, and how we differ
The closest are **laptop onlooker detection** (row 4) and **watermarking** (row 6).

| | SessionGuard | Closest alternative |
|---|---|---|
| What it looks for | A phone, and whether a person is at the desk | A person looking over the shoulder (row 4); nothing, it only traces (row 6) |
| Works on | Any Windows laptop with a webcam | Some features need specific hardware (row 4) |
| What it keeps | A time and an event line. No image | Watermark tools log captures; monitoring tools record screens |
| Consent | Asked every session | Not a design feature of most tools |
| Who buys it | A Service Company, to show its Bank client a working control | Usually the IT or security team |

**Our honest weakness.** Using the webcam is not unique to us, and a laptop maker or a VDI vendor could add phone detection. Our protection against that is not technology alone:
- the no-storage design and the consent flow, which a Bank can audit;
- the plan to add other capture devices (V2) and an audit view for the Bank (V3);
- selling as an add-on to a Bank’s VDI instead of competing with it. A VDI vendor then becomes a partner, which carries the risk that it later builds its own version.

### 11d. Compared with the customer’s manual alternative (100 seats, per year)
| | Office-only work | SessionGuard |
|---|---|---|
| Cost to the Service Company | About ₹10 lakh of lost people (5 of 100 leave, at ₹2,00,000 each, team assumption (A)), plus office space, not counted | ₹6 lakh (₹500 × 100 seats × 12 months) |
| Allows work from home | No | Yes, with consent every session |
| Phone-camera theft | Not covered while working from home, because there is no work from home | Covered when the phone is in the webcam’s view |
| What it cannot do | Keep critical people who want flexibility | See a device outside the webcam’s view, including a CCTV camera in the room |

### 11e. Limits of this analysis
- The prices and figures are public snapshots from the web, not quotes, and are marked as such.
- We did not find the price of a product like ours, and we found no source for a market share. We say so instead of guessing.
- Dell and HCLTech information comes from their public pages and brochures. We did not test their products or confirm whether they detect phones.

### Sources
- Citrix pricing, third-party: [Graphon](https://www.graphon.com/blog/examining-citrix-pricing), [Vendr](https://www.vendr.com/marketplace/citrix)
- [Azure Virtual Desktop licensing (Microsoft)](https://learn.microsoft.com/azure/virtual-desktop/licensing)
- [3M laptop privacy filters (Staples listings)](https://www.staples.com/Laptop-Privacy-Filters/cat_CL161004/00hf5)
- [HP Sure View (LaptopMag)](https://www.laptopmag.com/articles/hp-sure-view)
- [Dell Intelligent Privacy (PC Gamer)](https://www.pcgamer.com/dell-intelligent-privacy-optimizer)
- [HCLTech Onlooker Detection brochure](https://www.hcltech.com/sites/default/files/documents/HCLTech_Onlooker_Detection_Brochure_design.pdf)
- [Microsoft Purview Suite pricing](https://www.microsoft.com/en-us/security/business/purview-suite-pricing)
- [Curtain MonGuard (SourceForge)](https://www.sourceforge.net/software/product/Curtain-MonGuard)
- Teramind: [TechRadar review](https://www.techradar.com/reviews/teramind), [Capterra](https://www.capterra.com/p/172645/Teramind/pricing/)
- [Dell patent, Device anti-surveillance system](https://patents.justia.com/patent/11756296)
- [Gartner DaaS forecast (Virtualization Review)](https://virtualizationreview.com/articles/2025/08/14/gartner-daas-expands-beyond-remote-work-in-2025.aspx)
- [PeerSpot VDI mindshare](https://www.peerspot.com/products/comparisons/citrix-daas-formerly-citrix-virtual-apps-and-desktops-service_vs_horizon-cloud-service_vs_oracle-vdi)

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

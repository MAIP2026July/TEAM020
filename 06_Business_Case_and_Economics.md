# 06 – Business Case and Economics
Team 020 – SessionGuard | Members: see `README.md`

Figures marked **(A)** are team planning assumptions, not measured facts. The pilot is meant to replace every (A) figure with measured numbers. All amounts are in rupees. One **seat** is one Employee laptop protected by SessionGuard. We count everything per seat, per month.

The same numbers are in a workbook with live formulas, `06a_Economics_Workbook.xlsx`, with two sheets: **Customer case** (what the Service Company pays and gains, with the stress test) and **Our profitability** (our cost, the three-year volume plan, the licence sensitivity and the test with all costs up 20 %). Change a blue cell and everything recalculates.

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
| Model licence (Ultralytics YOLO) | A flat annual fee for the company that sells the product; quote only, no public price | **Unknown (A)**. Shown in section 2a. Not included in sections 5 to 8 |

We keep the two kinds apart. The ₹100 is the least we need from every seat. The ₹4,00,000 is earned back from what is left over.

## 2a. The model licence: a cost we do not know yet
**What the licence is.** The detector is Ultralytics YOLO. Ultralytics offers it under two licences:
- **Open-source (AGPL-3.0), free.** If we distribute a product built on it, or let people use it over a network, the licence requires us to publish the complete source of the whole application under the same licence.
- **Enterprise License, paid.** This is the route for a closed commercial product or a private company tool. It is an annual subscription held by the company that sells the end product. Ultralytics quotes the price for each case, based on the use and the size of the organisation. **No price is published.**

**What this means for us.** Selling SessionGuard as a closed product to Service Companies needs the Enterprise License. Until we have a quote, we cannot state a final price with confidence. The ₹0 licence cost in sections 5 to 8 is therefore a placeholder, not a fact.

**What each possible fee would do (100 seats, ₹500 price, ₹100 running cost, ₹4,00,000 build).** The fee is a flat annual amount for the company, not a per-seat fee. The per-seat figure is only a way to compare.

| Annual licence fee | Equal to, per seat per month | Our contribution per year | Build cost earned back after |
|---|---|---|---|
| ₹0 (the placeholder in sections 5 to 8) | ₹0 | ₹4,80,000 | 10 months |
| ₹1,00,000 | ₹83 | ₹3,80,000 | 12.6 months |
| ₹2,40,000 | ₹200 | ₹2,40,000 | 20 months |
| ₹3,60,000 | ₹300 | ₹1,20,000 | 40 months |
| ₹4,80,000 | ₹400 | ₹0 | Never |

- **Break-even fee:** at ₹4,80,000 a year the contribution is zero.
- **Room to pass it on:** the price can rise from ₹500 to ₹625 before the customer’s gain falls below 3 times. That is ₹125 per seat per month, or ₹1,50,000 a year at 100 seats. A fee up to that amount can be passed on without lowering our contribution.
- **A flat fee favours volume:** the same ₹2,40,000 a year is ₹200 per seat per month at 100 seats but ₹100 at 200 seats.

**Safety margin: all our costs up 20 %.** The professor’s test: if input costs rise by 20 %, are we still profitable? Running cost becomes ₹120 per seat per month, the build cost ₹4,80,000, and any licence fee 20 % higher. Price stays at ₹500, 100 seats.

| Case | Our contribution per year | Build cost earned back after |
|---|---|---|
| No licence fee, costs as planned | ₹4,80,000 | 10 months |
| No licence fee, all costs up 20 % | ₹4,56,000 | 12.6 months |
| Licence ₹1,00,000 a year, all costs up 20 % (licence ₹1,20,000) | ₹3,36,000 | 17.1 months |
| Licence ₹2,40,000 a year, all costs up 20 % (licence ₹2,88,000) | ₹1,68,000 | 34.3 months |

We stay profitable in every row above, but the payback passes one year once a licence fee is added. The product only works at ₹500 if the fee stays below about ₹1,50,000 a year at 100 seats, or if we accept a longer payback.

**Ways to reduce this risk**
1. Ask Ultralytics, or an authorised reseller such as Roboflow, for an Enterprise License quote for our expected volume. A volume discount needs a promised volume, so we need a volume plan first (see section 11f).
2. Test a detector with a permissive licence. Each model’s licence must be checked, and our accuracy tests repeated, because accuracy may differ.
3. Publish SessionGuard under AGPL-3.0. This keeps the licence free but means publishing the full source, which does not suit a product we sell.

**Sources:** [Ultralytics licensing](https://www.ultralytics.com/licensing), [Ultralytics Enterprise Software License](https://www.ultralytics.com/legal/enterprise-software-license), [Ultralytics staff reply on pricing basis](https://community.ultralytics.com/t/unable-to-submit-license-inquiry-via-website-requesting-commercial-license-information/1219), [Siemens listing of the Enterprise License](https://www.siemens.com/en-gb/products/ultralytics-enterprise-license/), [Roboflow as authorised licensor](https://roboflow.com/ultralytics). The licence terms and prices were read from public pages in November 2026 and must be confirmed with Ultralytics before any sale. This is not legal advice.

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
- This is **contribution, not profit.** It leaves out selling effort, legal and compliance work, the model licence fee (section 2a), any central server for a Security Reviewer view, tax and the team's own time.

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

### 11e. Who we sell to, and how
**The customer.** Service Companies (IT services, outsourcing and financial-services vendors) that deliver projects for banks and other financial institutions under strict rules. They fit because they:
- carry the liability when data leaks, and must show the Bank that controls are in place;
- often cannot offer work from home on critical projects, and lose people because of it;
- already use VDI or similar tools, so SessionGuard adds to what they have.

**Who decides (our assumption).** The person who owns the Bank relationship and the person who owns security, with the Bank’s approval of the control and the Compliance Officer’s sign-off on the consent text.

**The first customer.** A Service Company the team already knows through its own work. The path is the pilot already planned: 10 seats for 8 weeks, then 100 seats if the numbers hold. A Bank reference from the pilot is worth more to the next customer than any slide.

**Three ways to reach customers**
| Route | How it works | For | Against |
|---|---|---|---|
| **1. Direct to Service Companies** (our choice to start) | We sell and support it ourselves, using the pilot and the Bank reference | We keep the price and the customer relationship. Fastest to start | Selling effort is ours. Reach is small at first |
| **2. Through a VDI vendor or partner** (Citrix, Microsoft, VMware and others) | Our product is offered as an approved add-on to their platform | Reach and trust that come with a known name | The vendor must approve our product. We share revenue. If the vendor builds its own version, we are out of that market |
| **3. Through the Bank** | The Bank asks its vendors to use a control like ours | Demand is pulled in by the party that owns the data | Long decision cycle. The Bank may prefer to build or to buy from a big supplier |

**Our plan.** Start with route 1, and approach VDI vendors only after a measured pilot, because a partner will ask for proof that the product works and is safe. Route 3 starts naturally if the Bank in the pilot recommends us to its other vendors.

### 11f. Volume we are planning for (A)
These numbers are a **planning guess** and the first paying customer is the real test. Each customer is assumed to buy 100 seats, as in sections 5 and 6.

| Year | Customers | Paying seats (average) | Revenue at ₹500 | Our contribution (₹400 per seat per month) |
|---|---|---|---|---|
| 1 | 1 | 100 | ₹6,00,000 | ₹4,80,000 |
| 2 | 3 | 300 | ₹18,00,000 | ₹14,40,000 |
| 3 | 6 | 600 | ₹36,00,000 | ₹28,80,000 |

- Over three years the contribution is ₹48,00,000. After the ₹4,00,000 build cost that is ₹44,00,000, **before** the licence fee, selling effort, compliance work and tax, none of which is counted here.
- **Licence effect.** With a flat licence of ₹2,40,000 a year (section 2a), the three-year figure falls to ₹36,80,000 (₹48,00,000 − ₹7,20,000 − ₹4,00,000). The same flat fee is ₹200 per seat per month in year 1, about ₹67 in year 2 and about ₹33 in year 3, so volume lowers its weight.
- **Why this matters for the licence.** A licence discount needs a promised volume. We would only promise a volume we can defend. We would ask for a quote at 100 seats for year 1 and at 300 seats for year 2, and not promise more until the pilot is done.

### 11g. Making ourselves hard to replace
Our protection is not technology alone, because using a webcam to detect a phone can be copied. What can make us harder to replace:
- **Bank-accepted evidence.** A design a Bank can audit: nothing stored, consent every session, an incident log the Employee can read. Once a Bank has accepted a control, a customer does not change it lightly.
- **Approval by the platforms we sit on.** Approval by a VDI vendor and by the Bank is a barrier for a new rival.
- **A wider product.** Other capture devices (V2) and a counts-only view for the Security Reviewer (V3), both on the roadmap.
- **Learning from the pilot.** Measured catch rates and false covers on real laptops let us tune faster than a copy.

**An honest view.** Switching away from us is cheap for a customer, and a VDI vendor or laptop maker could add the same feature. If a platform vendor builds it in, we lose that market. That is why we would partner with such vendors after the pilot and not compete with them.

### 11h. Limits of this analysis
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
| Model licence fee | Quote only; no public price. A closed commercial product needs the Enterprise License | Ask for a quote at our expected volume and record it here (section 2a) |
| Volume plan: 1, 3 and 6 customers of 100 seats in years 1 to 3 | A planning guess; the first paying customer is the real test | Pilot conversion, and the first signed customer (section 11f) |

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
| Competitors | A few lines | A table of eight alternatives with public prices, our closest competitors and a comparison with office-only work (section 11) | The professor asked every team for a competitor analysis |
| Model licence | Not shown | Shown as an unknown cost with a margin table and a test with all costs up 20 % (section 2a) | The professor’s feedback on the YOLO licence and on safety margins |
| Go to market | Not covered | Who we sell to, three routes to customers, a three-year volume plan and how we stay hard to replace (sections 11e to 11g) | The professor asked about go to market, volume and replacement risk |
| Result | Ratio 2.3 | Ratio 3.75 | |

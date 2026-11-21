# 12 – Security Reviewer View (V3 concept, mock-up only)
Team 020 – SessionGuard | Members: see `README.md`

**Status: a mock-up screen, not part of the product.** Nothing in `prototype/` sends data anywhere. The mock-up lives in `demo_manager_view/` and opens by double-click (`manager_view.html`). It uses one real log copied for three sample employees. They are not real people.

## 1. Why this note exists
`01_PRD.md` lists a "counts-only report for the Security Reviewer" as a V3 idea, and `03`, `04` and `09` record that an admin screen with Employee names was dropped in V1 to protect trust. This note shows what the V3 idea could look like and what it would cost in privacy terms, so the team can say clearly why it is not in V1.

## 2. What the mock-up shows
- A banner: "SAMPLE DATA - one real log, copied for 3 employees. Not real people." and "A flag is a pattern, not proof. A person decides."
- Four totals: phone covers, absence locks, failed locks, employees needing review.
- One row per sample employee, and a timeline (same wording as the log, newest first) with filters by event type and by day.
- Review rules, in one place at the top of the page script: 10 or more "Phone detected" lines in one day; 10 or more absence-lock lines in one day; any one line with "workstation lock FAILED".
- Buttons "Mark reviewed" and "No action needed". They change only what the screen shows. Nothing is saved.
- Only time and event words are shown. No IP address, application name, image or real name.

## 3. What the mock-up found
The three sample employees are one real log (168 lines, 5 days) with the times shifted (B) or covers repeated (C). Every sample employee is flagged, because the real log itself has 18, 18 and 32 phone covers on three different days. So a limit of 10 phone covers a day is too low for normal use, and it must be calibrated on more data before any real use. A separate counting script (`count_events.py`) gives the same counts and the same flagged set as the page.

## 4. How the data would be stored (design only, not built)
Today the log stays on the Employee laptop. A central view needs the events to leave the laptop, so a store is required. Recommended design:
```
Employee laptop                          Bank side
guard.py -> session_log.txt  --HTTPS-->  small server -> database (SQLite for a pilot)
(unchanged, still local)      sync        Security Reviewer page reads the database
```
- The local log remains the source of truth; the guard is not changed. A separate sync program uploads only lines not yet sent, so a lost connection loses nothing.
- Uploaded fields: an Employee ID (a random token, not a name), the timestamp and the event words. Nothing else.
- The Security Reviewer page needs a login. The Employee can see exactly what was sent.
- Retention is set by the Compliance Officer; the 90-day proposal in `04_Data_Privacy_Ethics_Risk.md` would be enforced by the server.

## 5. What would have to change first
| Item | Why |
|---|---|
| Consent text | `03` and `04` say nothing leaves the laptop. The text would have to name the upload and who can see it |
| Compliance Officer sign-off | A new flow of personal data about Employees under the DPDP Act, 2023 |
| Calibrated rules | See section 3 |
| Pilot evidence | Employees' trust is not yet tested even for V1 |

## 6. Open question the team has not settled
`04` says the product cannot be used to rank Employees. A view that sorts flagged employees to the top is a form of ranking, even with the "a person decides" line. The Compliance Officer would have to decide whether per-employee flags are acceptable, or whether only team-level counts should be shown. This is the main reason the view stays a V3 concept.

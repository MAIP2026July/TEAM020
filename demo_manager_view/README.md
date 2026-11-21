# Security Reviewer view – V3 mock-up (not part of the product)

Open `manager_view.html` by double-click. It needs no internet, installs nothing and saves nothing.

| File | What it is |
|---|---|
| `manager_view.html` | The finished page: HTML, CSS and JavaScript in one file, with the three logs embedded |
| `page_template.html` | The page source, with markers where the logs go |
| `employee_A.txt` | Exact copy of one real `session_log.txt` (time and event words only), a snapshot of 168 lines covering 2026-11-11 to 2026-11-15 |
| `employee_B.txt` | The same lines with every time shifted by 7 minutes |
| `employee_C.txt` | The real lines plus repeated cover/removed pairs on one day (a labelled variation for the demo) |
| `count_events.py` | Separate counting script. Counts per employee and applies the same rules as the page, so the two can be compared |
| `build_mock.py` | Rebuilds B, C and the page from a real log: `python build_mock.py path\to\session_log.txt` |

Check the page against the script: `python count_events.py` (add `--json` for machine-readable output).

All three sample employees are flagged because the real log has days with 18, 18 and 32 phone covers. See `../12_Security_Reviewer_View_V3_Concept.md`.

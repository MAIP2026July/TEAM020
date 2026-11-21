"""Independent counter - NOT part of the page.

For each sample employee it counts phone covers per day, absence locks per day and failed
locks, then applies the same three review rules as the page. It reads employee_A/B/C.txt only.

Run:  python count_events.py            readable report
      python count_events.py --json     machine-readable (used to compare with the page)
"""
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILES = [("Employee A", "employee_A.txt"), ("Employee B", "employee_B.txt"), ("Employee C", "employee_C.txt")]

# Same rules as the page. The numbers are repeated here on purpose, so this script checks the page independently.
PHONE_COVERS_PER_DAY_LIMIT = 10
ABSENCE_LOCKS_PER_DAY_LIMIT = 10
FLAG_ANY_FAILED_LOCK = True

COVER = "Phone detected - screen covered"
REMOVED = "Screen cover removed"
ABSENCE_START = "No person detected for "
LOCKED_END = " seconds - SecureDesk closed and workstation locked"
FAILED_END = " seconds - SecureDesk closed; workstation lock FAILED"


def classify(words):
    if words == COVER:
        return "covered"
    if words == REMOVED:
        return "removed"
    if words.startswith(ABSENCE_START):
        middle = words[len(ABSENCE_START):]
        for end, kind in ((LOCKED_END, "locked"), (FAILED_END, "failed")):
            if middle.endswith(end) and middle[: -len(end)].isdigit():
                return kind
    return None


def count_file(path):
    raw = path.read_bytes().decode("utf-8")
    lines = raw.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    covers, absence = Counter(), Counter()
    result = {"lines": len(lines), "covers": 0, "absence": 0, "locked": 0, "failed": 0, "removed": 0,
              "last": "", "coversByDay": covers, "absenceByDay": absence, "failedLines": [], "unrecognised": []}
    for number, line in enumerate(lines, 1):
        line = line.rstrip("\r")
        stamp, separator, words = line.partition(" | ")
        try:
            datetime.strptime(stamp, "%Y-%m-%d %H:%M:%S")
            valid = bool(separator)
        except ValueError:
            valid = False
        kind = classify(words) if valid else None
        if kind is None:
            result["unrecognised"].append((number, line))
            continue
        day = stamp[:10]
        result["last"] = max(result["last"], stamp)
        if kind == "covered":
            result["covers"] += 1
            covers[day] += 1
        elif kind == "removed":
            result["removed"] += 1
        else:
            result["absence"] += 1
            absence[day] += 1
            result[kind] += 1
            if kind == "failed":
                result["failedLines"].append(stamp)
    return result


def reasons_for(result):
    reasons = []
    for day in sorted(result["coversByDay"]):
        if result["coversByDay"][day] >= PHONE_COVERS_PER_DAY_LIMIT:
            reasons.append(f"{result['coversByDay'][day]} phone covers on {day} (limit {PHONE_COVERS_PER_DAY_LIMIT})")
    for day in sorted(result["absenceByDay"]):
        if result["absenceByDay"][day] >= ABSENCE_LOCKS_PER_DAY_LIMIT:
            reasons.append(f"{result['absenceByDay'][day]} absence locks on {day} (limit {ABSENCE_LOCKS_PER_DAY_LIMIT})")
    if FLAG_ANY_FAILED_LOCK:
        for stamp in result["failedLines"]:
            reasons.append(f'A failed lock on {stamp[:10]} at {stamp[11:]} (line says "workstation lock FAILED")')
    return reasons


def main():
    report = {}
    for label, name in FILES:
        result = count_file(HERE / name)
        result["reasons"] = reasons_for(result)
        result["flagged"] = bool(result["reasons"])
        report[label] = result

    if "--json" in sys.argv:
        print(json.dumps({label: {"covers": r["covers"], "absence": r["absence"], "failed": r["failed"], "last": r["last"],
                                   "flagged": r["flagged"], "reasons": r["reasons"], "unrecognised": len(r["unrecognised"])}
                          for label, r in report.items()}, indent=1))
        return

    print(f"Limits in use: phone covers per day {PHONE_COVERS_PER_DAY_LIMIT}, absence locks per day {ABSENCE_LOCKS_PER_DAY_LIMIT}, any failed lock flags: {FLAG_ANY_FAILED_LOCK}\n")
    for label, r in report.items():
        print(f"{label}  ({r['lines']} lines, {len(r['unrecognised'])} unrecognised)")
        print(f"  phone covers per day : " + ", ".join(f"{d}: {n}" for d, n in sorted(r["coversByDay"].items())))
        print(f"  absence locks per day: " + (", ".join(f"{d}: {n}" for d, n in sorted(r["absenceByDay"].items())) or "none") + "   (locked + failed together)")
        print(f"  totals               : phone covers {r['covers']}, absence locks {r['absence']} (locked {r['locked']}, failed {r['failed']}), cover removed {r['removed']}")
        print(f"  last event           : {r['last']}")
        print(f"  Needs review         : {'YES' if r['flagged'] else 'no'}")
        for reason in r["reasons"]:
            print(f"      - {reason}")
        for number, text in r["unrecognised"]:
            print(f"      ! unrecognised line {number}: {text!r}")
        print()
    flagged = [label for label, r in report.items() if r["flagged"]]
    print("Flagged employees:", ", ".join(flagged) if flagged else "none")


if __name__ == "__main__":
    main()

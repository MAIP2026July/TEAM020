"""Builds the Manager view mock-up from ONE real log.

The real log is only READ. Everything this script writes goes next to the script:
  employee_A.txt        exact copy of the real log (same bytes)
  employee_B.txt        same lines, every timestamp shifted by SHIFT_MINUTES_FOR_B
  employee_C.txt        the real lines plus repeated "covered / removed" pairs on ONE day
  manager_view.html     page_template.html with the three files embedded

Run:  python build_mock.py [path-to-real-session_log.txt]
"""
import re
import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
REAL_LOG = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("session_log.txt")   # path to a real session_log.txt

SHIFT_MINUTES_FOR_B = 7
TARGET_COVERS_FOR_C = 12          # Employee C gets this many phone covers on the chosen day
C_FIRST_START = "09:07:12"        # time of the first repeated pair
C_SPACING_MINUTES = 41            # gap between repeated pairs

STAMP = "%Y-%m-%d %H:%M:%S"
LINE = re.compile(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})( \| (.*))$")
COVER, REMOVED = "Phone detected - screen covered", "Screen cover removed"


def split_keep_endings(text):
    return re.findall(r"[^\n]*\n|[^\n]+", text)


def body_and_ending(line):
    ending = "\r\n" if line.endswith("\r\n") else "\n" if line.endswith("\n") else ""
    return line[: len(line) - len(ending)], ending


def main():
    real_text = REAL_LOG.read_bytes().decode("utf-8")
    lines = split_keep_endings(real_text)
    if len(lines) < 4:
        sys.exit(f"The real log has only {len(lines)} lines - stopping, nothing invented.")

    # ---- Employee A: exact copy (same bytes) ----
    shutil.copyfile(REAL_LOG, HERE / "employee_A.txt")

    # ---- Employee B: every timestamp shifted, wording and line endings untouched ----
    shifted = []
    for line in lines:
        body, ending = body_and_ending(line)
        m = LINE.match(body)
        if m:
            body = (datetime.strptime(m.group(1), STAMP) + timedelta(minutes=SHIFT_MINUTES_FOR_B)).strftime(STAMP) + m.group(2)
        shifted.append(body + ending)
    (HERE / "employee_B.txt").write_bytes("".join(shifted).encode("utf-8"))

    # ---- Employee C: real lines + repeated pairs on the last day of the log ----
    parsed = []
    for index, line in enumerate(lines):
        body, _ = body_and_ending(line)
        m = LINE.match(body)
        if m:
            parsed.append((index, m.group(1), m.group(3)))
    day = max(stamp[:10] for _, stamp, _ in parsed)
    day_events = [(stamp, text) for _, stamp, text in parsed if stamp[:10] == day]
    pair_seconds = []
    for i, (stamp, text) in enumerate(day_events[:-1]):
        nxt_stamp, nxt_text = day_events[i + 1]
        if text == COVER and nxt_text == REMOVED:
            pair_seconds.append(int((datetime.strptime(nxt_stamp, STAMP) - datetime.strptime(stamp, STAMP)).total_seconds()))
    existing_covers = sum(1 for _, text in day_events if text == COVER)
    needed = max(0, TARGET_COVERS_FOR_C - existing_covers)
    if needed and not pair_seconds:
        sys.exit(f"No real covered/removed pair on {day} to repeat - stopping.")

    used = {stamp for _, stamp, _ in parsed}
    extra = []
    for i in range(needed):
        start = datetime.strptime(f"{day} {C_FIRST_START}", STAMP) + timedelta(minutes=C_SPACING_MINUTES * i)
        while start.strftime(STAMP) in used:
            start += timedelta(minutes=1)
        end = start + timedelta(seconds=pair_seconds[i % len(pair_seconds)])
        assert end.strftime(STAMP) not in used and end.strftime("%Y-%m-%d") == day
        used.update({start.strftime(STAMP), end.strftime(STAMP)})
        extra.append((start.strftime(STAMP), f"{start.strftime(STAMP)} | {COVER}\r\n"))
        extra.append((end.strftime(STAMP), f"{end.strftime(STAMP)} | {REMOVED}\r\n"))

    merged = [(parsed_stamp, idx, lines[idx]) for idx, parsed_stamp, _ in parsed]
    merged += [(stamp, len(lines) + k, text) for k, (stamp, text) in enumerate(extra)]
    merged.sort(key=lambda item: (item[0], item[1]))
    c_text = "".join(text if text.endswith("\n") else text + "\r\n" for _, _, text in merged)
    # every cover must still be followed by its removal (no overlapping pairs)
    kinds = [body_and_ending(t)[0].split(" | ", 1)[1] for _, _, t in merged]
    open_cover = False
    for kind in kinds:
        if kind == COVER:
            assert not open_cover, "two covers in a row after merging"
            open_cover = True
        elif kind == REMOVED:
            assert open_cover, "a removal without a cover after merging"
            open_cover = False
    (HERE / "employee_C.txt").write_bytes(c_text.encode("utf-8"))

    # ---- the page: template + the three files, embedded as plain text ----
    html = (HERE / "page_template.html").read_text(encoding="utf-8")
    for marker, name in (("@@LOG_A@@", "employee_A.txt"), ("@@LOG_B@@", "employee_B.txt"), ("@@LOG_C@@", "employee_C.txt")):
        text = (HERE / name).read_text(encoding="utf-8")          # line endings become plain newlines
        lowered = text.lower()
        assert "</script" not in lowered and "<!--" not in lowered, f"{name} contains text that could break the page"
        assert marker in html, f"marker {marker} missing in the template"
        html = html.replace(marker, text)
    with open(HERE / "manager_view.html", "w", encoding="utf-8", newline="\n") as out:
        out.write(html)

    print(f"real log read: {REAL_LOG} ({len(lines)} lines)")
    print(f"employee_A.txt: exact copy, {len(lines)} lines")
    print(f"employee_B.txt: every timestamp +{SHIFT_MINUTES_FOR_B} minutes, {len(shifted)} lines")
    print(f"employee_C.txt: {len(merged)} lines = {len(lines)} real + {len(extra)} added ({needed} repeated pairs on {day}; real covers that day: {existing_covers} -> {existing_covers + needed})")
    print("manager_view.html written")


if __name__ == "__main__":
    main()

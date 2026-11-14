import ctypes
import random
import re
import tkinter as tk
from collections import namedtuple
from datetime import datetime, timedelta
from pathlib import Path
from tkinter import ttk

LOG_PATH = Path(__file__).with_name("session_log.txt")
MAX_BYTES = 20 * 1024 * 1024
MAX_LINE_BYTES = 4096
MAX_TABLE_ROWS = 3000

NOTE = (
    "This log records only the time a phone was detected and the screen was covered, "
    "and absence locks. No images or personal data are stored."
)
EMPTY_MESSAGE = "No incidents recorded."
READ_ERROR_MESSAGE = "The log could not be read."
SAMPLE_BANNER = "SAMPLE DATA - NOT REAL"
PERIODS = ("All", "Today", "Last 7 days")

COVERED, REMOVED, ABSENCE_LOCKED, ABSENCE_FAILED = "covered", "removed", "absence_locked", "absence_failed"
COVERED_TEXT = "Phone detected - screen covered"
REMOVED_TEXT = "Screen cover removed"
LINE_PATTERN = re.compile(r"^(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) \| (.+)$")
LOCKED_PATTERN = re.compile(r"^No person detected for \d+ seconds - SecureDesk closed and workstation locked$")
FAILED_PATTERN = re.compile(r"^No person detected for \d+ seconds - SecureDesk closed; workstation lock FAILED$")

Event = namedtuple("Event", "ts kind text")
Row = namedtuple("Row", "ts kind text duration")


def parse_line(line):
    match = LINE_PATTERN.match(line.lstrip("﻿").strip())
    if not match:
        return None
    try:
        ts = datetime.fromisoformat(f"{match.group(1)} {match.group(2)}")
    except ValueError:
        return None
    text = match.group(3).strip()
    if text == COVERED_TEXT:
        return Event(ts, COVERED, COVERED_TEXT)
    if text == REMOVED_TEXT:
        return Event(ts, REMOVED, REMOVED_TEXT)
    if LOCKED_PATTERN.match(text):
        return Event(ts, ABSENCE_LOCKED, text)
    if FAILED_PATTERN.match(text):
        return Event(ts, ABSENCE_FAILED, text)
    return None


def load_events(path):
    events = []
    truncated = False
    with open(path, "rb") as log_file:
        size = log_file.seek(0, 2)
        start = max(0, size - MAX_BYTES)
        truncated = start > 0
        log_file.seek(start)
        if truncated:
            skip_rest_of_line(log_file)
        while True:
            line = log_file.readline(MAX_LINE_BYTES)
            if not line:
                break
            if len(line) == MAX_LINE_BYTES and not line.endswith(b"\n"):
                skip_rest_of_line(log_file)
                continue
            event = parse_line(line.decode("utf-8", errors="replace"))
            if event is not None:
                events.append(event)
    return events, truncated


def skip_rest_of_line(log_file):
    while True:
        chunk = log_file.readline(MAX_LINE_BYTES)
        if not chunk or chunk.endswith(b"\n"):
            return


def build_rows(events):
    rows = []
    waiting = None
    for _, event in sorted(enumerate(events), key=lambda pair: (pair[1].ts, pair[0])):
        if event.kind == COVERED:
            waiting = len(rows)
            rows.append(Row(event.ts, event.kind, event.text, "unknown"))
        elif event.kind == REMOVED:
            if waiting is not None:
                started = rows[waiting]
                seconds = max(0, int((event.ts - started.ts).total_seconds()))
                rows[waiting] = started._replace(duration=str(seconds))
                waiting = None
        else:
            waiting = None
            rows.append(Row(event.ts, event.kind, event.text, "-"))
    return rows


def event_label(row):
    if row.kind in (ABSENCE_LOCKED, ABSENCE_FAILED):
        seconds = re.search(r"for (\d+) seconds", row.text).group(1)
        outcome = "locked" if row.kind == ABSENCE_LOCKED else "lock failed"
        return f"No person for {seconds} seconds - SecureDesk closed, {outcome}"
    return row.text


def filter_rows(rows, period, now):
    if period == "Today":
        return [row for row in rows if row.ts.date() == now.date()]
    if period == "Last 7 days":
        cutoff = now - timedelta(days=7)
        return [row for row in rows if row.ts >= cutoff]
    return list(rows)


def compute_stats(rows):
    phone_incidents = sum(1 for row in rows if row.kind == COVERED)
    absence_locks = sum(1 for row in rows if row.kind == ABSENCE_LOCKED)
    last = max((row.ts for row in rows), default=None)
    return phone_incidents, absence_locks, last


def build_sample_events(now):
    rng = random.Random(7)
    events = []

    def add_cover(seconds_ago, duration):
        start = now - timedelta(seconds=seconds_ago)
        events.append(Event(start, COVERED, COVERED_TEXT))
        if duration is not None:
            events.append(Event(start + timedelta(seconds=duration), REMOVED, REMOVED_TEXT))

    add_cover(45, 6)
    add_cover(20 * 60, 4)
    for hours in (3, 9, 26, 30, 52, 55, 80, 101, 130, 150, 200, 240):
        add_cover(hours * 3600 + rng.randrange(0, 3000), rng.randint(2, 18))
    add_cover(60 * 3600, None)
    locked = "No person detected for 30 seconds - SecureDesk closed and workstation locked"
    for hours in (5, 75, 9 * 24):
        events.append(Event(now - timedelta(hours=hours), ABSENCE_LOCKED, locked))
    return events


def enable_dpi_awareness():
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass


class LogViewer:
    def __init__(self, root):
        self.root = root
        self.scale = root.winfo_fpixels("1i") / 96
        self.period = "All"
        self.sample = tk.BooleanVar(value=False)
        self.rows = []
        self.truncated = False
        self.read_error = False

        root.title("My Privacy Log")
        width, height = self.px(700), self.px(500)
        x = max(0, (root.winfo_screenwidth() - width) // 2)
        y = max(0, (root.winfo_screenheight() - height) // 3)
        root.geometry(f"{width}x{height}+{x}+{y}")
        root.minsize(self.px(560), self.px(420))

        self.build_widgets()
        self.refresh()

    def px(self, value):
        return int(round(value * self.scale))

    def build_widgets(self):
        root = self.root
        pad = self.px(14)

        self.banner = tk.Label(
            root, text=SAMPLE_BANNER, bg="#b00020", fg="white", font=("Segoe UI", 12, "bold"), pady=self.px(5)
        )

        self.note = tk.Label(
            root, text=NOTE, wraplength=self.px(670), justify="left", anchor="w", padx=pad, pady=self.px(8)
        )
        self.note.pack(side="top", fill="x")

        stats = tk.Frame(root)
        stats.pack(side="top", fill="x", padx=pad, pady=(0, self.px(6)))
        self.phone_value = self.make_card(stats, "Phone incidents", 0)
        self.lock_value = self.make_card(stats, "Absence locks", 1)
        self.last_value = self.make_card(stats, "Last incident", 2, small=True)
        for column in range(3):
            stats.columnconfigure(column, weight=1, uniform="cards")

        controls = tk.Frame(root)
        controls.pack(side="top", fill="x", padx=pad)
        self.period_buttons = {}
        for name in PERIODS:
            button = tk.Button(
                controls, text=name, width=11, command=lambda choice=name: self.set_period(choice), cursor="hand2"
            )
            button.pack(side="left", padx=(0, self.px(6)))
            self.period_buttons[name] = button
        tk.Button(controls, text="Close", width=9, command=root.destroy).pack(side="right")
        tk.Button(controls, text="Refresh", width=9, command=self.refresh).pack(side="right", padx=(0, self.px(6)))

        options = tk.Frame(root)
        options.pack(side="top", fill="x", padx=pad, pady=(self.px(6), self.px(6)))
        tk.Checkbutton(
            options, text="Show sample data (demo only)", variable=self.sample, command=self.refresh
        ).pack(side="left")

        self.footer = tk.Label(root, text="", anchor="w", fg="#555555", padx=pad, pady=self.px(4))
        self.footer.pack(side="bottom", fill="x")

        style = ttk.Style()
        style.configure("Treeview", rowheight=self.px(24))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

        self.table_frame = tk.Frame(root)
        self.tree = ttk.Treeview(
            self.table_frame, columns=("time", "event", "duration"), show="headings", selectmode="browse"
        )
        self.tree.heading("time", text="Time")
        self.tree.heading("event", text="Event")
        self.tree.heading("duration", text="Cover duration (seconds)")
        self.tree.column("time", width=self.px(124), anchor="w", stretch=False)
        self.tree.column("event", width=self.px(340), anchor="w", stretch=True)
        self.tree.column("duration", width=self.px(175), anchor="center", stretch=False)
        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.empty_label = tk.Label(root, text=EMPTY_MESSAGE, font=("Segoe UI", 13), fg="#555555")

    def make_card(self, parent, caption, column, small=False):
        card = tk.Frame(parent, bd=1, relief="solid", padx=self.px(8), pady=self.px(6))
        card.grid(row=0, column=column, sticky="nsew", padx=(0 if column == 0 else self.px(6), 0))
        inner = tk.Frame(card)
        inner.pack(expand=True)
        value = tk.Label(inner, text="0", font=("Segoe UI", 15 if small else 24, "bold"))
        value.pack()
        tk.Label(inner, text=caption, fg="#555555").pack()
        return value

    def set_period(self, name):
        self.period = name
        self.render()

    def refresh(self):
        self.truncated = False
        self.read_error = False
        if self.sample.get():
            events = build_sample_events(datetime.now())
        else:
            try:
                events, self.truncated = load_events(LOG_PATH)
            except FileNotFoundError:
                events = []
            except Exception:
                events = []
                self.read_error = True
        self.rows = build_rows(events)
        self.render()

    def render(self):
        if self.sample.get():
            self.banner.pack(side="top", fill="x", before=self.note)
        else:
            self.banner.pack_forget()

        for name, button in self.period_buttons.items():
            selected = name == self.period
            button.config(
                bg="#1d4ed8" if selected else "#e5e7eb",
                fg="white" if selected else "black",
                activebackground="#1e40af" if selected else "#d1d5db",
                activeforeground="white" if selected else "black",
                relief="sunken" if selected else "raised",
            )

        shown = filter_rows(self.rows, self.period, datetime.now())
        phone_incidents, absence_locks, last = compute_stats(shown)
        self.phone_value.config(text=str(phone_incidents))
        self.lock_value.config(text=str(absence_locks))
        self.last_value.config(text=last.strftime("%Y-%m-%d %H:%M:%S") if last else "-")

        self.tree.delete(*self.tree.get_children())
        newest_first = shown[::-1]
        for row in newest_first[:MAX_TABLE_ROWS]:
            self.tree.insert("", "end", values=(row.ts.strftime("%Y-%m-%d %H:%M:%S"), event_label(row), row.duration))

        if shown:
            self.empty_label.pack_forget()
            self.table_frame.pack(side="top", fill="both", expand=True, padx=self.px(14))
        else:
            self.table_frame.pack_forget()
            self.empty_label.config(text=READ_ERROR_MESSAGE if self.read_error else EMPTY_MESSAGE)
            self.empty_label.pack(side="top", fill="both", expand=True)

        notes = []
        if self.truncated:
            notes.append("This is a large log, so only the most recent part was read.")
        if len(shown) > MAX_TABLE_ROWS:
            notes.append(f"Showing the newest {MAX_TABLE_ROWS} of {len(shown)} entries.")
        self.footer.config(text=" ".join(notes))


def main():
    enable_dpi_awareness()
    root = tk.Tk()
    LogViewer(root)
    root.mainloop()


if __name__ == "__main__":
    main()

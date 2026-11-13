import ctypes
import json
import os
import tempfile
import time
import tkinter as tk
from pathlib import Path
from tkinter import filedialog

BASE_DIR = Path(__file__).parent
CONFIG_PATH = BASE_DIR / "config.json"
EXAMPLE_PATH = BASE_DIR / "config.example.json"
DEFAULT_APP_PATH = "securedesk.py"
DEFAULT_APP_NAME = "SecureDesk"

WARNING = "Browsers, Office programs, Teams and Store apps often hand over to another process and may not be protectable."
FILE_TYPES = [
    ("Programs and Python scripts", "*.exe *.py"),
    ("Programs (.exe)", "*.exe"),
    ("Python scripts (.py)", "*.py"),
]


def resolve_app_path(text):
    path = Path(str(text).strip().strip('"').strip())
    return path if path.is_absolute() else BASE_DIR / path


def read_current():
    try:
        config = json.loads(CONFIG_PATH.read_text(encoding="utf-8-sig"))
        raw_path = config.get("protected_app")
        raw_name = config.get("protected_app_name")
    except Exception:
        raw_path = raw_name = None

    default_path = resolve_app_path(DEFAULT_APP_PATH)
    path_text = raw_path.strip() if isinstance(raw_path, str) else ""
    if not path_text:
        return {"path": default_path, "name": DEFAULT_APP_NAME, "is_default": True, "exists": default_path.is_file()}

    path = resolve_app_path(path_text)
    name = raw_name.strip() if isinstance(raw_name, str) else ""
    return {"path": path, "name": name or path.stem, "is_default": path == default_path, "exists": path.is_file()}


def replace_with_retry(source, target, attempts=8):
    for attempt in range(attempts):
        try:
            os.replace(source, target)
            return
        except PermissionError:
            if attempt == attempts - 1:
                raise
            time.sleep(0.1)


def write_json_safely(path, data):
    fd, temp_name = tempfile.mkstemp(dir=path.parent, prefix=path.name + ".", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as temp_file:
            json.dump(data, temp_file)
            temp_file.write("\n")
            temp_file.flush()
            os.fsync(temp_file.fileno())
        replace_with_retry(temp_name, path)
    except BaseException:
        try:
            os.unlink(temp_name)
        except OSError:
            pass
        raise


def load_settings_to_edit():
    source = CONFIG_PATH if CONFIG_PATH.exists() else EXAMPLE_PATH
    if not source.exists():
        return None, "config.json and config.example.json are both missing, so nothing was saved."
    try:
        data = json.loads(source.read_text(encoding="utf-8-sig"))
    except Exception as error:
        return None, f"{source.name} could not be read, so nothing was saved. Please fix or remove it first.\n({error})"
    if not isinstance(data, dict):
        return None, f"{source.name} does not hold a settings object, so nothing was saved."
    return data, None


def save_settings(app_path, app_name):
    app_path = str(app_path or "").strip()
    if not app_path:
        return False, "Please choose a program first."
    resolved = resolve_app_path(app_path)
    if not resolved.is_file():
        return False, f"That file does not exist, so nothing was saved:\n{resolved}"

    data, problem = load_settings_to_edit()
    if problem:
        return False, problem

    data["protected_app"] = app_path if not Path(app_path).is_absolute() else os.path.normpath(app_path)
    data["protected_app_name"] = (app_name or "").strip() or resolved.stem
    try:
        write_json_safely(CONFIG_PATH, data)
    except OSError as error:
        return False, f"The settings could not be saved. The old settings are unchanged.\n({error})"
    return True, "Saved. The change applies the next time the guard starts."


def reset_to_default():
    return save_settings(DEFAULT_APP_PATH, DEFAULT_APP_NAME)


def enable_dpi_awareness():
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass


class SetupWindow:
    def __init__(self, root):
        self.root = root
        self.scale = root.winfo_fpixels("1i") / 96
        self.path_var = tk.StringVar()
        self.name_var = tk.StringVar()

        root.title("Guard Setup (IT Administrator)")
        width, height = self.px(660), self.px(520)
        x = max(0, (root.winfo_screenwidth() - width) // 2)
        y = max(0, (root.winfo_screenheight() - height) // 3)
        root.geometry(f"{width}x{height}+{x}+{y}")
        root.minsize(self.px(600), self.px(480))

        self.build_widgets()
        self.show_current()
        self.fill_form_from_current()

    def px(self, value):
        return int(round(value * self.scale))

    def build_widgets(self):
        root = self.root
        pad = self.px(14)

        tk.Label(root, text="Protected application", font=("Segoe UI", 16, "bold"), anchor="w", padx=pad).pack(
            side="top", fill="x", pady=(self.px(12), 0)
        )
        tk.Label(
            root,
            text="Choose which program the guard starts and protects. Changes apply the next time the guard starts.",
            wraplength=self.px(620),
            justify="left",
            anchor="w",
            padx=pad,
            fg="#555555",
        ).pack(side="top", fill="x", pady=(0, self.px(8)))

        current = tk.LabelFrame(root, text="Currently protected", padx=self.px(10), pady=self.px(8))
        current.pack(side="top", fill="x", padx=pad)
        self.current_name = tk.Label(current, text="", font=("Segoe UI", 12, "bold"), anchor="w")
        self.current_name.pack(fill="x")
        self.current_path = tk.Label(current, text="", anchor="w", justify="left", wraplength=self.px(600))
        self.current_path.pack(fill="x")
        self.current_status = tk.Label(current, text="", anchor="w")
        self.current_status.pack(fill="x")

        change = tk.LabelFrame(root, text="Change it", padx=self.px(10), pady=self.px(8))
        change.pack(side="top", fill="x", padx=pad, pady=(self.px(10), 0))
        file_row = tk.Frame(change)
        file_row.pack(fill="x")
        tk.Label(file_row, text="Program file:", width=14, anchor="w").pack(side="left")
        tk.Entry(file_row, textvariable=self.path_var, state="readonly").pack(side="left", fill="x", expand=True)
        tk.Button(file_row, text="Browse", width=10, command=self.browse).pack(side="left", padx=(self.px(8), 0))
        name_row = tk.Frame(change)
        name_row.pack(fill="x", pady=(self.px(8), 0))
        tk.Label(name_row, text="Friendly name:", width=14, anchor="w").pack(side="left")
        tk.Entry(name_row, textvariable=self.name_var).pack(side="left", fill="x", expand=True)

        tk.Label(
            root,
            text=WARNING,
            wraplength=self.px(620),
            justify="left",
            anchor="w",
            fg="#92400e",
            bg="#fef3c7",
            padx=self.px(10),
            pady=self.px(8),
            font=("Segoe UI", 10, "bold"),
        ).pack(side="top", fill="x", padx=pad, pady=(self.px(12), 0))

        self.status = tk.Label(root, text="", wraplength=self.px(620), justify="left", anchor="w", padx=pad)
        self.status.pack(side="top", fill="x", pady=(self.px(10), 0))

        buttons = tk.Frame(root)
        buttons.pack(side="bottom", fill="x", padx=pad, pady=pad)
        tk.Button(buttons, text="Save", width=12, command=self.save).pack(side="left")
        tk.Button(buttons, text="Reset to SecureDesk", width=20, command=self.reset).pack(side="left", padx=(self.px(8), 0))
        tk.Button(buttons, text="Close", width=10, command=root.destroy).pack(side="right")

    def show_current(self):
        current = read_current()
        suffix = "  (default application)" if current["is_default"] else ""
        self.current_name.config(text=current["name"] + suffix)
        self.current_path.config(text=str(current["path"]))
        if current["exists"]:
            self.current_status.config(text="File found.", fg="#166534")
        else:
            self.current_status.config(text="FILE NOT FOUND - the guard will not start anything until this is fixed.", fg="#b00020")

    def fill_form_from_current(self):
        current = read_current()
        self.path_var.set(str(current["path"]))
        self.name_var.set(current["name"])

    def set_status(self, text, good):
        self.status.config(text=text, fg="#166534" if good else "#b00020")

    def browse(self):
        current = read_current()
        start_dir = current["path"].parent if current["path"].parent.is_dir() else BASE_DIR
        chosen = filedialog.askopenfilename(
            parent=self.root,
            title="Choose the protected application",
            initialdir=str(start_dir),
            filetypes=FILE_TYPES,
        )
        if not chosen:
            return
        chosen_path = Path(chosen)
        self.path_var.set(str(chosen_path))
        self.name_var.set(chosen_path.stem)
        self.set_status("Selected. Edit the friendly name if you like, then click Save.", True)

    def save(self):
        ok, message = save_settings(self.path_var.get(), self.name_var.get())
        self.set_status(message, ok)
        if ok:
            self.show_current()
            self.fill_form_from_current()

    def reset(self):
        ok, message = reset_to_default()
        self.set_status(message if not ok else "Reset to SecureDesk. " + message, ok)
        if ok:
            self.show_current()
            self.fill_form_from_current()


def main():
    enable_dpi_awareness()
    root = tk.Tk()
    SetupWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()

import ctypes
import subprocess
import sys
import threading
import time
import tkinter as tk
from ctypes import wintypes
from datetime import datetime
from pathlib import Path
from tkinter import messagebox

from guard_common import STATUS_INSIDE, ask_consent, check_network

SECUREDESK_PATH = Path(__file__).with_name("securedesk.py")
LOG_PATH = Path(__file__).with_name("session_log.txt")
CAMERA_WINDOW = "Camera ON"
MAX_FAILED_READS = 30

PREVIEW_SIZE = (320, 240)
PREVIEW_MARGIN = 6
PREVIEW_RAISE_INTERVAL = 1.0
SPI_GETWORKAREA = 0x0030
SWP_NOSIZE = 0x0001
SWP_NOMOVE = 0x0002
SWP_NOACTIVATE = 0x0010
HWND_TOPMOST = -1
WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

COVER_SHOWN = "Phone detected - screen covered"
COVER_REMOVED = "Screen cover removed"


def preview_position(work_area, window_size, margin):
    left, top, right, bottom = work_area
    width, height = window_size
    return max(left, right - width - margin), max(top, bottom - height - margin)


class CameraPreview:
    def __init__(self, cv2):
        self.cv2 = cv2
        self.hwnd = None
        self.created = False
        self.last_raise = 0.0
        try:
            user32 = ctypes.WinDLL("user32")
            user32.GetForegroundWindow.restype = wintypes.HWND
            user32.SetForegroundWindow.argtypes = [wintypes.HWND]
            user32.SetWindowPos.argtypes = [
                wintypes.HWND, wintypes.HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, wintypes.UINT
            ]
            user32.GetWindowRect.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.RECT)]
            user32.SystemParametersInfoW.argtypes = [wintypes.UINT, wintypes.UINT, ctypes.c_void_p, wintypes.UINT]
            user32.GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
            user32.EnumThreadWindows.argtypes = [wintypes.DWORD, WNDENUMPROC, wintypes.LPARAM]
            self.user32 = user32
        except Exception:
            self.user32 = None

    def show(self, frame, high_risk):
        cv2 = self.cv2
        width, height = PREVIEW_SIZE
        image = cv2.resize(frame, PREVIEW_SIZE, interpolation=cv2.INTER_AREA)
        label, color = ("HIGH RISK", (0, 0, 255)) if high_risk else ("No risk", (0, 255, 0))
        cv2.rectangle(image, (0, 0), (width, 34), (25, 25, 25), -1)
        cv2.putText(image, label, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        if self.created:
            cv2.imshow(CAMERA_WINDOW, image)
            return

        previous = self._foreground()
        cv2.imshow(CAMERA_WINDOW, image)
        self.created = True
        self.hwnd = self._find_window()
        if self.hwnd:
            work_area = self._work_area()
            size = self._outer_size(self.hwnd)
            if work_area and size:
                x, y = preview_position(work_area, size, PREVIEW_MARGIN)
                self._move_topmost(self.hwnd, x, y)
            else:
                self._raise(self.hwnd)
            if previous and previous != self.hwnd and self._foreground() == self.hwnd:
                self._activate(previous)
        self.last_raise = time.time()

    def keep_on_top(self, force=False):
        if not self.hwnd:
            return
        now = time.time()
        if force or now - self.last_raise >= PREVIEW_RAISE_INTERVAL:
            self._raise(self.hwnd)
            self.last_raise = now

    def _find_window(self):
        found = []

        def callback(hwnd, lparam):
            buffer = ctypes.create_unicode_buffer(256)
            self.user32.GetWindowTextW(hwnd, buffer, 256)
            if buffer.value == CAMERA_WINDOW:
                found.append(hwnd)
            return True

        try:
            self.user32.EnumThreadWindows(threading.get_native_id(), WNDENUMPROC(callback), 0)
        except Exception:
            return None
        return found[0] if found else None

    def _work_area(self):
        try:
            rect = wintypes.RECT()
            if self.user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, ctypes.byref(rect), 0):
                return rect.left, rect.top, rect.right, rect.bottom
        except Exception:
            pass
        return None

    def _outer_size(self, hwnd):
        try:
            rect = wintypes.RECT()
            if self.user32.GetWindowRect(hwnd, ctypes.byref(rect)):
                return rect.right - rect.left, rect.bottom - rect.top
        except Exception:
            pass
        return None

    def _move_topmost(self, hwnd, x, y):
        try:
            self.user32.SetWindowPos(hwnd, wintypes.HWND(HWND_TOPMOST), x, y, 0, 0, SWP_NOSIZE | SWP_NOACTIVATE)
        except Exception:
            pass

    def _raise(self, hwnd):
        try:
            self.user32.SetWindowPos(
                hwnd, wintypes.HWND(HWND_TOPMOST), 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE
            )
        except Exception:
            pass

    def _foreground(self):
        try:
            return self.user32.GetForegroundWindow()
        except Exception:
            return None

    def _activate(self, hwnd):
        try:
            self.user32.SetForegroundWindow(hwnd)
        except Exception:
            pass


def log_event(text):
    try:
        needs_newline = False
        try:
            with open(LOG_PATH, "rb") as existing:
                existing.seek(-1, 2)
                needs_newline = existing.read(1) != b"\n"
        except OSError:
            pass

        with open(LOG_PATH, "a", encoding="utf-8") as log_file:
            if needs_newline:
                log_file.write("\n")
            log_file.write(f"{datetime.now():%Y-%m-%d %H:%M:%S} | {text}\n")
    except Exception:
        pass


def start_securedesk():
    return subprocess.Popen([sys.executable, str(SECUREDESK_PATH)])


def stop_securedesk(process):
    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()


def notify(message):
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    messagebox.showerror("Screen Privacy Guard", message, parent=root)
    root.destroy()


def preload_detection():
    loaded = {}

    def load():
        try:
            import detection

            loaded["detection"] = detection
            loaded["detector"] = detection.PhoneDetector()
        except Exception as error:
            loaded["error"] = error

    thread = threading.Thread(target=load, daemon=True)
    thread.start()
    return thread, loaded


def run_cleanup(*steps):
    first_error = None
    for step in steps:
        try:
            step()
        except Exception as error:
            first_error = first_error or error
    if first_error:
        raise first_error


def monitor(process, detector, detection):
    import cv2

    cover = None
    cover_up = False
    camera = None
    started = False

    def close_cover():
        if cover is not None:
            cover.close()
            if cover_up:
                log_event(COVER_REMOVED)

    try:
        from screen_cover import ScreenCover

        camera = detection.open_webcam()
        if not camera.isOpened():
            return "The webcam could not be opened, so SecureDesk was closed. Monitoring is required outside the office network."

        cover = ScreenCover()
        preview = CameraPreview(cv2)
        started = True
        print("Camera started")
        failed_reads = 0

        while process.poll() is None:
            ok, frame = camera.read()
            if not ok:
                failed_reads += 1
                if failed_reads > MAX_FAILED_READS:
                    return "The webcam stopped working, so SecureDesk was closed. Monitoring is required outside the office network."
                time.sleep(0.05)
                continue
            failed_reads = 0

            detector.process_frame(frame, blur=False)
            high_risk = detector.high_risk
            preview.show(frame, high_risk)

            if high_risk:
                if not cover_up:
                    cover.show()
                    cover_up = True
                    log_event(COVER_SHOWN)
                    preview.keep_on_top(force=True)
            elif cover_up:
                cover.hide()
                cover_up = False
                log_event(COVER_REMOVED)
            preview.keep_on_top()
            cover.update()

            if cv2.waitKey(1) & 0xFF == ord("q"):
                return None
            if cv2.getWindowProperty(CAMERA_WINDOW, cv2.WND_PROP_VISIBLE) < 1:
                return None
        return None
    finally:
        run_cleanup(
            close_cover,
            lambda: camera.release() if camera is not None else None,
            detector.close,
            cv2.destroyAllWindows,
            lambda: stop_securedesk(process),
        )
        if started:
            print("Camera stopped")


def main():
    status, message = check_network()

    if status == STATUS_INSIDE:
        start_securedesk().wait()
        return

    reason = message.removesuffix(" - monitoring ON").removesuffix(" - monitoring OFF")
    print(f"{reason} - consent required.")

    loader, loaded = preload_detection()

    if not ask_consent():
        print("Consent declined - SecureDesk not started.")
        loader.join()
        return

    loader.join()
    if "detector" not in loaded:
        notify(f"Monitoring could not be prepared, so SecureDesk was not started.\n\n{loaded.get('error')}")
        return

    process = start_securedesk()
    problem = monitor(process, loaded["detector"], loaded["detection"])
    if problem:
        notify(problem)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        notify(f"The guard stopped unexpectedly.\n\n{error}")
        raise

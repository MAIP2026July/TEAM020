import subprocess
import sys
import threading
import time
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

from guard_common import STATUS_INSIDE, ask_consent, check_network

SECUREDESK_PATH = Path(__file__).with_name("securedesk.py")
CAMERA_WINDOW = "Screen Privacy Guard"
MAX_FAILED_READS = 30


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
    camera = None
    started = False
    try:
        from screen_cover import ScreenCover

        camera = detection.open_webcam()
        if not camera.isOpened():
            return "The webcam could not be opened, so SecureDesk was closed. Monitoring is required outside the office network."

        cover = ScreenCover()
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

            cv2.imshow(CAMERA_WINDOW, detector.process_frame(frame, blur=False))

            if detector.high_risk:
                cover.show()
            else:
                cover.hide()
            cover.update()

            if cv2.waitKey(1) & 0xFF == ord("q"):
                return None
            if cv2.getWindowProperty(CAMERA_WINDOW, cv2.WND_PROP_VISIBLE) < 1:
                return None
        return None
    finally:
        run_cleanup(
            lambda: cover.close() if cover is not None else None,
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

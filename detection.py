import queue
import threading
import time
from collections import deque
from pathlib import Path

import cv2
import numpy as np
from ultralytics import YOLO

CONFIDENCE_THRESHOLD = 0.25
IMAGE_SIZE = 512
BLUR_DOWNSCALE = 4
PHONE_CLASS_ID = 67
GRACE_PERIOD_SECONDS = 2

INITIAL_WINDOW_SIZE = 5
INITIAL_TRIGGER_COUNT = 3

CONFIRM_WINDOW_SIZE = 10
CONFIRM_TRIGGER_COUNT = 3

STATE_IDLE = "idle"
STATE_CONFIRMING = "confirming"
STATE_ACTIVE = "active"

MODEL_PATH = Path(__file__).with_name("yolo11s.pt")


def open_webcam():
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    return camera


class PhoneDetector:
    def __init__(self):
        self.model = YOLO(str(MODEL_PATH))
        self.model(np.zeros((480, 640, 3), dtype=np.uint8), imgsz=IMAGE_SIZE, verbose=False)

        self.state = STATE_IDLE
        self.last_detected_time = None
        self.initial_window = deque(maxlen=INITIAL_WINDOW_SIZE)
        self.confirm_window = deque(maxlen=CONFIRM_WINDOW_SIZE)

        self.latest_frame = None
        self.frame_lock = threading.Lock()
        self.results_queue = queue.Queue()
        self.stop_event = threading.Event()
        threading.Thread(target=self._inference_loop, daemon=True).start()

    def _inference_loop(self):
        last_seen = None
        while not self.stop_event.is_set():
            with self.frame_lock:
                frame = self.latest_frame
            if frame is None or frame is last_seen:
                time.sleep(0.005)
                continue
            last_seen = frame
            results = self.model(
                frame,
                imgsz=IMAGE_SIZE,
                conf=CONFIDENCE_THRESHOLD,
                classes=[PHONE_CLASS_ID],
                verbose=False,
            )[0]
            self.results_queue.put(len(results.boxes) > 0)

    @property
    def high_risk(self):
        return self.state in (STATE_CONFIRMING, STATE_ACTIVE)

    def _drain_results(self):
        while not self.results_queue.empty():
            self.results_queue.get_nowait()

    def reset(self):
        with self.frame_lock:
            self.latest_frame = None
        self._drain_results()
        self.state = STATE_IDLE
        self.last_detected_time = None
        self.initial_window.clear()
        self.confirm_window.clear()

    def process_frame(self, frame, blur=True):
        with self.frame_lock:
            self.latest_frame = frame

        while not self.results_queue.empty():
            phone_detected = self.results_queue.get_nowait()

            if self.state == STATE_IDLE:
                self.initial_window.append(phone_detected)
                if sum(self.initial_window) >= INITIAL_TRIGGER_COUNT:
                    self.state = STATE_CONFIRMING
                    self.confirm_window.clear()
                    self.last_detected_time = time.time()

            elif self.state == STATE_CONFIRMING:
                self.confirm_window.append(phone_detected)
                if phone_detected:
                    self.last_detected_time = time.time()

                if len(self.confirm_window) == CONFIRM_WINDOW_SIZE:
                    if sum(self.confirm_window) < CONFIRM_TRIGGER_COUNT:
                        self.state = STATE_IDLE
                        self.initial_window.clear()
                        self.last_detected_time = None
                    else:
                        self.state = STATE_ACTIVE

            elif self.state == STATE_ACTIVE:
                if phone_detected:
                    self.last_detected_time = time.time()

        if self.state == STATE_ACTIVE and time.time() - self.last_detected_time >= GRACE_PERIOD_SECONDS:
            self.state = STATE_IDLE
            self.initial_window.clear()
            self.last_detected_time = None

        if self.high_risk:
            if blur:
                height, width = frame.shape[:2]
                small = cv2.resize(frame, (width // BLUR_DOWNSCALE, height // BLUR_DOWNSCALE))
                small = cv2.GaussianBlur(small, (25, 25), 8)
                display_frame = cv2.resize(small, (width, height))
            else:
                display_frame = frame.copy()
            text, color = "HIGH RISK", (0, 0, 255)
        else:
            display_frame = frame.copy()
            text, color = "No risk", (0, 255, 0)

        cv2.putText(display_frame, text, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
        return display_frame

    def close(self):
        self.stop_event.set()

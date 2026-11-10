import queue
import threading
import time
from collections import deque

import cv2
from ultralytics import YOLO

CONFIDENCE_THRESHOLD = 0.35
IMAGE_SIZE = 416
PHONE_CLASS_ID = 67
GRACE_PERIOD_SECONDS = 2

INITIAL_WINDOW_SIZE = 5
INITIAL_TRIGGER_COUNT = 3

CONFIRM_WINDOW_SIZE = 10
CONFIRM_TRIGGER_COUNT = 3

STATE_IDLE = "idle"
STATE_CONFIRMING = "confirming"
STATE_ACTIVE = "active"

model = YOLO("yolo11s.pt")

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

latest_frame = None
frame_lock = threading.Lock()
results_queue = queue.Queue()
stop_event = threading.Event()


def inference_loop():
    last_seen = None
    while not stop_event.is_set():
        with frame_lock:
            frame = latest_frame
        if frame is None or frame is last_seen:
            time.sleep(0.005)
            continue
        last_seen = frame
        results = model(
            frame,
            imgsz=IMAGE_SIZE,
            conf=CONFIDENCE_THRESHOLD,
            classes=[PHONE_CLASS_ID],
            verbose=False,
        )[0]
        results_queue.put(len(results.boxes) > 0)


threading.Thread(target=inference_loop, daemon=True).start()

state = STATE_IDLE
last_detected_time = None
initial_window = deque(maxlen=INITIAL_WINDOW_SIZE)
confirm_window = deque(maxlen=CONFIRM_WINDOW_SIZE)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    with frame_lock:
        latest_frame = frame

    while not results_queue.empty():
        phone_detected = results_queue.get_nowait()

        if state == STATE_IDLE:
            initial_window.append(phone_detected)
            if sum(initial_window) >= INITIAL_TRIGGER_COUNT:
                state = STATE_CONFIRMING
                confirm_window.clear()
                last_detected_time = time.time()

        elif state == STATE_CONFIRMING:
            confirm_window.append(phone_detected)
            if phone_detected:
                last_detected_time = time.time()

            if len(confirm_window) == CONFIRM_WINDOW_SIZE:
                if sum(confirm_window) < CONFIRM_TRIGGER_COUNT:
                    state = STATE_IDLE
                    initial_window.clear()
                    last_detected_time = None
                else:
                    state = STATE_ACTIVE

        elif state == STATE_ACTIVE:
            if phone_detected:
                last_detected_time = time.time()

    if state == STATE_ACTIVE and time.time() - last_detected_time >= GRACE_PERIOD_SECONDS:
        state = STATE_IDLE
        initial_window.clear()
        last_detected_time = None

    if state in (STATE_CONFIRMING, STATE_ACTIVE):
        display_frame = cv2.GaussianBlur(frame, (99, 99), 30)
        text, color = "HIGH RISK", (0, 0, 255)
    else:
        display_frame = frame.copy()
        text, color = "No risk", (0, 255, 0)

    cv2.putText(display_frame, text, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
    cv2.imshow("Screen Privacy Guard", display_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

stop_event.set()
cap.release()
cv2.destroyAllWindows()

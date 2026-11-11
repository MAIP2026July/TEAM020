import sys
import textwrap
import threading

import cv2
import numpy as np

from detection import PhoneDetector, open_webcam
from guard_common import (
    STATUS_CHECKING,
    STATUS_INSIDE,
    STATUS_OUTSIDE,
    ask_consent,
    check_network,
)

if not ask_consent():
    sys.exit(0)


NETWORK_CHECK_INTERVAL_SECONDS = 30


def make_status_image(message, color):
    image = np.full((480, 640, 3), 40, dtype=np.uint8)
    lines = textwrap.wrap(message, 34)
    y = 240 - (len(lines) - 1) * 20
    for line in lines:
        (text_width, _), _ = cv2.getTextSize(line, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
        cv2.putText(image, line, ((640 - text_width) // 2, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        y += 40
    return image


detector = PhoneDetector()

cap = None

stop_event = threading.Event()

network_status = (STATUS_CHECKING, "Checking network...")


def network_loop():
    global network_status
    while not stop_event.is_set():
        network_status = check_network()
        stop_event.wait(NETWORK_CHECK_INTERVAL_SECONDS)


threading.Thread(target=network_loop, daemon=True).start()

while True:
    status, status_message = network_status
    monitoring = status == STATUS_OUTSIDE

    if monitoring and cap is None:
        detector.reset()
        cap = open_webcam()

    elif not monitoring and cap is not None:
        cap.release()
        cap = None
        detector.reset()

    if cap is None:
        message_color = (255, 255, 255) if status in (STATUS_INSIDE, STATUS_CHECKING) else (0, 200, 255)
        cv2.imshow("Screen Privacy Guard", make_status_image(status_message, message_color))
        if cv2.waitKey(100) & 0xFF == ord("q"):
            break
        continue

    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Screen Privacy Guard", detector.process_frame(frame))

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

stop_event.set()
detector.close()
if cap is not None:
    cap.release()
cv2.destroyAllWindows()

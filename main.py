import cv2
import mediapipe as mp
import time
import math
import numpy as np
import threading
from pydub import AudioSegment
from pydub.playback import play

# ================= ALERT SYSTEM =================
alert_active = False
alarm_thread = None

def alarm_loop():
    global alert_active
    sound = AudioSegment.from_wav("alert.wav")
    while alert_active:
        play(sound)
        time.sleep(2)

def play_alert_sound():
    global alarm_thread
    if alarm_thread is None or not alarm_thread.is_alive():
        alarm_thread = threading.Thread(target=alarm_loop, daemon=True)
        alarm_thread.start()

def trigger_alert():
    global alert_active
    if not alert_active:
        alert_active = True
        play_alert_sound()

def reset_alert():
    global alert_active
    alert_active = False


# ================= MEDIAPIPE SETUP =================
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# Eye landmark indices
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

def eye_aspect_ratio(landmarks, eye_indices, w, h):
    points = [(int(landmarks[i].x * w), int(landmarks[i].y * h)) for i in eye_indices]

    v1 = math.dist(points[1], points[5])
    v2 = math.dist(points[2], points[4])
    h_dist = math.dist(points[0], points[3])

    ear = (v1 + v2) / (2.0 * h_dist)
    return ear


# ================= THRESHOLDS =================
EAR_THRESHOLD = 0.30
SLEEP_TIME = 3   # seconds

sleep_start = None


# ================= VIDEO CAPTURE =================
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark

        left_ear = eye_aspect_ratio(landmarks, LEFT_EYE, w, h)
        right_ear = eye_aspect_ratio(landmarks, RIGHT_EYE, w, h)
        avg_ear = (left_ear + right_ear) / 2.0

        cv2.putText(frame, f"EAR: {avg_ear:.2f}", (30, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # ================= SLEEP DETECTION =================
        if avg_ear < EAR_THRESHOLD:
            if sleep_start is None:
                sleep_start = time.time()
            elif time.time() - sleep_start > SLEEP_TIME:
                cv2.putText(frame, "SLEEP ALERT!", (50, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                trigger_alert()
        else:
            sleep_start = None
            reset_alert()

    else:
        cv2.putText(frame, "No Face Detected", (50, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        trigger_alert()

    cv2.imshow("Sleep Detection System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

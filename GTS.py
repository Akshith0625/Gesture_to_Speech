import mediapipe as mp
import cv2
import pyttsx3 as p
import threading
import time

hand = mp.solutions.hands.Hands()
cam = cv2.VideoCapture(0)

if not cam.isOpened():
    print("Error: Camera not accessible")
    exit()

gesture_detected = False

def speaker(text):
    def speak():
        engine = p.init()
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=speak).start()

def detect_gesture(lms):
    global gesture_detected
    if not gesture_detected:
        if all(lms[i].y < lms[i - 1].y for i in (4, 8, 12, 16, 20)):
            gesture_detected = True
            speaker("hello")
            # Reset the gesture_detected flag after a short delay
            threading.Timer(2.0, reset_gesture_detected).start()

def reset_gesture_detected():
    global gesture_detected
    gesture_detected = False

while True:
    ret, frame = cam.read()
    if not ret:
        print("Error: Failed to capture frame")
        continue

    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hand.process(img)
    if result.multi_hand_landmarks:
        for handlms in result.multi_hand_landmarks:
            detect_gesture(handlms.landmark)

    cv2.imshow("Hand Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
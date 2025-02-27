import mediapipe as mp
import cv2
import pyttsx3 as p
import threading
import time

hand = mp.solutions.hands.Hands()
cam = cv2.VideoCapture(0)
engine = p.init()

if not cam.isOpened():
    print("Error: Camera not accessible")
    exit()

gesture_detected = False



def speaker(text):
    def speak():
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=speak).start()

def detect_gesture(lms_list, frame):
    global gesture_detected
    gesture = None
    if not gesture_detected:
        if len(lms_list)==2:
            lms1,lms2 = lms_list


        elif len(lms_list)==1:
            lms=lms_list[0]
            if all(lms[i].y < lms[i - 1].y for i in (4, 8, 12, 16, 20)):
                gesture = "hello"
            elif lms[4].x > lms[8].x and all(lms[8].x < lms[i].x<lms[4].x for i in (12, 16, 20)):
                gesture = 'smile please'
            elif all(lms[4].y < lms[i].y for i in (6, 10, 14, 18)):
                gesture = 'thumbs up'
            else:
                gesture = None

        if gesture:
            gesture_detected = True
            speaker(gesture)
            threading.Timer(2.0, reset_gesture_detected).start()

    if gesture:
        cv2.putText(frame, gesture, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3, cv2.LINE_AA)

def reset_gesture_detected():
    global gesture_detected
    gesture_detected = False

while True:
    ret, frame = cam.read()
    if not ret:
        print("Error: Failed to capture frame")
        continue

    frame = cv2.flip(frame, 1)  # Flip the frame before processing
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hand.process(img)
    if result.multi_hand_landmarks:
        detect_gesture([h.landmark for h in result.multi_hand_landmarks], frame)

    cv2.imshow("Hand Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()

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

def detect_gestures(lms_list):
    global gesture_detected
    if not gesture_detected:
        if len(lms_list) == 2:
            lms1, lms2 = lms_list
            # Check if the tips of the index fingers and thumbs are close to each other (heart gesture)
            if (abs(lms1[8].x - lms2[8].x) < 0.05 and abs(lms1[8].y - lms2[8].y) < 0.05 and  # Index fingers
                abs(lms1[4].x - lms2[4].x) < 0.05 and abs(lms1[4].y - lms2[4].y) < 0.05):  # Thumbs
                gesture_detected = True
                speaker("love")
                # Reset the gesture_detected flag after a short delay
                threading.Timer(2.0, reset_gesture_detected).start()
        elif len(lms_list) == 1:
            lms = lms_list[0]
            # Check if the thumb and index finger are in a wide, opposite position near the mouth (smile gesture)
            if (abs(lms[8].x - lms[4].x) > 0.1 and abs(lms[8].y - lms[4].y) < 0.05 and  # Index finger and thumb
                lms[8].y < lms[0].y and lms[4].y < lms[0].y and  # Near the mouth (above the wrist)
                lms[12].y > lms[10].y and  # Middle finger not extended
                lms[16].y > lms[14].y and  # Ring finger not extended
                lms[20].y > lms[18].y):  # Pinky finger not extended
                gesture_detected = True
                speaker("smile please")
                # Reset the gesture_detected flag after a short delay
                threading.Timer(2.0, reset_gesture_detected).start()
            # Check if all fingers are extended (full palm)
            elif (lms[8].y < lms[6].y and  # Index finger
                  lms[12].y < lms[10].y and  # Middle finger
                  lms[16].y < lms[14].y and  # Ring finger
                  lms[20].y < lms[18].y and  # Pinky finger
                  lms[4].x > lms[3].x):  # Thumb (assuming right hand)
                gesture_detected = True
                speaker("hello")
                # Reset the gesture_detected flag after a short delay
                threading.Timer(2.0, reset_gesture_detected).start()
            # Check if the thumb is extended upwards (thumbs up gesture)
            elif (lms[4].y < lms[3].y and  # Thumb extended upwards
                  lms[8].y > lms[6].y and  # Index finger curled
                  lms[12].y > lms[10].y and  # Middle finger curled
                  lms[16].y > lms[14].y and  # Ring finger curled
                  lms[20].y > lms[18].y):  # Pinky finger curled
                gesture_detected = True
                speaker("Done")
                # Reset the gesture_detected flag after a short delay
                threading.Timer(2.0, reset_gesture_detected).start()
            # Check if the thumb is extended downwards (thumbs down gesture)
            elif (lms[4].y > lms[3].y and  # Thumb extended downwards
                  lms[8].y > lms[6].y and  # Index finger curled
                  lms[12].y > lms[10].y and  # Middle finger curled
                  lms[16].y > lms[14].y and  # Ring finger curled
                  lms[20].y > lms[18].y):  # Pinky finger curled
                gesture_detected = True
                speaker("not done")
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
        detect_gestures([handlms.landmark for handlms in result.multi_hand_landmarks])

    cv2.imshow("Hand Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
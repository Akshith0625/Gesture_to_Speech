import mediapipe as mp
import cv2
import pyttsx3 as p
import threading

hand = mp.solutions.hands.Hands()
cam = cv2.VideoCapture(0)

if not cam.isOpened():
    print("Error: Camera not accessible")
    exit()

gesture_detected = False

<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
def speaker(text):
    def speak():
        engine = p.init()
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=speak).start()

<<<<<<< Updated upstream
def detect_gestures(lms_list,frame):
=======
def detect_number(lms):
    fingers = [lms[i].y < lms[i - 2].y for i in [8, 12, 16, 20]]
    if fingers == [True, False, False, False]:
        return '1'
    elif fingers == [True, True, False, False]:
        return '2'
    elif fingers == [True, True, True, False]:
        return '3'
    elif fingers == [True, True, True, True]:
        return '4'
    elif fingers == [True, True, True, True] and lms[4].y < lms[3].y:
        return '5'
    elif fingers == [True, True, True, True] and lms[4].y > lms[3].y:
        return '6'
    elif fingers == [True, True, True, True] and lms[4].x < lms[3].x:
        return '7'
    elif fingers == [True, True, True, True] and lms[4].x > lms[3].x:
        return '8'
    elif fingers == [True, True, True, True] and lms[4].x < lms[3].x and lms[4].y < lms[3].y:
        return '9'
    elif fingers == [True, True, True, True] and lms[4].x > lms[3].x and lms[4].y < lms[3].y:
        return '10'
    return None

def detect_gesture(lms_list, frame):
>>>>>>> Stashed changes
    global gesture_detected
    gesture=None
    if not gesture_detected:
<<<<<<< Updated upstream
        if len(lms_list) == 2:
            lms1, lms2 = lms_list
            # Check if the tips of the index fingers and thumbs are close to each other (heart gesture)
            if (abs(lms1[8].x - lms2[8].x) < 0.05 and abs(lms1[8].y - lms2[8].y) < 0.05 and  # Index fingers
                abs(lms1[4].x - lms2[4].x) < 0.05 and abs(lms1[4].y - lms2[4].y) < 0.05):  # Thumbs
                gesture_detected = True
                gesture="heart"
=======
        if len(lms_list) == 1:
            lms = lms_list[0]
            number_gesture = detect_number(lms)
            if number_gesture:
                gesture = number_gesture
            elif all(lms[i].y < lms[i - 1].y for i in (4, 8, 12, 16, 20)):
                gesture = "hello"
            elif lms[4].x > lms[8].x and all(lms[8].x < lms[i].x < lms[4].x for i in (12, 16, 20)):
                gesture = 'smile please'
            elif all(lms[4].y < lms[i].y for i in (6, 10, 14, 18)):
                gesture = 'thumbs up'
            elif all(lms[4].y > lms[i].y for i in (6, 10, 14, 18)):
                gesture = 'thumbs down'
            elif all(abs(lms[4].x - lms[i].x) < 0.05 for i in (8, 12, 16, 20)) and \
                 all(lms[4].y > lms[i].y for i in (8, 12, 16, 20)) and \
                 abs(lms[4].y - lms[3].y) < 0.05:  # Heart symbol condition
                gesture = 'love'
>>>>>>> Stashed changes
            else:
                gesture=None


        elif len(lms_list) == 1:
            lms = lms_list[0]
            # Check if the thumb and index finger are in a wide, opposite position near the mouth (smile gesture)
            if (abs(lms[8].x - lms[4].x) > 0.1 and abs(lms[8].y - lms[4].y) < 0.05 and  # Index finger and thumb
                lms[8].y < lms[0].y and lms[4].y < lms[0].y and  # Near the mouth (above the wrist)
                lms[12].y > lms[10].y and  # Middle finger not extended
                lms[16].y > lms[14].y and  # Ring finger not extended
                lms[20].y > lms[18].y):  # Pinky finger not extended
                gesture_detected = True
                gesture="smile please"
            # Check if all fingers are extended (full palm)
            elif (lms[8].y < lms[6].y and  # Index finger
                  lms[12].y < lms[10].y and  # Middle finger
                  lms[16].y < lms[14].y and  # Ring finger
                  lms[20].y < lms[18].y and  # Pinky finger
                  lms[4].x > lms[3].x):  # Thumb (assuming right hand)
                gesture_detected = True
                gesture='hello'
            # Check if the thumb is extended upwards (thumbs up gesture)
            elif (lms[4].y < lms[3].y and  # Thumb extended upwards
                  lms[8].y > lms[6].y and  # Index finger curled
                  lms[12].y > lms[10].y and  # Middle finger curled
                  lms[16].y > lms[14].y and  # Ring finger curled
                  lms[20].y > lms[18].y):  # Pinky finger curled
                gesture_detected = True
                gesture="Done"
            elif (lms[4].y > lms[3].y and  # Thumb extended downwards
                  lms[8].y > lms[6].y and  # Index finger curled
                  lms[12].y > lms[10].y and  # Middle finger curled
                  lms[16].y > lms[14].y and  # Ring finger curled
                  lms[20].y > lms[18].y):  # Pinky finger curled
                gesture_detected = True
                gesture="not done"
            else:
                gesture=None

        
        if gesture:
            speaker(gesture)
<<<<<<< Updated upstream
            cv2.putText(frame, gesture, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            threading.Timer(2.0, reset_gesture_detected).start()    
=======
            threading.Timer(1.0, reset_gesture_detected).start()  # Set timer duration to 1 second
>>>>>>> Stashed changes


def reset_gesture_detected():
    global gesture_detected
    gesture_detected = False

while True:
    ret, frame = cam.read()
    if not ret:
        print("Error: Failed to capture frame")
        continue

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hand.process(frame)
    if result.multi_hand_landmarks:
        detect_gestures([handlms.landmark for handlms in result.multi_hand_landmarks],frame)

    cv2.imshow("Hand Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
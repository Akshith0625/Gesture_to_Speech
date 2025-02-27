import mediapipe as mp
import cv2
import pyttsx3 as p
import threading
import time, Letter

hand = mp.solutions.hands.Hands()
cam = cv2.VideoCapture(0)
engine = p.init()

if not cam.isOpened():
    print("Error: Camera not accessible")
    exit()

gesture_detected = False
mode = "normal"
captured_letters = []

def speaker(text):
    def speak():
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=speak).start()

def detect_number(lms):
    fingers = [lms[i].y < lms[i - 2].y for i in [8, 12, 16, 20]]
    if fingers == [True, True,True,False] and lms[4].x==lms[17].x:
        return '6'
    elif fingers == [True, True, False, True] and lms[4].x==lms[13].x:
        return '7'
    elif fingers == [True, False, True, True] and lms[4].x==lms[9].x:
        return '8'
    elif fingers == [False, True, True, True] and lms[4].x==lms[5].x:
        return '9'
    elif fingers == [True, False,False,False]:
        return '1'
    elif fingers == [True, True,False,False]:
        return '2'
    elif fingers == [True, True,True,False]:
        return '3'
    elif fingers == [True, True,True,True] and lms[4].x > lms[3].x and lms[4].y > lms[3].y:
        return '4'
    return None

def detect_gesture(lms_list, data, frame):
    global gesture_detected, mode, captured_letters
    gesture = None
    if not gesture_detected:
        if len(lms_list) == 2:
            lms1, lms2 = lms_list
            left, right = (lms_list[0], lms_list[1]) if data.multi_handedness[0].classification[0].label == "Left" else (lms_list[1], lms_list[0])
            if (abs(lms1[8].x - lms2[8].x) < 0.05 and abs(lms1[8].y - lms2[8].y) < 0.05 and  # Index fingers
                abs(lms1[4].x - lms2[4].x) < 0.05 and abs(lms1[4].y - lms2[4].y) < 0.05):  # Thumbs
                gesture_detected = True
                gesture = "heart"
            else:
                gesture = Letter.classify_isl_letter(left, right)

        elif len(lms_list) == 1:
            lms = lms_list[0]
            number_gesture = detect_number(lms)
            if number_gesture:
                gesture = number_gesture
            elif all(lms[i].y < lms[i - 1].y for i in (8, 12, 16, 20)):
                gesture = "hello"
            elif lms[4].x > lms[8].x and all(lms[8].x < lms[i].x < lms[4].x for i in (12, 16, 20)):
                gesture = 'smile please'
            elif all(lms[4].y < lms[i].y for i in (6, 10, 14, 18)):
                gesture = 'thumbs up'
            elif (lms[4].x > lms[3].x and  # Thumb pointing away from the body
                  all(lms[i].y > lms[i - 2].y for i in (8, 12, 16, 20))):  # All fingers curled
                gesture_detected = True
                gesture = "Done"
            else:
                gesture = Letter.classify_isl_letter(None, lms)

        if gesture:
            if mode == "normal":
                if gesture == "Done":
                    mode = "letter_mode"
                    captured_letters = []
                else:
                    speaker(gesture)
            elif mode == "letter_mode":
                if gesture == "Done":
                    word = ''.join(captured_letters)
                    speaker(word)
                    mode = "normal"
                elif gesture not in ["hello", "smile please", "thumbs up", "heart", "not done"]:
                    captured_letters.append(gesture)
            gesture_detected = True
            threading.Timer(3.0, reset_gesture_detected).start()  # Increased delay to 3 seconds

    if gesture:
        cv2.putText(frame, gesture, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3, cv2.LINE_AA)
        if mode == "letter_mode":
            cv2.putText(frame, ''.join(captured_letters), (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3, cv2.LINE_AA)

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
        detect_gesture([h.landmark for h in result.multi_hand_landmarks], result, frame)

    cv2.imshow("Hand Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()

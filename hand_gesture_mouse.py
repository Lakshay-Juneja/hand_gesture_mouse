import cv2
import mediapipe as mp
import pyautogui as ptg
import numpy as np
import threading
from pynput.mouse import Controller, Button as mouseButton
import tkinter as tk
from tkinter import Label, Button
from datetime import datetime  

# Initialize Mediapipe Hands
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.7,
    max_num_hands=1
)
mpDraw = mp.solutions.drawing_utils

# Mouse Controller
mouse = Controller()
screenWidth, screenHeight = ptg.size()

# Global Variables
capture = None
running = False

# Gesture Functions
def getAngle(a, b, c):
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    return np.abs(np.degrees(radians))

def getDistance(landMarkList):
    if len(landMarkList) < 2:
        return float('inf')
    (x1, y1), (x2, y2) = landMarkList[0], landMarkList[1]
    return np.hypot(x2 - x1, y2 - y1)

def findFingerTip(processed):
    if processed.multi_hand_landmarks:
        handLandMarks = processed.multi_hand_landmarks[0]
        return handLandMarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
    return None

def moveMouse(indexFingerTip):
    if indexFingerTip:
        x = np.clip(int(indexFingerTip.x * screenWidth), 0, screenWidth)
        y = np.clip(int(indexFingerTip.y * screenHeight), 0, screenHeight)
        ptg.moveTo(x, y, duration=0.1)

def closeMoving(landMarksList):
    return (
        getAngle(landMarksList[13], landMarksList[14], landMarksList[16]) < 90 and
        getAngle(landMarksList[17], landMarksList[18], landMarksList[20]) < 90 and
        getDistance([landMarksList[4], landMarksList[5]]) < 50
    )

def gesturesText(frame, txt):
    cv2.putText(frame, txt, (48, 48), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 255), 6)
    cv2.putText(frame, txt, (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 2)

def detectGestures(frame, landMarksList, processed):
    if len(landMarksList) < 21:
        return

    indexFingerTip = findFingerTip(processed)
    
    # Move Mouse
    if (
        getAngle(landMarksList[5], landMarksList[6], landMarksList[8]) > 90 and
        getAngle(landMarksList[9], landMarksList[10], landMarksList[12]) > 90 and
        closeMoving(landMarksList)
    ):
        moveMouse(indexFingerTip)

    # Left Click
    elif (
        getAngle(landMarksList[5], landMarksList[6], landMarksList[8]) < 50 and
        getAngle(landMarksList[9], landMarksList[10], landMarksList[12]) > 90 and
        getDistance([landMarksList[4], landMarksList[5]]) > 50
    ):
        mouse.click(mouseButton.left, 1)
        gesturesText(frame, "Left Click")

    # Right Click
    elif (
        getAngle(landMarksList[5], landMarksList[6], landMarksList[8]) > 90 and
        getAngle(landMarksList[9], landMarksList[10], landMarksList[12]) < 50 and
        getDistance([landMarksList[4], landMarksList[5]]) > 50
    ):
        mouse.click(mouseButton.right, 1)
        gesturesText(frame, "Right Click")

    # Scroll Gesture (Index and Middle Finger Extended)
    elif (
        getAngle(landMarksList[5], landMarksList[6], landMarksList[8]) < 50 and
        getAngle(landMarksList[9], landMarksList[10], landMarksList[12]) < 50 and
        getAngle(landMarksList[13], landMarksList[14], landMarksList[16]) > 90 and
        getDistance([landMarksList[4], landMarksList[5]]) > 50
    ):
        ptg.scroll(40)  # Scroll up
        gesturesText(frame, "Scroll Up")

    elif (
        getAngle(landMarksList[5], landMarksList[6], landMarksList[8]) < 50 and
        getAngle(landMarksList[9], landMarksList[10], landMarksList[12]) < 50 and
        getAngle(landMarksList[13], landMarksList[14], landMarksList[16]) < 90 and
        getDistance([landMarksList[4], landMarksList[5]]) > 50
    ):
        ptg.scroll(-40)  # Scroll down
        gesturesText(frame, "Scroll Down")

    # Screenshot
    elif (
        getAngle(landMarksList[5], landMarksList[6], landMarksList[8]) > 90 and
        getAngle(landMarksList[9], landMarksList[10], landMarksList[12]) > 90 and
        getAngle(landMarksList[13], landMarksList[14], landMarksList[16]) > 90 and
        getAngle(landMarksList[17], landMarksList[18], landMarksList[20]) < 50 and
        getDistance([landMarksList[4], landMarksList[5]]) > 50
    ):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        screenshot = ptg.screenshot()
        screenshot.save(filename)
        gesturesText(frame, "Screenshot Taken")

# Start Camera Capture
def startCamera():
    global capture, running
    if running:
        return
    running = True
    capture = cv2.VideoCapture(0)
    thread = threading.Thread(target=processCamera)
    thread.start()

# Stop Camera Capture
def stopCamera():
    global capture, running
    running = False
    if capture:
        capture.release()
        capture = None
    cv2.destroyAllWindows()

# Process Camera Feed
def processCamera():
    global running
    while running:
        ret, frame = capture.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        processed = hands.process(frameRGB)

        landMarksList = []
        if processed.multi_hand_landmarks:
            for handLandMarks in processed.multi_hand_landmarks:
                mpDraw.draw_landmarks(frame, handLandMarks, mpHands.HAND_CONNECTIONS)
                landMarksList = [(int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0])) 
                                 for lm in handLandMarks.landmark]

        detectGestures(frame, landMarksList, processed)

        cv2.imshow('Virtual Mouse', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    stopCamera()

# GUI Window
root = tk.Tk()
root.title("Hand Gesture Mouse")
root.geometry("400x300")
root.configure(bg="#2C3E50")  # Set background color

# Title Label
titleLabel = Label(root, text="Hand Gesture Mouse", font=("Arial", 16, "bold"), bg="#2C3E50", fg="white")
titleLabel.pack(pady=20)

# Start Button
startButton = Button(root, text="Start", font=("Arial", 12), bg="green", fg="white", width=15, command=startCamera)
startButton.pack(pady=10)

# Stop Button
stopButton = Button(root, text="Stop", font=("Arial", 12), bg="red", fg="white", width=15, command=stopCamera)
stopButton.pack(pady=10)

# Exit Button
exitButton = Button(root, text="Exit", font=("Arial", 12), bg="black", fg="white", width=15, command=root.quit)
exitButton.pack(pady=10)

# Hover Effect
def onEnter(e):
    # Change button color on hover
    if e.widget == startButton:
        e.widget['background'] = "#2ECC71"  
    elif e.widget == stopButton:
        e.widget['background'] = "#E74C3C"  
    elif e.widget == exitButton:
        e.widget['background'] = "#34495E" 

def onLeave(e):
    # Restore original button color
    if e.widget == startButton:
        e.widget['background'] = "green"
    elif e.widget == stopButton:
        e.widget['background'] = "red"
    elif e.widget == exitButton:
        e.widget['background'] = "black"

# Bind hover events to buttons
startButton.bind("<Enter>", onEnter)
startButton.bind("<Leave>", onLeave)

stopButton.bind("<Enter>", onEnter)
stopButton.bind("<Leave>", onLeave)

exitButton.bind("<Enter>", onEnter)
exitButton.bind("<Leave>", onLeave)

root.mainloop()
# Hand Gesture Virtual Mouse 🎯

This project enables controlling a computer mouse using hand gestures via a webcam. Using OpenCV, MediaPipe, and PyAutoGUI, users can move the cursor, click, scroll, and take screenshots through intuitive hand movements.

## 📌 Features
- **Move Cursor**: Control the mouse pointer using your index finger.
- **Left Click**: Perform a left-click using a designated gesture.
- **Right Click**: Execute a right-click with a specific hand gesture.
- **Scrolling**: Scroll up and down using finger positions.
- **Screenshot Capture**: Take a screenshot with a defined hand sign.
- **Graphical UI**: Easily start and stop tracking via a Tkinter-based interface.

## 🛠 Technologies Used
- Python
- OpenCV
- MediaPipe
- PyAutoGUI
- Pynput
- Tkinter

## 🚀 Installation & Usage
### Prerequisites
Ensure you have Python installed. Then, install the required dependencies:
```bash
pip install opencv-python mediapipe pyautogui numpy pynput tkinter
```

### Running the Application
1. Clone the repository:
   ```bash
   git clone https://github.com/Lakshay-Juneja/hand_gesture_mouse.git
   ```
2. Navigate to the project directory:
   ```bash
   cd hand_gesture_mouse
   ```
3. Run the script:
   ```bash
   python hand_gesture_mouse.py
   ```

### Controls
- Move your index finger to control the cursor.
- Specific gestures trigger left-click, right-click, scrolling, and screenshots.
- Press `Q` to exit the camera view.

## 🖥 GUI Interface
The Tkinter-based GUI allows easy control:
- **Start Button**: Begins hand gesture tracking.
- **Stop Button**: Stops tracking.
- **Exit Button**: Closes the application.

## ⚡ Notes
- Requires a webcam for hand tracking.
- Works best in well-lit conditions.
- Gesture detection may vary based on camera quality and lighting.

## 🤝 Contribution
Feel free to fork, contribute, and enhance this project! Pull requests are welcome.

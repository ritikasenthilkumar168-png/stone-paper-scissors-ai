# stone-paper-scissors-ai
# 🎮 Stone Paper Scissors AI

This is a simple fun project where I made a Stone Paper Scissors game using Python.

The game uses webcam to detect hand gestures and plays against a computer.

---

## 🧠 How it works
- Show your hand in front of webcam
- Make:
  - ✊ Stone (0 fingers)
  - ✋ Paper (4+ fingers)
  - ✌ Scissors (2 fingers)
- Press **R** to play a round
- Computer picks randomly
- Result is shown on screen

---

## 🛠 Tech used
- Python
- OpenCV
- MediaPipe

---
## main.py code:
```
# 🎮 Stone Paper Scissors AI Game
# Using OpenCV + MediaPipe + Python

import cv2
import mediapipe as mp
import random

# 📷 Start webcam
cam = cv2.VideoCapture(0)

# ✋ MediaPipe hand tracking setup
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)

mpDraw = mp.solutions.drawing_utils

# 👆 Finger tip IDs
tipIds = [4, 8, 12, 16, 20]

# 🎲 Game choices
choices = ["Stone", "Paper", "Scissors"]

computerMove = ""
result = ""

while True:

    # 📸 Read camera frame
    success, img = cam.read()

    # 🔄 Mirror image
    img = cv2.flip(img, 1)

    # 🎨 Convert BGR → RGB
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 🧠 Detect hands
    results = hands.process(imgRGB)

    lmList = []
    playerMove = None

    # ✋ If hand detected
    if results.multi_hand_landmarks:

        for handLms in results.multi_hand_landmarks:

            # 🖊 Draw hand landmarks
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            # 📍 Get landmark positions
            for id, lm in enumerate(handLms.landmark):

                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])

        fingers = []

        if len(lmList) != 0:

            # 👍 Thumb detection
            if lmList[4][1] > lmList[3][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            # ☝️ Other fingers detection
            for id in range(1, 5):

                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            totalFingers = fingers.count(1)

            # ✊ Gesture mapping
            if totalFingers == 0:
                playerMove = "Stone ✊"

            elif totalFingers == 2:
                playerMove = "Scissors ✌️"

            elif totalFingers >= 4:
                playerMove = "Paper ✋"

    # 🤖 Bot logic + result
    if computerMove != "" and playerMove is not None:

        # 😐 Draw
        if "Stone" in playerMove and computerMove == "Stone":
            result = "😐 Draw"

        elif "Paper" in playerMove and computerMove == "Paper":
            result = "😐 Draw"

        elif "Scissors" in playerMove and computerMove == "Scissors":
            result = "😐 Draw"

        # 🎉 Win condition
        elif (
            ("Stone" in playerMove and computerMove == "Scissors") or
            ("Paper" in playerMove and computerMove == "Stone") or
            ("Scissors" in playerMove and computerMove == "Paper")
        ):
            result = "🎉 You Win!"

        # 🤖 Lose condition
        else:
            result = "🤖 Computer Wins!"

    # 🧍 Display player
    displayPlayer = playerMove if playerMove else "🤚 Show Gesture"

    # 🤖 Display bot
    displayBot = computerMove if computerMove else "❓"

    # 🖥 Show text on screen
    cv2.putText(img, "👤 You: " + displayPlayer, (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.putText(img, "🤖 Bot: " + displayBot, (20, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.putText(img, "🏆 " + result, (20, 160),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.putText(img, "🔁 R = New Round | ❌ ESC = Exit", (20, 220),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # 📺 Show window
    cv2.imshow("🎮 Stone Paper Scissors AI", img)

    key = cv2.waitKey(1)

    # 🔁 New round
    if key == ord('r'):
        computerMove = random.choice(choices)
        result = ""

    # ❌ Exit game
    if key == 27:
        break

# 🧹 Cleanup
cam.release()
cv2.destroyAllWindows()
```
## test.py code:

## ▶ Run
```bash
pip install opencv-python mediapipe
python main.py

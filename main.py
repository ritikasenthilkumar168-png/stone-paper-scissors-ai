import cv2
import mediapipe as mp
import random

cam = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)

mpDraw = mp.solutions.drawing_utils

tipIds = [4, 8, 12, 16, 20]

choices = ["Stone", "Paper", "Scissors"]

computerMove = ""
result = ""

while True:

    success, img = cam.read()
    img = cv2.flip(img, 1)

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    lmList = []
    playerMove = None

    if results.multi_hand_landmarks:

        for handLms in results.multi_hand_landmarks:

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            for id, lm in enumerate(handLms.landmark):

                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])

        fingers = []

        if len(lmList) != 0:

            if lmList[4][1] > lmList[3][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            for id in range(1, 5):

                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            totalFingers = fingers.count(1)

            if totalFingers == 0:
                playerMove = "Stone ✊"

            elif totalFingers == 2:
                playerMove = "Scissors ✌️"

            elif totalFingers >= 4:
                playerMove = "Paper ✋"

    # BOT MOVE
    if computerMove != "" and playerMove is not None:

        if "Stone" in playerMove and computerMove == "Stone":
            result = "😐 Draw"

        elif "Paper" in playerMove and computerMove == "Paper":
            result = "😐 Draw"

        elif "Scissors" in playerMove and computerMove == "Scissors":
            result = "😐 Draw"

        elif (
            ("Stone" in playerMove and computerMove == "Scissors") or
            ("Paper" in playerMove and computerMove == "Stone") or
            ("Scissors" in playerMove and computerMove == "Paper")
        ):
            result = "🎉 You Win!"

        else:
            result = "🤖 Computer Wins!"

    displayPlayer = playerMove if playerMove else "🤚 Show Gesture"
    displayBot = computerMove if computerMove else "❓"

    cv2.putText(img, "👤 You: " + displayPlayer, (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.putText(img, "🤖 Bot: " + displayBot, (20, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.putText(img, "🏆 " + result, (20, 160),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.putText(img, "🔁 R = New Round | ❌ ESC = Exit", (20, 220),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow("🎮 Stone Paper Scissors AI", img)

    key = cv2.waitKey(1)

    if key == ord('r'):
        computerMove = random.choice(choices)
        result = ""

    if key == 27:
        break

cam.release()
cv2.destroyAllWindows()
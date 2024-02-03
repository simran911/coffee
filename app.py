import streamlit as st
import cv2
import os
from cvzone.HandTrackingModule import HandDetector
import uuid  # Import the uuid module

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread("Resources/Background.png")
folderPathModes = "Resources/Modes"
ListImagesModesPath = os.listdir(folderPathModes)
ListImagesModes = [cv2.imread(os.path.join(folderPathModes, imgMODEpath)) for imgMODEpath in ListImagesModesPath]

folderPathIcons = "Resources/Icons"
ListImagesIconsPath = os.listdir(folderPathIcons)
ListImagesIcons = [cv2.imread(os.path.join(folderPathIcons, imgIconspath)) for imgIconspath in ListImagesIconsPath]

modeType = 0
selection = -1
counter = 0
selectionSpeed = 9
detector = HandDetector(staticMode=False, maxHands=2)
modePositions = [(1136, 196), (1000, 384), (1136, 581)]
counterPause = 0
selectionList = [-1, -1, -1]

# Create a Streamlit column to display the image
col_image = st.image([], channels="RGB", use_column_width=True)

while True:
    success, img = cap.read()

    if not success:
        st.error("Error: Couldn't capture a frame from the webcam.")
        st.stop()

    hands, img = detector.findHands(img)

    if img is None:
        st.error("Error: Couldn't process the frame.")
        st.stop()

    imgBackground[139:139 + 480, 50:50 + 640] = img
    imgBackground[0:720, 847:1280] = ListImagesModes[modeType]

    if hands and counterPause == 0 and modeType < 3:
        hand1 = hands[0]
        fingers1 = detector.fingersUp(hand1)

        if fingers1 == [0, 1, 0, 0, 0]:
            if selection != 1:
                counter = 1
            selection = 1
        elif fingers1 == [0, 1, 1, 0, 0]:
            if selection != 2:
                counter = 1
            selection = 2
        elif fingers1 == [0, 1, 1, 1, 0]:
            if selection != 3:
                counter = 1
            selection = 3
        else:
            selection = -1
            counter = 0

        if counter > 0:
            counter += 1
            print(counter)

            cv2.ellipse(imgBackground, modePositions[selection - 1], (103, 103), 0, 0,
                        counter * selectionSpeed, (0, 225, 0), 20)

            if counter * selectionSpeed > 360:
                selectionList[modeType] = selection
                modeType += 1
                counter = 0
                selection = -1
                counterPause = 1

    if counterPause > 0:
        counterPause += 1
        if counterPause > 60:
            counterPause = 0

    if selectionList[0] != -1:
        imgBackground[636:636 + 65, 133:133 + 65] = ListImagesIcons[selectionList[0] - 1]
    if selectionList[1] != -1:
        imgBackground[636:636 + 65, 340:340 + 65] = ListImagesIcons[2 + selectionList[1]]
    if selectionList[2] != -1:
        imgBackground[636:636 + 65, 542:542 + 65] = ListImagesIcons[5 + selectionList[2]]

    imgBackground_rgb = cv2.cvtColor(imgBackground, cv2.COLOR_BGR2RGB)

    # Update the displayed image
    col_image.image(imgBackground_rgb)

    # Use a unique key for the button to avoid DuplicateWidgetID error
  #  exit_button_key = str(uuid.uuid4())  # Generate a unique key using uuid
   # if st.button("Exit", key=exit_button_key):
      #  break

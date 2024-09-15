import cv2
from PIL import Image
import random
import time
import streamlit as st

from utils import get_limits

colour_dict = {
    "purple": [255,0,157],
    "green": [0,204,0],
    "blue": [255,0,0],
}
font = cv2.FONT_HERSHEY_TRIPLEX
random_colour = key, val = random.choice(list(colour_dict.items()))
colour = str(key)
colour_bgr = val

start_time = time.time()

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Camera could not be opened.")
    exit()
    
stop_button_press = st.button("Stop")
start = st.button("Start game")
frame_placeholder = st.empty()
score = 0

while start and not stop_button_press:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to grab frame.")
        continue

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lowerLimit, upperLimit = get_limits(color=colour_bgr)
    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)
    mask_ = Image.fromarray(mask)

    bbox = mask_.getbbox()
    org = (50,50)
    frame = cv2.putText(frame, colour, org, font, 1, colour_bgr, 2, cv2.LINE_AA)

    # Calculate elapsed time
    elapsed_time = time.time() - start_time

    if bbox is not None:
        x1, y1, x2, y2 = bbox
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
        if elapsed_time >= 3:
            score = int(elapsed_time)
            st.toast(f'You found the colour, score:{score}', icon='🥶')
            break


    
    # Display the elapsed time on the frame
    
    time_text = f"Time Elapsed: {int(elapsed_time)}s/30"


    

    if cv2.waitKey(1) & 0xFF == ord('q') or stop_button_press:
        break
    elif int(elapsed_time) >= 30:
        time_text = "The time has ended, game ended, you are UNSUCESSFUL"
        # drame = cv2.putText(drame, time_text, (50,100), font, 1, (255,255,255), 2, cv2.LINE_AA)
        # cv2.imshow('frame', drame)
        
    frame = cv2.putText(frame, time_text, (50, 100), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    frame_placeholder.image(frame_rgb)
    
    # cv2.imshow('frame', frame)
    

cap.release()

col1, col2, col3 = st.columns(3)
col1.metric("Round 1", score, "1.2 °F")
# col2.metric("Round 2", "9 mph", "-8%")
# col3.metric("Round 3", "86%", "4%")

# cv2.destroyAllWindows()
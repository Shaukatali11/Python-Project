import cv2
import numpy as np


# web camera
cap = cv2.VideoCapture('video.mp4')

min_width_rect = 80  # min width rectangle
min_height_rect = 80  # min height rectangle

count_line_position = 550

# Initialize Subtractor
algo = cv2.createBackgroundSubtractorMOG()

def center_handle(x, y, w, h):
    xI = int(w/2)
    yI = int(h/2)
    cx = x + xI
    cy = y + yI
    return cx, cy

detect = []
offset = 6
counter = 0

while True:
    ret, frame1 = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 5)

    # applying on each frame
    img_sub = algo.apply(blur)
    dilat = cv2.dilate(img_sub, np.ones((5, 5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilatada = cv2.morphologyEx(dilat, cv2.MORPH_CLOSE, kernel)
    dilatada = cv2.morphologyEx(dilatada, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(dilatada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.line(frame1, (25, count_line_position), (1200, count_line_position), (255, 127, 0), 3)

    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        validate_counter = (w >= min_width_rect) and (h >= min_height_rect)
        if not validate_counter:
            continue

        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)

        center = center_handle(x, y, w, h)
        detect.append(center)
        cv2.circle(frame1, center, 4, (0, 0, 255), -1)

    for (x, y) in detect:
        if y > (count_line_position - offset) and y < (count_line_position + offset):
            counter += 1
            detect.remove((x, y))

    cv2.line(frame1, (25, count_line_position), (1200, count_line_position), (0, 127, 255), 3)
    cv2.putText(frame1, "VEHICLE COUNTER: " + str(counter), (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)

    cv2.imshow('Video Original', frame1)

    if cv2.waitKey(1) == 13:
        break

cv2.destroyAllWindows()
cap.release()


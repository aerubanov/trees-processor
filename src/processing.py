import cv2
import numpy as np
import imutils

color1 = (80, 80, 80)
color2 = (170, 250, 260)


def extract_contour(img):
    # image segmentation based on HSV colors
    hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(hsv_img, color1, color2)
    result = cv2.bitwise_and(img, img, mask=mask)

    # countours detection
    cnts = cv2.findContours(
            mask.copy(),
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_NONE,
            )

    # select countur with max area
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key = cv2.contourArea)
    return c


def select_points():
    pass


def mean_color():
    pass


def process_image(image):
    extract_contour(image)

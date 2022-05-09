import cv2
import numpy as np
import imutils
from typing import List, Tuple

#colors range for segmentation
color1 = (80, 80, 80)
color2 = (170, 250, 260)
r = 15 # cirles radius

def extract_contour(img: np.ndarray) -> np.ndarray:
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


def select_points(c: np.ndarray) -> List[Tuple[float, float]]:
    # find countur centr
    M = cv2.moments(c)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])

    points = []
    # points from bottom
    cb = c[np.where(c[:, 0, 1] > cy)]
    idx1 = np.abs(cb[:, 0, 0] - (cx-3*r)).argmin()
    idx2 = np.abs(cb[:, 0, 0] - (cx-r)).argmin()
    idx3 = np.abs(cb[:, 0, 0] - (cx+r)).argmin()
    idx4 = np.abs(cb[:, 0, 0] - (cx+3*r)).argmin()

    points.append((cb[idx1][0][0], cb[idx1][0][1]-r))
    points.append((cb[idx2][0][0], cb[idx2][0][1]-r))
    points.append((cb[idx3][0][0], cb[idx3][0][1]-r))
    points.append((cb[idx4][0][0], cb[idx4][0][1]-r))

    # points from top
    ct = c[np.where(c[:, 0, 1] < cy)]
    idx5 = np.abs(ct[:, 0, 0] - (cx-3*r)).argmin()
    idx6 = np.abs(ct[:, 0, 0] - (cx-r)).argmin()
    idx7 = np.abs(ct[:, 0, 0] - (cx+r)).argmin()
    idx8 = np.abs(ct[:, 0, 0] - (cx+3*r)).argmin()

    points.append((ct[idx5][0][0], ct[idx5][0][1]+r))
    points.append((ct[idx6][0][0], ct[idx6][0][1]+r))
    points.append((ct[idx7][0][0], ct[idx7][0][1]+r))
    points.append((ct[idx8][0][0], ct[idx8][0][1]+r))

    # points from right
    cr = c[np.where(c[:, 0, 0] > cx)]
    idx9 = np.abs(cr[:, 0, 1] - (cy-3*r)).argmin()
    idx10 = np.abs(cr[:, 0, 1] - (cy-r)).argmin()
    idx11 = np.abs(cr[:, 0, 1] - (cy+r)).argmin()
    idx12 = np.abs(cr[:, 0, 1] - (cy+3*r)).argmin()

    points.append((cr[idx9][0][0]-r, cr[idx9][0][1]))
    points.append((cr[idx10][0][0]-r, cr[idx10][0][1]))
    points.append((cr[idx11][0][0]-r, cr[idx11][0][1]))
    points.append(cr[idx12][0][0]-r, cr[idx12][0][1]))

    # points from left
    cl = c[np.where(c[:, 0, 0] < cx)]
    idx13 = np.abs(cl[:, 0, 1] - (cy-3*r)).argmin()
    idx14 = np.abs(cl[:, 0, 1] - (cy-r)).argmin()
    idx15 = np.abs(cl[:, 0, 1] - (cy+r)).argmin()
    idx16 = np.abs(cl[:, 0, 1] - (cy+3*r)).argmin()

    points.append((cl[idx13][0][0]+r, cl[idx13][0][1]))
    points.append((cl[idx14][0][0]+r, cl[idx14][0][1]))
    points.append((cl[idx15][0][0]+r, cl[idx15][0][1]))
    points.append((cl[idx16][0][0]+r, cl[idx16][0][1]))
    
    return points


def mean_color(points: List[Tuple[float, float]]) - > List[np.ndarray]:
    res = []
    for p in points:
        mask = np.zeros_like(img_copy)
        mask = cv2.circle(mask, p, r, (255,255,255), -1)
        result = cv2.cvtColor(img_copy.copy(), cv2.COLOR_BGR2BGRA)
        result[:, :, 3] = mask[:,:,0]
        res.append(result[np.where(result[:,:, 3] > 0)].mean(axis=0))
    return res


def process_image(image: np.ndarray):
    cnt = extract_contour(image)
    points = select_points(cnt)
    colors = mean_color(points)

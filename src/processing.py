import cv2
import numpy as np
import imutils
from typing import List, Tuple

from src.plots import plot_result
from src.constants import color1, color2, r


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


def calc_min_distance(point: Tuple[float, float], cnt: np.ndarray) -> float:
    x, y = point
    x_c, y_c = cnt[:, 0, 0], cnt[:, 0, 1]
    distancies = np.sqrt(np.power(x - x_c, 2) + np.power(y - y_c, 2))
    return np.min(distancies)


def check_point(point: Tuple[float, float], cnt: np.ndarray, point_type: str) -> Tuple[float, float]:
    while(calc_min_distance(point, cnt) < r):
        if point_type == "top":
            point = (point[0], point[1] + 1)
        elif point_type == "left":
            point = (point[0] +1, point[1])
        elif point_type == "right":
            point = (point[0] - 1, point[1])
        elif point_type == "bottom":
            point = (point[0], point[1] - 1)
    return point


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

    points.append(check_point((cb[idx1][0][0], cb[idx1][0][1]-r), cb, "bottom"))
    points.append(check_point((cb[idx2][0][0], cb[idx2][0][1]-r), cb, "bottom"))
    points.append(check_point((cb[idx3][0][0], cb[idx3][0][1]-r), cb, "bottom"))
    points.append(check_point((cb[idx4][0][0], cb[idx4][0][1]-r), cb, "bottom"))

    # points from top
    ct = c[np.where(c[:, 0, 1] < cy)]
    idx5 = np.abs(ct[:, 0, 0] - (cx-3*r)).argmin()
    idx6 = np.abs(ct[:, 0, 0] - (cx-r)).argmin()
    idx7 = np.abs(ct[:, 0, 0] - (cx+r)).argmin()
    idx8 = np.abs(ct[:, 0, 0] - (cx+3*r)).argmin()

    points.append(check_point((ct[idx5][0][0], ct[idx5][0][1]+r), ct, "top"))
    points.append(check_point((ct[idx6][0][0], ct[idx6][0][1]+r), ct, "top"))
    points.append(check_point((ct[idx7][0][0], ct[idx7][0][1]+r), ct, "top"))
    points.append(check_point((ct[idx8][0][0], ct[idx8][0][1]+r), ct, "top"))

    # points from right
    cr = c[np.where(c[:, 0, 0] > cx)]
    idx9 = np.abs(cr[:, 0, 1] - (cy-3*r)).argmin()
    idx10 = np.abs(cr[:, 0, 1] - (cy-r)).argmin()
    idx11 = np.abs(cr[:, 0, 1] - (cy+r)).argmin()
    idx12 = np.abs(cr[:, 0, 1] - (cy+3*r)).argmin()

    points.append(check_point((cr[idx9][0][0]-r, cr[idx9][0][1]), cr, "right"))
    points.append(check_point((cr[idx10][0][0]-r, cr[idx10][0][1]), cr, "right"))
    points.append(check_point((cr[idx11][0][0]-r, cr[idx11][0][1]), cr, "right"))
    points.append(check_point((cr[idx12][0][0]-r, cr[idx12][0][1]), cr, "right"))

    # points from left
    cl = c[np.where(c[:, 0, 0] < cx)]
    idx13 = np.abs(cl[:, 0, 1] - (cy-3*r)).argmin()
    idx14 = np.abs(cl[:, 0, 1] - (cy-r)).argmin()
    idx15 = np.abs(cl[:, 0, 1] - (cy+r)).argmin()
    idx16 = np.abs(cl[:, 0, 1] - (cy+3*r)).argmin()

    points.append(check_point((cl[idx13][0][0]+r, cl[idx13][0][1]), cl, "left"))
    points.append(check_point((cl[idx14][0][0]+r, cl[idx14][0][1]), cl, "left"))
    points.append(check_point((cl[idx15][0][0]+r, cl[idx15][0][1]), cl, "left"))
    points.append(check_point((cl[idx16][0][0]+r, cl[idx16][0][1]), cl, "left"))
    
    return points


def mean_color(points: List[Tuple[float, float]], img: np.ndarray) -> List[np.ndarray]:
    res = []
    for p in points:
        mask = np.zeros_like(img)
        mask = cv2.circle(mask, p, r, (255,255,255), -1)
        result = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2BGRA)
        result[:, :, 3] = mask[:,:,0]
        res.append(result[np.where(result[:,:, 3] > 0)].mean(axis=0))
    return res


def process_image(image: np.ndarray, plot=None):
    cnt = extract_contour(image)
    points = select_points(cnt)
    colors = mean_color(points, image)
    if plot:
        plot_result(image, cnt, points, r, plot)
    return colors

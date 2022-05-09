import cv2
import numpy as np
from typing import List, Tuple


def plot_result(
        img: np.ndarray,
        conture: np.ndarray,
        points: List[Tuple[float, float]],
        radius: int):
    img = cv2.drawContours(img, conture, -1, 255, 3)
    for point in points:
        cv2.circle(img, point, radius, (255, 0, 0))
    cv2.imshow("", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

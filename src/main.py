import cv2
import sys

from src.processing import process_image


def main(filename: str):
    img = cv2.imread(filename)
    img = cv2.resize(img, (1280, 1024))
    print(process_image(img, plot=True))


if __name__ == "__main__":
    main(sys.argv[1])

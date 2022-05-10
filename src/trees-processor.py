import cv2
import argparse
import os
import tarfile
import numpy as np

from src.processing import process_image

parser = argparse.ArgumentParser()
parser.add_argument(
        "filename",
        help="name of file to process", type=str)
parser.add_argument(
        "--save_result", 
        help="save processed image in specified file", type=str)
parser.add_argument(
        "--rar", "-r",
        help="process all images in archive (specified as filename argument)",
        action="store_true")


def main(filename: str, save_result=None):
    img = cv2.imread(filename)
    img = cv2.resize(img, (1280, 1024))
    print(process_image(img, plot=save_result))

def get_np_array_from_tar_object(tar_extractfl):
     '''converts a buffer from a tar file in np.array'''
     return np.asarray(
        bytearray(tar_extractfl.read())
        , dtype=np.uint8)


def process_rar(filename: str, save_result=None):
    tar = tarfile.open(filename, 'r|*')
    for file in tar:
        data = tar.extractfile(file)
        if data:
            img = cv2.imdecode(
                    get_np_array_from_tar_object(data),
                    cv2.IMREAD_COLOR,
                    )
            img = cv2.resize(img, (1280, 1024))
            out_file = None
            if save_result:
                out_file = os.path.join(save_result, file.name.split('/')[-1])
            print(process_image(img, plot=out_file))


if __name__ == "__main__":
    args = parser.parse_args()
    if args.rar:
        process_rar(args.filename, args.save_result)
    else:
        main(args.filename, args.save_result)

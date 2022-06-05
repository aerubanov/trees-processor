from typing import List
import numpy as np

def print_results(filenames: List[str], results: List[np.ndarray]):
    print("filename | south_ 1 | south_2 | south_3 | south_4 | nort_1 | nort_2 | nort_3 | nort_4 | east_1 | east_2 | east_3 | east_4 | west_1 | west_2 | west_3 | west_4")
    for filename, row in zip(filenames, results):
        output = filename + " " + " ".join([str([i for i in item[:3]]) for item in row])
        print(output)

# Trees processor
## Installation
You need to have installed python 3.9 to work with this project.
1. Create a virtual environment: </br>
    ```python3 -m venv env```
2. Activate virtual environment: </br>
    ```source env/bin/activate```
3. Install trees-processor and dependencies: </br>
    ```pip install git+https://github.com/aerubanov/trees-processor```
## Usage
### positional arguments:
    filename              name of file to process

### optional arguments:
    -h, --help            show this help message and exit <\br>
    --save_result SAVE_RESULT <\br>
                          save processed image in specified file <\br>
    --rar, -r             process all images in archive (specified as filename argument) <\br>
### examples
- ```python -m trees_processor image.tif``` - process image
- ```python -m trees_processor image.tif --save_result output.tif``` - process image and save image with countur and selected regions in ```output.tif```
- ```python -m trees_processor -r images.tar --save_result output``` - process all images in archive and save images with counturs and selected regions in ```output``` folder (will be created if not exist).
## Results
Input image:

![img](https://github.com/aerubanov/trees-processor/blob/main/examples/input.jpg)

Extracted contur and selected regions:

![img](https://github.com/aerubanov/trees-processor/blob/main/examples/output.jpg)

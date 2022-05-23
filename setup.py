# -*- coding: utf-8 -*-
from setuptools import setup
import os

here = os.path.abspath(os.path.dirname(__file__))

packages = ['trees_processor']

requires = [
    "numpy==1.21",
    "matplotlib==3.5.1",
    "opencv-python==4.5.5.64",
    "imutils==0.5.4",
]
test_requirements = []

about={}
with open(os.path.join(here, "src", "__version__.py")) as f:
    exec(f.read(), about)

with open('README.md') as f:
    readme = f.read()

history = ''

setup(
    name=about['__title__'],
    version=about['__version__'],
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    author=about['__author__'],
    author_email=about['__author_email__'],
    packages=packages,
    package_dir={'trees_processor': 'src'},
    include_package_data=True,
    install_requires=requires,
    license=about['__license__'],
    zip_safe=False,
    tests_require=test_requirements,
    project_urls={
        'Source': 'https://github.com/aerubanov/trees-processor',
    },
)

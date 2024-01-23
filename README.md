# metpetools

This repo contain tools for Metpet project
For use in your local machine see this instructions:

1. Prepare Python environment with below requirement
2. Download python file "shp2html.py" or Jupyter notebook version "shp2html.ipynb"
3. Open python file and update !!! User inputs !!! with your files and your project


## shp2html 
Contributors: @albdag, @gianfrancodp

This script converts a shapefile with polygons to an HTML image map.
see README.md for more info and usage

Python virtual env requirements: python 3.8.18, gdal 3.8.3

CREDITS:

- Python libraries used | Copyright 2001-2024, Python Software Foundation.
- GDAL/OGR libraries used | Copyright 1998-2024 Frank Warmerdam, Even Rouault, and others

Javascript libraries used:
- Image Map Resizer (imageMapResizer.min.js ) - v1.0.10 - 2019-04-10 | Copyright: (c) 2019 David J. Bradshaw - dave@bradshaw.net | License: MIT
- jQuery v3.5.1 | (c) JS Foundation and other contributors | jquery.org/license */


## Python environment

### Python environment
Requirement for python environment

1. Install native GDAL
    On Debian Linux

    `sudo apt-get install gdal-bin`

    On macOS with homebrew

    `brew install gdal`

2. Create Python virtual environment 

    `virtualenv metpetools` 

3. Activate virtual environment

    `source ./bin/activate`

4. Install python dependencies

    `pip install GDAL`

### Additonal for Jupyter notebook
in terminal with virtual environment activated run: `pip install jupyter`
    



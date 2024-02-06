# metpetools

This repo contain tools for Metpet project
For use in your local machine see this instructions:

## Using on a Qgis desktop as custom script

- See detalied [instruction](Qgis%20processing%20script/How%20to%20use.md)

<!-- ## Using on ArGIS desktop as Toolbox -->

<!-- -  -->


## Using in a python environment or Jupyter notebook

1. Prepare Python environment with below requirement
2. Download python file "shp2html.py" or Jupyter notebook version "shp2html.ipynb"
3. Open python file and update !!! User inputs !!! with your files and your project

### Python environment

#### Python environment
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
    



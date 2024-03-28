# -*- coding: utf-8 -*-

#==> CHANGE INPUT data below befor run! ==<


# !!! User inputs !!!
NAME = 'PAL22' # name of the project, used to name the output files


# Change these ABSOLUTE paths with the paths to your shapefile and raster
SHAPEFILE = r'C:\Users\Utente\Documents\repository\metpetools\metpetools\sample_data\PAL\PAL22\PAL22.shp'
RASTER = r'C:\Users\Utente\Documents\repository\metpetools\metpetools\sample_data\PAL\PAL22\PAL22.jpg'

# path where the output files will be saved 
# Make sure that the path exists and that you have write permissions
OUTDIR = r'C:\Users\Utente\Documents\repository\metpetools\metpetools\sample_data\PAL'


ORIGINCOORD = 'top-left' # Not implemented
# !!! End of user inputs !!!



"""
authors: @albdag, @gianfrancodp

This script converts a shapefile with polygons to an HTML image map.
see README.md for more info and usage

Python virtual env requirements: python 3.8.18, gdal 3.8.3

CREDITS:

for Python libraries used:
Copyright 2001-2024, Python Software Foundation.

for GDAL/OGR libraries used:
Copyright 1998-2024 Frank Warmerdam, Even Rouault, and others

Javascript libraries used:

Image Map Resizer (imageMapResizer.min.js ) - v1.0.10 - 2019-04-10
Desc: Resize HTML imageMap to scaled image.
Copyright: (c) 2019 David J. Bradshaw - dave@bradshaw.net
License: MIT

jQuery v3.5.1
(c) JS Foundation and other contributors
jquery.org/license


"""
import json
import os

from zipfile import ZipFile
from osgeo import ogr
import ntpath
import shutil

#####################################################################
#####################################################################

def fix_coords(coords, origin = ORIGINCOORD):
    '''
    Transform floating coordinates to integers and fixes their values based on
    origin. Removes the last couple if it coincides with the first.

    Parameters
    ----------
    coords : list
        List of (x, y) tuples.
    origin : str, optional
        Origin of the coordinates. Only the 'top-left' origin is currently
        available. The default is 'top-left'.

    Raises
    ------
    NotImplementedError
        Only 'top-left' origin is implemented.

    Returns
    -------
    fixed : list
        List of fixed (x, y) tuples.

    '''
    # Remove duplicated couples
    if coords[0] == coords[-1]:
        del coords[-1] 

    if origin == 'top-left':
        fixed = [(abs(round(x)), abs(round(y))) for x, y in coords]
        return fixed
    else:
        raise NotImplementedError(f"Can't convert coords with origin {origin}")


# Set a global variable that tracks the occurrence of inner rings in polygons
INRINGS = 0

# Set a global variable that holds the list of vertices of each polygon
polygons_vert = []
# set a global variable that holds the list of attributes of each polygon
attributes_list = []

#Get the name of rasterfile
RASTER_NAME = ntpath.basename(RASTER)

# Open the shapefile
shapefile = ogr.Open(SHAPEFILE)

# Get the layer
layer = shapefile.GetLayer()




# Iterate over the features in the layer
for feature in layer:
    attributes = feature.items() # get attributes
    attributes_list.append(attributes) # append attributes to list
    geometry = feature.geometry()

    # Track inner rings
    n_rings = geometry.GetGeometryCount()
    if n_rings > 1:
        INRINGS += n_rings-1

    # We only get vertices of outer ring (= first element of GetGeometryRef)
    vertices = geometry.GetGeometryRef(0).GetPoints()
    polygons_vert.append(fix_coords(vertices))


# Send warning if inner rings (holes) have been detected
if INRINGS:
    print(f'Warning: {INRINGS} holes detected. Not handled.')

    # HTML header and footer part

HTMLHEAD = '<!DOCTYPE html>\n<html>\n<head>\n\t<title>Image Map</title>\n'\
    '\t<meta charset="utf-8">\n\t<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>\n'\
    '\t<script src="https://cdnjs.cloudflare.com/ajax/libs/image-map-resizer/1.0.10/js/imageMapResizer.min.js"></script>\n'\
        '</head>\n<body>\n'   
HTMLFOOT = '<script>\n\t$(document).ready(function() {\n\t $(\'map\').imageMapResize();\n\t}); \n</script>\n</body>\n</html>'    

    
image_block = f'<img src="{RASTER_NAME}" usemap="#image-map" '\
               'style="width: 100%; height: auto;">\n'

HTMLPOLYGONS = f'<map name="image-map">\n'

for a, p in zip(attributes_list, polygons_vert):
    coordstr = str(p)[1:-1].replace('(','').replace(')','').replace(' ','')
    id_ = a['OBJECTID']
    line = f'\t<area target="_blank" id="imgzone{id_}" '\
           f'alt="Element #{id_}" title="Element #{id_}" '\
           f'coords="{coordstr}" shape="poly">\n'
    HTMLPOLYGONS += line
HTMLPOLYGONS += '</map>\n'

#preparing Path and files
html_path = ntpath.join(OUTDIR,f'{NAME}.html')
AttributeTable_path = ntpath.join(OUTDIR, f'{NAME}.json')
outputfile_path = ntpath.join(OUTDIR,f'{NAME}.zip')

# Create temporary raster file
raster_path = os.path.join(OUTDIR, RASTER_NAME)
shutil.copy(RASTER, raster_path)

# Save as file
with open(html_path, 'w', encoding="utf-8") as out_file:
    out_file.write(HTMLHEAD)
    out_file.write(image_block)
    out_file.write('\n')
    out_file.write(HTMLPOLYGONS)
    out_file.write(HTMLFOOT)

with open(AttributeTable_path, 'w', encoding="utf-8") as f:
    json.dump(attributes_list, f)


# Create zip file
with ZipFile(outputfile_path, 'w') as outzip:
    outzip.write(RASTER, ntpath.basename(raster_path))
    outzip.write(html_path, ntpath.basename(html_path))
    outzip.write(AttributeTable_path, ntpath.basename(AttributeTable_path))

# Remove temp files
os.remove(html_path)
os.remove(AttributeTable_path)
os.remove(raster_path)

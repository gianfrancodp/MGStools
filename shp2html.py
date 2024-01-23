# -*- coding: utf-8 -*-
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

/*! Image Map Resizer (imageMapResizer.min.js ) - v1.0.10 - 2019-04-10
 *  Desc: Resize HTML imageMap to scaled image.
 *  Copyright: (c) 2019 David J. Bradshaw - dave@bradshaw.net
 *  License: MIT
 */

 /*! jQuery v3.5.1 | (c) JS Foundation and other contributors | jquery.org/license */


"""
import json
import os
from zipfile import ZipFile
from osgeo import ogr

# !!! User inputs !!!
# Change this paths with the path to your shapefile and raster
shapefile_path = r'sample_data/TOR1/TOR1.shp'
raster_path = r'sample_data/TOR1/TOR1.jpg'
project_name = 'TEST' # name of the project, used to name the output files
# !!! End of user inputs !!!

#####################################################################
# Use True to export as single page HTML, script add header and footer tags
# to be able to open the file in a browser
# export_as_html_single_page = True # REMOVED, now always exported


# Use True to export the attribute table as json file separated from the html
# If false the attribute table will be not exported.
# export_attribute_table_to_json = True # REMOVED, now always exported

#####################################################################

def fix_coords(coords, origin='top-left'):
    '''
    Transform floating coordinates to integers and fixes their values based on
    origin. Removes the last couple, which coincides with the first.

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
    del coords[-1] # remove last coord

    if origin == 'top-left':
        fixed = [(int(round(x, 0)), int(round(abs(y), 0))) for x, y in coords]
        return fixed
    else:
        raise NotImplementedError(f"Can't convert coords with origin {origin}")


# Set a global variable that tracks the occurrence of inner rings in polygons
inner_rings_detected = 0

# Set a global variable that holds the list of vertices of each polygon
polygons_vert = []
# set a global variable that holds the list of attributes of each polygon
attributes_list = []

# Open the shapefile
shapefile = ogr.Open(shapefile_path)

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
        inner_rings_detected += n_rings-1

    # We only get vertices of outer ring (= first element of GetGeometryRef)
    vertices = geometry.GetGeometryRef(0).GetPoints()
    polygons_vert.append(fix_coords(vertices))


# Send warning if inner rings (holes) have been detected
if inner_rings_detected:
    print(f'Warning: {inner_rings_detected} holes detected. Not handled.')


    # Generate HTML code wiht header and footer tags
# if export_as_html_single_page == True: # REMOVED, now always exported
html_head = '<!DOCTYPE html>\n<html>\n<head>\n\t<title>Image Map</title>\n'\
    '\t<meta charset="utf-8">\n\t<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>\n'\
    '\t<script src="https://cdnjs.cloudflare.com/ajax/libs/image-map-resizer/1.0.10/js/imageMapResizer.min.js"></script>\n'\
        '</head>\n<body>\n'   
html_foot = '<script>\n\t$(document).ready(function() {\n\t $(\'map\').imageMapResize();\n\t}); \n</script>\n</body>\n</html>'    

# Generate HTML code wihtout header and footer tags # REMOVED, now always exported
# else:
#     html_head = ''
#     html_foot = ''
#    print('Warning: HTML file will not be a single page. '\
   
    
image_block = f'<img src="{raster_path}" usemap="#image-map" '\
               'style="width: 100%; height: auto;">\n'

polygons_block = '<map name="image-map">\n'
for n, p in enumerate(polygons_vert, start=1):
    coords_str = str(p)[1:-1].replace('(','').replace(')','').replace(' ','')
    line = f'\t<area target="_blank" id="imgzone{n}" '\
           f'alt="Element #{n}" title="Element #{n}" '\
           f'coords="{coords_str}" shape="poly">\n'
    polygons_block += line
polygons_block += '</map>\n'


# Save as file
with open(f'{project_name}.html', 'w') as out_file:
    out_file.write(html_head)
    out_file.write(image_block)
    out_file.write('\n')
    out_file.write(polygons_block)
    out_file.write(html_foot)


# if export_attribute_table_to_json == True:
with open(f'{project_name}.json', 'w') as f:
    json.dump(attributes_list, f)

# Required inputs
# raster_path = r'sample_data/TOR1/TOR1.jpg'
html_path = rf'{project_name}.html'
# js_path = r'imageMapResizer.min.js'
AttributeTable_path = rf'{project_name}.json'

# Create zip file
with ZipFile(rf'{project_name}.zip', 'w') as outzip:
    outzip.write(raster_path)
    outzip.write(html_path)
    # outzip.write(js_path)
    outzip.write(AttributeTable_path)

# Remove files
    os.remove(html_path)
    os.remove(AttributeTable_path)

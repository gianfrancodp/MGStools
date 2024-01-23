"""

authors: @albdag

This script converts a shapefile with polygons to an HTML image map within
the ArcGIS Desktop environment. 
NOTE: This script is not meant to be executed as is, but rather embedded within an ArcGIS toolbox! (see 'MetPetTools.tbx').
See also: https://desktop.arcgis.com/en/arcmap/latest/analyze/sharing-workflows/embedding-scripts-and-password-protecting-tools.htm

REQUIREMENTS:

ArcGIS Python env requirements: python 2.7.14

This script must be embedded in ArcGIS. It requires a licensed version
of ArcGIS Desktop (ArcMap) version >= 10.4 in order to work.

CREDITS:

for Python libraries used:
Copyright 2001-2024, Python Software Foundation.

for arcpy libraries used:
Copyright 1995-2021, Esri.


"""

import json
import os
import io
import shutil
from zipfile import ZipFile
import arcpy


def fix_coords(coords, origin='top-left'):
    '''
    Transform floating coordinates to integers and fixes their values based on
    origin. Removes the last couple if it coincides with the first.

    Parameters
    ----------
    coords : list
        List of (x, y) couples.
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
    # Remove duplicated xy couple 
    if coords[0] == coords[-1]:
        del coords[-1] 

    if origin == 'top-left':
        fixed = [(int(round(abs(x))), int(round(abs(y)))) for x, y in coords]
        return fixed
    else:
        raise NotImplementedError("Can't convert coords with origin {0}".format(origin))


def get_layer_fullpath(layer):
    '''
    Retrieve fullpath of layer when loaded from ArcGIS table of content.
    '''
    desc = arcpy.Describe(layer)
    fullpath = os.path.join(desc.path, desc.name)
    return fullpath


# !!! User inputs !!!
# They can be set from the ArcGIS tool interface
SHAPEFILE = arcpy.GetParameterAsText(0)
RASTER = get_layer_fullpath(arcpy.GetParameterAsText(1))
RASTER_NAME = os.path.split(RASTER)[1]
NAME = arcpy.GetParameterAsText(2)
OUTDIR = arcpy.GetParameterAsText(3)
# !!! End of user inputs !!!

# Define workspace
if not os.path.exists(OUTDIR):
    os.mkdir(OUTDIR)
arcpy.env.workspace = OUTDIR


# Set a global variable that tracks the occurrence of inner rings in polygons
INRINGS = 0

# Set a global variable that holds the list of vertices of each polygon
polygons_vert = []
# set a global variable that holds the list of attributes of each polygon
attributes_list = []


# Export shapefile features to temporary JSON file
features_path = os.path.join(OUTDIR, 'features.json')
arcpy.conversion.FeaturesToJSON(SHAPEFILE, features_path)

# Parse the exported JSON file
f = io.open(features_path, 'r')
layer = json.load(f)['features']
f.close()

# Iterate over the features in the layer
for feature in layer:
    attributes = feature['attributes'] # get attributes
    attributes_list.append(attributes) # append attributes to list

    geometry = feature['geometry']['rings']     # get geometry
    INRINGS += len(geometry)-1                  # track inner rings
    vertices = geometry[0]                      # get vertices from outer ring
    polygons_vert.append(fix_coords(vertices))  # append vertices to list

# Send warning if inner rings (holes) have been detected
if INRINGS:
    print('Warning: %d holes detected. Not handled.' %(INRINGS))

# HTML header and footer part
HTMLHEAD = u'<!DOCTYPE html>\n<html>\n<head>\n\t<title>Image Map</title>\n'\
    u'\t<meta charset="utf-8">\n\t<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>\n'\
    u'\t<script src="https://cdnjs.cloudflare.com/ajax/libs/image-map-resizer/1.0.10/js/imageMapResizer.min.js"></script>\n'\
        u'</head>\n<body>\n'   
HTMLFOOT = u'<script>\n\t$(document).ready(function() {\n\t $(\'map\').imageMapResize();\n\t}); \n</script>\n</body>\n</html>'    
    
image_block = u'<img src="{0}" usemap="#image-map" style="width: 100%; height: auto;">\n'.format(RASTER_NAME)

HTMLPOLYGONS = u'<map name="image-map">\n'
for n, p in enumerate(polygons_vert, start=1):
    COORDSSTR = str(p)[1:-1].replace('(','').replace(')','').replace(' ','')
    line = u'\t<area target="_blank" id="imgzone{0}" alt="Element #{0}" title="Element #{0}" coords="{1}" shape="poly">\n'.format(n, COORDSSTR)
    HTMLPOLYGONS += line
HTMLPOLYGONS += u'</map>\n'

html_path = os.path.join(OUTDIR, r'{0}.html'.format(NAME))
AttributeTable_path = os.path.join(OUTDIR, r'{0}.json'.format(NAME))

# Create temporary image map html file
with io.open(html_path, 'w', encoding="utf-8") as out_file:
    out_file.write(HTMLHEAD)
    out_file.write(image_block)
    out_file.write(u'\n')
    out_file.write(HTMLPOLYGONS)
    out_file.write(HTMLFOOT)

# Create temporary attribute table JSON file
with io.open(AttributeTable_path, 'w', encoding="utf-8") as f:
    text = json.dumps(unicode(attributes_list), ensure_ascii=False)
    f.write(text)

# Create temporary raster file
raster_path = os.path.join(OUTDIR, RASTER_NAME)
shutil.copy(RASTER, raster_path)

# Create zip file
zipfile_path = os.path.join(OUTDIR, r'{0}.zip'.format(NAME))
with ZipFile(zipfile_path, 'w') as outzip:
    outzip.write(raster_path, os.path.basename(raster_path))
    outzip.write(html_path, os.path.basename(html_path))
    outzip.write(AttributeTable_path, os.path.basename(AttributeTable_path))

# Remove temporary files
os.remove(features_path)
os.remove(raster_path)
os.remove(html_path)
os.remove(AttributeTable_path)


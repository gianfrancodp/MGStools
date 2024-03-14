"""

authors: @albdag

This script converts a shapefile with polygons to an HTML image map within
the ArcGIS Desktop environment. 
NOTE: This script is not meant to be executed as is, but rather embedded within an ArcGIS toolbox! (see 'Metpetools_ArcMap.tbx').
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
import arcpy
import json
import os
import shutil
import matplotlib
import numpy as np


def unique_values(layer, field):
    '''
    Iterate through layer's instances and returns all unique entries in a specific field

    Parameters
    ----------
    layer : ESRI Feature Layer
        Input layer.
    field : ArcGIS Field parameter
        Field of interest.

    Returns
    -------
    A set containing the unique entries.
    '''
    
    with arcpy.da.SearchCursor(layer, field.value) as cursor:
        return sorted({row[0] for row in cursor})

# !!! User inputs !!!
# They can be set from the ArcGIS tool interface
IN_LYR = arcpy.GetParameter(0)
MINERAL_FIELD = arcpy.GetParameter(1)
IN_RST = arcpy.GetParameterAsText(2)
OUT_DIR = arcpy.GetParameterAsText(3)
# !!! End of user inputs !!!

# Set environment settings
arcpy.env.extent = IN_RST
arcpy.env.overwriteOutput = True

# Set map document as current
MXD = arcpy.mapping.MapDocument('CURRENT')

# Create a temporary folder
TEMP_FLD = os.path.join(OUT_DIR, 'temp')
if not os.path.exists(TEMP_FLD):
    os.mkdir(TEMP_FLD)

# Store layer colormap
COLORMAP = dict()
LYR = arcpy.mapping.ListLayers(MXD, wildcard=IN_LYR)[0]
symbology = json.loads(LYR._arc_object.getsymbology())
for info in symbology['renderer']['uniqueValueInfos']:
    name = info['value']
    rgba = info['symbol']['color'] 
    rgba[3] = 128 # set transparency to 50%
    COLORMAP[name] = rgba


for unq in unique_values(IN_LYR, MINERAL_FIELD):

    # Select mineral class using mineral name in SQL query
    query = "\"{0}\" = '{1}'".format(MINERAL_FIELD, unq)
    temp_lyr = '{0}.shp'.format(unq)
    arcpy.MakeFeatureLayer_management(IN_LYR, temp_lyr, where_clause=query)

    # Convert layer to raster (.tif)
    temp_rst = os.path.join(TEMP_FLD, '{0}.tif'.format(unq))
    arcpy.FeatureToRaster_conversion(temp_lyr, MINERAL_FIELD, temp_rst, cell_size=1)

    # Convert raster to Numpy array
    temp_arr = arcpy.RasterToNumPyArray(temp_rst).astype('uint8')
    
    # Create RGB(A) array
    r, c = temp_arr.shape
    img = np.zeros((r, c, 4), dtype='uint8')
    img[temp_arr==0] = [255, 255, 255, 0]
    img[temp_arr==1] = COLORMAP[unq]
    
    # Save image with matplotlib
    out_png = os.path.join(OUT_DIR, '{0}.png'.format(unq))
    matplotlib.image.imsave(out_png, img)


# Remove temporary directory and all of its content
shutil.rmtree(TEMP_FLD)


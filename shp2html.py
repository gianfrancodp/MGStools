# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 08:17:34 2024

@author: albdag

requirements: python 3.8.18, gdal 3.8.3
"""

from osgeo import ogr


# !!! User inputs !!!
shapefile_path = r'sample_data/TOR1/TOR1.shp'
raster_path = r'sample_data/TOR1/TOR1.jpg'

# Use True to export as single page HTML, script add header and footer tags
# to be able to open the file in a browser
export_as_html_single_page = True 

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

# Open the shapefile
shapefile = ogr.Open(shapefile_path)

# Get the layer
layer = shapefile.GetLayer()

# Iterate over the features in the layer
for feature in layer:
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
if export_as_html_single_page == True:
    html_head = '<!DOCTYPE html>\n<html>\n<head>\n\t<title>Image Map</title>\n'\
        '\t<meta charset="utf-8">\n</head>\n<body>\n'
    html_foot = '</body>\n</html>'    
# Generate HTML code wihtout header and footer tags
else:
    html_head = ''
    html_foot = ''
   
    
image_block = f'<img src="{raster_path}" usemap="#image-map" '\
               'style="width: 100%; height: auto;">\n'

polygons_block = '<map name="image-map">\n'
for n, p in enumerate(polygons_vert, start=1):
    coords_str = str(p)[1:-1].replace('(','').replace(')','').replace(' ','')
    line = f'\t<area target="_blank" id="imgzone{n}" '\
           f'alt="Element #{n}" title="Element #{n}" '\
           f'coords="{coords_str}" shape="poly">\n'
    polygons_block += line
polygons_block += '</map>'


# Save as file


with open('.\HTML_out.html', 'w') as out_file:
    out_file.write(html_head)
    out_file.write(image_block)
    out_file.write('\n')
    out_file.write(polygons_block)
    out_file.write(html_foot)




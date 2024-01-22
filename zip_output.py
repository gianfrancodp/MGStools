# -*- coding: utf-8 -*-
"""

authors: @albdag

This script generates a compressed (.zip) folder that includes the original raster file, the 
converted HTML output and the Javascript ImageMapResizer. 

Python virtual env requirements: python 3.8.18

"""

from zipfile import ZipFile

# Required inputs
raster_path = r'sample_data/TOR1/TOR1.jpg'
html_path = r'HTML_out-test.html'
js_path = r'imageMapResizer.min.js'

# Create zip file
with ZipFile(r'zipfile_out-test.zip', 'w') as outzip:
    outzip.write(raster_path)
    outzip.write(html_path)
    outzip.write(js_path)



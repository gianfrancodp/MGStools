# Metpetools

After various decades of digital transition, publishing and spreading of geo-data actually is exclusively with Web and internet channels. Everybody know the effective communication and easy to access to the data and maps using web or mobile devices. The last decade of web-development and expecially web-gis technology development provided a very number of projects and libraries (OpenLayers, LeafLet etc..) for a better "production process" of geo-data publication on the web. Today especially in Opensource community we have a several front-end project that offer possibility to develop effective interface for data publishing on the web and mobile devices.

Geoscientists have a multitude of digital data across scales, across geometric types, across dataset types and more, such as Geo-graphic data, Geo-spatial data and Microscale-data.

**Metpetools** is a set of Python tools to create web-viewers of geological data provided from different type of analysis. A frist version of this project provided a multiscale web publication process for the site of Palmi shear zone  (Italy). A complex web-GIS viewer that contain different type of data at different scale: from microstructural data of thin section provided in a LIS-viewer (Litologic Information Sistem), a 3D model viewer of outcrops.
___

Actual version proposed is used in:

Di Pietro, G., D’Agostino, A., Ortolano, G., Fazio, E., Visalli, R., Musumeci, R.E., Cirrincione, R., 2024. Web publication of multiscale geological data, methodology, and processes. [DOI: 10.13140/RG.2.2.34955.50726](https://doi.org/10.13140/RG.2.2.34955.50726) (keynote available)

---

### Table of contents

1. Making a Web viewer of a "Thin section" (LIS) from data
2. *Web viewer of a 3D model from KMZ file* (UNDER DEVELOPMENT)
3. *Pakaging all into a web-gis framwork* (UNDER DEVELOPMENT)

---

# Making a Web viewer of a "Thin section" (LIS) from data

The file [`lis_functions.py`](LIS/lis_functions.py) contain the Python scripts and function to make a webviewe of a thin section and grain poligons from scratch using GDAL, Beautiful Soup in a Python environment.

Tu use in your enviroment you can use the [`lis_functions.py`](LIS/lis_functions.py) file as importing function, but please refer to [`requirements.txt`](LIS/requirements.txt) for a proper python environment.

Also described in the [notebook example](LIS/LIS_of_a_thinSection.ipynb), the process is a sequence of these phases:

1. Import files
2. Create Raster tiles using Gdal
3. Convert SHP to Geojson using GDAL ogr2ogr
4. Add GeoJson overlay to web-viewer
5. Add pop-up feature to the map
6. Add rosediagram and legend feature to the webpage

Please refer to the [notebook example](LIS/LIS_of_a_thinSection.ipynb) to see a complete and working test.

|Function name| Description|
|---|---|
|`upload_files_widgets`|isUsing ipywidgets to create a file upload widget for the file upload in Jupyter Notebook|
|`save_to_temp_dir`|Save to temporary directory the file uploaded by the user in Jupyter Notebook using *upload_files_widgets*|
|`run_gdal2tiles`|Run *gdal2tiles.py* command to create tiles from a raster file|
|`convert_shp_to_geojson`|Script to convert SHP into GeoJSON using ogr2ogr|
|`add_geojson_overlay_to_gdal2tiles_html_output`|Function script to append a GeoJSON overlay to the HTML created with *gdal2tiles*|
|`add_popup_feature_to_gdal2tiles_html_output`|Function script to append JS and CSS link of PopUp Feature to the HTML created with *gdal2tiles* and %append_js_to_html function|
|`add_legend_and_rosediagrams`|dd the legend icons to the HTML file and the Javascript code to update the rose diagrams based on the mineral name|
# -*- coding: utf-8 -*-
#TODO see line 148
## FOR TESTIN PURPOSES ONLY
"""
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

import json
import os

from zipfile import ZipFile
from osgeo import ogr
import ntpath
import shutil

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterFolderDestination,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterVectorLayer,
                       QgsProcessingParameterString,
                       QgsProcessingParameterDefinition)


from qgis import processing


class ExampleProcessingAlgorithm(QgsProcessingAlgorithm):
    """
    This is an example algorithm that takes a vector layer and
    creates a new identical one.

    It is meant to be used as an example of how to create your own
    algorithms and explain methods and variables used to do it. An
    algorithm like this will be available in all elements, and there
    is not need for additional work.

    All Processing algorithms should extend the QgsProcessingAlgorithm
    class.
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    NAME = 'NAME'
    SHAPEFILE = 'SHAPEFILE'
    RASTER = 'RASTER'
    ORIGINCOORD = 'ORIGINCOORD'
    OUTPUT = 'OUTDIR'

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return ExampleProcessingAlgorithm()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'myscript'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('My Script')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Example scripts')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'examplescripts'

    def shortHelpString(self):
        """
        Returns a localised short helper string for the algorithm. This string
        should provide a basic description about what the algorithm does and the
        parameters and outputs associated with it..
        """
        return self.tr("Example algorithm short description")

    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # We add the input vector features source. It can have any kind of
        # geometry.
        self.addParameter(
            QgsProcessingParameterString(
                self.NAME,
                self.tr('Name of task')
                )
            )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.SHAPEFILE,
                self.tr('Input Polygon (Shapefile)'),
                [QgsProcessing.TypeVectorPolygon]
            )
        )
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.RASTER,
                self.tr('Raster Baselayer')
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.ORIGINCOORD,
                self.tr('Set origin of local coordinates in Raster'),
                defaultValue=('top-left'),
                optional=True
            )#TODO .setFlags(QgsProcessingParameterDefinition.FlagOptional)
        )
        
        self.addParameter(
            QgsProcessingParameterFolderDestination(
                self.OUTPUT,
                self.tr('Output Folder')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        ORIGINCOORD = self.parameterAsString(
            parameters,
            self.ORIGINCOORD,
            context
        )
        SHAPEFILE = self.parameterAsString(
            parameters,
            self.SHAPEFILE,
            context
        )
        RASTER = self.parameterAsString(
            parameters,
            self.RASTER,
            context
        )
        NAME = self.parameterAsString(
            parameters,
            self.NAME,
            context
        )
        OUTDIR = self.parameterAsString(
            parameters,
            self.OUTPUT,
            context
        )
        
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

      
        # Send some information to the user
        #feedback.pushInfo('CRS is {}'.format(source.sourceCrs().authid()))

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
            feedback.pushInfo(f'WARNING:   {INRINGS} holes inside poligons detected. Not handled.')
        
        # HTML header and footer constructor
        HTMLHEAD = '<!DOCTYPE html>\n<html>\n<head>\n\t<title>Image Map</title>\n'\
            '\t<meta charset="utf-8">\n\t<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>\n'\
            '\t<script src="https://cdnjs.cloudflare.com/ajax/libs/image-map-resizer/1.0.10/js/imageMapResizer.min.js"></script>\n'\
            '</head>\n<body>\n'
        HTMLFOOT = '<script>\n\t$(document).ready(function() {\n\t $(\'map\').imageMapResize();\n\t}); \n</script>\n</body>\n</html>'    
        
        #img tag constructor
        image_block = f'<img src="{RASTER_NAME}" usemap="#image-map" '\
            'style="width: 100%; height: auto;">\n'
        
        #<area> and <coord> tags constructor
        HTMLPOLYGONS = f'<map name="image-map">\n'
        for n, p in enumerate(polygons_vert, start=1):
            COORDSSTR = str(p)[1:-1].replace('(','').replace(')','').replace(' ','')
            line = f'\t<area target="_blank" id="imgzone{n}" '\
                f'alt="Element #{n}" title="Element #{n}" '\
                f'coords="{COORDSSTR}" shape="poly">\n'
            HTMLPOLYGONS += line
        HTMLPOLYGONS += '</map>\n'
        
        #preparing Path and files
        html_path = ntpath.join(OUTDIR,f'{NAME}.html')
        AttributeTable_path = ntpath.join(OUTDIR, f'{NAME}.json')
        outputfile_path = ntpath.join(OUTDIR,f'{NAME}.zip')
        
        
        
        
        
        # Create temporary raster file
        raster_path = os.path.join(OUTDIR, RASTER_NAME)
        shutil.copy(RASTER, raster_path)
        
        feedback.pushInfo(f'html_path: {html_path}')
        feedback.pushInfo(f'Table path: {AttributeTable_path}')
        feedback.pushInfo(f'OutDIR: {OUTDIR}')
        feedback.pushInfo(f'output file: {outputfile_path}')
        
        feedback.pushInfo(f'raster path: {raster_path}')
        
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
        
        return {}

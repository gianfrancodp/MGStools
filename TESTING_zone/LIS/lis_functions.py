import os
import subprocess
from bs4 import BeautifulSoup
    
def upload_files_widgets():
    '''
    Using ipywidgets to create a file upload widget for the file upload
    in Jupyter Notebook

    NOTE: syncronize with save_to_temp_dir() the name of file and the directory
    TODO: change Jpg name reference to generic raster name reference
    '''
    import ipywidgets as widgets
    from IPython.display import display

    Shapefile_selector = widgets.FileUpload(
        description='Shapefile polygon layer',
        accept='.shp, .dbf, .shx, .cpg',  
        multiple=True  
    )
    Jpgfile_selector = widgets.FileUpload(
        description='Image',
        accept='',  
        multiple=False  
    )
    projectname = widgets.Text(
        description='Name:',
        placeholder='NAME'
    )
    # EPSGcode = widgets.Text(
    #     description='EPSG:',
    #     placeholder='54043'
    # )

    labelShp = widgets.Label(value='Select ALL the shapefile files [.shp, .dbf, .shx, .cpg]')
    labelImg = widgets.Label(value='Select the Image file')
    labelName = widgets.Label(value='Select the project name')
    # labelEPSG = widgets.Label(value='Select the EPSG code of files (not work with custom projection)')
    disclaimer = widgets.Label(value='Note: ouptut folder will be created in the same directory as the input files')
    
    # display(labelShp, Shapefile_selector, labelImg, Jpgfile_selector, labelName, projectname, labelEPSG, EPSGcode, disclaimer)

    # return Shapefile_selector, Jpgfile_selector, projectname, EPSGcode
    
    display(labelShp, Shapefile_selector, labelImg, Jpgfile_selector, labelName, projectname, disclaimer)
    
    return Shapefile_selector, Jpgfile_selector, projectname

def save_to_temp_dir(Shapefile_selector, Jpgfile_selector, projectname):
    '''
    Save to temporary directory the file uploaded by the user
    in Jupyter Notebook using upload_files_widgets()

    NOTE: syncronize with upload_files_widgets() the name of file and the directory
    TODO: change Jpg name reference to generic raster name reference
    '''
    
    
    # Create a temporary directory
    temp_dir = projectname

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    else:
        print("WARNING! - project name directory already exists. please rename it, or delete it before.")
        print("No file saved. Operation aborted.")
        return

    # Save the uploaded files to the temporary directory

    # RASTER file

    jpgfile_data = next(iter(Jpgfile_selector.value))
    jpgfile_name = jpgfile_data['name']
    # set raster path to the variable
    Raster_path = os.path.join(temp_dir, jpgfile_name)
    with open(Raster_path, 'wb') as f:
        f.write(jpgfile_data['content'])
    

    # Shapefile files save inside the temporary directory
    
    shapefiledata = iter(Shapefile_selector.value)
    for filename in shapefiledata:
        with open(os.path.join(temp_dir, filename['name']), 'wb') as f:
            f.write(filename['content'])
    # set shp path to the variable
    for filename in iter(Shapefile_selector.value):
        if filename['name'].endswith('.shp'):
            Shp_file_path = os.path.join(temp_dir, filename['name'])
    
    # a list of paths to the files
    files_path = {}
    files_path['Raster_path'] = Raster_path
    files_path['Shp_file_path'] = Shp_file_path
    return files_path
   
def run_gdal2tiles(input_raster, output_directory):
    '''
    Run gdal2tiles.py command to create tiles from a raster file
    '''
    # Check if the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    else:
        print("WARNING! - Directory already exists, Files with same name will be overwrited.")
        # user_input = input().strip().upper()
        # if user_input != 'Y':
        #     print("Operation aborted by the user.")
        #     return
       
    # command gdal2tiles.py parameters setting
    gdal2tiles_command = [
        'gdal2tiles.py',    # default gdal2tiles command
        '-p', 'raster',     # profile tiles raster
        '-z', '0-5',        # zoom levels
        input_raster,       # input raster file
        output_directory    # output directory
    ]
    try:
        subprocess.run(gdal2tiles_command, check=True)
        print(f'Tiles stored in: {output_directory}')
    except subprocess.CalledProcessError as e:
        print(f'{e}')
    return

def create_geojson_js(geojson_file_path, template_js_path, destination_path):
    """
    NOTE: deprecaded function

    Create a `destination_path` file with the GeoJSON file path.
    destination_path must be a .js file.
    destination path folder must be the same of the project name.

    Args:
        geojson_file_pat (str): path to the GeoJSON file.
        template_js_path (str): path to the OpenLayers GeoJSON vector overlay template.
    """

    # read template file and store in a string
    with open(template_js_path, 'r') as f:
        template_content = f.read()

    geojsonbasename = os.path.basename(geojson_file_path)
    # replace the placeholder with the GeoJSON file path

    new_content = template_content.replace("url: 'GEOJSON.geojson'", f"url: '{geojsonbasename}'")

    # write the new content to a new file
    with open(destination_path, 'w') as f:
        f.write(new_content)
        
    print(f'File created: {destination_path}')
    return

def append_js_to_html(js_file_path, html_file_path, new_htmlfile_path):
    """
    NOTE: deprecated function

    Append a JS file to an HTML file before the </body> tag.

    Args:
        js_file_path (str): path to the JS file to append as source.
        html_file_path (str): path to the HTML file.
        new_htmlfile_path (str): path to the new HTML file.
    """
    # read the JS file
    # with open(js_file_path, 'r') as f:
    #     js_content = f.read()

    # read the HTML file
    with open(html_file_path, 'r') as f:
        html_content = f.read()

    # Open the HTML file with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    # create a new script source with beautifulsoup
    srcbasename = os.path.basename(js_file_path)
    script_tag = soup.new_tag('script', src=srcbasename)
    if soup.body:
        soup.body.append(script_tag)
    else:
        print('No <body> tag found in the HTML file.')

    # write the new content to the HTML file
    with open(new_htmlfile_path, 'w') as f:
        f.write(str(soup))
        
    print(f'File updated: {new_htmlfile_path}')

def convert_shp_to_geojson(input_shp, output_geojson):
    """
    SHP to GeoJSON conversion using ogr2ogr.
    
    Args:
        input_shp (str): path to the input SHP file.
        output_geojson (str): path to the output GeoJSON file.
    """
    try:
        # gdal string command
        ogr2ogr_command = [
            'ogr2ogr',
            '-f', 'GeoJSON',  # output format
            output_geojson,   # output file
            input_shp         # input file
        ]
        
        # RUN
        subprocess.run(ogr2ogr_command, check=True)
        print(f'Conversion completed: {output_geojson}')
    except subprocess.CalledProcessError as e:
        print(f'{e}')

    return

def add_geojson_overlay_to_gdal2tiles_html_output(geojson_file_path, Html_path_input, Html_path_output):
    """
    Function to append a GeoJSON overlay to the HTML created with gdal2tiles.
    NOTE: this function work with a specific version of OpenLayers library and
    a specific version of gdal2tiles.
    
    Args:
        geojson_file_path (str): path to the GeoJSON file.
        Html_path_input (str): path to the HTML file to modify.
        Html_path_output (str): path to the new HTML file.
    """
    # read html files:
    with open(Html_path_input, 'r') as f:
        html_content = f.read()
    
    # Open html with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')


    
    # get the basename of the GeoJSON file path

    geojsonURI = os.path.basename(geojson_file_path)

    # Create new HTML contents (Javascript code, using double {{ to escape curly braces)}})
    geojsonJSscript = f"""
    // Add GeoJSON vector to the map
    var vectorSource = new ol.source.Vector({{
        url: '{geojsonURI}', // Path to GeoJSON
        format: new ol.format.GeoJSON({{
            dataProjection: 'EPSG:3857',
            featureProjection: 'EPSG:3857'
        }})
    }});
    var vectorLayer = new ol.layer.Vector({{
        source: vectorSource,
        style: new ol.style.Style({{
            stroke: new ol.style.Stroke({{
                color: 'blue',
                width: 2
            }}),
            fill: new ol.style.Fill({{
                color: 'rgba(0, 0, 255, 0.1)'
            }})
        }})
    }});
    map.addLayer(vectorLayer);
    """
    # add script to soup
    script_tag = soup.new_tag('script')
    script_tag.string = geojsonJSscript
    if soup.body:
        soup.body.append(script_tag)
    else:
        print('Error accessing to html file')

    # Save the new HTML file
    with open(Html_path_output, 'w') as f:
        f.write(str(soup))
    
    print(f'File updated: {Html_path_output}')

    return

def add_popup_feature_to_gdal2tiles_html_output(Html_path_input, Html_path_output):

    """
    Function to append JS and CSS link of PopUp Feature to the HTML created with 
    gdal2tiles and %append_js_to_html function.
    NOTE: this function work with a specific version of OpenLayers-Extension library
    Change the version of the library if needed.

    Args:
        Html_path (str): path to the html file to modify
    """

    # read html files:
    with open(Html_path_input, 'r') as f:
        html_content = f.read()
    
    

    # Open html with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Create new HTML contents

    #OPENLAYERS-EXTENSION LIBRARY
    Ol_ext_CSS = soup.new_tag('link', href="https://cdn.jsdelivr.net/npm/ol-ext@4.0.23/dist/ol-ext.min.css", rel="stylesheet")
    Ol_ext_JS = soup.new_tag('script', src="https://cdn.jsdelivr.net/npm/ol-ext@4.0.23/dist/ol-ext.min.js", attrs={'id': 'olextJS'}) 
    # add CSS link to the head
    if soup.head:
        soup.head.append(Ol_ext_CSS)
    else:
        print('Error accessing to html file')
    # add JS link to the body
    if soup.body:
        soup.body.append(Ol_ext_JS)
    else:
        print('Error accessing to html file')
        
    # STEP 2 POPUP FEATURE
    # Javasript code:
    popup_script = """
    // Select  interaction
    var select = new ol.interaction.Select({
        hitTolerance: 5,
        multi: true,
        condition: ol.events.condition.singleClick
    });
    map.addInteraction(select);

    // Function to get the mineral name
    function getMineralName(mineral) {
        switch (mineral) {
            case 'Amph': return 'Amphibole';
            case 'Ep': return 'Epidote';
            case 'Ap': return 'Apatite';
            case 'Kfs': return 'K-Feldspar';
            case 'Ol': return 'Olivine';
            case 'Pl': return 'Plagioclase';
            case 'Px': return 'Pyroxene';
            case 'Qtz': return 'Quartz';
            case 'Cal': return 'Calcite';
            case 'Ca-Si min': return 'Calc-Silicate Mineral';
            case 'Scap (aggr)': return 'Scapolite (aggregate)';
            case 'Scap': return 'Scapolite';
            case 'Oth': return 'Other';
        }
    }

    // popup
    var popup = new ol.Overlay.PopupFeature({
    popupClass: 'default anim',
    select: select,
    canFix: true,
 
    template: {
        title: 
          // 'nom',   // only display the name
          function(f) {
            return f.get('Mineral') + ' - ' + getMineralName(f.get('Mineral'));
          },
        attributes: //
            {
            'O' : { 
                    title: 'Orientation', 
                    before:'', 
                    format: ol.Overlay.PopupFeature.localString(), // format as local string APPROX
                    after:'°' 
                },
            'AsR' : { title: 'Aspect Ratio' },
            'R': { title: 'Roundness' },
            'A': { title: 'Area' },
            'GSI': {title: 'Grain Shape Index'} // ,
            }
        }
    });
    map.addOverlay (popup);

    // Event on attribute click
    popup.on('attribute', console.log);
    """
    # add script to soup
    script_tag = soup.new_tag('script')
    script_tag.string = popup_script
    if soup.body:
        soup.body.append(script_tag)
    else:
        print('Error accessing to html file')

    # CSS code:
    popup_CSS = """
    .ol-popup h1 {font-size: 1.2em; background-size: 2em; padding-left: 3em; width: 100%;}
    .ol-attribution ul {font-size: .8em;}
    .ol-control button i, .ol-control.ol-bar, .ol-control button i {color: inherit;}
    """
    # add CSS to soup
    style_tag = soup.new_tag('style')
    style_tag.string = popup_CSS
    if soup.head:
        soup.head.append(style_tag)
    else:
        print('Error accessing to html file')


    # Save the new HTML file
    with open(Html_path_output, 'w') as f:
        f.write(str(soup))
    
    print(f'File updated: {Html_path_output}')


    return

def add_legend_and_rosediagrams(Html_input,Html_output, legend_icons, map_view_height, blankdiagram, rose_diagrams):
    """
    Add the legend icons to the HTML file and the Javascript code to update the rose diagrams
    based on the mineral name.
    @param Html_input: the path of the input HTML file
    @param Html_output: the path of the output HTML file
    @param legend_icons: dictionary of the legend icons paths
    @param map_view_height: the height of the map view after adding the legend icons
    @param blankdiagram: the path of the blank diagram file
    """

    def generate_update_svg_JS_function(rose_diagrams, blankdiagram_name):
        """
        
        Generate the Javascript function to update the SVG images of the rose diagrams
        based on the mineral name.
        @param rose_diagrams: dictionary of the rose diagrams paths, using key as the mineral name coded
        with the condition (e.g. 'Qtz_UnW' for Quartz Unweathered)
        @param blankdiagram_name: the final path of the blank diagram file to be subsituted in case of error
        @return: the Javascript code as a string
        """
        js_code = "function updateSVG(mineral) {\n"
        for key, value in rose_diagrams.items():
            value = os.basename(value)
            value = os.path.join('asset',value) # add the path to the asset folder
            mineral, condition = key.split('_')
            if condition == 'UnW':
                js_code += f"    if (mineral === '{mineral}') {{\n"
                js_code += f"        SvgURI1 = '{value}';\n"
            else:
                js_code += f"        SvgURI2 = '{value}';\n"
                js_code += "    }\n"
        js_code += """
        var imgElement1 = document.getElementById('svg1');
        if (imgElement1) {
            imgElement1.src = SvgURI1;
            imgElement1.onerror = function() {
                imgElement1.src = '""" + blankdiagram_name + """';
            }
        }
        var imgElement2 = document.getElementById('svg2');
        if (imgElement2) {
            imgElement2.src = SvgURI2;
            imgElement2.onerror = function() {
                imgElement2.src = '""" + blankdiagram_name + """';
            }
        }\n"""
        js_code += "}\n"
        
        return js_code
    

    # open file
    with open(Html_input, 'r') as f:
        html_content = f.read()
    # parse with BeautifulSoup

    soup = BeautifulSoup(html_content, 'html.parser')

    # copy the files stored in legend_icons dictionary to the output subdirectory
    subdirectoryLEGEND = os.path.join(os.path.dirname(Html_output), 'asset')
    os.makedirs(subdirectoryLEGEND, exist_ok=True)

    for key in legend_icons:
        icon_path = legend_icons[key]
        icon_name = os.path.basename(icon_path)
        icon_output_path = os.path.join(subdirectoryLEGEND, icon_name)
        with open(icon_path, 'rb') as f:
            with open(icon_output_path, 'wb') as f1:
                f1.write(f.read())
    
    # add HTML tags for Legend icon
    new_div_tag = soup.new_tag('div')
    new_div_tag['id'] = 'legendbar'
    new_div_tag['style'] = 'display: flex; justify-content: center;'

    table_tag = soup.new_tag('table')
    tr_tag = soup.new_tag('tr')
    for key in legend_icons:
        td_tag = soup.new_tag('td')
        img_tag = soup.new_tag('img')
        img_tag['src'] = legend_icons[key]
        img_tag['id'] = f'{key}_legend'
        img_tag['onclick'] = f'legendClick(\'{key}\')' # call the Javascript legendClic(mineral) function with the mineral name
        td_tag.append(img_tag)
        tr_tag.append(td_tag)
    table_tag.append(tr_tag)
    new_div_tag.append(table_tag)
    # add the new div tag to the body
    soup.body.append(new_div_tag)
    
    #reduce the height of the map to make space for the legend
    style_tag = soup.find('style')
    if style_tag:
        css_content = style_tag.string
        # Modifica il CSS specifico
        css_content = css_content.replace('#map { height: 90%; border: 1px solid #888; }', f'#map {{ height: {map_view_height}; border: 1px solid #888; }}')
        style_tag.string = css_content

    # add CSS style for legend icons
    new_style_tag = soup.new_tag('style')
    css_string = "#ShowAll, #HideAll"
    for key in legend_icons:
        css_string += f", #{key}_legend"
    css_string += " {width: 80px; filter: grayscale(0);}"
    new_style_tag.string = css_string
    #new_style_tag.string = """#ShowAll, #Amph_legend, #Ep_legend, #Ap_legend, #Kfs_legend, #HideAll, #Ol_legend, #Pl_legend, #Px_legend, #Qtz_legend {width: 80px; filter: grayscale(0);}"""
    soup.head.append(new_style_tag)

    # ROSE DIAGRAMS file and paths
    # create the path for the rose diagrams
    # TESTING_zone/LIS/templates/asset/rose/PAL12_A_Amph_2.svg
    subdirectoryRoseD = os.path.join(os.path.dirname(Html_output), 'asset')
    os.makedirs(subdirectoryRoseD, exist_ok=True)

    #copy files stored in rose_diagrams dictionary to the output subdirectory
    for key in rose_diagrams:
        rose_diagram_path = rose_diagrams[key]
        rose_diagram_name = os.path.basename(rose_diagram_path)
        rose_diagram_output_path = os.path.join(subdirectoryRoseD, rose_diagram_name)
        with open(rose_diagram_path, 'rb') as f:
            with open(rose_diagram_output_path, 'wb') as f1:
                f1.write(f.read())
    

    # write blank diagram svg in subfolder
    blankdiagram_name = os.path.basename(blankdiagram)
    blankdiagram_output_path = os.path.join(subdirectoryRoseD, blankdiagram_name)

    with open(blankdiagram, 'rb') as f:
        with open(blankdiagram_output_path, 'wb') as f1:
            f1.write(f.read())
    
    
    # add Javascript code


    JSscriptText ="""
    // Selection interaction
    const selectInteraction = new ol.interaction.Select({
        layers: [vectorLayer], //
        condition: ol.events.condition.click // Click selection
    });
    map.addInteraction(selectInteraction);

    // listener for the selection interaction
    selectInteraction.on('select', function(event) {
        const selectedFeatures = event.selected;
        selectedFeatures.forEach(function(feature) {
            updateSVG(feature.getProperties().Mineral);
        });
    });
    """
    Javascript_updateSVG = generate_update_svg_JS_function(rose_diagrams, blankdiagram_name)
    JSscriptText += Javascript_updateSVG
    JSscriptText += """
    function legendClick(mineral) {
    //addFilter(mineral);
    updateSVG(mineral);
    };
    """
   
    new_script_tag = soup.new_tag('script')
    new_script_tag.string = JSscriptText
    soup.body.append(new_script_tag)


    # Add the rose diagrams tags with BeautifulSoup

    #adding HTML tags

    tableRoseDiagram = soup.new_tag('table')
    rowRoseDiagram = soup.new_tag('tr')
    columnRoseDiagram1 = soup.new_tag('td')
    RoseDiagram1 = soup.new_tag('img')
    RoseDiagram1['id'] = 'svg1'
    RoseDiagram1['src'] = blankdiagram
    RoseDiagram1['width'] = '100%'
    columnRoseDiagram1.append(RoseDiagram1)
    rowRoseDiagram.append(columnRoseDiagram1)
    columnRoseDiagram2 = soup.new_tag('td')
    RoseDiagram2 = soup.new_tag('img')
    RoseDiagram2['id'] = 'svg2'
    RoseDiagram2['src'] = blankdiagram
    RoseDiagram2['width'] = '100%'
    columnRoseDiagram2.append(RoseDiagram2)
    rowRoseDiagram.append(columnRoseDiagram2)
    tableRoseDiagram.append(rowRoseDiagram)
    soup.append(tableRoseDiagram)

        
    #write the modified html to a new file
    with open(Html_output, 'w') as file:
        file.write(soup.prettify())
    
    # copy the files stored in legend_icons dictionary to the output subdirectory
    subdirectory = os.path.join(os.path.dirname(Html_output), 'templates','asset', 'legend')
    os.makedirs(subdirectory, exist_ok=True)

    for key in legend_icons:
        icon_path = legend_icons[key]
        icon_name = os.path.basename(icon_path)
        icon_output_path = os.path.join(subdirectory, icon_name)
        with open(icon_path, 'rb') as f:
            with open(icon_output_path, 'wb') as f1:
                f1.write(f.read())

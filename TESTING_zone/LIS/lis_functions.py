import os
import sys
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
        print("WARNING! - Directory already exists, Files will be overwrited! Continue? (Y).")
        user_input = input().strip().upper()
        if user_input != 'Y':
            print("Operation aborted by the user.")
            return
       
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


def append_js_to_html(js_file_path, html_file_path, new_htmlfile_path):
    """
    Append a JS file to an HTML file before the </body> tag.

    Args:
        js_file_path (str): path to the JS file to append as source.
        html_file_path (str): path to the HTML file.
        new_htmlfile_path (str): path to the new HTML file.
    """
    # read the JS file
    with open(js_file_path, 'r') as f:
        js_content = f.read()

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

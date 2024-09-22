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


def save_to_temp_dir(Shapefile_selector, Jpgfile_selector):
    '''
    Save to temporary directory the file uploaded by the user
    in Jupyter Notebook using upload_files_widgets()

    NOTE: syncronize with upload_files_widgets() the name of file and the directory
    TODO: change Jpg name reference to generic raster name reference
    '''
    import os
    
    # Create a temporary directory
    temp_dir = 'temporary_files'
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

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
    

    return Raster_path, Shp_file_path
   



    # # Get the uploaded files from the widgets
    # shapefiledata = iter(Shapefile_selector.value)
    # for filename in shapefiledata:
    #     with open(filename['name'], 'wb') as f:
    #         f.write(filename['content'])
    #     # set the shapefile name variable
    #     ShpFileName = filename['name']
    #     if ShpFileName.endswith('.shp'):
    #         SHAPEFILE = ShpFileName
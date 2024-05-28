## TODO: implement https://gdal.org/programs/gdal2tiles.html



def fix_coords(coords, origin='top-left'):
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

def polygoniterate(layer,attributes_list,INRINGS,polygons_vert):
    '''
    Iterates through the polygons in the shapefile and writes the html code
    '''
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
    # if INRINGS:
    print(f'Warning: {INRINGS} holes detected. Not handled.')

    return attributes_list, polygons_vert
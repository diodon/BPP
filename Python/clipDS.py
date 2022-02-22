## clip a dataset using a list of coordinates
import matplotlib.pyplot as plt
import xarray as xr
import rioxarray as rio


def clipMap(nc, geometries, type="Polygon", crs=4326):
    '''
    Clip a xarray datastet or data array providing a list of coordinates that define the vertices of a geometry
    the dataset is opened with the decode_coords="all" argument
    depends on rioxarray
    eklein at ocean-analytics dot com dot au
    :param nc: xarray dataset
    :param geometries: list of coordinates pairs
    :param type: polygon by default
    :param crs: projection. EPSG 4326 by default
    :return: clipped dataset to the defined geometry
    '''

    geometries = [
        {'type': type,
         'coordinates': [geometry]}]

    ## assign projection.
    nc = nc.rio.write_crs(crs)

    ## clip using geometries
    nc_clip = nc.rio.clip(geometries)

    return nc_clip

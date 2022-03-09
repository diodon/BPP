## clip DHW files by the IPCC areas
## save as clipped netcdf
import os
import xarray as xr
import geopandas

def clipMap(nc, geometry, type="Polygon", crs=4326):
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



## read IPCC polygons
ipcc = geopandas.read_file("GIS/IPPC_corals.shp").explode(ignore_index=True)

basePath = 'Data'
outPath = 'Data'
fileName = 'test_DHWmax.nc'
with xr.open_dataset(os.path.join(basePath, fileName)) as nc:
    ## make a list of coordinates for each polygon
    oldAcronym = ""
    for area in range(len(ipcc)):
        print(ipcc.Name[area])
        outFileName = ipcc.Acronym[area]
        if outFileName == oldAcronym:
            outFileName = outFileName + "-1"
        outFileName = "IPCC-" + outFileName
        oldAcronym = ipcc.Acronym[area]
        coords = list(ipcc.geometry[area].exterior.coords)
        coords_list = [list(item) for item in coords]
        ncClip = clipMap(nc, coords_list)
        ncClip.to_netcdf(os.path.join(outPath, outFileName + "_" + fileName))



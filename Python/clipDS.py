## clip a dataset using a dictionary of coordinates
import matplotlib.pyplot as plt
import xarray as xr
import rioxarray as rio

## read dataset
nc = xr.open_dataset("Data/test_DHWmax.nc", decode_coords="all")

## this is the hourglass
geometries = [
    {
        'type': 'Polygon',
        'coordinates': [[[95.097656, -19.47695],
                         [111.005859, -19.145168],
                         [93.691406, -37.788081],
                         [113.730469, -37.71859],
                         [95.097656, -19.47695]]]
    }
]

## assign projection. Assuming EPSG:4326
nc = nc.rio.write_crs(4326)

## clip using geometries
nc_clip = nc.rio.clip(geometries)

## plot
nc_clip.DHW[0,:,:].plot()

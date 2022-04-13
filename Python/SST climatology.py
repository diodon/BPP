## extract the yDay of the min/max temp from the climatology

import xarray as xr
import numpy as np

fileName = 'Data/ESA_SST_1985-2016_mean_climatology.nc'
with xr.open_dataset(fileName) as nc:
    ## prepare the dataset
    nc = nc.drop_vars(["latitude_bnds", "longitude_bnds"])
    tos = nc.tos


## create land mask
mask = tos[1,:,:].values
mask[~np.isnan(mask)] = 1

## coldest day of the climatological year
# replace NaN by zero to avoid argmax all-NaN slice error
tosNA_min = tos.fillna(9999)
tosMin = tosNA_min.argmin(dim="time")
tosMin = tosMin + mask

## hottest day of the climatological year
tosNA_max = tos.fillna(-9999)
tosMax = tosNA_max.argmax(dim="time")
tosMax = tosMax + mask

## mak a dataset
DOYclimatology = xr.Dataset({'SSTmin_doy': tosMin,
                             'SSTmax_doy': tosMax})

DOYclimatology['SSTmin_doy'].attrs = {'long_name': 'day of the year when SST is minimum'}
DOYclimatology['SSTmax_doy'].attrs = {'long_name': 'day of the year when SST is maximum'}
DOYclimatology.attrs = {'title': 'day of the year when SST reaches its minimum/maximum value',
                        'author': 'E Klein',
                        'author_email': 'eklein@ocean-analytics.com.au',
                        'comments': 'based on the climatological file ESA_SST_1985-2016_mean_climatology.nc'}

DOYclimatology.to_netcdf('Data/SSTminmax_DOY.nc')
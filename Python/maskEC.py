## mask EC Earth3 model bad pixels
## needs to be done by year to avoid memory overflow

import xarray as xr
import numpy as np
import os

outDir = 'Data/raw/maskEC'
with xr.open_dataset("Data/raw/ssp245/ssp245_EC-Earth3_DHW.nc") as nc:
    nc = nc.drop_vars("time_bnds")
    DHW = nc.DHW

with xr.open_dataset("Data/raw/masked_lon_lat_EC-Earth3.nc") as nc:
    ECmask = nc.pixel_mask.squeeze()
ECmask = ECmask.where(ECmask==1, 0, drop=False).astype(bool)

DHW.coords['mask'] = (('lat', 'lon'), ECmask.values)
DHW.coords['year'] = DHW['time'].dt.year

DHWyear = DHW.groupby('year')
years = list(DHWyear.groups)

## do first year
print(years[0])
DHWyear_tmp = DHWyear[years[0]]
DHWmasked = DHWyear_tmp.where(DHWyear_tmp.mask, np.nan, drop=False)
DHWmasked.to_netcdf(os.path.join(outDir, ('DHWmasked_' + str(years[0]) + '.nc')))

## do the rest
for yy in years[1:]:
    print(yy)
    DHWyear_tmp = DHWyear[yy]
    DHWmasked = DHWyear_tmp.where(DHWyear_tmp.mask, np.nan, drop=False)
    DHWmasked.to_netcdf(os.path.join(outDir, ('DHWmasked_' + str(yy) + '.nc')))

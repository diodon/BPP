## process IPCC model/scenario daily files
## returns dataset with DHWmax, DHWdoy and DHWdoyrel, DHWNDays

import os
import sys
import xarray as xr
import numpy as np
from datetime import datetime

from tools.DHWtools import *


DHWbleach = 4.0
DHWdead = 8.0

fileRoot = '/home/data/raw/shifted/'
outFileRoot = '/home/data/DHWmax/Aggregates_shifted_may23/'
filePrefix = sys.argv[1]
fileName = os.path.join(fileRoot + filePrefix)
print(fileName)


## load model data
with xr.open_dataset(fileName) as nc:
    if "time_bnds" in nc.data_vars:
        nc = nc.drop_vars("time_bnds")
    yearMin = int(nc.time.dt.year.min())
    yearMax = int(nc.time.dt.year.max())
    nc['time'] = nc.time.dt.year
    DHW = nc['DHW']

## group and extract the day of DHWmax per year
DHWyear = DHW.groupby("time")
years = list(DHWyear.groups)

## create the first data arrays
DHWyear_tmp = DHWyear[years[0]]
DHWdoyrel_4 = getDOY(DHWyear_tmp, 4)
DHWdoyrel_8 = getDOY(DHWyear_tmp, 8)

## process the rest of the years
for yy in years[1:]:
    print(yy)
    DHWyear_tmp = DHWyear[yy]
    DHWdoyrel_4 = xr.concat([DHWdoyrel_4, getDOY(DHWyear_tmp, 4)], 'time')
    DHWdoyrel_8 = xr.concat([DHWdoyrel_8, getDOY(DHWyear_tmp, 8)], 'time')

## make data sewt
ds = xr.Dataset({'DoYrel_DHW4': DHWdoyrel_4,
                 'DoYrel_DHW8': DHWdoyrel_8})


## add variable attributes
ds.DoYrel_DHW4.attrs = {'long_name': 'first day of the year when DHW exceeds 4 degree-weeks, relative to the climatological coldest DOY',
                     'units': 'day of the year',
                     'comment': 'considering the coldest climatological DoY as the first day of the year'}
ds.DoYrel_DHW8.attrs = {'long_name': 'first day of the year when DHW exceeds 8 degree-weeks, relative to the climatological coldest DOY',
                     'units': 'day of the year',
                     'comment': 'considering the coldest climatological DoY as the first day of the year'}

## add global attributes
modelString = filePrefix.split('.nc')[0].split('_')
scenario = modelString[0]
modelName = modelString[1]
ds.attrs = {'title': 'DHW general yearly statistics',
            'abstract': 'Projections of future coral bleaching risk, expressed as annual maximum Degree Heating Weeks (DHW), '
                        'onset and duration of severe bleaching in every year between 1985 and 2100. '
                        'For details on the methods and results, please cite. '
                        'This project is a collaboration between University of Adelaide, James Cook University and Ocean Analytics',
            'source_file': filePrefix,
            'model_name': modelName,
            'IPCC_scenario': scenario,
            'time_coverage_start': yearMin,
            'time_coverage_end': yearMax,
            'creation_date': str(datetime.now()),
            'citation': '',
            'author_name': 'Klein, Eduardo',
            'author_email': 'eklein at ocean-analytics dot com.au'}

## add compression
comp = dict(zlib=True, complevel=5)
encoding = {var: comp for var in ds.data_vars}

ds.to_netcdf(os.path.join(outFileRoot, ('DHW_shifted_' + filePrefix)), encoding=encoding)




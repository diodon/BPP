## Extract the first day when the maximun DHW occurs in any year.

import xarray as xr
import numpy as np

def dayDHWmax(nc, varName="DHW"):
    '''
    determines the first day in a year with the yearly maximum DHW
    :param nc: xarray dataset
    :param varName: name of the variable. DHW by default
    :return: dataset
    '''

    ## prepare the dataset
    nc = nc.drop_vars("time_bnds")
    nc['time'] = nc.time.dt.year

    ## create land mask
    mask = nc[varName][1,:,:].values
    mask[~np.isnan(mask)] = 1

    # replace NaN by zero to avoid argmax all-NaN slice error
    nc0 = nc.fillna(0)

    ## group and extract the day of DHWmax per year
    DHWyear = nc0.DHW.groupby("time")
    years = list(DHWyear.groups)

    ## create the first dataarray
    dayDHWmax = DHWyear[years[0]].argmax(dim="time").astype("int")
    dayDHWmax = dayDHWmax * mask
    for yy in years[1:]:
        print(yy)
        DHWmaxyear = DHWyear[yy].argmax(dim="time")
        # apply mask
        DHWmaxyear = DHWmaxyear * mask
        dayDHWmax = xr.concat([dayDHWmax, DHWmaxyear], "time")

    ## add 1 to the index to start the year at 1
    dayDHWmax = dayDHWmax + 1

    ## add time coordinate
    dayDHWmax = dayDHWmax.assign_coords({'time': years})

    return dayDHWmax


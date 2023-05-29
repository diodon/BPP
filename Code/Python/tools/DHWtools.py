## Functions to extract DHWmax and associated variables from a yearly DHW[time,lat,lon] data array
#

import xarray as xr
import numpy as np

def getDHWmax(da):
    '''
    Get the max DHW of the year
    :param da: one-year data array of DHW daily values [time,lat,lon]
    :return: data array DHWmax[lat.lon] as integer with a scale factor = 0.1
    '''
    dhwMax = da.max(dim='time')
    dhwMax = dhwMax.rename("DHW_max")
    dhwMax.attrs = {'long name': 'Maximum DHW',
                     'units': 'degree Celsius - week'}

    return dhwMax

def getDHWmin(da):
    '''
    Get the min DHW of the year
    :param da: one-year data array of DHW daily values [time,lat,lon]
    :return: data array DHWmax[lat.lon] as integer with a scale factor = 0.1
    '''
    dhwMax = da.min(dim='time')
    dhwMax = dhwMax.rename("DHW_min")
    dhwMax.attrs = {'long name': 'Minimum DHW',
                     'units': 'degree Celsius - week'}
    return dhwMax


def getDHWp99(da, q=0.99):
    '''
    Get the 99th quantile DHW of the year
    :param da: one-year data array of DHW daily values [time,lat,lon]
    :param q: quantile requested
    :return: data array DHWmax[lat.lon] as integer with a scale factor = 0.1
    '''
    ## create land mask
    mask = da[1, :, :].values
    mask[~np.isnan(mask)] = 1
    da = da.fillna(0.0)

    daQ = da.quantile(q, dim='time') * mask
    daQ = daQ.rename('DHW_q' + str(q).split(".")[1])
    daQ = daQ.drop_vars('quantile')
    daQ.attrs = {'long name': 'DHW quantile ' + str(q),
                 'units': 'degree Celsius - week'}
    return daQ


def getYdayDHWmax(da):
    '''
    Get the first day when the max DHW is reached in a year
    :param da: one-year data array of DHW daily values [time,lat,lon]
    :return: data array DHWmax[lat.lon] as integer with a scale factor = 0.1
    '''

    ## create land mask
    mask = da[1, :, :].values
    mask[~np.isnan(mask)] = 1

    ## get max value
    da = da.fillna(0.0)
    DHWmax = da.argmax(dim="time").astype("int") * mask
    DHWmax.attrs = {'long name': 'maximum DHW value in a year',
                   'units': 'degree Celsius - week',
                  'scale factor': 0.1}
    DHWmax = DHWmax.rename('DHWmax')

    return DHWmax


def getYdayDHWmax_rel(da, ref):
    '''
    Get the first day when the max DHW is reached in a year
    and make it relative to a reference, usually the coldest climatological DOY
    :param ref: DOY data array to reference the start of the year
    :param da: one-year data array of DHW daily values [time,lat,lon]
    :return: data array DHWmax[lat.lon] as integer with a scale factor = 0.1
    '''
    ## mask zero DHWvalues
    da = da.where(da>0, np.nan, drop=False)

    ## create land mask
    mask = da[1, :, :].values
    mask[~np.isnan(mask)] = 1

    ## get max value
    da = da.fillna(0.0)
    DHWmax = da.argmax(dim="time").astype("int") * mask

    ## make it relative
    DHWmax = DHWmax - ref.values
    DHWmax = DHWmax.where(DHWmax>0, DHWmax + 365, drop=False)
    DHWmax.attrs = {'long name': 'day of maximum DHW value in a year, relative to climatology',
                   'units': 'days'}
    DHWmax = DHWmax.rename('DOYmax')

    return DHWmax

def landMask(da):
    '''
    Cretate a land mask
    :param da: data array
    :return: numpy array: mask 0 land, 1 value
    '''
    ## create land mask
    mask = da[1, :, :].values
    mask[~np.isnan(mask)] = 1
    return mask


def getYdayDHWmin(da):
    '''
    Get the first day when the min DHW is reached in a year
    :param da: one-year data array of DHW daily values [time,lat,lon]
    :return: data array DHWmax[lat.lon] as integer with a scale factor = 0.1
    '''

    ## create land mask
    mask = da[1, :, :].values
    mask[~np.isnan(mask)] = 1

    ## get max value
    da = da.fillna(0.0)
    DHWmax = da.argmin(dim="time").astype("int") * mask
    DHWmax.attrs = {'long name': 'maximum DHW value in a year',
                   'units': 'degree Celsius - week',
                  'scale factor': 0.1}
    DHWmax = DHWmax.rename('DHWmax')

    return DHWmax



def getTdayDHWp99(da):
    '''
    Get the first day of the reach that reaches the 99th percentile of the DHW 
    :param da: one-year data array of DHW daily values [time,lat,lon]
    :return: data array DHWmax[lat.lon] as integer with a scale factor = 0.1
    '''
    return

def getDOY(da, threshold):
    '''
    get the first day of the year when the variable surpass the threshold value
    takes care of the all-NAN slices error by masking
    :param threshold: threshold value
    :param da: data array
    :return: data array with the DOY
    '''
    mask = landMask(da)
    daThreshold = da.where(da > threshold, np.nan, drop=False).squeeze()
    ## Create mask for values below threshold
    da_min = daThreshold.min(dim='time')
    maskMin = da_min.values
    maskMin[~np.isnan(maskMin)] = 1
    ## get the first doy
    daThreshold = daThreshold.fillna(9999)
    daDOY = daThreshold.argmin(dim='time').astype('int') + 1
    ## apply maskMin
    daDOY = daDOY * (maskMin) * mask
    daDOY.attrs = {'long name': 'absolute first day of the year when DHW reaches ' +
                                str(threshold)}
    daDOY = daDOY.rename('DoY_DHW' + str(threshold))

    return daDOY

def getDOYrel(da, threshold, ref, q=None):
    '''
    get the first day of the year when the variable surpass the threshold value
    relative to a climatological reference
    takes care of the all-NAN slices error by masking
    :param ref: climatological start of the year day
    :param threshold: threshold value
    :param da: data array
    :return: data array with the DOY
    '''

    mask = landMask(da)
    if q!=None:
        da = da.where(da <= da.quantile(q), np.nan, drop=False)

    daThreshold = da.where(da > threshold, np.nan, drop=False)

    ## Create mask for values below threshold
    da_min = daThreshold.min(dim='time')
    maskMin = da_min.values
    maskMin[~np.isnan(maskMin)] = 1
    ## get the first doy
    daThreshold = daThreshold.fillna(9999)
    daDOY = daThreshold.argmin(dim='time').astype('int') + 1

    ## make it relative
    daDOY = daDOY - ref.values
    daDOY = daDOY.where(daDOY > 0, daDOY + 365, drop=False)

    ## apply maskMin
    daDOY = daDOY * maskMin * mask
    daDOY.attrs = {'long name': 'relative first day of the year when DHW reaches ' +
                                str(threshold)}
    daDOY = daDOY.rename('DoYrel_DHW' + str(threshold))

    return daDOY




def getNDays(da, threshold):
    '''
    get the number of days above DHW threshold
    :param da: data array of daily DHW[time,lat,lon)
    :param threshold: threshold value to count the n days above. Exclusive
    :return: dataarray with the number of days above threshold [lat,lon]
    '''

    ## create land mask
    mask = da[1, :, :].values
    mask[~np.isnan(mask)] = 1

    nDays = da.where(da > threshold, np.nan, drop=False).count(dim='time')
    nDays = nDays.astype(int) * mask

    nDays.attrs = {'long name': 'number of days above DHW ' +
                                str(threshold)}
    nDays = nDays.rename('nDaysAbove_DHW' + str(threshold))
    return nDays


def DHWthreshold(nc, DOYref, DHWthreshold = 4, relativeDOY=True):
    '''
    find the first day of the year that exceeds DHW threshold
    :param relativeDOY: make the DOY relative to the reference DOY
    :param DOYref: data array reference of the DOY of the min climatological SST
    :param nc: xarray dataarray with variable[time,lat,lon]
    :param DHWthreshold: min DHW to be reached
    :return: dataset
    '''

    ## prepare the data array
    nc['time'] = nc.time.dt.year
    ncYear = nc.groupby("time")
    years = list(ncYear.groups)

    ## create the first dataarray
    DOY = getDOY(ncYear[years[0]], DHWthreshold)
    if relativeDOY:
        DOY = DOY - np.flipud(DOYref.values)
    ncYearAll = DOY

    ## do the rest of the years
    for yy in years[1:]:
        print(yy)
        DOY = getDOY(ncYear[yy], DHWthreshold)
        if relativeDOY:
            DOY = DOY - np.flipud(DOYref.values)

        ncYearAll = xr.concat([ncYearAll, DOY], dim='time')

    ## add 1 to the index to start the year at 1
    ncYearAll = ncYearAll + 1
    ## add time coordinates
    ncYearAll = ncYearAll.assign_coords({'time': years})

    return ncYearAll

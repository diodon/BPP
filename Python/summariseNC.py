## summarise DHW values from a selected area
import xarray as xr
import pandas as pd
import numpy as np



def summariseDHWperYear(nc, varName, pandas=False):
    '''
    Compute summary statistics of DHW per year from a selected region of interest.
    If the data array os the day when DHWmax occurs, the statistics are based on the median
    record dimension is 'time' which is the year
    requires xarray, pandas
    eklein at ocean dash analytics dot com dot au
    :param nc: data array of DHWmax[time,lat,lon]
    :param varName: variable name
    :param pandas: True if dataframe is the output; False returns a xarray dataset
    :return: pandas table or a dataset with summary statistics per year
    '''

    ## compute basics stats along lat lon dimensions
    DHWmin = nc.min(dim=['lat', 'lon'], skipna=True)
    DHWmax = nc.max(dim=['lat', 'lon'], skipna=True)
    DHWmedian = nc.median(dim=['lat', 'lon'], skipna=True)
    DHWmean = nc.mean(dim=['lat', 'lon'], skipna=True)
    DHWstd = nc.std(dim=['lat', 'lon'], skipna=True)
    DHWq01 = nc.quantile(0.01, dim=['lat', 'lon']).drop_vars('quantile')
    DHWq05 = nc.quantile(0.05, dim=['lat', 'lon']).drop_vars('quantile')
    DHWq95 = nc.quantile(0.95, dim=['lat', 'lon']).drop_vars('quantile')

    ds = xr.Dataset({varName + '_min': DHWmin,
                     varName + '_q01': DHWq01,
                     varName + '_q05': DHWq05,
                     varName + '_mean': DHWmean,
                     varName + '_median': DHWmedian,
                     varName + '_q95': DHWq95,
                     varName + '_max': DHWmax,
                     varName + '_std': DHWstd})

    if pandas:
        return ds.to_pandas()
    else:
        return ds



def lmDHW(x,y):
    '''
    Compute linear regression on a data frame with year as index and column[0] the variable of interest
    Also compute the predicted values and the confidence interval of the prediction (lower/upper limits)
    requires numpy, pandas
    eklein at ocean dash analytics dot com dot au
    :param x: time array
    :param y: Variable of interest array (DHWmean usually)
    :return: df with orinal and predicted values and a list of regression parameters
    '''

    coeffs = np.polyfit(x,y, deg=1)
    xPred = x * coeffs[0] + coeffs[1]
    return coeffs, xPred







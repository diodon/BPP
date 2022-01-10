## Extract DHWmax by year and save in a yearly file
import sys
import xarray as xr
import pandas as pd

def getDHWmax(nc):
    '''
    Convert DHW model/scenario file into a yearly file, extracting the DHWmax for each year
    E Klein. 2022-01-09
    :param nc: xarray dataset
    :return: xarray dataset
    '''

    ## prepare the dataset
    nc = nc.drop_vars("time_bnds")
    nc['time'] = nc.time.dt.year

    ## group and extract the DHWmax per year
    DHWmax = nc.groupby("time").max()

    DHWmax.DHW.attrs = {'description': 'Maximum value of the Degree Heating Week of the year',
                        'longname': 'Degree Heating Week',
                        'units': 'degC.week'}

    return DHWmax


if __name__ == "__main__":
    fileName = sys.argv[1]
    print(fileName)
    with xr.open_dataset(fileName) as nc:
        DHWmax = getDHWmax(nc)

    DHWmax.to_netcdf('DHWmax_' + fileName)

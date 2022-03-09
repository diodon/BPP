## Make model ensemble by averaging daily DHW from all models

import os
import glob
import xarray as xr

scenario = "ssp245"

dataDir = "Data/raw/" + scenario
outDir = "Data/raw/ensemble/" + scenario
fileList = glob.glob("Data/raw/" + scenario + "/*.nc")
yearList = list(range(1985, 2101))


## do the first year
yy = yearList[0]
print(yy)
# do the first two models
nc0 = xr.open_dataset(fileList[0])
nc1 = xr.open_dataset(fileList[1])

nc0 = nc0.drop_vars("time_bnds")
nc1 = nc1.drop_vars("time_bnds")
dhwSum = nc0['DHW'].where(nc0.time.dt.year == yy, drop=True) + nc1['DHW'].where(nc1.time.dt.year == yy, drop=True)

nc0.close()
nc1.close()

# loop over the rest of the models
for ff in fileList[2:]:
    print(ff)
    with xr.open_dataset(ff) as nc0:
        nc0 = nc0.drop_vars("time_bnds")
        dhwSum = dhwSum + nc0['DHW'].where(nc0.time.dt.year == yy, drop=True)

dhwSum = dhwSum / len(fileList)
dhwMax = dhwSum.max(dim="time")
dhwMax = dhwMax.assign_coords(year=yy)
dhwMax = dhwMax.expand_dims({'year': 1})

## loop over the rest of the years
for yy in yearList[1:]:
    print(yy)
    # do the first two models
    nc0 = xr.open_dataset(fileList[0])
    nc1 = xr.open_dataset(fileList[1])

    nc0 = nc0.drop_vars("time_bnds")
    nc1 = nc1.drop_vars("time_bnds")
    dhwSum = nc0['DHW'].where(nc0.time.dt.year == yy, drop=True) + nc1['DHW'].where(nc1.time.dt.year == yy, drop=True)

    nc0.close()
    nc1.close()

    # loop over the rest of the models
    for ff in fileList[2:]:
        print(ff)
        with xr.open_dataset(ff) as nc0:
            nc0 = nc0.drop_vars("time_bnds")
            dhwSum = dhwSum + nc0['DHW'].where(nc0.time.dt.year == yy, drop=True)

    dhwSum = dhwSum / len(fileList)
    dhwMax0 = dhwSum.max(dim="time")
    dhwMax0 = dhwMax0.assign_coords(year=yy)
    dhwMax0 = dhwMax0.expand_dims({'year': 1})

    dhwMax = xr.concat([dhwMax, dhwMax0], dim="year")

dhwMax.attrs = dict(description='Ensemble maximum value of the Degree Heating Week of the year',
                    longname='Degree Heating Week', units='degC.week',
                    comment='this ensemble corresponds to the {0} scenario'.format(scenario))


dhwMax.to_netcdf(os.path.join(outDir, (scenario + "_ensemble.nc")))




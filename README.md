# Check NetCDF program repository

This program is used to check netcdf files, their integrity and inspect their variables.

## Install

~~~bash
$ ./install.bash
~~~

## Activate environment

~~~bash
$ source .venvj/bin/activate
~~~

## To use

~~~bash
$ python check_nc.py <file.nc> [--var <name_variable>] [--minmax] [--xarray] [--check]

--var <name_variable>     : variable to be inspected.
--check                   : only checks file integrity.
--minmax		  : variable to be inspected with minimum and maximum values calculated.
--xarray		  : variable to be inspected with minimum and maximum values calculated with xarray method.
~~~

## Versions

0.2.0 - Add: '--minmax' flag for Min e Max values and '--xarray' for method using xarray import. 
0.1.0 - First version

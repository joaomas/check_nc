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
$ python check_nc.py <file.nc> [--var <name_variable>] [--check]

--var <name_variable>     : variable to be inspected
--check                   : only checks file integrity
~~~

## Versions

0.1.0 - First version

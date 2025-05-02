from django.contrib.gis import gdal
from django.contrib.gis import geos

print("GDAL Version:", gdal.gdal_version())
print("GEOS Version:", geos.geos_version())

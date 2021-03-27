---
title: 'eemont: A Python package that extends Google Earth Engine'
tags:
  - Python
  - Google Earth Engine
  - Remote Sensing
  - GIS
  - R
authors:
  - name: David Montero
    orcid: 0000-0002-9010-3286
    affiliation: "1"
affiliations:
 - name: Independent Researcher
   index: 1
date: 26 March 2021
bibliography: paper.bib
---

# Summary

[Google Earth Engine](https://earthengine.google.com/) is a cloud-based service for geospatial processing of vector and raster data [@Gorelick2017].
The Earth Engine platform has a [JavaScript and a Python API](https://developers.google.com/earth-engine/guides) with different methods to process geospatial objects.
Google Earth Engine also provides a [huge petabyte-scale catalog](https://developers.google.com/earth-engine/datasets/) of raster and vector data that users can process online
(e.g. Landsat Missions Image Collections, Sentinel Missions Image Collections, MODIS Products Image Collections, World Database of Protected Areas, etc.).
The eemont package extends the [Google Earth Engine Python API](https://developers.google.com/earth-engine/guides/python_install) with pre-processing and processing tools
for the most used satellite platforms (e.g. Sentinel, Landsat and MODIS) by adding new methods for different
[Earth Engine Objects](https://developers.google.com/earth-engine/guides/objects_methods_overview) that are friendly with the Python method chaining. The package
can be used with [geemap](https://geemap.org/) [@Wu2020] for interactive visualization and it can be used in R with [rgee](https://github.com/r-spatial/rgee) [@Aybar2020].

# Statement of need

The eemont python package extends the following Earth Engine classes:

- [ee.Feature](https://developers.google.com/earth-engine/guides/features)
- [ee.FeatureCollection](https://developers.google.com/earth-engine/guides/feature_collections)
- [ee.Geometry](https://developers.google.com/earth-engine/guides/geometries)
- [ee.Image](https://developers.google.com/earth-engine/guides/image_overview)
- [ee.ImageCollection](https://developers.google.com/earth-engine/guides/ic_creating)

New utility methods and constructors are added to above-mentioned classes in order to create a more fluid code by being friendly with the Python method chaining.
The added methods are mandatory for pre-processing and processing tasks (e.g. clouds masking, shadows masking, image scaling, spectral indices computation, time series, etc.),
and they are presented as simple functions that give researchers, students and analysts the chance to process large numbers of geospatial objects with far fewer lines of code,
improving code-writing and giving ready-to-analyze geospatial data. The following chunk shows an example of the simple usage of eemont:

```python
import ee, eemont

ee.Authenticate()
ee.Initialize()

point = ee.Geometry.Point([-74.0592,11.3172])

S2 = (ee.ImageCollection('COPERNICUS/S2_SR')
    .filterBounds(point)
    .closest('2020-10-15') # Extended (pre-processing)
    .maskClouds(prob = 70) # Extended (pre-processing)
    .scale() # Extended (pre-processing)
    .index(['NDVI','NDWI','BAIS2'])) # Extended (processing)
```

# Compatibility with R

The eemont python package can be used in R with [rgee](https://github.com/r-spatial/rgee) by using the [reticulate](https://rstudio.github.io/reticulate/) package [@Ushey2021].
This compatibility increases the number of researchers who can use the eemont functionalities by using a different programming language.
The following chunk shows the eemont configuration and usage for R:

```r
library(rgee)
library(reticulate)

ee_Initialize()

py_install("eemont",pip = TRUE)

eemont <- import("eemont")

point <- ee$Geometry$Point(c(-74.0592,11.3172))
L8 <- ee$ImageCollection('LANDSAT/LC08/C01/T1_SR')$filterBounds(point)
L8 <- L8$maskClouds()$scale()$index("NDWI")
```

# Acknowledgements

The author would like to thank the Google Earth Engine team, Qiusheng Wu and César Aybar for their big contribution to the GEE community.

# References
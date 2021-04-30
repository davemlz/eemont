---
title: 'eemont: A Python package that extends Google Earth Engine'
tags:
  - Python
  - Google Earth Engine
  - Remote Sensing
  - GIS
  - QGIS
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
can be used with [geemap](https://geemap.org/) [@Wu2020] for interactive visualization in Jupyter Notebooks, with the
[Google Earth Engine Plugin for QGIS](https://gee-community.github.io/qgis-earthengine-plugin/) for processing and visualization inside [QGIS](https://www.qgis.org/es/site/) [@QGIS_software], and it can be used in R with [rgee](https://github.com/r-spatial/rgee) [@Aybar2020].

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
improving code-writing and giving ready-to-analyze geospatial data.

The following chunk shows an example of the required code in order to pre-process and process the Landsat-8
Surface Reflectance Image Collection using the Google Earth Engine Python API:

```python
import ee

ee.Authenticate()
ee.Initialize()

point = ee.Geometry.Point([-74.0592,11.3172])

def maskClouds(img):
    cloudShadowBitMask = (1 << 3)
    cloudsBitMask = (1 << 5)
    qa = img.select('pixel_qa')
    cloudShadowMask = qa.bitwiseAnd(cloudShadowBitMask).eq(0)
    cloudMask = qa.bitwiseAnd(cloudsBitMask).eq(0)
    mask = cloudShadowMask.And(cloudMask)
    return image.updateMask(mask)

def scaleImage(img):
    sc = img.select('B[1-7]').multiply(0.0001)
    sc = sc.addBands(img.select(['B10','B11']).multiply(0.1))
    sc = sc.addBands(img.select(['sr_aerosol','pixel_qa','radsat_qa']))
    return sc.copyProperties(img,img.propertyNames())

def addIndices(img):
    NDVI = img.normalizedDifference(['B5','B4']).rename('NDVI')
    imgDict = {
        'N': img.select('B5'),
        'R': img.select('B4'),
        'B': img.select('B2')
    }
    formula = '2.5 * (N - R) / (N + 6.0 * R - 7.5 * B + 1.0)'
    EVI = img.expression(formula,imgDict).rename('EVI')
    GNDVI = img.normalizedDifference(['B5','B3']).rename('GNDVI')
    return img.addBands([NDVI,EVI,GNDVI])

L8 = (ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
    .filterBounds(point)
    .map(maskClouds)
    .map(scaleImage)
    .map(addIndices)
```

The above 39 lines of code can be simplified to 9 lines of code using eemont, which supports method chaining:

```python
import ee, eemont

ee.Authenticate()
ee.Initialize()

L8 = (ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
    .maskClouds()
    .scale()
    .index(['NDVI','EVI','GNDVI']))
```

These methods support multiple datasets of the [Google Earth Engine STAC](https://earthengine-stac.storage.googleapis.com/catalog/catalog.json)
and can be coupled with additional packages built on top of the Google Earth Engine Python API such as [geemap](https://geemap.org/),
[geetools](https://github.com/gee-community/gee_tools) [@Principe2021] and [restee](https://kmarkert.github.io/restee/) [@Markert2021], extending and simplifying the
use of Google Earth Engine.

# Google Earth Engine Community: Developer Resources

The eemont package is featured in the [Google Earth Engine Community: Developer Resources](https://developers.google.com/earth-engine/tutorials/community/developer-resources))
together with a curated list of resources developed by the Google Earth Engine developer community, and works as one of the modules that simplify workflows,
extending the Earth Engine Python API for the Earth Engine community.

# Compatibility with QGIS

The eemont python package can be used in QGIS with the [Google Earth Engine Plugin for QGIS](https://gee-community.github.io/qgis-earthengine-plugin/) by installing the package
using the OSGeo4W Shell:

```
py3_env
python -m pip install eemont
```

After installation, eemont can be used in the Python console inside QGIS:

```python
import ee, eemont
from ee_plugin import Map

S2 = (ee.ImageCollection('COPERNICUS/S2_SR')
    .maskClouds()
    .scale()
    .index(['NDVI','EVI','GNDVI'])
    .first())

Map.addLayer(S2,{'min':0,'max':1,'bands':'NDVI'},'NDVI',True)
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

The author would like to thank the Google Earth Engine team, Justin Braaten, Qiusheng Wu, César Aybar and Gennadii Donchyts for their big contribution to the GEE community.

# References
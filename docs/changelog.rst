Changelog
============

v0.2.5
--------------

New Features
~~~~~~~~~~~~~~~~~~~~~~

- The :code:`panSharpen()` extended method for ee.Image and ee.ImageCollection classes was created.
- The :code:`matchHistogram()` extended method for ee.Image classes was created.

v0.2.4
--------------

Improvements
~~~~~~~~~~~~~~~~~~~~~~

- The :code:`maskClouds()`, :code:`spectralIndices()`, :code:`scaleAndOffset()` and :code:`preprocess()` extended methods for ee.Image and ee.ImageCollection classes now support the following platforms:
   
   - `USGS Landsat 8 Level 2, Collection 2, Tier 1 <https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C02_T1_L2>`_
   - `USGS Landsat 7 Level 2, Collection 2, Tier 1 <https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LE07_C02_T1_L2>`_

v0.2.3
--------------

Improvements
~~~~~~~~~~~~~~~~~~~~~~

- Conflicts of the :code:`__len__` Container Emulation method of the *ee.Dictionary* module were solved.

v0.2.2
--------------

New Modules
~~~~~~~~~~~~~~~~~~~~~~

- The *ee.Dictionary* module was created.

New Features
~~~~~~~~~~~~~~~~~~~~~~

- The :code:`__contains__` container emulation method was overloaded for ee.Dictionary and ee.List objects.
- The :code:`__len__` container emulation method was overloaded for ee.Dictionary, ee.List, ee.FeatureCollection and ee.ImageCollection objects.
- The :code:`__getitem__` container emulation method was overloaded for ee.Dictionary, ee.List, ee.Feature, ee.FeatureCollection, ee.Image and ee.ImageCollection objects.

v0.2.1
--------------

New Features
~~~~~~~~~~~~~~~~~~~~~~

- The :code:`LinearRingFromPlusCodes()` extended constructor for ee.Gemoetry classes was created.
- The :code:`LineStringFromPlusCodes()` extended constructor for ee.Gemoetry classes was created.
- The :code:`MultiLineStringFromPlusCodes()` extended constructor for ee.Gemoetry classes was created.
- The :code:`MultiPointFromPlusCodes()` extended constructor for ee.Gemoetry classes was created.
- The :code:`MultiPolygonFromPlusCodes()` extended constructor for ee.Gemoetry classes was created.
- The :code:`PointFromPlusCode()` extended constructor for ee.Gemoetry classes was created.
- The :code:`PolygonFromPlusCodes()` extended constructor for ee.Gemoetry classes was created.
- The :code:`RectangleFromPlusCodes()` extended constructor for ee.Gemoetry classes was created.
- The :code:`plusCodes()` extended method for ee.Gemoetry and ee.Feature classes was created.

v0.2.0
--------------

New Modules
~~~~~~~~~~~~~~~~~~~~~~

- The *ee.Number* module was created.
- The *ee.List* module was created.
- The *extending* module was created.

New Features
~~~~~~~~~~~~~~~~~~~~~~

- The :code:`getOffsetParams()` extended method for ee.Image and ee.ImageCollection classes was created.
- The :code:`getScaleParams()` extended method for ee.Image and ee.ImageCollection classes was created.
- The :code:`scaleAndOffset()` extended method for ee.Image and ee.ImageCollection classes was created and will replace the :code:`scale()` method.
- The :code:`spectralIndices()` extended method for ee.Image and ee.ImageCollection classes was created and will replace the :code:`index()` method.
- The :code:`preprocess()` extended method for ee.Image and ee.ImageCollection classes was created.
- The :code:`getDOI()` extended method for ee.Image and ee.ImageCollection classes was created.
- The :code:`getCitation()` extended method for ee.Image and ee.ImageCollection classes was created.
- The :code:`getSTAC()` extended method for ee.Image and ee.ImageCollection classes was created.
- The binary operators (+, -, \*\, /, //, %, \**\ , <<, >>, &, |) were overloaded for ee.Number objects.
- The binary operators (+, \*\) were overloaded for ee.List objects.
- The rich comparisons (<, <=, ==, !=, >, >=) were overloaded for ee.Number objects.
- The unary operators (-, ~) were overloaded for ee.Number objects.

Improvements
~~~~~~~~~~~~~~~~~~~~~~

- The :code:`maskClouds()` extended method for ee.Image and ee.ImageCollection classes now supports the following platforms:
   
   - `VNP09GA: VIIRS Surface Reflectance Daily 500m and 1km <https://developers.google.com/earth-engine/datasets/catalog/NOAA_VIIRS_001_VNP09GA?hl=en>`_
   - `VNP13A1: VIIRS Vegetation Indices 16-Day 500m <https://developers.google.com/earth-engine/datasets/catalog/NOAA_VIIRS_001_VNP13A1?hl=en>`_
- The :code:`scaleAndOffset()` extended method for ee.Image and ee.ImageCollection classes now supports ALL raster datasets from the `Google Earth Engine STAC Catalog <https://developers.google.com/earth-engine/datasets>`_.
- The :code:`spectralIndices()` extended method for ee.Image and ee.ImageCollection classes now supports ALL indices from the `Awesome List of Spectral Indices for Google Earth Engine <https://github.com/davemlz/awesome-ee-spectral-indices>`_.
   
Pending Deprecation
~~~~~~~~~~~~~~~~~~~~~~

- The :code:`index()` method for ee.Image and ee.ImageCollection classes will be deprecated in future versions.
- The :code:`scale()` method for ee.Image and ee.ImageCollection classes will be deprecated in future versions.

v0.1.9
--------------

Improvements
~~~~~~~~~~~~~~~~~~~~~~

- :code:`kernel`, :code:`sigma`, :code:`p` and :code:`c` parameters were added to the :code:`index()` extended method for ee.Image and ee.ImageCollection classes.
- The following vegetation indices were added to the :code:`index()` extended method for ee.Image and ee.ImageCollection:

   - 'GARI' : Green Atmospherically Resistant Vegetation Index.
   - 'GEMI' : Global Environment Monitoring Index.
   - 'GLI' : Green Leaf Index.
   - 'GVMI' : Global Vegetation Moisture Index.
   - 'VARI' : Visible Atmospherically Resistant Index.
- The following drought indices were added to the :code:`index()` extended method for ee.Image and ee.ImageCollection:

   - 'NDDI' : Normalized Difference Drought Index.
- The following kernel indices were added to the :code:`index()` extended method for ee.Image and ee.ImageCollection:

   - 'kEVI' : Kernel Enhanced Vegetation Index.
   - 'kNDVI' : Kernel Normalized Difference Vegetation Index.
   - 'kRVI' : Kernel Ratio Vegetation Index.
   - 'kVARI' : Kernel Visible Atmospherically Resistant Index.

v0.1.8
--------------

New Modules
~~~~~~~~~~~~~~~~~~~~~~

- The *ee.Feature* module was created.
- The *ee.FeatureCollection* module was created.
- The *ee.Geometry* module was created.

New Features
~~~~~~~~~~~~~~~~~~~~~~

- The :code:`getTimeSeriesByRegion()` extended method for ee.ImageCollection classes was created.
- The :code:`getTimeSeriesByRegions()` extended method for ee.ImageCollection classes was created.
- The :code:`indices()` function was created.
- The :code:`listIndices()` function was created.
- The :code:`BBoxFromQuery()` extended constructor for ee.Geometry and ee.Feature classes was created.
- The :code:`PointFromQuery()` extended constructor for ee.Geometry and ee.Feature classes was created.
- The :code:`MultiPointFromQuery()` extended constructor for ee.Geometry and ee.FeatureCollection classes was created.


Improvements
~~~~~~~~~~~~~~~~~~~~~~

- The :code:`index()` extended method for ee.Image and ee.ImageCollection classes now supports the following platforms:
   
   - `MCD43A4.006 MODIS Nadir BRDF-Adjusted Reflectance Daily 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MCD43A4>`_
   - `MOD09GQ.006 Terra Surface Reflectance Daily Global 250m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD09GQ>`_
   - `MOD09GA.006 Terra Surface Reflectance Daily Global 1km and 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD09GA>`_
   - `MOD09Q1.006 Terra Surface Reflectance 8-Day Global 250m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD09Q1>`_
   - `MOD09A1.006 Terra Surface Reflectance 8-Day Global 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD09A1>`_
   - `MYD09GQ.006 Aqua Surface Reflectance Daily Global 250m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MYD09GQ>`_
   - `MYD09GA.006 Aqua Surface Reflectance Daily Global 1km and 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MYD09GA>`_
   - `MYD09Q1.006 Aqua Surface Reflectance 8-Day Global 250m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MYD09Q1>`_
   - `MYD09A1.006 Aqua Surface Reflectance 8-Day Global 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MYD09A1>`_
- The :code:`maskClouds()` extended method for ee.Image and ee.ImageCollection classes now supports the following platforms:
   
   - `MYD09GA.006 Aqua Surface Reflectance Daily Global 1km and 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MYD09GA>`_
   - `MYD09Q1.006 Aqua Surface Reflectance 8-Day Global 250m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MYD09Q1>`_
   - `MYD09A1.006 Aqua Surface Reflectance 8-Day Global 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MYD09A1>`_   
   - `MYD17A2H.006: Aqua Gross Primary Productivity 8-Day Global 500M 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MYD17A2H>`_   
   - `MYD13Q1.006 Aqua Vegetation Indices 16-Day Global 250m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MYD13Q1>`_
   - `MYD13A1.006 Aqua Vegetation Indices 16-Day Global 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MYD13A1>`_
   - `MYD13A2.006 Aqua Vegetation Indices 16-Day Global 1km <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MYD13A2>`_
- The :code:`scale()` extended method for ee.Image and ee.ImageCollection classes now supports the following platforms:
   
   - `MYD09GQ.006 Aqua Surface Reflectance Daily Global 250m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MYD09GQ>`_
   - `MYD09GA.006 Aqua Surface Reflectance Daily Global 1km and 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MYD09GA>`_
   - `MYD09Q1.006 Aqua Surface Reflectance 8-Day Global 250m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MYD09Q1>`_
   - `MYD09A1.006 Aqua Surface Reflectance 8-Day Global 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MYD09A1>`_
   - `MYD10A1.006 Aqua Snow Cover Daily Global 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MYD10A1>`_
   - `MYD11A1.006 Aqua Land Surface Temperature and Emissivity Daily Global 1km <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MYD11A1>`_
   - `MYD11A2.006 Aqua Land Surface Temperature and Emissivity 8-Day Global 1km <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MYD11A2>`_
   - `MYDOCGA.006 Aqua Ocean Reflectance Daily Global 1km <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MYDOCGA>`_
   - `MYD14A1.006: Aqua Thermal Anomalies & Fire Daily Global 1km <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MYD14A1>`_   
   - `MYD17A2H.006: Aqua Gross Primary Productivity 8-Day Global 500M 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MYD17A2H>`_
   - `MYD17A3HGF.006: Aqua Net Primary Production Gap-Filled Yearly Global 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MYD17A3HGF>`_   
   - `MYD13Q1.006 Aqua Vegetation Indices 16-Day Global 250m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MYD13Q1>`_
   - `MYD13A1.006 Aqua Vegetation Indices 16-Day Global 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MYD13A1>`_
   - `MYD13A2.006 Aqua Vegetation Indices 16-Day Global 1km <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MYD13A2>`_
   - `MYD08_M3.061 Aqua Atmosphere Monthly Global Product <https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MYD08_M3>`_
- The following vegetation indices were added to the :code:`index()` extended method for ee.Image and ee.ImageCollection:

   - 'EVI2' : Two-Band Enhanced Vegetation Index.
   
- The following burn indices were added to the :code:`index()` extended method for ee.Image and ee.ImageCollection:

   - 'CSIT' : Char Soil Index Thermal.
   - 'NBRT' : Normalized Burn Ratio Thermal.
   - 'NDVIT' : Normalized Difference Vegetation Index Thermal
   - 'SAVIT' : Soil-Adjusted Vegetation Index Thermal.

v0.1.7
--------------

New Modules
~~~~~~~~~~~~~~~~~~~~~~

- The *pd.DataFrame* module was created.
- The *common* module was created (it feeds the :code:`index()`, :code:`scale()` and :code:`maskClouds()` methods for both ee.Image and ee.ImageCollection).

New Features
~~~~~~~~~~~~~~~~~~~~~~

- The :code:`toEEFeatureCollection()` extended method for pd.DataFrame classes was created.
- The binary operators (+, -, \*\, /, //, %, \**\ , <<, >>, &, |) were overloaded for ee.Image objects.
- The rich comparisons (<, <=, ==, !=, >, >=) were overloaded for ee.Image objects.
- The unary operators (-, ~) were overloaded for ee.Image objects.

Improvements
~~~~~~~~~~~~~~~~~~~~~~

- *Exceptions* and *Warnings* were added to most methods.
- Conflicts between the Gain factor and the Green band in the :code:`index()` method were solved.
- :code:`tolerance` and :code:`unit` parameters were added to the :code:`closest()` extended method for ee.ImageCollection classes.
- The :code:`maskClouds()` extended method for ee.Image and ee.ImageCollection classes now supports the following platforms:

   - `Sentinel-3 OLCI EFR: Ocean and Land Color Instrument Earth Observation Full Resolution <https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S3_OLCI>`_
   - `MOD09GA.006 Terra Surface Reflectance Daily Global 1km and 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD09GA>`_
   - `MOD09Q1.006 Terra Surface Reflectance 8-Day Global 250m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD09Q1>`_
   - `MOD09A1.006 Terra Surface Reflectance 8-Day Global 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD09A1>`_
   - `MCD15A3H.006 MODIS Leaf Area Index/FPAR 4-Day Global 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MCD15A3H>`_
   - `MOD17A2H.006: Terra Gross Primary Productivity 8-Day Global 500M 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD17A2H>`_
   - `MOD16A2.006: Terra Net Evapotranspiration 8-Day Global 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD16A2>`_
   - `MOD13Q1.006 Terra Vegetation Indices 16-Day Global 250m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD13Q1>`_
   - `MOD13A1.006 Terra Vegetation Indices 16-Day Global 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD13A1>`_
   - `MOD13A2.006 Terra Vegetation Indices 16-Day Global 1km <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD13A2>`_
- The :code:`scale()` extended method for ee.Image and ee.ImageCollection classes now supports the following platforms:

   - `Sentinel-3 OLCI EFR: Ocean and Land Color Instrument Earth Observation Full Resolution <https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S3_OLCI>`_
   - `MCD43A4.006 MODIS Nadir BRDF-Adjusted Reflectance Daily 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MCD43A4>`_
   - `MCD43A3.006 MODIS Albedo Daily 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MCD43A3>`_
   - `MOD09GQ.006 Terra Surface Reflectance Daily Global 250m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD09GQ>`_
   - `MOD09GA.006 Terra Surface Reflectance Daily Global 1km and 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD09GA>`_
   - `MOD09Q1.006 Terra Surface Reflectance 8-Day Global 250m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD09Q1>`_
   - `MOD09A1.006 Terra Surface Reflectance 8-Day Global 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD09A1>`_
   - `MOD10A1.006 Terra Snow Cover Daily Global 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD10A1>`_
   - `MOD11A1.006 Terra Land Surface Temperature and Emissivity Daily Global 1km <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD11A1>`_
   - `MOD11A2.006 Terra Land Surface Temperature and Emissivity 8-Day Global 1km <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD11A2>`_
   - `MODOCGA.006 Terra Ocean Reflectance Daily Global 1km <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MODOCGA>`_
   - `MOD14A1.006: Terra Thermal Anomalies & Fire Daily Global 1km <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD14A1>`_
   - `MCD43A1.006 MODIS BRDF-Albedo Model Parameters Daily 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MCD43A1>`_
   - `MCD15A3H.006 MODIS Leaf Area Index/FPAR 4-Day Global 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MCD15A3H>`_
   - `MOD17A2H.006: Terra Gross Primary Productivity 8-Day Global 500M 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD17A2H>`_
   - `MOD17A3HGF.006: Terra Net Primary Production Gap-Filled Yearly Global 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD17A3HGF>`_
   - `MOD16A2.006: Terra Net Evapotranspiration 8-Day Global 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD16A2>`_
   - `MOD13Q1.006 Terra Vegetation Indices 16-Day Global 250m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD13Q1>`_
   - `MOD13A1.006 Terra Vegetation Indices 16-Day Global 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD13A1>`_
   - `MOD13A2.006 Terra Vegetation Indices 16-Day Global 1km <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD13A2>`_
   - `MOD08_M3.061 Terra Atmosphere Monthly Global Product <https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MOD08_M3>`_
- The following vegetation indices were added to the :code:`index()` extended method for ee.Image and ee.ImageCollection:

   - 'GBNDVI' : Green-Blue Normalized Difference Vegetation Index.
   - 'GRNDVI' : Green-Red Normalized Difference Vegetation Index.
   - 'MNDVI' : Modified Normalized Difference Vegetation Index.
- The following snow indices were added to the :code:`index()` extended method for ee.Image and ee.ImageCollection:

   - 'NDSI' : Normalized Difference Snow Index.
- The 'SR' vegetation index was replaced by 'RVI' in the :code:`index()` extended method for ee.Image and ee.ImageCollection.
Changelog
============

v0.1.7
--------------

New Modules
~~~~~~~~~~~~~~~~~~~~~~

- The *pd.DataFrame* module was created.
- The *common* module was created (it feeds the :code:`index()`, :code:`scale()` and :code:`maskClouds()` methods for both ee.Image and ee.ImageCollection).

New Features
~~~~~~~~~~~~~~~~~~~~~~

- The :code:`toFeatureCollection()` extended method for pd.DataFrame classes was created.

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
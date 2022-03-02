Time Series By Regions
====================================

Let's see how to extract time series by region (or regions) with eemont!

Before anything, let's import our modules and authenticate in Google Earth Engine:

.. code-block:: python

   import ee, eemont, geemap
   import pandas as pd
   import numpy as np
   
   ee.Authenticate()
   ee.Initialize()

Now, we are ready to go!

Overview
-----------

The eemont package extends the ee.ImageCollection classes with the methods :code:`getTimeSeriesByRegion()` and :code:`getTimeSeriesByRegions()`:
    
ee.ImageCollection
~~~~~~~~~~~~~~~~~~~~~~~~

.. currentmodule:: eemont.imagecollection

.. autosummary::

   getTimeSeriesByRegion
   getTimeSeriesByRegions
   
Usage
------------------

The :code:`getTimeSeriesByRegion()` and :code:`getTimeSeriesByRegions()` methods extract time series by region (or regions) according to the specified ee.Geometry, ee.Feature or ee.FeatureCollection.

Let's create an ee.FeatureCollection as example (two crops in France with two identifiers: A and B):

.. code-block:: python

   f1 = ee.Feature(ee.Geometry.Point([3.984770,48.767221]).buffer(50),{'ID':'A'})
   f2 = ee.Feature(ee.Geometry.Point([4.101367,48.748076]).buffer(50),{'ID':'B'})
   fc = ee.FeatureCollection([f1,f2])

Let's take the Sentinel-2 SR image collection as example (compute NDVI and EVI to extract their values):

.. code-block:: python

   S2 = (ee.ImageCollection('COPERNICUS/S2_SR')
      .filterBounds(fc)
      .filterDate('2020-01-01','2021-01-01')
      .maskClouds()
      .scale()
      .index(['EVI','NDVI']))

Time Series By Region
~~~~~~~~~~~~~~~~~~~~~~~~

Let's assume that we want the mean of all pixels inside our collection as a single geometry. In that case, we'll use the :code:`getTimeSeriesByRegion()`:

.. code-block:: python

   ts = S2.getTimeSeriesByRegion(reducer = ee.Reducer.mean(),
                                 geometry = fc,
                                 bands = ['EVI','NDVI'],
                                 scale = 10)
                                 
Here, we are extracting the EVI and NDVI time series from the S2 collection by the geometry of our feature collection. If required, we can use more than one reducer:

.. code-block:: python

   ts = S2.getTimeSeriesByRegion(reducer = [ee.Reducer.mean(),ee.Reducer.median()],
                                 geometry = fc,
                                 bands = ['EVI','NDVI'],
                                 scale = 10)
                                 
Now we are not extracting just the mean values, but also the median values. A column named :code:`reducer` is created indicating the corresponding reducer.

We can also add arguments that are valid for the :code:`reduceRegion()` method:

.. code-block:: python

   ts = S2.getTimeSeriesByRegion(reducer = [ee.Reducer.mean(),ee.Reducer.median()],
                                 geometry = fc,
                                 bands = ['EVI','NDVI'],
                                 scale = 10,
                                 bestEffort = True,
                                 maxPixels = 1e13,
                                 tileScale = 2)

By default, the output date column is named :code:`reducer`, but it can be modified:

.. code-block:: python

   ts = S2.getTimeSeriesByRegion(reducer = [ee.Reducer.mean(),ee.Reducer.median()],
                                 geometry = fc,
                                 bands = ['EVI','NDVI'],
                                 scale = 10,
                                 dateColumn = 'my_date_column')
                                 
The date value is by default retrieved in the Standard ISO format, but it can be changed by :code:`ms` (milliseconds) or any other format:

.. code-block:: python

   ts = S2.getTimeSeriesByRegion(reducer = [ee.Reducer.mean(),ee.Reducer.median()],
                                 geometry = fc,
                                 bands = ['EVI','NDVI'],
                                 scale = 10,
                                 dateFormat = 'YYYYMMdd')

When the region is masked and the reducer doesn't retrieve any value, a NA value of :code:`-9999` is used, but if required, it can be modified: 

.. code-block:: python

   ts = S2.getTimeSeriesByRegion(reducer = [ee.Reducer.mean(),ee.Reducer.median()],
                                 geometry = fc,
                                 bands = ['EVI','NDVI'],
                                 scale = 10,
                                 naValue = -9999999)
                                 
Time Series By Regions
~~~~~~~~~~~~~~~~~~~~~~~~

Now, if we want a time series by each feature in our feature collection, we require the :code:`getTimeSeriesByRegions()` method:

.. code-block:: python

   ts = S2.getTimeSeriesByRegions(reducer = [ee.Reducer.mean(),ee.Reducer.median()],
                                  collection = fc,
                                  bands = ['EVI','NDVI'],
                                  scale = 10)

The same parameters of the :code:`getTimeSeriesByRegion()` method can be used here, except for :code:`bestEffort` and :code:`maxPixels`:

.. code-block:: python

   ts = S2.getTimeSeriesByRegions(reducer = [ee.Reducer.mean(),ee.Reducer.median()],
                                  collection = fc,
                                  bands = ['EVI','NDVI'],
                                  scale = 10,
                                  naValue = -99999999,
                                  dateColumn = 'my_date_colum',
                                  dateFormat = 'ms')
                                  
Conversion to Pandas
~~~~~~~~~~~~~~~~~~~~~~~~

The time series is always retrieved as an ee.FeatureCollection. To convert the collection to a pandas data frame, we'll use the geemap package:

.. code-block:: python

   tsPandas = geemap.ee_to_pandas(ts)
   
Then we can convert the NA value to a real NA and the date column to a datetime class:

.. code-block:: python

   tsPandas[tsPandas == -9999] = np.nan
   tsPandas['date'] = pd.to_datetime(tsPandas['date'],infer_datetime_format = True)
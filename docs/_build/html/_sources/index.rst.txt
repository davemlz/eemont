Welcome to eemont!
==================

.. toctree::   
   :maxdepth: 2
   :caption: Documentation 
   :hidden:
      
   classes/eeimage
   classes/eeimagecollection
   classes/pddataframe
   
.. toctree::
   :maxdepth: 2
   :caption: User Guide      
   :hidden:
   
   guide/overloadedOperators
   guide/closestImage
   guide/maskingClouds
   guide/imageScaling
   guide/spectralIndices
   guide/dataConversion
   
.. toctree::
   :maxdepth: 2
   :caption: What's new? 
   :hidden:
      
   changelog

The eemont package extends Google Earth Engine with pre-processing and processing tools for the most used satellite platforms.

Look at this simple example where a Sentinel-2 collection is pre-processed and processed in just one step:

.. code-block:: python

   import ee, eemont
   
   ee.Authenticate()
   ee.Initialize()
   
   point = ee.Geometry.Point([-76.21, 3.45])
   
   S2 = (ee.ImageCollection('COPERNICUS/S2_SR')
       .filterBounds(point)
       .closest('2020-10-15') # Extended (pre-processing)
       .maskClouds(prob = 70) # Extended (pre-processing)
       .scale() # Extended (pre-processing)
       .index(['NDVI','NDWI','BAIS2'])) # Extended (processing)

And just like that, the collection was pre-processed and processed!

Features
--------

The following features are extended to Google Earth Engine thorugh eemont:

- Clouds and shadows masking
- Image scaling
- Spectral indices calculation (vegetation, burn and water indices)
- Closest images to a specific date

These features extends both ee.Image and ee.ImageCollection classes:

ee.Image
~~~~~~~~

.. currentmodule:: eemont.image

.. autosummary::

   index
   maskClouds
   scale
   
ee.ImageCollection
~~~~~~~~~~~~~~~~~~~~~~~~

.. currentmodule:: eemont.imagecollection
.. autosummary::

   closest 
   index
   maskClouds
   scale

Non-Earth Engine classes such as pd.DataFrame are also extended:

pd.DataFrame
~~~~~~~~~~~~~~~~~~~~~~~~

.. currentmodule:: eemont.dataframe
.. autosummary::

   toEEFeatureCollection   

Satellite Platforms
------------------------

Some methods, like :code:`.maskClouds()` or :code:`.index()`, only accept specific platforms. The accepted platforms for all methods are:

- Sentinel 2
- Landsat 8
- Landsat 7
- Landsat 5
- Landsat 4

The method :code:`.closest()` accepts any image collection.

Installation
------------

Install the latest eemont version from PyPI by running:

    pip install eemont

Install the eemont development version by running:

    pip install git+https://github.com/davemlz/eemont

License
-------

The project is licensed under the MIT license.
eemont
========

The eemont package extends Google Earth Engine with pre-processing and processing tools for the most used satellite platforms.

Look at this simple example where a Sentinel2 collection is pre-processed and processed in just one step:

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

- Clouds and shadows masking
- Image scaling
- Spectral indices calculation (vegetation, burn and water indices)
- Closest images to a specific date

Installation
------------

Install the latest eemont version from PyPI:

    pip install eemont

Or install the eemont development version by running:

    pip install git+https://github.com/davemlz/eemont

License
-------

The project is licensed under the MIT license.
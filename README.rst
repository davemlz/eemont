eemont
========

.. image:: https://img.shields.io/pypi/v/eemont.svg
        :target: https://pypi.python.org/pypi/eemont
        
.. image:: https://img.shields.io/badge/License-MIT-blue.svg
        :target: https://opensource.org/licenses/MIT
        
.. image:: https://img.shields.io/badge/Documentation-0.1.6-green.svg
        :target: https://eemont.readthedocs.io/en/0.1.6/index.html

.. image:: https://img.shields.io/badge/Donate-buy%20me%20a%20coffee-yellow.svg
        :target: https://www.buymeacoffee.com/davemlz
        
.. image:: https://static.pepy.tech/personalized-badge/eemont?period=total&units=international_system&left_color=grey&right_color=lightgrey&left_text=Downloads
        :target: https://pepy.tech/project/eemont

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

The following features are extended to Google Earth Engine thorugh eemont:

- Clouds and shadows masking
- Image scaling
- Spectral indices calculation (vegetation, burn and water indices)
- Closest images to a specific date

Satellite Platforms
------------------------

Some methods, like :code:`.maskClouds()` or :code:`.index()`, only support specific platforms. The supported platforms for all methods are:

- Sentinel 2
- Landsat 8
- Landsat 7
- Landsat 5
- Landsat 4

The method :code:`.closest()` supports any image collection.

Installation
------------

Install the latest eemont version from PyPI by running:

    pip install eemont

Install the eemont development version by running:

    pip install git+https://github.com/davemlz/eemont

License
-------

The project is licensed under the MIT license.

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

How does it work?
----------------

Earth Engine classes, such as ee.Image and ee.ImageCollection, are extended with eemont. New methods are added to these classes to make the code more fluid.

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

Installation
------------

Install the latest eemont version from PyPI by running:

.. code-block:: python   
      
   pip install eemont

Features
--------

The following features are extended through eemont:

.. code-block:: python   
   
   point = ee.Geometry.Point([-76.21, 3.45]) # Example ROI

- Overloaded operators (+, -, \*\, /, //, %, \**\ , <<, >>, &, \|\, <, <=, ==, !=, >, >=, -, ~):

.. code-block:: python   
   
   S2 = (ee.ImageCollection('COPERNICUS/S2_SR')
       .filterBounds(point)
       .sort('CLOUDY_PIXEL_PERCENTAGE')
       .first()
       .maskClouds()
       .scale())
   
   N = S2.select('B8')
   R = S2.select('B4')
   B = S2.select('B2')
   
   EVI = 2.5 * (N - R) / (N + 6.0 * R - 7.5 * B + 1.0) # Overloaded operators

- Clouds and shadows masking:

.. code-block:: python   
   
   S2 = (ee.ImageCollection('COPERNICUS/S2_SR')
       .maskClouds(prob = 65, cdi = -0.5, buffer = 300) # Clouds and shadows masking
       .first())

- Image scaling:

.. code-block:: python   
   
   MOD13Q1 = ee.ImageCollection('MODIS/006/MOD13Q1').scale() # Image scaling

- Spectral indices computation (vegetation, burn, water and snow indices):

.. code-block:: python   
   
   L8 = (ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
       .filterBounds(point)
       .maskClouds()
       .scale()
       .index(['GNDVI','NDWI','BAI','NDSI'])) # Indices computation

- Closest image to a specific date:

.. code-block:: python   
      
   S5NO2 = (ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_NO2')
       .filterBounds(point)
       .closest('2020-10-15')) # Closest image to a date

Supported Platforms
------------------------

The Supported Platforms for each method can be found in the eemont documentation.

- Masking clouds and shadows supports Sentinel Missions (Sentinel-2 SR and Sentinel-3), Landsat Missions (SR products) and some MODIS Products. Check all details in User Guide > Masking Clouds and Shadows > Supported Platforms.
- Image scaling supports Sentinel Missions (Sentinel-2 and Sentinel-3), Landsat Missions and most MODIS Products. Check all details in User Guide > Image Scaling > Supported Platforms.
- Spectral indices computation supports Sentinel-2 and Landsat Missions. Check all details in User Guide > Spectral Indices > Supported Platforms.
- Getting the closest image to a specific date supports all image collections with the :code:`system:time_start` property.

License
-------

The project is licensed under the MIT license.

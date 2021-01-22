Closest Image to a Specific Date
====================================

Let's see how to get the closest image (or set of images) to a specific date.

Before anything, let's import our modules and authenticate in Google Earth Engine:

.. code-block:: python

   import ee, eemont
   
   ee.Authenticate()
   ee.Initialize()

Now, we are ready to go!

Overview
-----------

The eemont package extends the ee.ImageCollection class with the method :code:`closest()`:

.. currentmodule:: eemont.imagecollection

.. autosummary::

   closest

This method automatically filters any image collection to get the closest image to a specific date.

.. warning::
   This method uses the :code:`system:time_start` property, therefore, make sure your image collection has it!   

Let's check how the :code:`closest()` method works:

Usage
------------------

The :code:`closest()` method can work on any image colection that has a :code:`system:time_start` property.

First, let's take the Sentinel-2 image collection as example:

.. code-block:: python

   S2 = ee.ImageCollection('COPERNICUS/S2_SR')
   
Now, we have to filter the collection to our ROI. The result of the :code:`closest()` method will vary depending on this.
Let's assume a single point is our ROI.

.. code-block:: python

   ROI = ee.Geometry.Point([-76.45, 4.32])
   S2 = S2.filterBounds(ROI)

Now, the :code:`closest()` method has just one parameter, :code:`date`, and this parameter can be a string...

.. code-block:: python

   S2.closest('2020-10-15')
   
Or an ee.Date class:

.. code-block:: python

   dateOfInterest = ee.Date('2020-10-15')
   S2.closest(dateOfInterest)
   
Both chunks will give you the same result here: an ee.ImageCollection of size 1. The result has just one image since our ROI intersects just one scene.
To get that image as a single image, we can use the :code:`first()` method.

.. code-block:: python

   S2.closest('2020-10-15').first()
   
Now, let's assume that our ROI is larger, in this case, a whole department (state) of Colombia:

.. code-block:: python

   ROI = ee.FeatureCollection('FAO/GAUL_SIMPLIFIED_500m/2015/level1').filter(ee.Filter.eq('ADM1_NAME','Valle Del Cauca'))
   S2 = ee.ImageCollection('COPERNICUS/S2_SR').filterBounds(ROI).closest('2020-10-15')

You'll note that the size of the resulting ee.ImageCollection here is greater than 1. This result has more than one image since our ROI now intersects more than one scene.
To get those images together as a single image, you can mosaic them or use an ee.Reducer, for example :code:`median()`.

.. code-block:: python
   
   S2.median()
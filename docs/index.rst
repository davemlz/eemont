Welcome to eemont!
==================

**A Python package that extends** `Google Earth Engine <https://earthengine.google.com/>`_

.. image:: images/eemont.png        
        :align: center

.. toctree::   
   :maxdepth: 2
   :caption: Extended Classes 
   :hidden:      
   
   classes/index
   
.. toctree::
   :maxdepth: 2
   :caption: User Guide      
   :hidden:
      
   guide/index
   
.. toctree::
   :maxdepth: 2
   :caption: Other Languages     
   :hidden:
   
   guide/eemontR
   
.. toctree::
   :maxdepth: 2
   :caption: What's new? 
   :hidden:
      
   changelog
   
.. toctree::
   :maxdepth: 2
   :caption: Tutorials 
   :hidden:
      
   tutorials

Overview
-------------------

`Google Earth Engine <https://earthengine.google.com/>`_ is a cloud-based service for geospatial processing of vector and raster data. The Earth Engine platform has a `JavaScript and a Python API <https://developers.google.com/earth-engine/guides>`_ with different methods to process geospatial objects. Google Earth Engine also provides a `HUGE PETABYTE-SCALE CATALOG <https://developers.google.com/earth-engine/datasets/>`_ of raster and vector data that users can process online (e.g. Landsat Missions Image Collections, Sentinel Missions Image Collections, MODIS Products Image Collections, World Database of Protected Areas, etc.). The eemont package extends the `Google Earth Engine Python API <https://developers.google.com/earth-engine/guides/python_install>`_ with pre-processing and processing tools for the most used satellite platforms by adding utility methods for different `Earth Engine Objects <https://developers.google.com/earth-engine/guides/objects_methods_overview>`_ that are friendly with the Python method chaining.

Google Earth Engine Community: Developer Resources
-----------------------------------------------------

The eemont Python package can be found in the `Google Earth Engine Community: Developer Resources <https://developers.google.com/earth-engine/tutorials/community/developer-resources>`_ together with other awesome resources such as `geemap <https://geemap.org/>`_ and `rgee <https://github.com/r-spatial/rgee>`_.

How does it work?
-------------------

The eemont python package extends the following Earth Engine classes:

- `ee.Feature <https://developers.google.com/earth-engine/guides/features>`_
- `ee.FeatureCollection <https://developers.google.com/earth-engine/guides/feature_collections>`_
- `ee.Geometry <https://developers.google.com/earth-engine/guides/geometries>`_
- `ee.Image <https://developers.google.com/earth-engine/guides/image_overview>`_
- `ee.ImageCollection <https://developers.google.com/earth-engine/guides/ic_creating>`_

New utility methods and constructors are added to above-mentioned classes in order to create a more fluid code by being friendly with the Python method chaining. These methods are mandatory for some pre-processing and processing tasks (e.g. clouds masking, shadows masking, image scaling, spectral indices computation, etc.), and they are presented as simple functions that give researchers, students and analysts the chance to analyze data with far fewer lines of code.

Look at this simple example where a `Sentinel-2 Surface Reflectance Image Collection <https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR>`_ is pre-processed and processed in just one step:

.. code-block:: python

   import ee, eemont
   
   ee.Authenticate()
   ee.Initialize()
   
   point = ee.Geometry.PointFromQuery('Cali, Colombia',user_agent = 'eemont-example') # Extended constructor
   
   S2 = (ee.ImageCollection('COPERNICUS/S2_SR')
       .filterBounds(point)
       .closest('2020-10-15') # Extended (pre-processing)
       .maskClouds(prob = 70) # Extended (pre-processing)
       .scale() # Extended (pre-processing)
       .index(['NDVI','NDWI','BAIS2'])) # Extended (processing)

And just like that, the collection was pre-processed, processed and ready to be analyzed!

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

- Spectral indices computation (vegetation, burn, water, snow, drought and kernel indices):

.. code-block:: python   
   
   L8 = (ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
       .filterBounds(point)
       .maskClouds()
       .scale()
       .index(['GNDVI','NDWI','BAI','NDSI','kNDVI'])) # Indices computation
       
   indices = eemont.indices() 
   indices.BAIS2.formula # check info about spectral indices
   indices.BAIS2.reference
   
   eemont.listIndices() # Check all available indices

- Closest image to a specific date:

.. code-block:: python   
      
   S5NO2 = (ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_NO2')
       .filterBounds(point)
       .closest('2020-10-15')) # Closest image to a date
       
- Time series by region (or regions):

.. code-block:: python

   f1 = ee.Feature(ee.Geometry.Point([3.984770,48.767221]).buffer(50),{'ID':'A'})
   f2 = ee.Feature(ee.Geometry.Point([4.101367,48.748076]).buffer(50),{'ID':'B'})
   fc = ee.FeatureCollection([f1,f2])

   S2 = (ee.ImageCollection('COPERNICUS/S2_SR')
      .filterBounds(fc)
      .filterDate('2020-01-01','2021-01-01')
      .maskClouds()
      .scale()
      .index(['EVI','NDVI']))

   # By Region
   ts = S2.getTimeSeriesByRegion(reducer = [ee.Reducer.mean(),ee.Reducer.median()],
                                 geometry = fc,
                                 bands = ['EVI','NDVI'],
                                 scale = 10)
   
   # By Regions
   ts = S2.getTimeSeriesByRegions(reducer = [ee.Reducer.mean(),ee.Reducer.median()],
                                  collection = fc,
                                  bands = ['EVI','NDVI'],
                                  scale = 10)
                                  
- New Geometry, Feature and Feature Collection constructors:

.. code-block:: python

   seattle_bbox = ee.Geometry.BBoxFromQuery('Seattle',user_agent = 'my-eemont-query-example')
   cali_coords = ee.Feature.PointFromQuery('Cali, Colombia',user_agent = 'my-eemont-query-example')
   amazonas_river = ee.FeatureCollection.MultiPointFromQuery('Río Amazonas',user_agent = 'my-eemont-query-example')

Supported Platforms
------------------------

The Supported Platforms for each method can be found in the eemont documentation.

- Masking clouds and shadows supports Sentinel Missions (Sentinel-2 SR and Sentinel-3), Landsat Missions (SR products) and some MODIS Products. Check all details in User Guide > Masking Clouds and Shadows > Supported Platforms.
- Image scaling supports Sentinel Missions (Sentinel-2 and Sentinel-3), Landsat Missions and most MODIS Products. Check all details in User Guide > Image Scaling > Supported Platforms.
- Spectral indices computation supports Sentinel-2 and Landsat Missions. Check all details in User Guide > Spectral Indices > Supported Platforms.
- Getting the closest image to a specific date and time series supports all image collections with the :code:`system:time_start` property.

License
-------

The project is licensed under the MIT license.

Contributing
------------------

Contributions to eemont are welcome! Here you will find how to do it:

Bugs
~~~~~~~~~~~

If you find a bug, please report it by opening an issue. if possible, please attach the error, code, version, and other details.

If you want to contributte by fixing an issue, please check the eemont issues: contributions are welcome for open issues with labels :code:`bug` and :code:`help wanted`.

Enhancement
~~~~~~~~~~~

New features and modules are welcome! You can check the eemont issues: contributions are welcome for open issues with labels :code:`enhancement` and :code:`help wanted`.

Documentation
~~~~~~~~~~~~~~~~~~~~~~

You can add examples, notes and references to the eemont documentation by using the NumPy Docstrings of the eemont documentation, or by creating blogs, tutorials or papers.

Contribution Steps
---------------------

First, fork the `eemont <https://github.com/davemlz/eemont>`_ repository and clone it to your local machine. Then, create a development branch::

   git checkout -b name-of-dev-branch
   
eemont is divided according to Earth Engine classes, and you will find a module for each class (e.g. :code:`imagecollection.py`). Look for the required class as follows:

- ee.Feature: :code:`feature.py`
- ee.FeatureCollection: :code:`featurecollection.py`
- ee.Geometry: :code:`geometry.py`
- ee.Image: :code:`image.py`
- ee.ImageCollection: :code:`imagecollection.py`

The :code:`common.py` is used for methods that can be used for more than one Earth Engine class.

When creating new features, please start with the :code:`self` argument and add the corresponding decorator (e.g. :code:`@_extend_eeImageCollection()`). Check this example:

.. code-block:: python

   @_extend_eeImage()
   def my_new_method(self,other):
        '''Returns the addition of and image and a float.
    
        Parameters
        ----------    
        self : ee.Image [this]
            Image to add.
        other : float
            Float to add.

        Returns
        -------    
        ee.Image
            Addition of an ee.Image and a float.

        Examples
        --------
        >>> import ee, eemont
        >>> ee.Initialize()
        >>> img = ee.Image(0).my_new_method(other = 3.14)
        '''
        return self.add(other)
        
By using the :code:`@_extend_eeImage()` decorator, the :code:`my_new_method()` method is added to the :code:`ee.Image` class. Look for the required decorator as follows:

- ee.Feature: :code:`@_extend_eeFeature()`
- ee.FeatureCollection: :code:`@_extend_eeFeatureCollection()`
- ee.Geometry: :code:`@_extend_eeGeometry()`
- ee.Image: :code:`@_extend_eeImage()`
- ee.ImageCollection: :code:`@_extend_eeImageCollection()`
   
In order to test additions, you can use :code:`pytest` over the :code:`tests` folder::

   pytest tests
   
This will autmatically test all modules for the available satellite platforms through eemont. If you have added a new feature, please include it in the tests.

To test across different Python versions, please use :code:`tox`.

Now it's time to commit your changes and push your development branch::

   git add .
   git commit -m "Description of your work"
   git push origin name-of-dev-branch
  
And finally, submit a pull request.
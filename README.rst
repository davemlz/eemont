eemont
======

**A Python package that extends** `Google Earth Engine <https://earthengine.google.com/>`_

.. image:: https://img.shields.io/pypi/v/eemont.svg
        :target: https://pypi.python.org/pypi/eemont
        
.. image:: https://img.shields.io/conda/vn/conda-forge/eemont.svg
        :target: https://anaconda.org/conda-forge/eemont
        
.. image:: https://img.shields.io/badge/License-MIT-blue.svg
        :target: https://opensource.org/licenses/MIT
        
.. image:: https://readthedocs.org/projects/eemont/badge/?version=latest
        :target: https://eemont.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://github.com/davemlz/eemont/actions/workflows/tests.yml/badge.svg
        :target: https://github.com/davemlz/eemont/actions/workflows/tests.yml  

.. image:: https://img.shields.io/badge/GitHub%20Sponsors-Donate-ff69b4.svg
        :target: https://github.com/sponsors/davemlz

.. image:: https://img.shields.io/badge/Buy%20me%20a%20coffee-Donate-ff69b4.svg
        :target: https://www.buymeacoffee.com/davemlz
        
.. image:: https://img.shields.io/badge/kofi-Donate-ff69b4.svg
        :target: https://ko-fi.com/davemlz
        
.. image:: https://static.pepy.tech/personalized-badge/eemont?period=total&units=international_system&left_color=grey&right_color=green&left_text=Downloads
        :target: https://pepy.tech/project/eemont
        
.. image:: https://img.shields.io/badge/GEE%20Community-Developer%20Resources-00b6ff.svg
        :target: https://developers.google.com/earth-engine/tutorials/community/developer-resources
        
.. image:: https://img.shields.io/twitter/follow/dmlmont?style=social
        :target: https://twitter.com/dmlmont
        
.. image:: https://joss.theoj.org/papers/34696c5b62c50898b4129cbbe8befb0a/status.svg
    :target: https://joss.theoj.org/papers/34696c5b62c50898b4129cbbe8befb0a
        
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black


- GitHub: `https://github.com/davemlz/eemont <https://github.com/davemlz/eemont>`_
- Documentation: `https://eemont.readthedocs.io/ <https://eemont.readthedocs.io/>`_
- PyPI: `https://pypi.org/project/eemont/ <https://pypi.org/project/eemont/>`_
- Conda-Forge: `https://anaconda.org/conda-forge/eemont <https://anaconda.org/conda-forge/eemont>`_
- Tutorials: `https://github.com/davemlz/eemont/tree/master/tutorials <https://github.com/davemlz/eemont/tree/master/tutorials>`_

**Table of Contents**

- `Overview`_
- `Google Earth Engine Community: Developer Resources`_
- `Additional Resources`_
- `How does it work?`_
- `Installation`_
- `Features`_
- `Supported Platforms`_
- `License`_
- `Contributing`_
- `How to cite`_
- `Artists`_
- `Credits`_

Overview
-------------------

`Google Earth Engine <https://earthengine.google.com/>`_ is a cloud-based service for geospatial processing of vector and raster data. The Earth Engine platform has a `JavaScript and a Python API <https://developers.google.com/earth-engine/guides>`_ with different methods to process geospatial objects. Google Earth Engine also provides a `HUGE PETABYTE-SCALE CATALOG <https://developers.google.com/earth-engine/datasets/>`_ of raster and vector data that users can process online (e.g. Landsat Missions Image Collections, Sentinel Missions Image Collections, MODIS Products Image Collections, World Database of Protected Areas, etc.). The eemont package extends the `Google Earth Engine Python API <https://developers.google.com/earth-engine/guides/python_install>`_ with pre-processing and processing tools for the most used satellite platforms by adding utility methods for different `Earth Engine Objects <https://developers.google.com/earth-engine/guides/objects_methods_overview>`_ that are friendly with the Python method chaining.

Google Earth Engine Community: Developer Resources
-----------------------------------------------------

The eemont Python package can be found in the `Earth Engine Community: Developer Resources <https://developers.google.com/earth-engine/tutorials/community/developer-resources>`_ together with other awesome resources such as `geemap <https://geemap.org/>`_ and `rgee <https://github.com/r-spatial/rgee>`_.

Additional Resources
--------------------

If you like eemont, you might be interested in...

- `Awesome Spectral Indices for GEE <https://github.com/davemlz/awesome-ee-spectral-indices>`_: A ready-to-use curated list of spectral indices for Google Earth Engine.
- `spectral <https://github.com/davemlz/spectral>`_: Awesome Spectral Indices for the Google Earth Engine JavaScript API (Code Editor).
- `eeExtra <https://github.com/r-earthengine/ee_extra>`_: A ninja Python package behind rgee, rgeeExtra and eemont.
- `rgeeExtra <https://github.com/r-earthengine/rgeeExtra>`_: High-level functions to process spatial and simple Earth Engine objects.

How does it work?
-------------------

The eemont python package extends the following Earth Engine classes:

- `ee.Feature <https://developers.google.com/earth-engine/guides/features>`_
- `ee.FeatureCollection <https://developers.google.com/earth-engine/guides/feature_collections>`_
- `ee.Geometry <https://developers.google.com/earth-engine/guides/geometries>`_
- `ee.Image <https://developers.google.com/earth-engine/guides/image_overview>`_
- `ee.ImageCollection <https://developers.google.com/earth-engine/guides/ic_creating>`_
- `ee.List <https://developers.google.com/earth-engine/guides/objects_methods_overview>`_
- `ee.Number <https://developers.google.com/earth-engine/guides/objects_methods_overview>`_

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
       .scaleAndOffset() # Extended (pre-processing)
       .spectralIndices(['NDVI','NDWI','BAIS2'])) # Extended (processing)

And just like that, the collection was pre-processed, processed and ready to be analyzed!

Installation
------------

Install the latest eemont version from PyPI by running:

.. code-block::   
      
   pip install eemont

Upgrade eemont by running:

.. code-block::   
      
   pip install -U eemont

Install the development version from GitHub by running:

.. code-block::   
      
   pip install git+https://github.com/davemlz/eemont
   
Install the latest eemont version from conda-forge by running:

.. code-block::   
      
   conda install -c conda-forge eemont

Features
--------

Let's see some of the main features of eemont and how simple they are compared to the GEE Python API original methods:

Overloaded Operators
~~~~~~~~~~~~~~~~~~~~~~~

The following operators are overloaded: +, -, \*\, /, //, %, \**\ , <<, >>, &, \|\, <, <=, ==, !=, >, >=, -, ~. (and you can avoid the :code:`ee.Image.expression()` method!)

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - GEE Python API
     - eemont-style     
   * - .. code-block:: python             
          
          ds = 'COPERNICUS/S2_SR'
          
          S2 = (ee.ImageCollection(ds)
            .first())
          
          def scaleImage(img):
              scaling = img.select('B.*')
              x = scaling.multiply(0.0001)
              scaling = img.select(['AOT','WVP'])
              scaling = scaling.multiply(0.001)
              x = x.addBands(scaling)
              notScaling = img.select([
                  'SCL',
                  'TCI.*',
                  'MSK.*',
                  'QA.*'
              ]))
              return x.addBands(notScaling)
              
          S2 = scaleImage(S2)
          
          exp = '2.5*(N-R)/(N+(6*R)-(7.5*B)+1)'
          
          imgDict = {
            'N': S2.select('B8'),
            'R': S2.select('B4'),
            'B': S2.select('B2')
          }
   
          EVI = S2.expression(exp,imgDict)
     - .. code-block:: python                     
   
          ds = 'COPERNICUS/S2_SR'
          
          S2 = (ee.ImageCollection(ds)
            .first()
            .scale())

          N = S2.select('B8')
          R = S2.select('B4')
          B = S2.select('B2')

          EVI = 2.5*(N-R)/(N+(6*R)-(7.5*B)+1)

Clouds and Shadows Masking
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Masking clouds and shadows can be done using eemont with just one method: :code:`maskClouds()`!

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - GEE Python API
     - eemont-style     
   * - .. code-block:: python             
          
          ds = 'LANDSAT/LC08/C01/T1_SR'
          
          def maskCloudsShadows(img):
              c = (1 << 3)
              s = (1 << 5)
              qa = 'pixel_qa'
              qa = img.select(qa)
              cm = qa.bitwiseAnd(c).eq(0)
              sm = qa.bitwiseAnd(s).eq(0)
              mask = cm.And(sm)
              return img.updateMask(mask)
              
          (ee.ImageCollection(ds)
            .map(maskCloudsShadows))
     - .. code-block:: python                 
   
          ds = 'LANDSAT/LC08/C01/T1_SR'
          
          (ee.ImageCollection(ds)
            .maskClouds())

Image Scaling and Offsetting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Scaling and offsetting can also be done using eemont with just one method: :code:`scale()`!

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - GEE Python API
     - eemont-style     
   * - .. code-block:: python                    
   
          def scaleBands(img):
              scaling = img.select([
                'NDVI',
                'EVI',
                'sur.*'
              ])
              x = scaling.multiply(0.0001)
              scaling = img.select('.*th')
              scaling = scaling.multiply(0.01)
              x = x.addBands(scaling)
              notScaling = img.select([
                'DetailedQA',
                'DayOfYear',
                'SummaryQA'
              ])
              return x.addBands(notScaling)              
          
          ds = 'MODIS/006/MOD13Q1'
          
          (ee.ImageCollection(ds)
            .map(scaleBands))
     - .. code-block:: python                    
   
          ds = 'MODIS/006/MOD13Q1'
          
          (ee.ImageCollection(ds)
            .scale())

Complete Preprocessing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The complete preprocessing workflow (Masking clouds and shadows, and image scaling and offsetting) can be done using eemont with just one method: :code:`preprocess()`!

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - GEE Python API
     - eemont-style     
   * - .. code-block:: python          
          
          ds = 'LANDSAT/LC08/C01/T1_SR'
          
          def maskCloudsShadows(img):
              c = (1 << 3)
              s = (1 << 5)
              qa = 'pixel_qa'
              qa = img.select(qa)
              cm = qa.bitwiseAnd(c).eq(0)
              sm = qa.bitwiseAnd(s).eq(0)
              mask = cm.And(sm)
              return img.updateMask(mask)
              
          def scaleBands(img):
              scaling = img.select('B[1-7]')
              x = scaling.multiply(0.0001)
              scaling = img.select([
                'B10','B11'
              ])
              scaling = scaling.multiply(0.1)
              x = x.addBands(scaling)
              notScaling = img.select([
                'sr_aerosol',
                'pixel_qa',
                'radsat_qa'
              ])
              return x.addBands(notScaling)
              
          (ee.ImageCollection(ds)
            .map(maskCloudsShadows)
            .map(scaleBands))
     - .. code-block:: python                
   
          ds = 'LANDSAT/LC08/C01/T1_SR'
          
          (ee.ImageCollection(ds)
            .preprocess())

Spectral Indices
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Do you need to compute several spectral indices? Use the :code:`index()` method! A lot of built-in vegetation, burn, water, snow, drought and kernel indices can be computed:

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - GEE Python API
     - eemont-style     
   * - .. code-block:: python                    
   
          ds = 'LANDSAT/LC08/C01/T1_SR'
          
          def scaleImage(img):
              scaling = img.select('B[1-7]')
              x = scaling.multiply(0.0001)
              scaling = img.select(['B10','B11'])
              scaling = scaling.multiply(0.1)
              x = x.addBands(scaling)
              notScaling = img.select([
                  'sr_aerosol',
                  'pixel_qa',
                  'radsat_qa'
              ]))
              return x.addBands(notScaling)
          
          def addIndices(img):
              x = ['B5','B4']
              a = img.normalizedDifference(x)
              a = a.rename('NDVI')
              x = ['B5','B3']
              b = img.normalizedDifference(x)
              b = b.rename('GNDVI')
              x = ['B3','B6']
              c = img.normalizedDifference(x)
              c = b.rename('NDSI')
              return img.addBands([a,b,c])                    
          
          (ee.ImageCollection(ds)
            .map(scaleImage)
            .map(addIndices))
          
     - .. code-block:: python                 
   
          ds = 'LANDSAT/LC08/C01/T1_SR'
          
          (ee.ImageCollection(ds)
            .scale()
            .index(['NDVI','GNDVI','NDSI']))

The list of available indices can be retrieved by running:

.. code-block:: python  
   
   eemont.listIndices()

Information about the indices can also be checked:

.. code-block:: python   
       
   indices = eemont.indices() 
   indices.BAIS2.formula
   indices.BAIS2.reference

Closest Image to a Specific Date
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Struggling to get the closest image to a specific date? Here is the solution: the :code:`closest()` method!

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - GEE Python API
     - eemont-style     
   * - .. code-block:: python                   
   
          ds = 'COPERNICUS/S5P/OFFL/L3_NO2'
          
          xy = [-76.21, 3.45]
          poi = ee.Geometry.Point(xy)
          
          date = ee.Date('2020-10-15')
          date = date.millis()
          
          def setTimeDelta(img):              
              prop = 'system:time_start'
              prop = img.get(prop)
              prop = ee.Number(prop)              
              delta = prop.subtract(date)
              delta = delta.abs()              
              return img.set(
                'dateDist',
                delta)                     
          
          (ee.ImageCollection(ds)
            .filterBounds(poi)
            .map(setTimeDelta)
            .sort('dateDist')
            .first())
          
     - .. code-block:: python                  
   
          ds = 'COPERNICUS/S5P/OFFL/L3_NO2'
          
          xy = [-76.21, 3.45]
          poi = ee.Geometry.Point(xy)
          
          (ee.ImageCollection(ds)
            .filterBounds(poi)
            .closest('2020-10-15'))
       
Time Series By Regions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The JavaScript API has a method for time series extraction (included in the ui.Chart module), but this method is missing in the Python API... so, here it is!

PD: Actually, there are two methods that you can use: :code:`getTimeSeriesByRegion()` and :code:`getTimeSeriesByRegions()`!

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
                                  
Constructors by Queries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Don't you have the coordinates of a place? You can construct them by using queries!

.. code-block:: python

   usr = 'my-eemont-query-example'
   
   seattle_bbox = ee.Geometry.BBoxFromQuery('Seattle',user_agent = usr)
   cali_coords = ee.Feature.PointFromQuery('Cali, Colombia',user_agent = usr)
   amazonas_river = ee.FeatureCollection.MultiPointFromQuery('Río Amazonas',user_agent = usr)

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

- **Bugs:** If you find a bug, please report it by opening an issue. if possible, please attach the error, code, version, and other details. 

- **Fixing Issues:** If you want to contributte by fixing an issue, please   check the eemont issues: contributions are welcome for open issues with labels :code:`bug` and :code:`help wanted`.

- **Enhancement:** New features and modules are welcome! You can check the eemont issues: contributions are welcome for open issues with labels :code:`enhancement` and :code:`help wanted`.

- **Documentation:** You can add examples, notes and references to the eemont documentation by using the NumPy Docstrings of the eemont documentation, or by creating blogs, tutorials or papers.

Contribution Steps
~~~~~~~~~~~~~~~~~~~~~~~~

First, fork the `eemont <https://github.com/davemlz/eemont>`_ repository and clone it to your local machine. Then, create a development branch::

   git checkout -b name-of-dev-branch
   
eemont is divided according to Earth Engine classes, and you will find a module for each class (e.g. :code:`imagecollection.py`). Look for the required class as follows:

- ee.Feature: :code:`feature.py`
- ee.FeatureCollection: :code:`featurecollection.py`
- ee.Geometry: :code:`geometry.py`
- ee.Image: :code:`image.py`
- ee.ImageCollection: :code:`imagecollection.py`

The :code:`common.py` is used for methods that can be used for more than one Earth Engine class.

When creating new features, please start with the :code:`self` argument and add the corresponding decorator (
:code:`@extend()` from the :code:`extending` module). Check this example:

.. code-block:: python

   from .extending import extend
   
   @extend(ee.image.Image, static = False)
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
        
By using the :code:`@extend()` decorator, the :code:`my_new_method()` method is added to the :code:`ee.Image` class. If you want to add a static method, please set the :code:`static` argument to :code:`False`. Look for the required class as follows:

- ee.Feature: :code:`ee.feature.Feature`
- ee.FeatureCollection: :code:`ee.featurecollection.FeatureCollection`
- ee.Geometry: :code:`ee.geometry.Geometry`
- ee.Image: :code:`ee.image.Image`
- ee.ImageCollection: :code:`ee.imagecollection.ImageCollection`
- ee.List: :code:`ee.ee_list.List`
- ee.Number: :code:`ee.ee_number.Number`

Remember to use `Black <https://github.com/psf/black>`_!

In order to test additions, you can use :code:`pytest` over the :code:`tests` folder::

   pytest tests
   
This will autmatically test all modules for the available satellite platforms through eemont. If you have added a new feature, please include it in the tests.

To test across different Python versions, please use :code:`tox`.

Now it's time to commit your changes and push your development branch::

   git add .
   git commit -m "Description of your work"
   git push origin name-of-dev-branch
  
And finally, submit a pull request.

How to cite
-----------

Do you like using eemont and think it is useful? Share the love by citing it!::

   Montero, D., (2021). eemont: A Python package that extends Google Earth Engine. Journal of Open Source Software, 6(62), 3168, https://doi.org/10.21105/joss.03168
   
If required, here is the BibTex!::

   @article{Montero2021,
     doi = {10.21105/joss.03168},
     url = {https://doi.org/10.21105/joss.03168},
     year = {2021},
     publisher = {The Open Journal},
     volume = {6},
     number = {62},
     pages = {3168},
     author = {David Montero},
     title = {eemont: A Python package that extends Google Earth Engine},
     journal = {Journal of Open Source Software}
   }

Artists
-------

- `David Montero Loaiza <https://github.com/davemlz>`_: Lead Developer of eemont and eeExtra.
- `César Aybar <https://github.com/csaybar>`_: Lead Developer of rgee and eeExtra.
- `Aaron Zuspan <https://github.com/aazuspan>`_: Plus Codes Constructors and Methods, Panchromatic Sharpening and Histogram Matching Developer.

Credits
-------

Special thanks to `Justin Braaten <https://github.com/jdbcode>`_ for featuring eemont in tutorials and the GEE Community: Developer Resources Page, to `César Aybar <https://github.com/csaybar>`_ for the formidable help with Awesome Spectral Indices for GEE and to the JOSS Review Team (`Katy Barnhart <https://github.com/kbarnhart>`_, `Jayaram Hariharan <https://github.com/elbeejay>`_, `Qiusheng Wu <https://github.com/giswqs>`_ and `Patrick Gray <https://github.com/patrickcgray>`_) for the comments, suggestions and contributions!
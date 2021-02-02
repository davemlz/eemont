Masking Clouds and Shadows
====================================

Masking clouds and shadows may seem hard, but it isn't! Let's take a look on it!

Before anything, let's import our modules and authenticate in Google Earth Engine:

.. code-block:: python

   import ee, eemont
   
   ee.Authenticate()
   ee.Initialize()

Now, we are ready to go!

Overview
-----------

The eemont package extends the ee.Image and ee.ImageCollection classes with the method :code:`maskClouds()`:

ee.Image
~~~~~~~~

.. currentmodule:: eemont.image

.. autosummary::

   maskClouds
      
ee.ImageCollection
~~~~~~~~~~~~~~~~~~~~~~~~

.. currentmodule:: eemont.imagecollection

.. autosummary::

   maskClouds

Supported Platforms
----------------------

This method automatically masks clouds and shadows on the following supported satellite platforms:

Sentinel Missions
~~~~~~~~~~~~~~~~~~~

- `Sentinel-3 OLCI EFR: Ocean and Land Color Instrument Earth Observation Full Resolution <https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S3_OLCI>`_
- `Sentinel-2 MSI: MultiSpectral Instrument, Level-2A <https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR?hl=en>`_

Landsat Missions
~~~~~~~~~~~~~~~~~~~

- `USGS Landsat 8 Surface Reflectance Tier 1 and 2 <https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C01_T1_SR>`_
- `USGS Landsat 7 Surface Reflectance Tier 1 and 2 <https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LE07_C01_T1_SR>`_
- `USGS Landsat 5 Surface Reflectance Tier 1 and 2 <https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LT05_C01_T1_SR>`_
- `USGS Landsat 4 Surface Reflectance Tier 1 and 2 <https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LT04_C01_T1_SR>`_

MODIS Products
~~~~~~~~~~~~~~~~~~~

- `MOD09GA.006 Terra Surface Reflectance Daily Global 1km and 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD09GA>`_
- `MOD09Q1.006 Terra Surface Reflectance 8-Day Global 250m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD09Q1>`_
- `MOD09A1.006 Terra Surface Reflectance 8-Day Global 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD09A1>`_
- `MCD15A3H.006 MODIS Leaf Area Index/FPAR 4-Day Global 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MCD15A3H>`_
- `MOD17A2H.006: Terra Gross Primary Productivity 8-Day Global 500M 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD17A2H>`_
- `MOD16A2.006: Terra Net Evapotranspiration 8-Day Global 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD16A2>`_
- `MOD13Q1.006 Terra Vegetation Indices 16-Day Global 250m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD13Q1>`_
- `MOD13A1.006 Terra Vegetation Indices 16-Day Global 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD13A1>`_
- `MOD13A2.006 Terra Vegetation Indices 16-Day Global 1km <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD13A2>`_

.. warning::
   Not supported satellite platforms will raise an *Exception*.   

QA Method
----------------------

By default, the :code:`maskClouds()` uses the QA band of each paltform to compute the clouds and shadows masks (except for Sentinel-2, where the default method is Cloud Probability). The following table shows the band and the bits used for each platform (The value in parentheses is the valid value of the bitmask):

.. list-table:: QA bits used for clouds/shadows masking
   :widths: 20 20 20 20 20
   :header-rows: 1

   * - Platform
     - QA Band
     - Cloud Bitmask
     - Cirrus Bitmask
     - Shadow Bitmask
   * - Sentinel-3
     - quality_flags
     - 27 (0)
     -
     -
   * - Sentinel-2
     - QA60
     - 10 (0)
     - 11 (0)
     -
   * - Landsat Series
     - pixel_qa
     - 5 (0)
     - 
     - 3 (0)
   * - MOD09GA
     - state_1km
     - 0 (0)
     - 8 (0)
     - 2 (0)
   * - MOD09Q1
     - State
     - 0 (0)
     - 8 (0)
     - 2 (0)
   * - MOD09A1
     - StateQA
     - 0 (0)
     - 8 (0)
     - 2 (0)
   * - MCD15A3H
     - FparExtra_QC
     - 5 (0)
     - 4 (0)
     - 6 (0)
   * - MOD17A2H
     - Psn_QC
     - 3 (0)
     - 
     - 
   * - MOD16A2
     - ET_QC
     - 3 (0)
     - 
     - 
   * - MOD13Q1
     - SummaryQA
     - 0 (0)
     - 
     - 
   * - MOD13A1
     - SummaryQA
     - 0 (0)
     - 
     -

Usage
-----

Let's check how to use the :code:`maskClouds()` method for different platforms:

Sentinel-3
~~~~~~~~~~~~~~

On Sentinel 3, clouds are masked according to the bright pixels in the quality_flags band of the `Sentinel-3 OLCI EFR: Ocean and Land Color Instrument Earth Observation Full Resolution <https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S3_OLCI>`_.

.. warning::
   This method may mask water as well on Sentinel-3 images. 

Let's take the Sentinel-3 image collection as example:

.. code-block:: python

   S3 = ee.ImageCollection('COPERNICUS/S3/OLCI')
   
There is no need to specify any arguments, since they're ignored.

.. code-block:: python

   S3.maskClouds()
  
This method can also be applied to a single image:

.. code-block:: python

   S3.first().maskClouds()
   
And can be used for scaled images without specifying it:

.. code-block:: python

   S3.scale().maskClouds()

Sentinel-2
~~~~~~~~~~~~~~~~

On Sentinel 2, clouds can be masked using two methods: *QA* and *Cloud Probability*. The *QA* method uses the QA60 band in the `Surface Reflectance Product <https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR?hl=en>`_ to mask clouds, while the *Cloud Probability* method uses the
`COPERNICUS/S2_CLOUD_PROBABILITY <https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_CLOUD_PROBABILITY?hl=en>`_ collection to do it.

Shadows are masked based on the clouds mask, where shadows are searched within a range from clouds edges in the shadows direction.

.. seealso::
   For more info on masking shadows, please visit
   `‘Braaten, J. 2020. Sentinel-2 Cloud Masking with s2cloudless. Google Earth Engine, Community Tutorials’ <https://developers.google.com/earth-engine/tutorials/community/sentinel-2-s2cloudless>`_.

First, let's take the Sentinel-2 image collection:

.. code-block:: python

   S2 = ee.ImageCollection('COPERNICUS/S2_SR')

In order to use the *QA* method, it must be specified using the :code:`method` parameter:

.. code-block:: python

   S2.maskClouds(method = 'qa')
   
This line maps the *QA* masking method over the whole collection, but the method can also be applied to a single image:

.. code-block:: python

   S2.first().maskClouds(method = 'qa')
   
The *QA* method gives us the option to avoid masking cirrus clouds, but it must be specified using the :code:`maskCirrus` parameter:

.. code-block:: python

   S2.maskClouds(method = 'qa', maskCirrus = False)

And we can also avoid masking shadows by specifying the :code:`maskShadows` parameter:

.. code-block:: python

   S2.maskClouds(method = 'qa', maskShadows = False)
   
Now, in order to use the *Cloud Probability* method, we can specify it in the :code:`method` parameter:

.. code-block:: python

   S2.maskClouds(method = 'cloud_prob')
   
But, it is the default method, so you can just let the extended method with no additional parameters:

.. code-block:: python

   S2.maskClouds()
   
The *Cloud Probability* method uses a probability threshold to mask clouds, by default, the threshold is set to 60, but it can be modified using the :code:`prob` parameter:

.. code-block:: python

   S2.maskClouds(prob = 70)
   
If your image or collection is scaled, the :code:`scaledImage` parameter must be set to :code:`True`:

.. code-block:: python

   S2.scale().maskClouds(scaledImage = True)
   
In order to search for shadows, portental shadow pixels must be specified. Pixels with a NIR reflectance below 0.15 are considered potential shadow pixels, but this can be modified using the
:code:`dark` parameter:

.. code-block:: python

   S2.maskClouds(dark = 0.2)
   
Shadows are searched whitin a maximum range of 1000 m in the shadow direction from cloud edges, but this range can be modified using the :code:`cloudDist` parameter:

.. code-block:: python

   S2.maskClouds(cloudDist = 1500)
   
After finding all clouds and shadows, the mask can be dilated to avoid border effects. By default, clouds and shadows are dilated by 250 m, but this can be modified using the :code:`buffer` parameter:

.. code-block:: python

   S2.maskClouds(buffer = 100)
   
Finally, in order to avoid confusion between clouds and bright surface objects, the Cloud Displacement Index (CDI) can be used. By default, the CDI is not used, but it can be modified
using the :code:`cdi` parameter:

.. code-block:: python

   S2.maskClouds(cdi = -0.5)
   
.. seealso::
   For more info on CDI, please visit
   `‘Frantz, D., HaS, E., Uhl, A., Stoffels, J., Hill, J. 2018. Improvement of the Fmask algorithm for Sentinel-2 images: 
   Separating clouds from bright surfaces based on parallax effects. Remote Sensing of Environment 2015: 471-481’ 
   <https://www.sciencedirect.com/science/article/pii/S0034425718302037#:~:text=In%20this%20paper%2C%20we%20present,separated%20from%20bright%20ground%20objects.>`_.

Landsat Series
~~~~~~~~~~~~~~~~

On Landsat Series, both clouds and shadows are masked based on the pixel_qa band in the `Surface Reflectance Products <https://developers.google.com/earth-engine/datasets/catalog/landsat>`_.

Let's take the Landsat 8 image collection as example:

.. code-block:: python

   L8 = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
   
There is no need to specify most of the arguments showed for Sentinel-2, since they're ignored.

.. code-block:: python

   L8.maskClouds()
   
Shadows are masked by default, but if required, the :code:`maskShadows` parameter can be modified.

.. code-block:: python

   L8.maskClouds(maskShadows = False)
   
This method can also be applied to a single image:

.. code-block:: python

   L8.first().maskClouds()
   
And can be used for scaled images without specifying it:

.. code-block:: python

   L8.scale().maskClouds()
   
MODIS Products
~~~~~~~~~~~~~~~~

On MODIS Products, clouds and shadows are masked according to the specific QA band.

Let's take the MOD13Q1 image collection as example:

.. code-block:: python

   MOD13Q1 = ee.ImageCollection('MODIS/006/MOD13Q1')
   
There is no need to specify most of the arguments showed for Sentinel-2, since they're ignored.

.. code-block:: python

   MOD13Q1.maskClouds()
   
MOD13Q1, MOD13A1, MOD17A2H and MOD16A2 products don't have cirrus and shadow bitmasks, therefore, the arguments :code:`maskShadows` and :code:`maskCirrus` are ignored. MOD09GA, MOD09Q1, MOD09A1 and MCD15A3H products have cirrus and shadows bitmasks, and by default, they are set to *True*. If required, they can be set to *False*:

.. code-block:: python

   MOD09GA = ee.ImageCollection('MODIS/006/MOD09GA').maskClouds(maskShadows = False, maskCirrus = False)
   
This method can also be applied to a single image:

.. code-block:: python

   MOD09GA.first().maskClouds()
   
And can be used for scaled images without specifying it:

.. code-block:: python

   MOD09GA.scale().maskClouds()
   
MOD13A2 doesn't have a bitmask QA band, instead, it has a Class QA band, where a value of zero means that the pixel has good data.

.. code-block:: python

   MOD13A2 = ee.ImageCollection('MODIS/006/MOD13A2').maskClouds()
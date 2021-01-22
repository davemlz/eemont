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

This method automatically masks clouds and shadows on specific supported satellite platforms:

- `Sentinel-2 MSI: MultiSpectral Instrument, Level-2A <https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR?hl=en>`_
- `USGS Landsat 8 Surface Reflectance Tier 1 and 2 <https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C01_T1_SR>`_
- `USGS Landsat 7 Surface Reflectance Tier 1 and 2 <https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LE07_C01_T1_SR>`_
- `USGS Landsat 5 Surface Reflectance Tier 1 and 2 <https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LT05_C01_T1_SR>`_
- `USGS Landsat 4 Surface Reflectance Tier 1 and 2 <https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LT04_C01_T1_SR>`_

.. warning::
   Not supported satellite platforms or not Surface Reflectance Products of the supported platforms will raise an *Exception*.   

Let's check how to use the :code:`maskClouds()` method for:

- :ref:`S2`.
- :ref:`LS`.

.. _S2:

Sentinel-2
------------------

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

.. _LS:

Landsat Series
------------------

On Landsat Series, both clouds and shadows are masked based on the pixel_qa band in the `Surface Reflectance Products <https://developers.google.com/earth-engine/datasets/catalog/landsat>`_.

Let's take the Landsat 8 image collection as example:

.. code-block:: python

   L8 = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
   
There is no need to specify most of the methods showed for Sentinel-2, since they're ignored.

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
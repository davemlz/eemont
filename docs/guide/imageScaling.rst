Image Scaling
====================================

Image scaling now is A LOT EASIER with eemont! Let's see how!

Before anything, let's import our modules and authenticate in Google Earth Engine:

.. code-block:: python

   import ee, eemont
   
   ee.Authenticate()
   ee.Initialize()

Now, we are ready to go!

Overview
-----------

The eemont package extends the ee.Image and ee.ImageCollection classes with the following methods:

ee.Image
~~~~~~~~

.. currentmodule:: eemont.image

.. autosummary::

   getOffsetParams
   getScaleParams
   preprocess
   scaleAndOffset
      
ee.ImageCollection
~~~~~~~~~~~~~~~~~~~~~~~~

.. currentmodule:: eemont.imagecollection

.. autosummary::

   getOffsetParams
   getScaleParams
   preprocess
   scaleAndOffset

Supported Platforms
----------------------

This method automatically scales ALL images from the `Google Earth Engine STAC Catalog <https://developers.google.com/earth-engine/datasets>`_ by using the `List of Scale and Offset Parameters from the GEE STAC Catalog Repository <https://github.com/davemlz/ee-catalog-scale-offset-params>`_.

Usage
------------------

The :code:`scaleAndOffset()` method scales each image according to the *Scale* and *Offset* parameters for each band of the image. 

Let's take the Sentinel-2 SR image collection as example:

.. code-block:: python

   S2 = ee.ImageCollection('COPERNICUS/S2_SR')
   
The spectral bands from Sentinel-2 have values close to the (0, 10000) range, but they're unscaled. In order to get the real values, each spectral band must be multiplied by 0.0001, while AOT and WVP bands must be multiplied by 0.001. This scaling is automatically done by the :code:`scaleAndOffset()` method, without any additional parameters:

.. code-block:: python

   S2.scaleAndOffset()

The *Scale* and *Offset* parameters vary according to the satellite platform and the :code:`scaleAndOffset()` method detects the platform and do the scaling according to its parameters.

Let's take now the MOD11A2 product from MODIS. The LST_Day_1km and LST_Night_1km bands must be multiplied by 0.02, the Day_view_time and Night_view_time bands must be multiplied by 0.1,
the Emis_31 and Emis_32 bands must be multiplied by 0.002 and added by 0.49, while the Day_view_angl and Night_view_angl bands must be added by -65. All of this scaling
is simply done by the :code:`scaleAndOffset()` method:

.. code-block:: python

   MOD11A2scaled = ee.ImageCollection('MODIS/006/MOD11A2').scaleAndOffset()
   
The :code:`scale()` method can be applied to single images as well:

.. code-block:: python

   MOD11A2scaled = ee.ImageCollection('MODIS/006/MOD11A2').first().scaleAndOffset()
   
Preprocessing
~~~~~~~~~~~~~~~~~
   
Additionally, if required, the :code:`preprocess()` method can be used to scale and mask images and image collections:

.. code-block:: python

   S2 = ee.ImageCollection('COPERNICUS/S2_SR').preprocess()
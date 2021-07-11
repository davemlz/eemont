Panchromatic Sharpening
====================================
Guide by `Aaron Zuspan <https://github.com/aazuspan>`_


Panchromatic sharpening is simple in eemont!

Before anything, let's import our modules and authenticate in Google Earth Engine:

.. code-block:: python

   import ee, eemont
   
   ee.Authenticate()
   ee.Initialize()

Now, we are ready to go!

Overview
-----------

The eemont package extends the ee.Image and ee.ImageCollection classes with the method :code:`panSharpen()`:

ee.Image
~~~~~~~~

.. currentmodule:: eemont.image

.. autosummary::

   panSharpen

ee.ImageCollection
~~~~~~~~

.. currentmodule:: eemont.imagecollection

.. autosummary::
   
      panSharpen

Supported Platforms
----------------------

Pansharpening is supported for the following platforms:

Landsat Missions
~~~~~~~~~~~~~~~~~~~

- `USGS Landsat 8 Collection 1 Tier 1 <https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C01_T1>`_
- `USGS Landsat 8 Collection 1 Tier 1 OLI <https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LO08_C01_T1>`_
- `USGS Landsat 8 Collection 1 Tier 1 and Real-Time data <https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C01_T1_RT>`_
- `USGS Landsat 8 Collection 1 Tier 2 <https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C01_T2>`_
- `USGS Landsat 8 Collection 1 Tier 2 OLI <https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LO08_C01_T2>`_
- `USGS Landsat 8 Collection 1 Tier 1 TOA Reflectance <https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C01_T1_TOA>`_
- `USGS Landsat 8 Collection 1 Tier 1 and Real-Time data TOA Reflectance <https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C01_T1_RT_TOA>`_
- `USGS Landsat 8 Collection 1 Tier 2 TOA Reflectance <https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C01_T2_TOA>`_


- `USGS Landsat 7 Collection 1 Tier 1 <https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LE07_C01_T1>`_
- `USGS Landsat 7 Collection 1 Tier 1 and Real-Time data <https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LE07_C01_T1_RT>`_
- `USGS Landsat 7 Collection 1 Tier 2 <https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LE07_C01_T2>`_
- `USGS Landsat 7 Collection 1 Tier 1 TOA Reflectance <https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LE07_C01_T1_TOA>`_
- `USGS Landsat 7 Collection 1 Tier 1 and Real-Time data TOA Reflectance <https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LE07_C01_T1_RT_TOA>`_
- `USGS Landsat 7 Collection 1 Tier 2 TOA Reflectance <https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LE07_C01_T2_TOA>`_

.. warning::
    Surface Reflectance products do not contain panchromatic bands and do not support pan-sharpening.

Algorithms
-----------

The :code:`panSharpen` method can be run using a variety of different algorithms by setting the :code:`method` argument. The following sharpening algorithms are supported by eemont:

.. list-table:: Available algorithm methods.
   :widths: 25 65 15
   :header-rows: 1

   * - Method
     - Name
     - kwargs
   * - :code:`SFIM` (default)
     - Smoothing-Filter Based Intensity Modulation
     - No
   * - :code:`HPFA`
     - High-Pass Filter Addition
     - No
   * - :code:`PCS`
     - Principal Component Substitution
     - Yes
   * - :code:`SM`
     - Simple Mean
     - No


.. seealso::
     Some algorithms take additional keyword arguments (kwargs) such as :code:`maxPixels`, :code:`geometry`, or 
     :code:`bestEffort`. These are passed to :code:`ee.Image.reduceRegion`. More information on how to set these arguments
     can be found `here <https://developers.google.com/earth-engine/guides/reducers_reduce_region>`_.
 
Usage
------------------
Let's load a supported image from Landsat 8:

.. code-block:: python

    img = ee.Image("LANDSAT/LC08/C01/T1_TOA/LC08_047027_20160819")

And sharpen it using the :code:`panSharpen` method with the default :code:`SFIM` algorithm.

.. code-block:: python

    sharp = img.panSharpen()

Easy as that!

We can also try sharpening with a different algorithm. Remember that some algorirthms take additional keyword arguments.
Here, we'll specify :code:`maxPixels` to avoid pixel limitations with the :code:`PCS` algorithm.

.. code-block:: python

    sharp = img.panSharpen(method="PCS", maxPixels=1e13)

Pan-sharpening image collections is identical to sharpening images:

.. code-block:: python

    imgCollection = ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA")
    sharpCollection = imgCollection.panSharpen()

Quality Assessment
~~~~~~~~~~~~~~~~
Quality assessment (QA) metrics can be calculated by the :code:`panSharpen` method to measure how much spectral distortion 
was introduced by sharpening and to compare different sharpening algorithms. eemont supports the following QA metrics:

.. list-table:: Available QA metrics.
   :widths: 20 65 25 25
   :header-rows: 1

   * - QA
     - Name
     - Ideal Value
     - Mode
   * - :code:`MSE`
     - Mean Squared Error
     - 0
     - Band
   * - :code:`RMSE`
     - Root-Mean Squared Error
     - 0
     - Band
   * - :code:`RASE`
     - Relative Average Spectral Error 
     - 0
     - Image
   * - :code:`ERGAS`
     - Dimensionless Global Relative Error of Synthesis
     - 0
     - Image
   * - :code:`DIV`
     - Difference in Variance
     - 0
     - Band
   * - :code:`bias`
     - Bias
     - 0
     - Band
   * - :code:`CC`
     - Correlation Coefficient
     - 1
     - Band
   * - :code:`CML`
     - Change in mean luminance
     - 1
     - Band
   * - :code:`CMC`
     - Change in mean contrast
     - 1
     - Band
   * - :code:`UIQI`
     - Universal Image Quality Index
     - 1
     - Band

.. note::
    Some metrics are calculated image-wise and others are calculated band-wise. Image-wise metrics return one value for
    the entire image while band-wise metrics return one value for each band.

QA metrics are calculated by passing a list of one or more metrics to the :code:`qa` argument of the :code:`panSharpen`
method. Below, we'll calculate :code:`RASE` and :code:`UIQI` while sharpening an image.

.. code-block:: python

    metrics = ["RASE", "UIQI"]
    img = ee.Image("LANDSAT/LC08/C01/T1_TOA/LC08_047027_20160819")
    sharp = img.panSharpen(qa=metrics, maxPixels=1e13)

.. seealso::
    All QA metrics take additional keyword arguments (kwargs) such as :code:`maxPixels`, :code:`geometry`, or 
    :code:`bestEffort`. These are passed to :code:`ee.Image.reduceRegion`. More information can be found `here <https://developers.google.com/earth-engine/guides/reducers_reduce_region>`_.

Calculated QA metrics are set as properties of the sharpened image and can be retrieved with the :code:`get` method.
QA property names use the format :code:`eemont:{QA}`.

.. code-block:: python

    sharp.get("eemont:RASE").getInfo()


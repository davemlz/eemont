Histogram Matching
====================================
Guide by `Aaron Zuspan <https://github.com/aazuspan>`_


Overview
-----------

The eemont package extends the ee.Image class with the method :code:`matchHistogram()`:

ee.Image
~~~~~~~~

.. currentmodule:: eemont.image

.. autosummary::

    matchHistogram

Usage
------------------
Histogram matching performs band-wise adjustments to match the spectral response of one image to a target image. 
Let's look at a few examples of how histogram matching can be used for different platform combinations in eemont.

.. seealso::
    For more info on histogram matching and details on eemont's implementation, please visit `Braaten, J. 2021. Histogram 
    Matching. Google Earth Engine, Community Tutorials <https://developers.google.com/earth-engine/tutorials/community/histogram-matching>`_.

Landsat 5 and 8
~~~~~~~~~~~~~~~
In this example, we'll match the histograms of a Landsat 5 image to a Landsat 8 image. This can be helpful for performing 
consistent time series analysis using different sensors.

First, we'll load the source image and the target image.

.. code-block:: python

    source = ee.Image("LANDSAT/LT05/C01/T1_SR/LT05_195028_20110208")
    target = ee.Image("LANDSAT/LC08/C02/T1_L2/LC08_196027_20130714")

.. warning::
    Images must overlap. Cloud cover or major changes in land cover may cause inaccurate results.

Now, we'll specify which bands should be matched. We do this using a dictionary with the source bands as keys and target
bands as values.

.. code-block:: python

    bands = {
        # Red
        "B3": "SR_B4",
        # Green
        "B2": "SR_B3",
        # Blue
        "B1": "SR_B2"
    }

.. note::
    Any bands that aren't listed will be removed from the matched image.

Finally, we'll call the :code:`matchHistogram` method to create a new image representing the source image matched to the
target image.

.. code-block:: python

    matched = source.matchHistogram(target, bands)


Sentinel-2 and MODIS
~~~~~~~~~~~~~~~~~~~~
In this example, we'll match the histogram of a Sentinel-2 image to a MODIS image.

.. code-block:: python
    
    source = ee.Image("COPERNICUS/S2/20180923T081641_20180923T083023_T35PQQ")
    target = ee.Image("MODIS/006/MOD09A1/2018_08_05")

Specify the matching bands between images:

.. code-block:: python

    bands = {
        # Red
        "B4": "sur_refl_b01",
        # Green
        "B3": "sur_refl_b04",
        # Blue
        "B2": "sur_refl_b03"
    }

And match the Sentinel-2 image to the MODIS image!

.. code-block:: python

    matched = source.match(target, bands)


You can adjust the quality and speed of histogram matching using the :code:`maxBuckets` argument. Fewer buckets will run
faster but produce less accurate matching. By default, 256 buckets are used.

.. code-block:: python

    matched = source.matchHistogram(target, bands, maxBuckets=64)

.. note::

    :code:`maxBuckets` are automatically adjusted to the nearest power of 2, so :code:`maxBuckets=50` is the same as :code:`maxBuckets=64.`
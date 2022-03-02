Tasseled Cap
====================================
Guide by `Aaron Zuspan <https://github.com/aazuspan>`_


Overview
-----------

The eemont package extends the ee.Image and ee.ImageCollection classes with the method :code:`tasseledCap()`:

ee.Image
~~~~~~~~

.. currentmodule:: eemont.image

.. autosummary::

    tasseledCap

ee.ImageCollection
~~~~~~~~~~~~~~~~~~

.. currentmodule:: eemont.imagecollection

.. autosummary::

    tasseledCap


Supported Platforms
----------------------

Tasseled cap transformation coefficients are published for a number of sensors and processing levels:

* `Sentinel-2 MSI Level 1C <https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2>`_ [1]_
* `Landsat 8 OLI TOA <https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C01_T1_TOA>`_ [2]_
* `Landsat 7 ETM+ TOA <https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LE07_C01_T1_TOA>`_ [3]_
* `Landsat 5 TM Raw DN <https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LT05_C01_T1>`_ [4]_
* `Landsat 4 TM Raw DN <https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LT04_C01_T1>`_ [5]_
* `Landsat 4 TM Surface Reflectance <https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LT04_C02_T1_L2>`_ [6]_
* `MODIS NBAR <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MCD43A4>`_ [7]_


Usage
------------------
Tasseled cap transformation calculates brightness, greenness, and wetness components from spectral bands. These data transformations can be helpful for 
both visualization and dimensionality reduction. 

To calculate tasseled cap components, we'll load a supported image (Sentinel-2) and run the :code:`tasseledCap` method.

.. code-block:: python

    img = ee.Image("COPERNICUS/S2/20160111T112432_20160111T113311_T28PDT")
    img = img.tasseledCap()

Now if we check the image band names, we'll see tasseled cap brightness (TCB), greenness (TCG), and wetness (TCW) component bands 
have been added to our image.

.. code-block:: python

    >>> img.bandNames().getInfo()
    ['B1', 'B2', 'B3' ... 'TCB', 'TCG', 'TCW']

.. warning::

    :code:`tasseledCap` requires a specific set of bands depending on the dataset. If your image does not contain the correct bands, 
    you will receive an error like :code:`Image.select: Pattern 'B1' did not match any bands`. To avoid that, it is safest to run :code:`tasseledCap`
    before subsetting your image bands.

For convenience, we could also run the :code:`tasseledCap` method on an :code:`ee.ImageCollection`, which would add TCB, TCG, and TCW bands
to each image.

.. code-block:: python

    col = ee.ImageCollection("COPERNICUS/S2")
    col = col.tasseledCap()


References
----------

.. [1] Shi, T., & Xu, H. (2019). Derivation of Tasseled Cap Transformation
    Coefficients for Sentinel-2 MSI At-Sensor Reflectance Data. IEEE Journal
    of Selected Topics in Applied Earth Observations and Remote Sensing, 1–11.
    doi:10.1109/jstars.2019.2938388
.. [2] Baig, M.H.A., Zhang, L., Shuai, T. and Tong, Q., 2014. Derivation of a
    tasselled cap transformation based on Landsat 8 at-satellite reflectance.
    Remote Sensing Letters, 5(5), pp.423-431.
.. [3] Huang, C., Wylie, B., Yang, L., Homer, C. and Zylstra, G., 2002.
    Derivation of a tasselled cap transformation based on Landsat 7 at-satellite
    reflectance. International journal of remote sensing, 23(8), pp.1741-1748.
.. [4] Crist, E.P., Laurin, R. and Cicone, R.C., 1986, September. Vegetation and
    soils information contained in transformed Thematic Mapper data. In
    Proceedings of IGARSS’86 symposium (pp. 1465-1470). Paris: European Space
    Agency Publications Division.
.. [5] Crist, E.P. and Cicone, R.C., 1984. A physically-based transformation of
    Thematic Mapper data---The TM Tasseled Cap. IEEE Transactions on Geoscience
    and Remote sensing, (3), pp.256-263.
.. [6] Crist, E.P., 1985. A TM tasseled cap equivalent transformation for
    reflectance factor data. Remote sensing of Environment, 17(3), pp.301-306.
.. [7] Lobser, S.E. and Cohen, W.B., 2007. MODIS tasselled cap: land cover
    characteristics expressed through transformed MODIS data. International
    Journal of Remote Sensing, 28(22), pp.5079-5101.

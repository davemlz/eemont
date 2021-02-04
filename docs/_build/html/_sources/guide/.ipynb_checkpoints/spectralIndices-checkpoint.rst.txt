Spectral Indices
====================================

Let's see how to compute built-in spectral indices with eemont!

Before anything, let's import our modules and authenticate in Google Earth Engine:

.. code-block:: python

   import ee, eemont
   
   ee.Authenticate()
   ee.Initialize()

Now, we are ready to go!

Overview
-----------

The eemont package extends the ee.Image and ee.ImageCollection classes with the method :code:`index()`:

ee.Image
~~~~~~~~

.. currentmodule:: eemont.image

.. autosummary::

   index
      
ee.ImageCollection
~~~~~~~~~~~~~~~~~~~~~~~~

.. currentmodule:: eemont.imagecollection

.. autosummary::

   index

Supported Platforms
----------------------

This method automatically computes spectral indices for the following supported satellite platforms:

Sentinel Missions
~~~~~~~~~~~~~~~~~~~

- `Sentinel-2 MSI: MultiSpectral Instrument, Level-2A <https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR?hl=en>`_
- `Sentinel-2 MSI: MultiSpectral Instrument, Level-1C <https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2#bands>`_

Landsat Missions
~~~~~~~~~~~~~~~~~~~

- `USGS Landsat 8 Surface Reflectance Tier 1 and 2 <https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C01_T1_SR>`_
- `USGS Landsat 7 Surface Reflectance Tier 1 and 2 <https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LE07_C01_T1_SR>`_
- `USGS Landsat 5 Surface Reflectance Tier 1 and 2 <https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LT05_C01_T1_SR>`_
- `USGS Landsat 4 Surface Reflectance Tier 1 and 2 <https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LT04_C01_T1_SR>`_

.. important::
   It is highly recommended to scale the image (or image collection) before computing spectral indices. See the :code:`scale()` method for more info.  

List of Indices
----------------------

Vegetation Indices
~~~~~~~~~~~~~~~~~~~

The following table shows the list of built-in vegetation indices:

.. list-table:: Built-in vegetation indices.
   :widths: 20 50 30
   :header-rows: 1

   * - Index
     - Description     
     - Reference
   * - BNDVI
     - Blue Normalized Difference Vegetation Index
     - `Index DataBase BNDVI <https://www.indexdatabase.de/db/i-single.php?id=135>`_  
   * - CIG
     - Chlorophyll Index - Green
     - `Index DataBase CIG <https://www.indexdatabase.de/db/i-single.php?id=128>`_
   * - CVI
     - Chlorophyll Vegetation Index
     - `Index DataBase CVI <https://www.indexdatabase.de/db/i-single.php?id=391>`_
   * - EVI
     - Enhanced Vegetation Index
     - `Index DataBase EVI <https://www.indexdatabase.de/db/i-single.php?id=16>`_
   * - GBNDVI
     - Green-Blue Normalized Difference Vegetation Index
     - `Index DataBase GBNDVI <https://www.indexdatabase.de/db/i-single.php?id=186>`_
   * - GNDVI
     - Green Normalized Difference Vegetation Index
     - `Index DataBase GNDVI <https://www.indexdatabase.de/db/i-single.php?id=401>`_
   * - GRNDVI
     - Green-Red Normalized Difference Vegetation Index
     - `Index DataBase GRNDVI <https://www.indexdatabase.de/db/i-single.php?id=185>`_
   * - MNDVI
     - Modified Normalized Difference Vegetation Index
     - `Index DataBase MNDVI <https://www.indexdatabase.de/db/i-single.php?id=245>`_
   * - NDVI
     - Normalized Difference Vegetation Index
     - `Index DataBase NDVI <https://www.indexdatabase.de/db/i-single.php?id=58>`_
   * - NGRDI
     - Normalized Green Red Difference Index
     - `Index DataBase NGRDI <https://www.indexdatabase.de/db/i-single.php?id=390>`_
   * - RVI
     - Ratio Vegetation Index
     - `Index DataBase RVI <https://www.indexdatabase.de/db/i-single.php?id=72>`_
   * - SAVI
     - Soil-Adjusted Vegetation Index
     - `Index DataBase SAVI <https://www.indexdatabase.de/db/i-single.php?id=87>`_
     
     
Burn Indices
~~~~~~~~~~~~~~~~~~~

The following table shows the list of built-in burn indices:

.. list-table:: Built-in burn indices.
   :widths: 20 50 30
   :header-rows: 1

   * - Index
     - Description     
     - Reference
   * - BAI
     - Burned Area Index
     - `(Martín, 1998) [spanish] <https://digital.csic.es/bitstream/10261/6426/1/Martin_Isabel_Serie_Geografica.pdf>`_ 
   * - BAIS2
     - Burned Area Index for Sentinel 2
     - `(Filipponi, 2018) <https://doi.org/10.3390/ecrs-2-05177>`_
   * - NBR
     - Normalized Burn Ratio
     - `Index DataBase NBR <https://www.indexdatabase.de/db/i-single.php?id=53>`_
     
Water Indices
~~~~~~~~~~~~~~~~~~~

The following table shows the list of built-in water indices:

.. list-table:: Built-in water indices.
   :widths: 20 50 30
   :header-rows: 1

   * - Index
     - Description     
     - Reference
   * - MNDWI
     - Modified Normalized Difference Water Index
     - `(Xu, 2006) <https://doi.org/10.1080/01431160600589179>`_  
   * - NDWI
     - Normalized Difference Water Index
     - `(McFeeters, 1996) <https://doi.org/10.1080/01431169608948714>`_
     
Snow Indices
~~~~~~~~~~~~~~~~~~~

The following table shows the list of built-in snow indices:

.. list-table:: Built-in snow indices.
   :widths: 20 50 30
   :header-rows: 1

   * - Index
     - Description     
     - Reference
   * - NDSI
     - Normalized Difference Snow Index
     - `(Riggs et al., 1994) <https://doi.org/10.1109/IGARSS.1994.399618>`_ 

.. warning::
   If the satellite platform doesn't have the required bands for computing an index, it won't be computed.

Usage
------------------

The :code:`index()` method computes the specified spectral index and adds it as a new band.

Let's take the Sentinel-2 SR image collection as example (remember to scale your image or image collection!):

.. code-block:: python

   S2 = ee.ImageCollection('COPERNICUS/S2_SR').scale()
   
By default, the :code:`index()` method computes the NDVI:

.. code-block:: python

   S2withIndices = S2.index()
   S2withIndices.select('NDVI')
   
If required, any of the above-mentioned indices can be computed by modifying the :code:`index` parameter:

.. code-block:: python

   S2withIndices = S2.index(index = 'EVI')
   S2withIndices.select('EVI')
   
Specific index-parameters can be changed, for example, the canopy background adjustment L is set to 1.0 for EVI, but for SAVI it can be changed to 0.5:

.. code-block:: python

   S2withIndices = S2.index('SAVI',L = 0.5)
   S2withIndices.select('SAVI')
   
If more than one index is required, a list of indices can be used:

.. code-block:: python

   S2withIndices = S2.index(['CIG','NBR','NDWI'])
   S2withIndices.select('CIG')
   S2withIndices.select('NBR')
   S2withIndices.select('NDWI')
   
Indices can also be computed for single images:

.. code-block:: python

   S2withIndices = S2.first().index(['GBNDVI','MNDVI','EVI'])
   S2withIndices.select('GBNDVI')
   S2withIndices.select('MNDVI')
   S2withIndices.select('EVI')
   
All vegetation indices can be computed by setting :code:`index = vegetation`:

.. code-block:: python

   S2withIndices = S2.index('vegetation')
   S2withIndices.select('NDVI')
   S2withIndices.select('GNDVI')
   S2withIndices.select('RVI')
   # ...
   
All burn indices can be computed by setting :code:`index = burn`:

.. code-block:: python

   S2withIndices = S2.index('burn')
   S2withIndices.select('BAI')
   S2withIndices.select('BAIS2')
   S2withIndices.select('NBR')
   
All water indices can be computed by setting :code:`index = water`:

.. code-block:: python

   S2withIndices = S2.index('water')
   S2withIndices.select('NDWI')
   S2withIndices.select('MNDWI')
   
All snow indices can be computed by setting :code:`index = snow`:

.. code-block:: python

   S2withIndices = S2.index('snow')
   S2withIndices.select('NDSI')
   
If you want to compute all available indices, you can set :code:`index = all`:

.. code-block:: python

   S2withIndices = S2.index('all')
   S2withIndices.select('NDVI')
   S2withIndices.select('BAI')
   S2withIndices.select('NDWI')
   S2withIndices.select('NDSI')
   # ...
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

MODIS Products (Terra + Aqua)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- `MCD43A4.006 MODIS Nadir BRDF-Adjusted Reflectance Daily 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MCD43A4>`_

MODIS Products (Terra)
~~~~~~~~~~~~~~~~~~~~~~~~~~

- `MOD09GQ.006 Terra Surface Reflectance Daily Global 250m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD09GQ>`_
- `MOD09GA.006 Terra Surface Reflectance Daily Global 1km and 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD09GA>`_
- `MOD09Q1.006 Terra Surface Reflectance 8-Day Global 250m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD09Q1>`_
- `MOD09A1.006 Terra Surface Reflectance 8-Day Global 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD09A1>`_

MODIS Products (Aqua)
~~~~~~~~~~~~~~~~~~~~~~~~~~

- `MYD09GQ.006 Aqua Surface Reflectance Daily Global 250m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MYD09GQ>`_
- `MYD09GA.006 Aqua Surface Reflectance Daily Global 1km and 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MYD09GA>`_
- `MYD09Q1.006 Aqua Surface Reflectance 8-Day Global 250m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MYD09Q1>`_
- `MYD09A1.006 Aqua Surface Reflectance 8-Day Global 500m <https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MYD09A1>`_

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
   * - EVI2
     - Two-Band Enhanced Vegetation Index
     - `(Jiang et al., 2008) <https://doi.org/10.1016/j.rse.2008.06.006>`_
   * - GARI
     - Green Atmospherically Resistant Vegetation Index
     - `Index DataBase GARI <https://www.indexdatabase.de/db/i-single.php?id=363>`_
   * - GBNDVI
     - Green-Blue Normalized Difference Vegetation Index
     - `Index DataBase GBNDVI <https://www.indexdatabase.de/db/i-single.php?id=186>`_
   * - GEMI
     - Global Environment Monitoring Index
     - `Index DataBase GEMI <https://www.indexdatabase.de/db/i-single.php?id=25>`_
   * - GLI
     - Green Leaf Index
     - `Index DataBase GLI <https://www.indexdatabase.de/db/i-single.php?id=375>`_
   * - GNDVI
     - Green Normalized Difference Vegetation Index
     - `Index DataBase GNDVI <https://www.indexdatabase.de/db/i-single.php?id=401>`_
   * - GRNDVI
     - Green-Red Normalized Difference Vegetation Index
     - `Index DataBase GRNDVI <https://www.indexdatabase.de/db/i-single.php?id=185>`_
   * - GVMI
     - Global Vegetation Moisture Index
     - `Index DataBase GVMI <https://www.indexdatabase.de/db/i-single.php?id=372>`_
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
   * - VARI
     - Visible Atmospherically Resistant Index
     - `Index DataBase VARI <https://www.indexdatabase.de/db/i-single.php?id=356>`_     
     
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
   * - CSIT
     - Char Soil Index Thermal
     - `(Smith et al., 2007) <https://doi.org/10.1080/01431160600954704>`_
   * - NBR
     - Normalized Burn Ratio
     - `Index DataBase NBR <https://www.indexdatabase.de/db/i-single.php?id=53>`_
   * - NBRT
     - Normalized Burn Ratio Thermal
     - `(Holden et al., 2005) <https://doi.org/10.1080/01431160500239008>`_
   * - NDVIT
     - Normalized Difference Vegetation Index Thermal
     - `(Smith et al., 2007) <https://doi.org/10.1080/01431160600954704>`_
   * - SAVIT
     - Soil-Adjusted Vegetation Index Thermal
     - `(Smith et al., 2007) <https://doi.org/10.1080/01431160600954704>`_
     
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
     
Drought Indices
~~~~~~~~~~~~~~~~~~~

The following table shows the list of built-in drought indices:

.. list-table:: Built-in snow indices.
   :widths: 20 50 30
   :header-rows: 1

   * - Index
     - Description     
     - Reference
   * - NDDI
     - Normalized Difference Drought Index
     - `(Gu et al., 2007) <https://doi.org/10.1029/2006GL029127>`_
     
Generalized Kernel Indices
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following table shows the list of built-in kernel indices:

.. list-table:: Built-in kernel indices.
   :widths: 20 50 30
   :header-rows: 1

   * - Index
     - Description     
     - Reference
   * - kEVI
     - Kernel Enhanced Vegetation Index
     - `(Camps-Valls et al., 2021) <https://doi.org/10.1126/sciadv.abc7447>`_
   * - kNDVI
     - Kernel Normalized Difference Vegetation Index
     - `(Camps-Valls et al., 2021) <https://doi.org/10.1126/sciadv.abc7447>`_
   * - kRVI
     - Kernel Ratio Vegetation Index
     - `(Camps-Valls et al., 2021) <https://doi.org/10.1126/sciadv.abc7447>`_
   * - kVARI
     - Kernel Visible Atmospherically Resistant Index
     - `(Camps-Valls et al., 2021) <https://doi.org/10.1126/sciadv.abc7447>`_

Kernels
----------------------

In the case of generalized kernel indices, the following kernels are available:

Linear Kernel
~~~~~~~~~~~~~~~~~~~

The linear kernel for generalized kernel indices can be selected by setting :code:`kernel = 'linear'`.

.. math::

   k(a,b) = ab
   
RBF Kernel
~~~~~~~~~~~~~~~~~~~

The Radial Basis Function (RBF) kernel for generalized kernel indices can be selected by setting :code:`kernel = 'RBF'`.

.. math::

   k(a,b) = exp(- \frac{(a - b) ^ 2}{2 \sigma ^ 2})
   
Where :math:`\sigma` is a free length-scale parameter.
   
Polynomial Kernel
~~~~~~~~~~~~~~~~~~~

The polynomial kernel for generalized kernel indices can be selected by setting :code:`kernel = 'poly'`.

.. math::

   k(a,b) = (ab + c) ^ p

Where :math:`c` is a free parameter that trades off the influence of higher-order versus lower-order terms and :math:`p` is the kernel degree.

List of Bands
----------------------

The following table shows the list of bands used for spectral indices computation:

.. list-table:: Bands used for spectral indices computation.
   :widths: 18 18 16 16 16 16
   :header-rows: 1

   * - Description
     - Name     
     - Sentinel-2
     - Landsat 8
     - Landsat 457
     - MODIS     
   * - Aerosols
     - A
     - B1
     - B1
     -
     -     
   * - Blue
     - B
     - B2
     - B2
     - B1
     - B3 
   * - Green
     - G
     - B3
     - B3
     - B2
     - B4    
   * - Red
     - R
     - B4
     - B4
     - B3
     - B1
   * - Red Edge 1
     - RE1
     - B5
     - 
     -
     -     
   * - Red Edge 2
     - RE2
     - B6
     - 
     -
     -     
   * - Red Edge 3
     - RE3
     - B7
     - 
     -
     -     
   * - Red Edge 4
     - RE4
     - B8A
     - 
     -
     -     
   * - NIR
     - N
     - B8
     - B5
     - B4
     - B2
   * - SWIR 1
     - S1
     - B11
     - B6
     - B5
     - B6     
   * - SWIR 2
     - S2
     - B12
     - B7
     - B7
     - B7   
   * - Thermal 1
     - T1
     - 
     - B10
     - B6
     -     
   * - Thermal 2
     - T2
     - 
     - B11
     - 
     -     

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

Generalized Kernel Indices
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Generalized kernel indices are availabe through eemont (e.g. kNDVI):

.. code-block:: python

   S2withIndices = S2.index('kNDVI')
   S2withIndices.select('kNDVI')
   
By default, the RBF kernel is used and the :code:`sigma` parameter is :code:`0.5 * (a + b)` (this means, that for :code:`k(N,R)`, :code:`sigma = '0.5 * (N + R)'`). If required, :code:`sigma` can be modified by another expression (using :code:`a` and :code:`b`) or a float:

.. code-block:: python

   S2withIndices = S2.index('kNDVI',sigma = 1)
   S2withIndices.select('kNDVI')
   
The kernel can be modified by modifying the :code:`kernel` parameter:

.. code-block:: python

   S2withIndices = S2.index('kNDVI',kernel = 'poly')
   S2withIndices.select('kNDVI')
   
For the polynomial kernel, the :code:`p` and :code:`c` parameters can be modified:

.. code-block:: python

   S2withIndices = S2.index('kNDVI',kernel = 'poly',p = 4,c = 0)
   S2withIndices.select('kNDVI')
   
All kernel indices can be computed by setting :code:`index = kernel`:

.. code-block:: python

   S2withIndices = S2.index('kernel')
   S2withIndices.select('kEVI')
   S2withIndices.select('kNDVI')
   S2withIndices.select('kRVI')
   S2withIndices.select('kVARI')
   
.. seealso::
   For more info on generalized kernel indices, please visit
   `‘Camps-Valls, G., et al. 2021. A unified vegetation index for quantifying the terrestrial biosphere. Science Advances 7 (9): eabc7447. Doi: 10.1126/sciadv.abc7447’ <https://doi.org/10.1126/sciadv.abc7447>`_.

Contribute
------------------

Do you know a spectral index that would fit in here? Check this, I'll show you how to add it to eemont!

First, fork the `eemont <https://github.com/davemlz/eemont>`_ repository and clone it to your local machine. Then, create a development branch::

   git checkout -b name-of-dev-branch
   
Now, you'll have to look for the :code:`common.py` module (eemont > eemont > common.py). Open this module and look for the :code:`_get_indices()` method. Inside this method, you'll find 4 dictionaries: :code:`vegetationIndices`, :code:`burnIndices`, :code:`waterIndices`, and :code:`snowIndices`. Go for the dictionary that best fits your spectral index and create a new item (this new item will be the new spectral index). Indices in each dictionary are structured as follows:

.. code-block:: python

   vegetationIndices = {
       ...,
       'NGRDI' : {
            'formula' : '(G - R) / (G + R)',
            'description' : 'Normalized Green Red Difference Index',
            'type' : 'vegetation',
            'requires' : ['G','R'],
            'reference' : 'https://www.indexdatabase.de/db/i-single.php?id=390',
            'contributor' : 'davemlz'
        },
        ...
   }
   
Now, let's image you are going to create a new index. Each index is a dictionary with the following items:

- Key of dictionary: This is the official index name, make sure the index doesn't exist yet.
- *formula* (string): Spectral index expression. This is the formula that eemont will use to compute the index. Follow the names described in the *List of Bands* table.
- *description* (string): Full name of the spectral index.
- *type* (string): One of 'vegetation', 'burn', 'water', 'snow'.
- *requires* (list[string]): List of bands required to compute the spectral index. Follow the names described in the *List of Bands* table.
- *reference* (string): Link to the DOI of the spectral index paper or to the `Index Database Link <https://www.indexdatabase.de/>`_. Include the full link.
- *contributor* (string | list[string]): Your GitHub username, and, if you want, your Twitter username (If using both, please create a list with both usernames ['gh_username','t_username']).

.. important::
   Make sure you have all the items. Spectral indices with missing elements WON'T be accepted.
   
After you have your own index, add it to the dictionary that best fits. It should look like this:

.. code-block:: python

   vegetationIndices = {
       ...,
       'your_index_name' : {
            'formula' : 'expression_formula_of_your_index',
            'description' : 'full_name_of_your_index',
            'type' : 'vegetation',
            'requires' : ['band1_used','band2_used',...], # e.g. ['N','R']
            'reference' : 'link_to_index_reference',
            'contributor' : 'your_gh_username'
        },
   }

Now it's time to test your index! Go to the :code:`tests` folder (eemont > tests) and run the following lines::

  cd tests
  python test_image.py
  python test_imagecollection.py

The tests will start running for ee.Image and ee.ImageCollection classes. At the end, no ERRORS should appear and the final message should be OK. If any deprecation warning appears, please ignore it, I'll look into it later.

Now it's time to commit your changes and push your development branch::

  git add .
  git commit -m "Description of your work"
  git push origin name-of-dev-branch
  
And finally, submit a pull request (and don't forget to add the tests!).
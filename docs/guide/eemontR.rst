Extensions
====================================

Did you know that you can use eemont inside QGIS or R? Let's see how!

QGIS
-----------

In order to use eemont inside QGIS, please follow these steps:

First, make sure that you have successfully installed the `Google Earth Engine Plugin for QGIS <https://gee-community.github.io/qgis-earthengine-plugin/>`_.

Then, open the OSGeo4W shell and run the following line:

.. code-block::

   py3_env
   
This will set the Python 3 environment. Afterwards, you can install eemont by running:

.. code-block::

   python -m pip install eemont
   
After installation, eemont can be used in the Python console inside QGIS:

.. code-block:: python

   import ee, eemont
   from ee_plugin import Map

   S2 = (ee.ImageCollection('COPERNICUS/S2_SR')
       .maskClouds()
       .scaleAndOffset()
       .spectralIndices(['NDVI','EVI','GNDVI'])
       .first())

   Map.addLayer(S2,{'min':0,'max':1,'bands':'NDVI'},'NDVI',True)


R
------

In order to use eemont inside R, please follow these steps:

First, make sure that you have successfully installed the `rgee <https://github.com/r-spatial/rgee>`_ and `reticulate <https://rstudio.github.io/reticulate/>`_.

Then, open a new R script and run the following chunk:

.. code-block:: r

   library(rgee)
   library(reticulate)
   
   ee_Initialize()

Now, we are ready to go!

First, we have to install :code:`eemont` (if required):

.. code-block:: r

   py_install("eemont",pip = TRUE)
   
Then, :code:`eemont` can be imported!

.. code-block:: r

   eemont <- import("eemont")
   
All python methods are available here, let's take a look!

Define a point of interest:

.. code-block:: r

   point <- ee$Geometry$Point(c(-74.0592,11.3172))
   
Get and filter the Landsat 8 SR collection:

.. code-block:: r

   L8 <- ee$ImageCollection('LANDSAT/LC08/C01/T1_SR')$filterBounds(point)
   
And use :code:`eemont` as you wish!

.. code-block:: r

   L8 <- L8$maskClouds()$scaleAndOffset()$spectralIndices("NDWI")

Julia
------

In order to use eemont inside Julia, please follow these steps:

First, make sure that you have successfully installed `EarthEngine.jl <https://docs.juliahub.com/EarthEngine/jof0K/0.3.2/index.html>`_.

Then, open a new Julia script and run the following chunk:

.. code-block:: julia

   using EarthEngine, PyCall
   
   Initialize()

Now, we are ready to go!

First, we have to install :code:`eemont` (if required):

.. code-block:: julia

   import Conda; Conda.add("eemont",channel="conda-forge")
   
Then, :code:`eemont` can be imported!

.. code-block:: julia

   eemont = pyimport("eemont");
   
All python methods are available here, let's take a look!

Define a point of interest:

.. code-block:: julia

   point = Point(-74.0592,11.3172)
   
Get and filter the Landsat 8 SR collection:

.. code-block:: julia

   L8 = filterBounds(EE.ImageCollection('LANDSAT/LC08/C01/T1_SR'),point)
   
And use :code:`eemont` as you wish!

.. code-block:: julia

   L8 = spectralIndices(scaleAndOffset(maskClouds(L8)),"NDWI")
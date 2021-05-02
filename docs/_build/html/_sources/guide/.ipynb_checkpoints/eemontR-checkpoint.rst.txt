eemont in R
====================================

Let's see how to use eemont in R with rgee!

Before anything, let's import our modules and authenticate in Google Earth Engine:

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

   L8 <- L8$maskClouds()$scale()$index("NDWI")
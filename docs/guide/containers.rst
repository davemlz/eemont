Emulating Containers
====================================

Let's see how to use container emulation methods in eemont!

Before anything, let's import our modules and authenticate in Google Earth Engine:

.. code-block:: python

   import ee, eemont
   
   ee.Authenticate()
   ee.Initialize()

Now, we are ready to go!

Overview
-----------

The eemont package extends the ee.Image, ee.ImageCollection, ee.Feature, ee.FeatureCollection, ee.List and ee.Dictionary classes with container emulation methods.

ee.Image
~~~~~~~~~~~~~~~~~~~

The following table shows the list of container emulation methods that are overloaded:

.. list-table:: Container emulation methods.
   :widths: 20 40 40
   :header-rows: 1

   * - Operation
     - GEE Python method     
     - Container Emulation Method
   * - Get Item By Key
     - Image.select(bands)
     - Image[bands]
   * - Get Item By Index
     - Image.select(index)
     - Image[index]
   * - Get Item By Slice
     - Image.slice(start,stop)
     - Image[start:stop]
     
ee.ImageCollection 
~~~~~~~~~~~~~~~~~~~

The following table shows the list of container emulation methods that are overloaded:

.. list-table:: Container emulation methods.
   :widths: 20 40 40
   :header-rows: 1

   * - Operation
     - GEE Python method     
     - Container Emulation Method
   * - Get Item By Key
     - ImageCollection.select(bands)
     - ImageCollection[bands]
   * - Get Item By Index
     - ImageCollection.select(index)
     - ImageCollection[index]
   * - Get Item By Slice
     - ImageCollection.map(lambda x: x.slice(start,stop))
     - ImageCollection[start:stop]
   * - Length
     - ImageCollection.size().getInfo()
     - len(ImageCollection)

ee.Feature 
~~~~~~~~~~~~~~~~~~~

The following table shows the list of container emulation methods that are overloaded:

.. list-table:: Container emulation methods.
   :widths: 20 40 40
   :header-rows: 1

   * - Operation
     - GEE Python method     
     - Container Emulation Method
   * - Get Item By Key
     - Feature.select(properties)
     - Feature[properties]

ee.FeatureCollection 
~~~~~~~~~~~~~~~~~~~~~~

The following table shows the list of container emulation methods that are overloaded:

.. list-table:: Container emulation methods.
   :widths: 20 40 40
   :header-rows: 1

   * - Operation
     - GEE Python method     
     - Container Emulation Method
   * - Get Item By Key
     - FeatureCollection.select(properties)
     - FeatureCollection[properties]
   * - Length
     - FeatureCollection.size().getInfo()
     - len(FeatureCollection)
     
ee.List 
~~~~~~~~~~~~~~~~~~~

The following table shows the list of container emulation methods that are overloaded:

.. list-table:: Container emulation methods.
   :widths: 20 40 40
   :header-rows: 1

   * - Operation
     - GEE Python method     
     - Container Emulation Method
   * - Get Item By Index
     - List.select(index)
     - List[index]
   * - Get Item By Slice
     - List.slice(start,stop)
     - List[start:stop]
   * - Length
     - List.length().getInfo()
     - len(List)
   * - Contains
     - List.contains(value).getInfo()
     - value in List
     
ee.Dictionary 
~~~~~~~~~~~~~~~~~~~

The following table shows the list of container emulation methods that are overloaded:

.. list-table:: Container emulation methods.
   :widths: 20 40 40
   :header-rows: 1

   * - Operation
     - GEE Python method     
     - Container Emulation Method
   * - Get Item By Key
     - Dictionary.get(key)
     - Dictionary[key]
   * - Length
     - Dictionary.size().getInfo()
     - len(Dictionary)
   * - Contains
     - Dictionary.contains(key).getInfo()
     - key in Dictionary

Usage
------------------

Container emulation methods can be used on any of the Earth Engine objects mentioned above. Let's see how to use them!

Raster Types
~~~~~~~~~~~~~~~~~~~

Let's take the Sentinel-2 SR image collection as example:

.. code-block:: python

   point = ee.Geometry.Point([-76.0269,2.92846])
   S2 = (ee.ImageCollection('COPERNICUS/S2_SR')
      .filterBounds(point)
      .sort('CLOUDY_PIXEL_PERCENTAGE')
      .first()
      .maskClouds()
      .scale())

Now, if we want to select a specific band, we can do it as follows:

.. code-block:: python

   NIR = S2['B8']
   
Or multiple bands:

.. code-block:: python

   NIRRED = S2[['B8','B4']]
   
We can also use regex!:

.. code-block:: python

   bands = S2['B.*']
   
Or an index:

.. code-block:: python

   BLUE = S2[1]
   
Or even better, a slice:

.. code-block:: python

   RGB = S2[1:4]
   
All of these methods can also be done for ee.ImageCollection objects:

.. code-block:: python

   S2 = ee.ImageCollection('COPERNICUS/S2_SR').filterBounds(point)['B.*']
   
And, additionally, we can check the size of the image collection by using :code:`len()`:

.. code-block:: python

   len(S2)
 
Vector Types
~~~~~~~~~~~~~~~~~~~

Let's see another example, but using features:

.. code-block:: python

   WDPA = ee.FeatureCollection("WCMC/WDPA/current/polygons") 
   
And now, let's take some properties:

.. code-block:: python

   WDPA = WDPA[['WDPAID','NAME','REP_AREA']]
   
Now, let's check the size of the feature collection:

.. code-block:: python

   len(WDPA)
   
For the ee.List objects, we can also use container emulaion methods!

Lists
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   l = ee.List([100,120,230,310,450])

You can get an item by using its index:

.. code-block:: python

   l[0]
   
Or multiple items by using an slice:

.. code-block:: python

   l[1:4]
   
You can also check if an item is in the list:

.. code-block:: python

   370 in l
   
And get the length of the list:

.. code-block:: python

   len(l)

Dictionaries
~~~~~~~~~~~~~~~~~~~

Things work in a similar way for ee.Dictionary classes:

.. code-block:: python

   d = ee.Dictionary({'ID': 1,'Name': 'Natural Park','Area': 3240})
   
We can get a value by using its key:

.. code-block:: python

   d['Name']
   
We can also check if a key is in a dictionary:

.. code-block:: python

   'Area' in d
   
And check the size of the dictionary:

.. code-block:: python

   len(d)
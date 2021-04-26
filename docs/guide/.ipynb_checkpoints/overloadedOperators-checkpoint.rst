Overloaded Operators
====================================

Let's see how to use overloaded operators in eemont!

Before anything, let's import our modules and authenticate in Google Earth Engine:

.. code-block:: python

   import ee, eemont
   
   ee.Authenticate()
   ee.Initialize()

Now, we are ready to go!

Overview
-----------

The eemont package extends the ee.Image and ee.Number classes with the binary and unary operators (including rich comparisons).

ee.Image 
-------------------

Binary Operators
~~~~~~~~~~~~~~~~~~~

The following table shows the list of binary operators that are overloaded:

.. list-table:: Binary operators.
   :widths: 20 40 40
   :header-rows: 1

   * - Operation
     - GEE Python method     
     - Overloaded Operator
   * - Addition
     - Image1.add(Image2)
     - Image1 + Image2 
   * - Subtraction
     - Image1.subtract(Image2)
     - Image1 - Image2
   * - Multiplication
     - Image1.multiply(Image2)
     - Image1 * Image2
   * - Division
     - Image1.divide(Image2)
     - Image1 / Image2
   * - Floor Division
     - Image1.divide(Image2).floor()
     - Image1 // Image2
   * - Modulo
     - Image1.mod(Image2)
     - Image1 % Image2
   * - Power
     - Image1.pow(Image2)
     - Image1 ** Image2
   * - Left Shift
     - Image1.leftShift(Image2)
     - Image1 << Image2
   * - Right Shift
     - Image1.rightShift(Image2)
     - Image1 >> Image2
   * - And
     - Image1.And(Image2)
     - Image1 & Image2
   * - Or
     - Image1.Or(Image2)
     - Image1 | Image2
          
Rich Comparisons
~~~~~~~~~~~~~~~~~~~

The following table shows the list of rich comparisons that are overloaded:

.. list-table:: Rich comparisons.
   :widths: 20 40 40
   :header-rows: 1

   * - Operation
     - GEE Python method          
     - Overloaded Operator
   * - Lower Than
     - Image1.lt(Image2)
     - Image1 < Image2 
   * - Lower Than or Equal
     - Image1.lte(Image2)
     - Image1 <= Image2
   * - Equal
     - Image1.eq(Image2)
     - Image1 == Image2
   * - Not Equal
     - Image1.neq(Image2)    
     - Image1 != Image2
   * - Greater Than
     - Image1.gt(Image2)
     - Image1 > Image2 
   * - Greater Than or Equal
     - Image1.gte(Image2)
     - Image1 >= Image2
   * - Equal
     - Image1.eq(Image2)
     - Image1 == Image2
     
Unary Operators
~~~~~~~~~~~~~~~~~~~

The following table shows the list of unary operators that are overloaded:

.. list-table:: Unary operators.
   :widths: 20 40 40
   :header-rows: 1

   * - Operation
     - GEE Python method          
     - Overloaded Operator
   * - Negation
     - Image.multiply(-1)
     - \-\ Image
   * - Invert
     - Image.Not()
     - ~ Image
     
ee.Number 
-------------------

Binary Operators
~~~~~~~~~~~~~~~~~~~

The following table shows the list of binary operators that are overloaded:

.. list-table:: Binary operators.
   :widths: 20 40 40
   :header-rows: 1

   * - Operation
     - GEE Python method     
     - Overloaded Operator
   * - Addition
     - Number1.add(Number2)
     - Number1 + Number2 
   * - Subtraction
     - Number1.subtract(Number2)
     - Number1 - Number2
   * - Multiplication
     - Number1.multiply(Number2)
     - Number1 * Number2
   * - Division
     - Number1.divide(Number2)
     - Image1 / Image2
   * - Floor Division
     - Number1.divide(Number2).floor()
     - Number1 // Number2
   * - Modulo
     - Number1.mod(Number2)
     - Number1 % Number2
   * - Power
     - Number1.pow(Number2)
     - Number1 ** Number2
   * - Left Shift
     - Number1.leftShift(Number2)
     - Number1 << Number2
   * - Right Shift
     - Number1.rightShift(Number2)
     - Number1 >> Number2
   * - And
     - Number1.And(Number2)
     - Number1 & Number2
   * - Or
     - Number1.Or(Number2)
     - Number1 | Number2
          
Rich Comparisons
~~~~~~~~~~~~~~~~~~~

The following table shows the list of rich comparisons that are overloaded:

.. list-table:: Rich comparisons.
   :widths: 20 40 40
   :header-rows: 1

   * - Operation
     - GEE Python method          
     - Overloaded Operator
   * - Lower Than
     - Number1.lt(Number2)
     - Number1 < Number2 
   * - Lower Than or Equal
     - Number1.lte(Number2)
     - Number1 <= Number2
   * - Equal
     - Number1.eq(Number2)
     - Number1 == Number2
   * - Not Equal
     - Number1.neq(Number2)    
     - Number1 != Number2
   * - Greater Than
     - Number1.gt(Number2)
     - Number1 > Number2 
   * - Greater Than or Equal
     - Number1.gte(Number2)
     - Number1 >= Number2
   * - Equal
     - Number1.eq(Number2)
     - Number1 == Number2
     
Unary Operators
~~~~~~~~~~~~~~~~~~~

The following table shows the list of unary operators that are overloaded:

.. list-table:: Unary operators.
   :widths: 20 40 40
   :header-rows: 1

   * - Operation
     - GEE Python method          
     - Overloaded Operator
   * - Negation
     - Number.multiply(-1)
     - \-\ Number
   * - Invert
     - Number.Not()
     - ~ Number
     
ee.List 
-------------------

Binary Operators
~~~~~~~~~~~~~~~~~~~

The following table shows the list of binary operators that are overloaded:

.. list-table:: Binary operators.
   :widths: 20 40 40
   :header-rows: 1

   * - Operation
     - GEE Python method     
     - Overloaded Operator
   * - Concatenation
     - List1.cat(List2)
     - List1 + List2
   * - Repeat
     - ee.List.repeat(List,Value)
     - List * Value

Usage
------------------

Overloaded operators can be used on any ee.Image or ee.Number object. Let's see how to compute the EVI using overloaded operators!

Let's take the Sentinel-2 SR image collection as example (remember to scale your image or image collection!):

.. code-block:: python

   point = ee.Geometry.Point([-76.0269,2.92846])
   S2 = (ee.ImageCollection('COPERNICUS/S2_SR')
      .filterBounds(point)
      .sort('CLOUDY_PIXEL_PERCENTAGE')
      .first()
      .maskClouds()
      .scale())

Now, let's take apart the bands that we need (it is not necessary, but it's easier to use :code:`N` instead of :code:`S2.select('B8')`):

.. code-block:: python

   N = S2.select('B8')
   R = S2.select('B4')
   B = S2.select('B2')
   
And finally, let's compute the EVI using overloaded operators:

.. code-block:: python

   EVI = 2.5 * (N - R) / (N + 6.0 * R - 7.5 * B + 1.0)

Let's see another example, but using rich comparisons. We are going to compute a snow cover mask!

First, compute the NDSI:

.. code-block:: python

   S2 = S2.index('NDSI')   
   
And now, let's take apart the bands that we need:

.. code-block:: python

   NDSI = S2.select('NDSI')
   N = S2.select('B8')
   G = S2.select('B3')
   
Finally, compute the snow cover mask `(Hall et al., 2001) <https://modis.gsfc.nasa.gov/data/atbd/atbd_mod10.pdf>`_:

.. code-block:: python

   snowPixels = (NDSI > 0.4) & (N >= 0.1) & (G > 0.11)

And update the mask (if required):

.. code-block:: python

   S2 = S2.updateMask(snowPixels)
Data Conversion
====================================

Let's see how to convert non-Earth Engine classes to Earth Engine classes.

Before anything, let's import our modules and authenticate in Google Earth Engine:

.. code-block:: python

   import ee, eemont
   import pandas as pd
   
   ee.Authenticate()
   ee.Initialize()

Now, we are ready to go!

Overview
-----------

The eemont package extends the pd.DataFrame classes with the method :code:`toEEFeatureCollection()`:

pd.DataFrame
~~~~~~~~

.. currentmodule:: eemont.dataframe

.. autosummary::

   toEEFeatureCollection

Methods
-----------

A table of availabe conversion options is shown below:

.. list-table:: Available options
   :widths: 30 30 40
   :header-rows: 1

   * - From
     - To
     - Method
   * - pd.DataFrame
     - ee.FeatureCollection
     - :code:`toEEFeatureCollection()`

Usage
------------------

Let's create a pandas data frame:

.. code-block:: python

   df = pd.DataFrame()
   df['lat'] = [2.92846, 4.8927]
   df['lon'] = [-76.0269, -75.3188]
   df['name'] = ['Nevado del Huila', 'Nevado del Ruiz']
   
This data frame can be easily converted into a ee.FeatureCollection (with no geometries) using the :code:`toEEFeatureCollection()` method for pd.DataFrame classes:

.. code-block:: python

   fcWithNoGeometries = df.toEEFeatureCollection()

If the data frame has latitude and longitude columns, these can be specified in the :code:`latitude` and :code:`longitude` parameters:

.. code-block:: python

   fcWithGeometries = df.toEEFeatureCollection(latitude = 'lat',longitude = 'lon')
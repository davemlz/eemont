Constructors
====================================

Let's see how to use the extended constructors available through eemont!

Before anything, let's import our modules and authenticate in Google Earth Engine:

.. code-block:: python

   import ee, eemont
   
   ee.Authenticate()
   ee.Initialize()

Now, we are ready to go!

Overview
-----------

The eemont package extends the ee.Geometry, ee.Feature and ee.FeatureCollection classes with the following constructors:

ee.Geometry
~~~~~~~~~~~~~~~~~~~~~~~~

.. currentmodule:: eemont.geometry

.. autosummary::

   BBoxFromQuery
   PointFromQuery
   MultiPointFromQuery

ee.Feature
~~~~~~~~~~~~~~~~~~~~~~~~

.. currentmodule:: eemont.feature

.. autosummary::

   BBoxFromQuery
   PointFromQuery

ee.FeatureCollection
~~~~~~~~~~~~~~~~~~~~~~~~

.. currentmodule:: eemont.featurecollection

.. autosummary::

   MultiPointFromQuery
   
Usage
------------------

Constructors By Query
~~~~~~~~~~~~~~~~~~~~~~~~

The constructors by query use the `geopy package <https://pypi.org/project/geopy/>`_ to construct geometries, features and feature collections.

The simplest geometry to construct is the Point, and can be constructed for ee.Geometry and ee.Feature classes;

.. code-block:: python

   geometry = ee.Geometry.PointFromQuery('Cali, Colombia',user_agent = 'eemont-user-guide-constructors')
   feature = ee.Feature.PointFromQuery('Cali, Colombia',user_agent = 'eemont-user-guide-constructors')
   
It has to be noted that the :code:`user_agent` argument is mandatory and it can be set to any string representing the app or the GEE username.

.. warning::
   If the :code:`user_agent` argument is not defined, the constructor will raise an Exception.

By default, to geocode the query, the Nominatim geocoder is used. If required, this parameter can be modified:

.. code-block:: python

   geometry = ee.Geometry.PointFromQuery('Cali, Colombia',geocoder = 'arcgis',user_agent = 'eemont-user-guide-constructors')
                                 
The second geometry to construct is the MultiPoint, and can be constructed for ee.Geometry and ee.FeatureCollection classes:

.. code-block:: python

   geometry = ee.Geometry.MultiPointFromQuery('Colombia',user_agent = 'eemont-user-guide-constructors')
   feature_collection = ee.FeatureCollection.MultiPointFromQuery('Colombia',user_agent = 'eemont-user-guide-constructors')

.. note::
   When a query is submitted, a set of locations is retrieved. The MultiPoint constructors create a class taking all locations into account. The Point constructors just take the first one.

The last geometry to construct is the Bounding Box, and can be constructed for ee.Geometry and ee.Feature classes:

.. code-block:: python

   geometry = ee.Geometry.BBoxFromQuery('Europe',user_agent = 'eemont-user-guide-constructors')
   feature = ee.Feature.BBoxFromQuery('Europe',user_agent = 'eemont-user-guide-constructors')
   
.. note::
   When using constructors for ee.Feature and ee.FeatureCollection classes, the raw properties of the location, or locations, are set for the feature or feature collection.
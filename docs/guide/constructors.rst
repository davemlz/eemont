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
   LinearRingFromPlusCodes
   LineStringFromPlusCodes
   MultiLineStringFromPlusCodes
   MultiPointFromPlusCodes
   MultiPointFromQuery
   MultiPolygonFromPlusCodes
   PointFromPlusCode
   PointFromQuery
   PolygonFromPlusCodes
   RectangleFromPlusCodes   

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
   
Constructors By Plus Codes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::
   The awesome Plus Codes constructors and methods were created by `Aaron Zuspan <https://github.com/aazuspan>`_ (creator of `sankee <https://github.com/aazuspan/sankee>`_).

`Plus Codes <https://maps.google.com/pluscodes/>`_ are street addresses that represent an area based on longitude and latitude coordinates (e.g. 
"89MH+PW").

.. warning::
   In order to use Plus Codes constructors, it is required to install :code:`openlocationcode`. Please install it by running :code:`pip install openlocationcode`.
   
There are two ways to use the Plus Codes constructors.

1. By using a full Plus Code (e.g. "85FPQXGV+XH").
2. By using a short Plus Code (e.g. "QXGV+XH Denver, CO, USA").

When using full Plus Codes, just use it as the principal argument in the constructor:

.. code-block:: python

   point = ee.Geometry.PointFromPlusCode("85FPQXGV+XH")
   
When using a short Plus Code, it is required to use a geocoder (just like the constructors by queries), and therefore, an user agent must be declared:

.. code-block:: python

   point = ee.Geometry.PointFromPlusCode("QXGV+XH Denver, CO, USA",user_agent = 'eemont-user-guide-constructors')
   
More complex geometries can be constructed using a list of Plus Codes or a nested list of Plus Codes:

.. code-block:: python

   codes = ['85FQ2222+22', '85FR2222+22', '85GR2222+22']
   
   multipoint = ee.Geometry.MultiPointFromPlusCodes(codes)
   linestring = ee.Geometry.LineStringFromPlusCodes(codes)
   polygon = ee.Geometry.PolygonFromPlusCodes(codes)
   
   nestedCodes = [
        ['85FQ2222+22', '85FR2222+22', '85GR2222+22'], 
        ['85FP8PC2+G2', '85FPJF23+G4', '85FPMW2R+RP'],
        ['85FPRJ5W+82', '85GP3M67+CP', '85GQ2R7C+38'],
    ]
    
    multilinestring = ee.Geometry.MultiLineStringFromPlusCodes(nestedCodes)
    multipolygon = ee.Geometry.MultiPolygonFromPlusCodes(nestedCodes)
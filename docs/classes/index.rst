API Reference
================

.. toctree::
   :caption: Earth Engine Module
   :maxdepth: 2
   :hidden:
   
   ee

.. toctree::
   :caption: Earth Engine Classes
   :maxdepth: 2
   :hidden:
   
   eedictionary
   eefeature
   eefeaturecollection
   eegeometry
   eeimage
   eeimagecollection
   eelist

.. toctree::
   :caption: New Classes
   :maxdepth: 2
   :hidden:
   
   eeapp
   
.. toctree::
   :caption: Non-Earth Engine Classes
   :maxdepth: 2
   :hidden:
   
   pddataframe
   
.. toctree::
   :caption: Additional Modules
   :maxdepth: 2
   :hidden:
   
   common

Extended Methods for the Earth Engine Module
--------------------------------------------

ee
~~

..
   .. currentmodule:: eemont.extra

   .. autosummary::

      install
      require
      uninstall

.. currentmodule:: eemont.app

.. autosummary::

   listApps

.. currentmodule:: eemont.common

.. autosummary::

   listDatasets

Extended Earth Engine Object Classes
------------------------------------------

Here you can find the reference of the new methods for each one of the Earth Engine classes:

ee.Dictionary
~~~~~~~~~~~~~

.. currentmodule:: eemont.eeDictionary

.. autosummary::

   __contains__
   __getitem__

ee.Feature
~~~~~~~~~~~~~

.. currentmodule:: eemont.feature

.. autosummary::

   BBoxFromQuery
   PointFromQuery
   plusCodes

ee.FeatureCollection
~~~~~~~~~~~~~~~~~~~~~~~

.. currentmodule:: eemont.featurecollection

.. autosummary::
   
   MultiPointFromQuery
   
ee.Geometry
~~~~~~~~~~~~~

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
   plusCodes

ee.Image
~~~~~~~~

.. currentmodule:: eemont.image

.. autosummary::
   
   getCitation
   getDOI
   getOffsetParams
   getScaleParams
   getSTAC
   index
   maskClouds
   matchHistogram
   panSharpen
   preprocess
   scale
   scaleAndOffset
   spectralIndices
   tasseledCap
   
ee.ImageCollection
~~~~~~~~~~~~~~~~~~~~~~~~

.. currentmodule:: eemont.imagecollection
.. autosummary::

   closest
   getCitation
   getDOI
   getOffsetParams
   getScaleParams
   getSTAC
   getTimeSeriesByRegion
   getTimeSeriesByRegions
   index
   maskClouds
   panSharpen
   preprocess
   scale
   scaleAndOffset
   spectralIndices
   tasseledCap

ee.List
~~~~~~~
   
.. currentmodule:: eemont.eeList

.. autosummary::

   __add__
   __contains__
   __getitem__
   __len__
   __mul__
   __radd__
   __rmul__

Extended Non-Earth Engine Object Classes
------------------------------------------

Non-Earth Engine classes such as pd.DataFrame are also extended:

pd.DataFrame
~~~~~~~~~~~~~~~~~~~~~~~~

.. currentmodule:: eemont.dataframe
.. autosummary::

   toEEFeatureCollection
   
Additional Modules
------------------------------------------

Functions of additional modules:

Common
~~~~~~~~~~~~~~~~~~~~~~~~

.. currentmodule:: eemont.common
.. autosummary::

   indices
   listDatasets
   listIndices
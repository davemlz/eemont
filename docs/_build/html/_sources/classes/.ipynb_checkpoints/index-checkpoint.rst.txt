API Reference
================

.. toctree::
   :caption: Extended Classes
   :maxdepth: 2
   :hidden:

   common
   pddataframe
   eefeature
   eefeaturecollection
   eegeometry
   eeimage
   eeimagecollection   

Extended Earth Engine Object Classes
------------------------------------------

Here you can find the reference of the new methods for each one of the Earth Engine classes:

ee.Feature
~~~~~~~~~~~~~

.. currentmodule:: eemont.feature

.. autosummary::

   BBoxFromQuery
   PointFromQuery
   
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
   PointFromQuery
   MultiPointFromQuery

ee.Image
~~~~~~~~

.. currentmodule:: eemont.image

.. autosummary::
   
   index
   maskClouds
   scale
   
ee.ImageCollection
~~~~~~~~~~~~~~~~~~~~~~~~

.. currentmodule:: eemont.imagecollection
.. autosummary::

   closest 
   getTimeSeriesByRegion
   getTimeSeriesByRegions
   index
   maskClouds
   scale

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
   listIndices
API Reference
================

.. toctree::
   :caption: Earth Engine Classes
   :maxdepth: 2
   :hidden:
   
   eefeature
   eefeaturecollection
   eegeometry
   eeimage
   eeimagecollection
   
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
   
   getOffsetParams
   getScaleParams
   index
   maskClouds
   preprocess
   scale
   scaleAndOffset
   spectralIndices
   
ee.ImageCollection
~~~~~~~~~~~~~~~~~~~~~~~~

.. currentmodule:: eemont.imagecollection
.. autosummary::

   closest
   getOffsetParams
   getScaleParams
   getTimeSeriesByRegion
   getTimeSeriesByRegions
   index
   maskClouds
   preprocess
   scale
   scaleAndOffset
   spectralIndices

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
eemont
======

.. image:: https://img.shields.io/pypi/v/eemont.svg
    :target: https://pypi.python.org/pypi/eemont
    :alt: Latest PyPI version

#### A Python package for Google Earth Engine utilities

## Installation
While eemont gets to its first release, you can install the development version by runnig the following command:

```python
!pip install git+https://github.com/davemlz/eemont
```

## Usage
**[Remember!]** To use eemont, you **must** have a Google Earth Engine account and authenticate using your credentials.

```python
import ee
ee.Authenticate()
ee.Initialize()
```

Let's take a look on how easy is to use this package!

Now, let's take a Sentinel-2 collection: we will mask clouds and shadows, scale the image, select the closest image to a specified date, compute some spectral indices and visualize the image (We are goin to use the awesome geemap package for this!).

```python
# Import the modules from eemont
from eemont import sentinel2, time, visualization

# Import geemap for visualization
import geemap

# Point of interest
point = ee.Geometry.Point([-76.21, 4.32])

# Take the Sentinel-2 SR product
S2 = ee.ImageCollection('COPERNICUS/S2_SR').filterBounds(point)

# Mask clouds and shadows using the cloud probability and the Cloud Displacement index (CDI)
S2 = sentinel2.maskCLouds(S2, prob = 70, cdi = -0.5)

# Scale the image to [0,1]
S2 = sentinel2.scale(S2)

# Select the closest image to a specified date
S2closest = time.closest(S2, date = '2020-03-23')

# Compute some vegetation, water and burn indices
# (Indices are added as new bands)
S2closest = sentinel2.index(S2closest, index = ['GNDVI','NDWI','BAIS2'])

# Visualize the image
Map = geemap.Map()
Map.addLayer(S2closest, visualization.rgb(), 'RGB') # RGB visualization
Map.addLayer(S2closest, visualization.infrared(), 'Infrared') # Infrared visualization
Map.addLayer(S2closest.select('GNDVI'), visualization.index(palette = 'vegetation'), 'GNDVI') # Vegetation index visualization
Map.addLayer(S2closest.select('NDWI'), visualization.index(palette = 'water'), 'NDWI') # Water index visualization
Map.addLayer(S2closest.select('BAIS2'), visualization.index(palette = 'burn'), 'BAIS2') # Burn index visualization
Map
```

And as simple like, the job is done!

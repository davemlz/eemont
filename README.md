eemont
======

.. image:: https://img.shields.io/pypi/v/eemont.svg
    :target: https://pypi.python.org/pypi/eemont
    :alt: Latest PyPI version

#### A Python package for Google Earth Engine utilities

## Installation
While eemont gets to its first release, you can install the development version by runnig the following command:

```python
pip install git+https://github.com/davemlz/eemont
```

## Usage
**[Remember!]** To use eemont, you **must** have a Google Earth Engine account and authenticate using your credentials.

```python
import ee
ee.Authenticate()
ee.Initialize()
```

### Sentinel-2 module

Let's take the Sentinel-2 Surface Reflectance product and select the first 10 images:

```python
S2 = ee.ImageCollection('COPERNICUS/S2_SR').limit(10)
```

Now, let's import the Sentinel-2 module:

```python
from eemont import Sentinel2
```

#### Masking clouds and shadows

To mask clouds and shadows (automatically using cloud probability):

```python
S2masked = Sentinel2.maskClouds(S2)
```

To mask clouds and shadows using the QA band:

```python
S2masked = Sentinel2.maskClouds(S2, method = 'qa')
```

To mask just clouds:

```python
S2masked = Sentinel2.maskClouds(S2, maskShadows = False)
```

To mask clouds and shadows (automatically using cloud probability):

```python
S2masked = Sentinel2.maskClouds(S2)
```

To mask clouds and shadows with a 80% cloud probability:

```python
S2masked = Sentinel2.maskClouds(S2, prob = 80)
```

To mask clouds and shadows with a 60% cloud probability and using a Cloud Displacement Index (CDI) threshold of -0.5:

```python
S2masked = Sentinel2.maskClouds(S2, prob = 60, cdi = -0.5)
```

You can also mask clouds and shadows from a single image:

```python
S2singleImageMasked = Sentinel2.maskClouds(S2.first())
```

#### Scaling pixel values

To scale the pixel values to [0,1]:

```python
S2scaled = Sentinel2.reflectance(S2masked)
```

You can also scale values of a single image:

```python
S2singleImageScaled = Sentinel2.reflectance(S2masked.first())
```

#### Spectral Indices

Spectral indices ar added as new bands.

To compute a spectral index:

```python
S2index = Sentinel2.spectralIndex(S2scaled, index = 'GNDVI')
```

To compute more than one spectral index:

```python
S2index = Sentinel2.spectralIndex(S2scaled, index = ['GNDVI','NDWI','NBR'])
```

To compute all available Vegetation Indices:

```python
S2index = Sentinel2.spectralIndex(S2scaled, index = 'vegetation')
```

To compute all available Burn Indices:

```python
S2index = Sentinel2.spectralIndex(S2scaled, index = 'burn')
```

To compute all available Water Indices:

```python
S2index = Sentinel2.spectralIndex(S2scaled, index = 'water')
```

To compute all available indices:

```python
S2index = Sentinel2.spectralIndex(S2scaled, index = 'all')
```

You can also compute indices for a single image:

To compute all available Vegetation Indices:

```python
S2singleImageIndex = Sentinel2.spectralIndex(S2singleImageScaled, index = 'vegetation')
```

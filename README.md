<p align="center">
  <a href="https://github.com/davemlz/eemont"><img src="https://raw.githubusercontent.com/davemlz/eemont/master/docs/_static/header2.png" alt="header"></a>
</p>
<p align="center">
    <em>A python package that extends Google Earth Engine</em>
</p>
<p align="center">
<a href='https://pypi.python.org/pypi/eemont'>
    <img src='https://img.shields.io/pypi/v/eemont.svg' alt='PyPI' />
</a>
<a href='https://anaconda.org/conda-forge/eemont'>
    <img src='https://img.shields.io/conda/vn/conda-forge/eemont.svg' alt='conda-forge' />
</a>
<a href="https://opensource.org/licenses/MIT" target="_blank">
    <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License">
</a>
<a href='https://eemont.readthedocs.io/en/latest/?badge=latest'>
    <img src='https://readthedocs.org/projects/eemont/badge/?version=latest' alt='Documentation Status' />
</a>
<a href="https://github.com/davemlz/eemont/actions/workflows/tests.yml" target="_blank">
    <img src="https://github.com/davemlz/eemont/actions/workflows/tests.yml/badge.svg" alt="Tests">
</a>
<a href="https://github.com/sponsors/davemlz" target="_blank">
    <img src="https://img.shields.io/badge/GitHub%20Sponsors-Donate-ff69b4.svg" alt="GitHub Sponsors">
</a>
<a href="https://www.buymeacoffee.com/davemlz" target="_blank">
    <img src="https://img.shields.io/badge/Buy%20me%20a%20coffee-Donate-ff69b4.svg" alt="Buy me a coffee">
</a>
<a href="https://ko-fi.com/davemlz" target="_blank">
    <img src="https://img.shields.io/badge/kofi-Donate-ff69b4.svg" alt="Ko-fi">
</a>
<a href="https://developers.google.com/earth-engine/tutorials/community/developer-resources" target="_blank">
    <img src="https://img.shields.io/badge/GEE%20Community-Developer%20Resources-00b6ff.svg" alt="GEE Community">
</a>
<a href="https://twitter.com/dmlmont" target="_blank">
    <img src="https://img.shields.io/twitter/follow/dmlmont?style=social" alt="Twitter">
</a>
<a href='https://joss.theoj.org/papers/34696c5b62c50898b4129cbbe8befb0a'>
    <img src='https://joss.theoj.org/papers/34696c5b62c50898b4129cbbe8befb0a/status.svg' alt='JOSS' />
</a>
<a href="https://github.com/psf/black" target="_blank">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Black">
</a>
<a href="https://pycqa.github.io/isort/" target="_blank">
    <img src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336" alt="isort">
</a>
</p>

---

**GitHub**: [https://github.com/davemlz/eemont](https://github.com/davemlz/eemont)

**Documentation**: [https://eemont.readthedocs.io/](https://eemont.readthedocs.io/)

**PyPI**: [https://pypi.org/project/eemont/](https://pypi.org/project/eemont/)

**Conda-forge**: [https://anaconda.org/conda-forge/eemont](https://anaconda.org/conda-forge/eemont)

**Tutorials**: [https://github.com/davemlz/eemont/tree/master/docs/tutorials](https://github.com/davemlz/eemont/tree/master/docs/tutorials)

**Paper**: [https://joss.theoj.org/papers/10.21105/joss.03168](https://joss.theoj.org/papers/10.21105/joss.03168)

---

## Overview

[Google Earth Engine](https://earthengine.google.com/) is a cloud-based service for 
geospatial processing of vector and raster data. The Earth Engine platform has a 
[JavaScript and a Python API](https://developers.google.com/earth-engine/guides) with 
different methods to process geospatial objects. Google Earth Engine also provides a 
[HUGE PETABYTE-SCALE CATALOG](https://developers.google.com/earth-engine/datasets/) of 
raster and vector data that users can process online (e.g. Landsat Missions Image 
Collections, Sentinel Missions Image Collections, MODIS Products Image Collections, World 
Database of Protected Areas, etc.). The eemont package extends the 
[Google Earth Engine Python API](https://developers.google.com/earth-engine/guides/python_install) 
with pre-processing and processing tools for the most used satellite platforms by adding 
utility methods for different 
[Earth Engine Objects](https://developers.google.com/earth-engine/guides/objects_methods_overview) 
that are friendly with the Python method chaining.


## Google Earth Engine Community: Developer Resources

The eemont Python package can be found in the 
[Earth Engine Community: Developer Resources](https://developers.google.com/earth-engine/tutorials/community/developer-resources) 
together with other awesome resources such as [geemap](https://geemap.org/) and 
[rgee](https://github.com/r-spatial/rgee).


## How does it work?

The eemont python package extends the following Earth Engine classes:

- [ee.Feature](https://developers.google.com/earth-engine/guides/features)
- [ee.FeatureCollection](http://developers.google.com/earth-engine/guides/feature_collections)
- [ee.Geometry](https://developers.google.com/earth-engine/guides/geometries)
- [ee.Image](https://developers.google.com/earth-engine/guides/image_overview)
- [ee.ImageCollection](https://developers.google.com/earth-engine/guides/ic_creating)
- [ee.List](https://developers.google.com/earth-engine/guides/objects_methods_overview)
- [ee.Number](https://developers.google.com/earth-engine/guides/objects_methods_overview)

New utility methods and constructors are added to above-mentioned classes in order
to create a more fluid code by being friendly with the Python method chaining. These
methods are mandatory for some pre-processing and processing tasks (e.g. clouds masking,
shadows masking, image scaling, spectral indices computation, etc.), and they are
presented as simple functions that give researchers, students and analysts the chance to
analyze data with far fewer lines of code.

Look at this simple example where a
[Sentinel-2 Surface Reflectance Image Collection](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR)
is pre-processed and processed in just one step:

```python
import ee, eemont
   
ee.Authenticate()
ee.Initialize()

point = ee.Geometry.PointFromQuery(
    'Cali, Colombia',
    user_agent = 'eemont-example'
) # Extended constructor

S2 = (ee.ImageCollection('COPERNICUS/S2_SR')
    .filterBounds(point)
    .closest('2020-10-15') # Extended (pre-processing)
    .maskClouds(prob = 70) # Extended (pre-processing)
    .scaleAndOffset() # Extended (pre-processing)
    .spectralIndices(['NDVI','NDWI','BAIS2'])) # Extended (processing)
```

And just like that, the collection was pre-processed, processed and ready to be analyzed!

## Installation

Install the latest version from PyPI:

```
pip install eemont
```

Upgrade `eemont` by running:

```
pip install -U eemont
```

Install the latest version from conda-forge:

```
conda install -c conda-forge eemont
```

Install the latest dev version from GitHub by running:

```
pip install git+https://github.com/davemlz/eemont
```

## Features

Let's see some of the main features of eemont and how simple they are compared to the GEE
Python API original methods:

### Overloaded Operators

The following operators are overloaded: +, -, \*\, /, //, %, \**\ , <<, >>, &, \|\, <, <=,
==, !=, >, >=, -, ~. (and you can avoid the `ee.Image.expression()` method!)

<table>

<tr>
<th> GEE Python API </th>
<th> eemont-style </th>
</tr>

<tr>
<td>
  
``` python
ds = 'COPERNICUS/S2_SR'
          
S2 = (ee.ImageCollection(ds)
.first())

def scaleImage(img):
    scaling = img.select('B.*')
    x = scaling.multiply(0.0001)
    scaling = img.select(['AOT','WVP'])
    scaling = scaling.multiply(0.001)
    x = x.addBands(scaling)
    notScaling = img.select([
        'SCL',
        'TCI.*',
        'MSK.*',
        'QA.*'
    ]))
    return x.addBands(notScaling)
    
S2 = scaleImage(S2)

exp = '2.5*(N-R)/(N+(6*R)-(7.5*B)+1)'

imgDict = {
'N': S2.select('B8'),
'R': S2.select('B4'),
'B': S2.select('B2')
}

EVI = S2.expression(exp,imgDict)
```

</td>
<td>

``` python
ds = 'COPERNICUS/S2_SR'
          
S2 = (ee.ImageCollection(ds)
.first()
.scale())

N = S2.select('B8')
R = S2.select('B4')
B = S2.select('B2')

EVI = 2.5*(N-R)/(N+(6*R)-(7.5*B)+1)
```
</td>
</tr>

</table>

### Clouds and Shadows Masking

Masking clouds and shadows can be done using eemont with just one method: `maskClouds()`!

<table>

<tr>
<th> GEE Python API </th>
<th> eemont-style </th>
</tr>

<tr>
<td>
  
``` python
ds = 'LANDSAT/LC08/C01/T1_SR'
          
def maskCloudsShadows(img):
    c = (1 << 3)
    s = (1 << 5)
    qa = 'pixel_qa'
    qa = img.select(qa)
    cm = qa.bitwiseAnd(c).eq(0)
    sm = qa.bitwiseAnd(s).eq(0)
    mask = cm.And(sm)
    return img.updateMask(mask)
    
(ee.ImageCollection(ds)
    .map(maskCloudsShadows))
```

</td>
<td>

``` python
ds = 'LANDSAT/LC08/C01/T1_SR'
          
(ee.ImageCollection(ds)
    .maskClouds())
```
</td>
</tr>

</table>

### Image Scaling and Offsetting

Scaling and offsetting can also be done using eemont with just one method: `scale()`!

<table>

<tr>
<th> GEE Python API </th>
<th> eemont-style </th>
</tr>

<tr>
<td>
  
``` python
def scaleBands(img):
    scaling = img.select([
    'NDVI',
    'EVI',
    'sur.*'
    ])
    x = scaling.multiply(0.0001)
    scaling = img.select('.*th')
    scaling = scaling.multiply(0.01)
    x = x.addBands(scaling)
    notScaling = img.select([
    'DetailedQA',
    'DayOfYear',
    'SummaryQA'
    ])
    return x.addBands(notScaling)              

ds = 'MODIS/006/MOD13Q1'

(ee.ImageCollection(ds)
    .map(scaleBands))
```

</td>
<td>

``` python
ds = 'MODIS/006/MOD13Q1'
          
(ee.ImageCollection(ds)
    .scaleAndOffset())
```
</td>
</tr>

</table>


### Complete Preprocessing

The complete preprocessing workflow (Masking clouds and shadows, and image scaling and
offsetting) can be done using eemont with just one method: `preprocess()`!


<table>

<tr>
<th> GEE Python API </th>
<th> eemont-style </th>
</tr>

<tr>
<td>
  
``` python
ds = 'LANDSAT/LC08/C01/T1_SR'
          
def maskCloudsShadows(img):
    c = (1 << 3)
    s = (1 << 5)
    qa = 'pixel_qa'
    qa = img.select(qa)
    cm = qa.bitwiseAnd(c).eq(0)
    sm = qa.bitwiseAnd(s).eq(0)
    mask = cm.And(sm)
    return img.updateMask(mask)
    
def scaleBands(img):
    scaling = img.select('B[1-7]')
    x = scaling.multiply(0.0001)
    scaling = img.select([
    'B10','B11'
    ])
    scaling = scaling.multiply(0.1)
    x = x.addBands(scaling)
    notScaling = img.select([
    'sr_aerosol',
    'pixel_qa',
    'radsat_qa'
    ])
    return x.addBands(notScaling)
    
(ee.ImageCollection(ds)
    .map(maskCloudsShadows)
    .map(scaleBands))
```

</td>
<td>

``` python
ds = 'LANDSAT/LC08/C01/T1_SR'
          
(ee.ImageCollection(ds)
    .preprocess())
```
</td>
</tr>

</table>


### Spectral Indices

Do you need to compute several spectral indices? Use the `spectralIndices()` method! The
indices are taken from [Awesome Spectral Indices](https://github.com/davemlz/awesome-spectral-indices).

<table>

<tr>
<th> GEE Python API </th>
<th> eemont-style </th>
</tr>

<tr>
<td>
  
``` python
ds = 'LANDSAT/LC08/C01/T1_SR'
          
def scaleImage(img):
    scaling = img.select('B[1-7]')
    x = scaling.multiply(0.0001)
    scaling = img.select(['B10','B11'])
    scaling = scaling.multiply(0.1)
    x = x.addBands(scaling)
    notScaling = img.select([
        'sr_aerosol',
        'pixel_qa',
        'radsat_qa'
    ]))
    return x.addBands(notScaling)

def addIndices(img):
    x = ['B5','B4']
    a = img.normalizedDifference(x)
    a = a.rename('NDVI')
    x = ['B5','B3']
    b = img.normalizedDifference(x)
    b = b.rename('GNDVI')
    x = ['B3','B6']
    c = img.normalizedDifference(x)
    c = b.rename('NDSI')
    return img.addBands([a,b,c])                    

(ee.ImageCollection(ds)
    .map(scaleImage)
    .map(addIndices))
```

</td>
<td>

``` python
ds = 'LANDSAT/LC08/C01/T1_SR'
          
(ee.ImageCollection(ds)
    .scaleAndOffset()
    .spectralIndices([
        'NDVI',
        'GNDVI',
        'NDSI'])
)
```
</td>
</tr>

</table>

The list of available indices can be retrieved by running:

``` python 
eemont.listIndices()
```

Information about the indices can also be checked:

``` python 
indices = eemont.indices() 
indices.BAIS2.formula
indices.BAIS2.reference
```

### Closest Image to a Specific Date

Struggling to get the closest image to a specific date? Here is the solution: the
`closest()` method!

<table>

<tr>
<th> GEE Python API </th>
<th> eemont-style </th>
</tr>

<tr>
<td>
  
``` python
ds = 'COPERNICUS/S5P/OFFL/L3_NO2'
          
xy = [-76.21, 3.45]
poi = ee.Geometry.Point(xy)

date = ee.Date('2020-10-15')
date = date.millis()

def setTimeDelta(img):              
    prop = 'system:time_start'
    prop = img.get(prop)
    prop = ee.Number(prop)              
    delta = prop.subtract(date)
    delta = delta.abs()              
    return img.set(
    'dateDist',
    delta)                     

(ee.ImageCollection(ds)
    .filterBounds(poi)
    .map(setTimeDelta)
    .sort('dateDist')
    .first())
```

</td>
<td>

``` python
ds = 'COPERNICUS/S5P/OFFL/L3_NO2'
          
xy = [-76.21, 3.45]
poi = ee.Geometry.Point(xy)

(ee.ImageCollection(ds)
    .filterBounds(poi)
    .closest('2020-10-15'))
```
</td>
</tr>

</table>


### Time Series By Regions

The JavaScript API has a method for time series extraction (included in the `ui.Chart`
module), but this method is missing in the Python API... so, here it is!

PD: Actually, there are two methods that you can use: `getTimeSeriesByRegion()` and
`getTimeSeriesByRegions()`!

``` python
f1 = ee.Feature(ee.Geometry.Point([3.984770,48.767221]).buffer(50),{'ID':'A'})
f2 = ee.Feature(ee.Geometry.Point([4.101367,48.748076]).buffer(50),{'ID':'B'})
fc = ee.FeatureCollection([f1,f2])

S2 = (ee.ImageCollection('COPERNICUS/S2_SR')
    .filterBounds(fc)
    .filterDate('2020-01-01','2021-01-01')
    .maskClouds()
    .scaleAndOffset()
    .spectralIndices(['EVI','NDVI']))

# By Region
ts = S2.getTimeSeriesByRegion(reducer = [ee.Reducer.mean(),ee.Reducer.median()],
                                geometry = fc,
                                bands = ['EVI','NDVI'],
                                scale = 10)

# By Regions
ts = S2.getTimeSeriesByRegions(reducer = [ee.Reducer.mean(),ee.Reducer.median()],
                                collection = fc,
                                bands = ['EVI','NDVI'],
                                scale = 10)
```

### Constructors by Queries

Don't you have the coordinates of a place? You can construct them by using queries!

``` python
usr = 'my-eemont-query-example'
   
seattle_bbox = ee.Geometry.BBoxFromQuery('Seattle',user_agent = usr)
cali_coords = ee.Feature.PointFromQuery('Cali, Colombia',user_agent = usr)
amazonas_river = ee.FeatureCollection.MultiPointFromQuery('Río Amazonas',user_agent = usr)
```

### JavaScript Modules

This is perhaps the most important feature in `eeExtra`! What if you could use a
JavaScript module (originally just useful for the Code Editor) in python or R? Well,
wait no more for it!

<table>

<tr>
<th> JS (Code Editor) </th>
<th> Python (eemont) </th>
<th> R (rgee+) </th>
</tr>

<tr>
<td>
  
``` javascript
var usr = 'users/sofiaermida/'
var rep = 'landsat_smw_lst:'
var fld = 'modules/'
var fle = 'Landsat_LST.js'
var pth = usr+rep+fld+fle
var mod = require(pth)
var LST = mod.collection(
    ee.Geometry.Rectangle([
        -8.91,
        40.0,
        -8.3,
        40.4
    ]),
    'L8',
    '2018-05-15',
    '2018-05-31',
    true
)
```

</td>
<td>
  
``` python
import ee, eemont
ee.Initialize()
usr = 'users/sofiaermida/'
rep = 'landsat_smw_lst:'
fld = 'modules/'
fle = 'Landsat_LST.js'
pth = usr+rep+fld+fle
ee.install(pth)
mod = ee.require(pth)
LST = mod.collection(
    ee.Geometry.Rectangle([
        -8.91,
        40.0,
        -8.3,
        40.4
    ]),
    'L8',
    '2018-05-15',
    '2018-05-31',
    True
)
```

</td>
<td>

``` r
library(rgee)
library(rgeeExtra)
ee_Initialize()
usr <- 'users/sofiaermida/'
rep <- 'landsat_smw_lst:'
fld <- 'modules/'
fle <- 'Landsat_LST.js'
pth <- paste0(usr,rep,fld,fle)
mod <- ee$require(pth)
LST = mod$collection(
    ee$Geometry$Rectangle(c(
        -8.91,
        40.0,
        -8.3,
        40.4
    )),
    'L8',
    '2018-05-15',
    '2018-05-31',
    TRUE
)
```
</td>
</tr>

</table>

## License

The project is licensed under the MIT license.

## How to cite

Do you like using eemont and think it is useful? Share the love by citing it!:

```
Montero, D., (2021). eemont: A Python package that extends Google Earth Engine. 
Journal of Open Source Software, 6(62), 3168, https://doi.org/10.21105/joss.03168
```
   
If required, here is the BibTex!:

```
@article{Montero2021,
    doi = {10.21105/joss.03168},
    url = {https://doi.org/10.21105/joss.03168},
    year = {2021},
    publisher = {The Open Journal},
    volume = {6},
    number = {62},
    pages = {3168},
    author = {David Montero},
    title = {eemont: A Python package that extends Google Earth Engine},
    journal = {Journal of Open Source Software}
}
```

## Artists

- [David Montero Loaiza](https://github.com/davemlz): Lead Developer of eemont and eeExtra.
- [César Aybar](https://github.com/csaybar): Lead Developer of rgee and eeExtra.
- [Aaron Zuspan](https://github.com/aazuspan): Plus Codes Constructors and Methods, Panchromatic Sharpening and Histogram Matching Developer.

## Credits

Special thanks to [Justin Braaten](https://github.com/jdbcode) for featuring eemont in
tutorials and the GEE Community: Developer Resources Page, to
[César Aybar](https://github.com/csaybar) for the formidable help with Awesome Spectral
Indices and to the JOSS Review Team ([Katy Barnhart](https://github.com/kbarnhart),
[Jayaram Hariharan](https://github.com/elbeejay), [Qiusheng Wu](https://github.com/giswqs)
and [Patrick Gray](https://github.com/patrickcgray)) for the comments, suggestions and contributions!
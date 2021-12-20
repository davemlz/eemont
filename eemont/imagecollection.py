import warnings

import ee
import ee_extra
import ee_extra.Spectral.core
import numpy as np
import requests

from .common import _panSharpen
from .extending import extend


@extend(ee.imagecollection.ImageCollection)
def __len__(self):
    """Returns the size of the image collection.

    Parameters
    ----------
    self : ee.ImageCollection
        Image Collection to get the size from.

    Returns
    -------
    int
        Size of the image collection.
    """
    return self.size().getInfo()


@extend(ee.imagecollection.ImageCollection)
def __getitem__(self, key):
    """Gets the band of each image in the image collection according to the specified key.

    Parameters
    ----------
    self : ee.ImageCollection
        Image Collection to get the bands from.
    key : numeric | string | list[numeric] | list[string] | slice
        Key used to get the specified band. If numeric, it gets the band at that index.
        If string, it gets the band with that name or that matches with regex. If list,
        it gets multiple bands. If slice, it calls the slice() method (the step parameter
        is ignored).

    Returns
    -------
    ee.ImageCollection
        Image Collection with the selected bands.
    """
    if isinstance(key, slice):

        if key.start == None:
            start = 0
        else:
            start = key.start

        if key.stop == None:
            stop = self.first().bandNames().size()
        else:
            stop = key.stop

        def sliceCollection(img):
            return img.slice(start, stop)

        selected = self.map(sliceCollection)

    else:
        selected = self.select(key)

    return selected


@extend(ee.imagecollection.ImageCollection)
def closest(self, date, tolerance=1, unit="month"):
    """Gets the closest image (or set of images if the collection intersects a region that
    requires multiple scenes) to the specified date.

    Tip
    ----------
    Check more info about getting the closest image to a specific date in the
    :ref:`User Guide<Closest Image to a Specific Date>`.

    Parameters
    ----------
    self : ee.ImageCollection [this]
        Image Collection from which to get the closest image to the specified date.
    date : ee.Date | string
        Date of interest. The method will look for images closest to this date.
    tolerance : float, default = 1
        Filter the collection to [date - tolerance, date + tolerance) before searching the
        closest image. This speeds up the searching process for collections
        with a high temporal resolution.
    unit : string, default = 'month'
        Units for tolerance. Available units: 'year', 'month', 'week', 'day', 'hour',
        'minute' or 'second'.

    Returns
    -------
    ee.ImageCollection
        Closest images to the specified date.

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Initialize()
    >>> S2 = ee.ImageCollection('COPERNICUS/S2_SR').closest('2020-10-15')
    """
    return ee_extra.ImageCollection.core.closest(self, date, tolerance, unit)


@extend(ee.imagecollection.ImageCollection)
def getTimeSeriesByRegion(
    self,
    reducer,
    bands=None,
    geometry=None,
    scale=None,
    crs=None,
    crsTransform=None,
    bestEffort=False,
    maxPixels=1e12,
    tileScale=1,
    dateColumn="date",
    dateFormat="ISO",
    naValue=-9999,
):
    """Gets the time series by region for the given image collection and geometry (feature
    or feature collection are also supported) according to the specified reducer (or
    reducers).

    Tip
    ----------
    Check more info about time series in the :ref:`User Guide<Time Series By Regions>`.

    Parameters
    ----------
    self : ee.ImageCollection (this)
        Image collection to get the time series from.
    reducer : ee.Reducer | list[ee.Reducer]
        Reducer or list of reducers to use for region reduction.
    bands : str | list[str], default = None
        Selection of bands to get the time series from. Defaults to all bands in the image
        collection.
    geometry : ee.Geometry | ee.Feature | ee.FeatureCollection, default = None
        Geometry to perform the region reduction. If ee.Feature or ee.FeatureCollection,
        the geometry() method is called. In order to get reductions by each feature please
        see the getTimeSeriesByRegions() method. Defaults to the footprint of the first
        band for each image in the collection.
    scale : numeric, default = None
        Nomical scale in meters.
    crs : Projection, default = None
        The projection to work in. If unspecified, the projection of the image's first
        band is used. If specified in addition to scale, rescaled to the specified scale.
    crsTransform : list, default = None
        The list of CRS transform values. This is a row-major ordering of the 3x2
        transform matrix. This option is mutually exclusive with 'scale', and replaces any
        transform already set on the projection.
    bestEffort : boolean, default = False
        If the polygon would contain too many pixels at the given scale, compute and use a
        larger scale which would allow the operation to succeed.
    maxPixels : numeric, default = 1e12
        The maximum number of pixels to reduce.
    tileScale : numeric, default = 1
        A scaling factor used to reduce aggregation tile size; using a larger tileScale
        (e.g. 2 or 4) may enable computations that run out of memory with the default.
    dateColumn : str, default = 'date'
        Output name of the date column.
    dateFormat : str, default = 'ISO'
        Output format of the date column. Defaults to ISO. Available options: 'ms' (for
        milliseconds), 'ISO' (for ISO Standard Format) or a custom format pattern.
    naValue : numeric, default = -9999
        Value to use as NA when the region reduction doesn't retrieve a value due to
        masked pixels.

    Returns
    -------
    ee.FeatureCollection
        Time series by region retrieved as a Feature Collection.

    See Also
    --------
    getTimeSeriesByRegions : Gets the time series by regions for the given image
        collection and feature collection according to the specified reducer (or reducers).

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Initialize()
    >>> f1 = ee.Feature(ee.Geometry.Point([3.984770,48.767221]).buffer(50),{'ID':'A'})
    >>> f2 = ee.Feature(ee.Geometry.Point([4.101367,48.748076]).buffer(50),{'ID':'B'})
    >>> fc = ee.FeatureCollection([f1,f2])
    >>> S2 = (ee.ImageCollection('COPERNICUS/S2_SR')
    ...      .filterBounds(fc)
    ...      .filterDate('2020-01-01','2021-01-01')
    ...      .maskClouds()
    ...      .scaleAndOffset()
    ...      .spectralIndices(['EVI','NDVI']))
    >>> ts = S2.getTimeSeriesByRegion(reducer = [ee.Reducer.mean(),ee.Reducer.median()],
    ...                               geometry = fc,
    ...                               bands = ['EVI','NDVI'],
    ...                               scale = 10)
    """
    return ee_extra.TimeSeries.core.getTimeSeriesByRegion(
        self,
        reducer,
        bands,
        geometry,
        scale,
        crs,
        crsTransform,
        bestEffort,
        maxPixels,
        tileScale,
        dateColumn,
        dateFormat,
        naValue,
    )


@extend(ee.imagecollection.ImageCollection)
def getTimeSeriesByRegions(
    self,
    reducer,
    collection,
    bands=None,
    scale=None,
    crs=None,
    crsTransform=None,
    tileScale=1,
    dateColumn="date",
    dateFormat="ISO",
    naValue=-9999,
):
    """Gets the time series by regions for the given image collection and feature
    collection according to the specified reducer (or reducers).

    Tip
    ----------
    Check more info about time series in the :ref:`User Guide<Time Series By Regions>`.

    Parameters
    ----------
    self : ee.ImageCollection (this)
        Image collection to get the time series from.
    reducer : ee.Reducer | list[ee.Reducer]
        Reducer or list of reducers to use for region reduction.
    collection : ee.FeatureCollection
        Feature Collection to perform the reductions on. Image reductions are applied to
        each feature in the collection.
    bands : str | list[str], default = None
        Selection of bands to get the time series from. Defaults to all bands in the image
        collection.
    scale : numeric, default = None
        Nomical scale in meters.
    crs : Projection, default = None
        The projection to work in. If unspecified, the projection of the image's first
        band is used. If specified in addition to scale, rescaled to the specified scale.
    crsTransform : list, default = None
        The list of CRS transform values. This is a row-major ordering of the 3x2
        transform matrix. This option is mutually exclusive with 'scale', and replaces
        any transform already set on the projection.
    tileScale : numeric, default = 1
        A scaling factor used to reduce aggregation tile size; using a larger tileScale
        (e.g. 2 or 4) may enable computations that run out of memory with the default.
    dateColumn : str, default = 'date'
        Output name of the date column.
    dateFormat : str, default = 'ISO'
        Output format of the date column. Defaults to ISO. Available options: 'ms' (for
        milliseconds), 'ISO' (for ISO Standard Format) or a custom format pattern.
    naValue : numeric, default = -9999
        Value to use as NA when the region reduction doesn't retrieve a value due to
        masked pixels.

    Returns
    -------
    ee.FeatureCollection
        Time series by regions retrieved as a Feature Collection.

    See Also
    --------
    getTimeSeriesByRegion : Gets the time series by region for the given image collection
        and geometry (feature or feature collection are also supported)
        according to the specified reducer (or reducers).

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Initialize()
    >>> f1 = ee.Feature(ee.Geometry.Point([3.984770,48.767221]).buffer(50),{'ID':'A'})
    >>> f2 = ee.Feature(ee.Geometry.Point([4.101367,48.748076]).buffer(50),{'ID':'B'})
    >>> fc = ee.FeatureCollection([f1,f2])
    >>> S2 = (ee.ImageCollection('COPERNICUS/S2_SR')
    ...      .filterBounds(fc)
    ...      .filterDate('2020-01-01','2021-01-01')
    ...      .maskClouds()
    ...      .scaleAndOffset()
    ...      .spectralIndices(['EVI','NDVI']))
    >>> ts = S2.getTimeSeriesByRegions(reducer = [ee.Reducer.mean(),ee.Reducer.median()],
    ...                                collection = fc,
    ...                                bands = ['EVI','NDVI'],
    ...                                scale = 10)
    """
    return ee_extra.TimeSeries.core.getTimeSeriesByRegions(
        self,
        reducer,
        collection,
        bands,
        scale,
        crs,
        crsTransform,
        tileScale,
        dateColumn,
        dateFormat,
        naValue,
    )


@extend(ee.imagecollection.ImageCollection)
def index(
    self,
    index="NDVI",
    G=2.5,
    C1=6.0,
    C2=7.5,
    L=1.0,
    cexp=1.16,
    nexp=2.0,
    alpha=0.1,
    slope=1.0,
    intercept=0.0,
    gamma=1.0,
    kernel="RBF",
    sigma="0.5 * (a + b)",
    p=2.0,
    c=1.0,
    online=False,
    drop=False,
):
    """Computes one or more spectral indices (indices are added as bands) for an image
    collection.

    .. deprecated:: 0.3.0
       Use :func:`spectralIndices()` instead.

    Tip
    ----------
    Check more info about the supported platforms and spectral indices in the
    :ref:`User Guide<Spectral Indices Computation>`.

    Parameters
    ----------
    self : ee.ImageCollection
        Image collection to compute indices on. Must be scaled to [0,1].
    index : string | list[string], default = 'NDVI'
        Index or list of indices to compute.\n
        Available options:
            - 'vegetation' : Compute all vegetation indices.
            - 'burn' : Compute all burn indices.
            - 'water' : Compute all water indices.
            - 'snow' : Compute all snow indices.
            - 'drought' : Compute all drought indices.
            - 'urban' : Compute all urban (built-up) indices.
            - 'kernel' : Compute all kernel indices.
            - 'all' : Compute all indices listed below.
        Awesome Spectral Indices for GEE:
            Check the complete list of indices
            `here <https://awesome-ee-spectral-indices.readthedocs.io/en/latest/list.html>`_.
    G : float, default = 2.5
        Gain factor. Used just for index = 'EVI'.
    C1 : float, default = 6.0
        Coefficient 1 for the aerosol resistance term. Used just for index = 'EVI'.
    C2 : float, default = 7.5
        Coefficient 2 for the aerosol resistance term. Used just for index = 'EVI'.
    L : float, default = 1.0
        Canopy background adjustment. Used just for index = ['EVI','SAVI'].
    cexp : float, default = 1.16
        Exponent used for OCVI.
    nexp : float, default = 2.0
        Exponent used for GDVI.
    alpha : float, default = 0.1
        Weighting coefficient  used for WDRVI.
    slope : float, default = 1.0
        Soil line slope.
    intercept : float, default = 0.0
        Soil line intercept.
    gamma : float, default = 1.0
        Weighting coefficient  used for ARVI.
    kernel : str, default = 'RBF'
        Kernel used for kernel indices.\n
        Available options:
            - 'linear' : Linear Kernel.
            - 'RBF' : Radial Basis Function (RBF) Kernel.
            - 'poly' : Polynomial Kernel.
    sigma : str | float, default = '0.5 * (a + b)'
        Length-scale parameter. Used for kernel = 'RBF'. If str, this must be an
        expression including 'a' and 'b'. If numeric, this must be positive.
    p : float, default = 2.0
        Kernel degree. Used for kernel = 'poly'.
    c : float, default = 1.0
        Free parameter that trades off the influence of higher-order versus lower-order
        terms in the polynomial kernel. Used for kernel = 'poly'. This must be greater
        than or equal to 0.
    online : boolean, default = False
        Wheter to retrieve the most recent list of indices directly from the GitHub
        repository and not from the local copy.
    drop : boolean, default = True
        Whether to drop all bands except the new spectral indices.

    Returns
    -------
    ee.ImageCollection
        Image collection with the computed spectral index, or indices, as new bands.

    See Also
    --------
    scale : Scales bands on an image collection.

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> S2 = ee.ImageCollection('COPERNICUS/S2_SR').scale()

    - Computing one spectral index:

    >>> S2.index('NDVI')

    - Computing indices with different parameters:

    >>> S2.index('SAVI',L = 0.5)

    - Computing multiple indices:

    >>> S2.index(['NDVI','EVI','GNDVI'])

    - Computing a specific group of indices:

    >>> S2.index('vegetation')

    - Computing kernel indices:

    >>> S2.index(['kNDVI'],kernel = 'poly',p = 5)

    - Computing all indices:

    >>> S2.index('all')

    References
    ----------
    .. [1] https://awesome-ee-spectral-indices.readthedocs.io/en/latest/list.html
    """
    warnings.warn(
        "index() is deprecated, please use spectralIndices() instead",
        DeprecationWarning,
    )

    return ee_extra.Spectral.core.spectralIndices(
        self,
        index,
        G,
        C1,
        C2,
        L,
        cexp,
        nexp,
        alpha,
        slope,
        intercept,
        gamma,
        kernel,
        sigma,
        p,
        c,
        online,
        drop,
    )


@extend(ee.imagecollection.ImageCollection)
def spectralIndices(
    self,
    index="NDVI",
    G=2.5,
    C1=6.0,
    C2=7.5,
    L=1.0,
    cexp=1.16,
    nexp=2.0,
    alpha=0.1,
    slope=1.0,
    intercept=0.0,
    gamma=1.0,
    kernel="RBF",
    sigma="0.5 * (a + b)",
    p=2.0,
    c=1.0,
    online=False,
    drop=False,
):
    """Computes one or more spectral indices (indices are added as bands) for an image
    collection from the Awesome List of Spectral Indices.

    Tip
    ----------
    Check more info about the supported platforms and spectral indices in the
    :ref:`User Guide<Spectral Indices Computation>`.

    Parameters
    ----------
    self : ee.ImageCollection
        Image collection to compute indices on. Must be scaled to [0,1].
    index : string | list[string], default = 'NDVI'
        Index or list of indices to compute.\n
        Available options:
            - 'vegetation' : Compute all vegetation indices.
            - 'burn' : Compute all burn indices.
            - 'water' : Compute all water indices.
            - 'snow' : Compute all snow indices.
            - 'drought' : Compute all drought indices.
            - 'urban' : Compute all urban (built-up) indices.
            - 'kernel' : Compute all kernel indices.
            - 'all' : Compute all indices listed below.
        Awesome Spectral Indices for GEE:
            Check the complete list of indices
            `here <https://awesome-ee-spectral-indices.readthedocs.io/en/latest/list.html>`_.
    G : float, default = 2.5
        Gain factor. Used just for index = 'EVI'.
    C1 : float, default = 6.0
        Coefficient 1 for the aerosol resistance term. Used just for index = 'EVI'.
    C2 : float, default = 7.5
        Coefficient 2 for the aerosol resistance term. Used just for index = 'EVI'.
    L : float, default = 1.0
        Canopy background adjustment. Used just for index = ['EVI','SAVI'].
    cexp : float, default = 1.16
        Exponent used for OCVI.
    nexp : float, default = 2.0
        Exponent used for GDVI.
    alpha : float, default = 0.1
        Weighting coefficient  used for WDRVI.
    slope : float, default = 1.0
        Soil line slope.
    intercept : float, default = 0.0
        Soil line intercept.
    gamma : float, default = 1.0
        Weighting coefficient  used for ARVI.
    kernel : str, default = 'RBF'
        Kernel used for kernel indices.\n
        Available options:
            - 'linear' : Linear Kernel.
            - 'RBF' : Radial Basis Function (RBF) Kernel.
            - 'poly' : Polynomial Kernel.
    sigma : str | float, default = '0.5 * (a + b)'
        Length-scale parameter. Used for kernel = 'RBF'. If str, this must be an
        expression including 'a' and 'b'. If numeric, this must be positive.
    p : float, default = 2.0
        Kernel degree. Used for kernel = 'poly'.
    c : float, default = 1.0
        Free parameter that trades off the influence of higher-order versus lower-order
        terms in the polynomial kernel. Used for kernel = 'poly'. This must be greater
        than or equal to 0.
    online : boolean, default = False
        Whether to retrieve the most recent list of indices directly from the GitHub
        repository and not from the local copy.
    drop : boolean, default = True
        Whether to drop all bands except the new spectral indices.

    Returns
    -------
    ee.ImageCollection
        Image collection with the computed spectral index, or indices, as new bands.

    See Also
    --------
    scaleAndOffset : Scales bands on an image collection.

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> S2 = ee.ImageCollection('COPERNICUS/S2_SR').scaleAndOffset()

    - Computing one spectral index:

    >>> S2.spectralIndices('NDVI')

    - Computing indices with different parameters:

    >>> S2.spectralIndices('SAVI',L = 0.5)

    - Computing multiple indices:

    >>> S2.spectralIndices(['NDVI','EVI','GNDVI'])

    - Computing a specific group of indices:

    >>> S2.spectralIndices('vegetation')

    - Computing kernel indices:

    >>> S2.spectralIndices(['kNDVI'],kernel = 'poly',p = 5)

    - Computing all indices:

    >>> S2.spectralIndices('all')
    """
    return ee_extra.Spectral.core.spectralIndices(
        self,
        index,
        G,
        C1,
        C2,
        L,
        cexp,
        nexp,
        alpha,
        slope,
        intercept,
        gamma,
        kernel,
        sigma,
        p,
        c,
        online,
        drop,
    )


@extend(ee.imagecollection.ImageCollection)
def maskClouds(
    self,
    method="cloud_prob",
    prob=60,
    maskCirrus=True,
    maskShadows=True,
    scaledImage=False,
    dark=0.15,
    cloudDist=1000,
    buffer=250,
    cdi=None,
):
    """Masks clouds and shadows in an image collection (valid just for Surface
    Reflectance products).

    Tip
    ----------
    Check more info about the supported platforms and clouds masking in the
    :ref:`User Guide<Masking Clouds and Shadows>`.

    Parameters
    ----------
    self : ee.ImageCollection [this]
        Image collection to mask.
    method : string, default = 'cloud_prob'
        Method used to mask clouds.\n
        Available options:
            - 'cloud_prob' : Use cloud probability.
            - 'qa' : Use Quality Assessment band.
        This parameter is ignored for Landsat products.
    prob : numeric [0, 100], default = 60
        Cloud probability threshold. Valid just for method = 'cloud_prob'. This parameter
        is ignored for Landsat products.
    maskCirrus : boolean, default = True
        Whether to mask cirrus clouds. Valid just for method = 'qa'. This parameter is
        ignored for Landsat products.
    maskShadows : boolean, default = True
        Whether to mask cloud shadows. For more info see 'Braaten, J. 2020. Sentinel-2
        Cloud Masking with s2cloudless. Google Earth Engine, Community Tutorials'.
    scaledImage : boolean, default = False
        Whether the pixel values are scaled to the range [0,1] (reflectance values). This
        parameter is ignored for Landsat products.
    dark : float [0,1], default = 0.15
        NIR threshold. NIR values below this threshold are potential cloud shadows. This
        parameter is ignored for Landsat products.
    cloudDist : int, default = 1000
        Maximum distance in meters (m) to look for cloud shadows from cloud edges. This
        parameter is ignored for Landsat products.
    buffer : int, default = 250
        Distance in meters (m) to dilate cloud and cloud shadows objects. This parameter
        is ignored for Landsat products.
    cdi : float [-1,1], default = None
        Cloud Displacement Index threshold. Values below this threshold are considered
        potential clouds. A cdi = None means that the index is not used. For more info see
        'Frantz, D., HaS, E., Uhl, A., Stoffels, J., Hill, J. 2018. Improvement of the
        Fmask algorithm for Sentinel-2 images: Separating clouds from bright surfaces
        based on parallax effects. Remote Sensing of Environment 2015: 471-481'.
        This parameter is ignored for Landsat products.

    Returns
    -------
    ee.ImageCollection
        Cloud-shadow masked image collection.

    Notes
    -----
    This method may mask water as well as clouds for the Sentinel-3 Radiance product.

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> S2 = (ee.ImageCollection('COPERNICUS/S2_SR')
    ...     .maskClouds(prob = 75,buffer = 300,cdi = -0.5))
    """
    return ee_extra.QA.clouds.maskClouds(
        self,
        method,
        prob,
        maskCirrus,
        maskShadows,
        scaledImage,
        dark,
        cloudDist,
        buffer,
        cdi,
    )


@extend(ee.imagecollection.ImageCollection)
def scale(self):
    """Scales bands on an image collection.

    .. deprecated:: 0.3.0
       Use :func:`scaleAndOffset()` instead.

    Tip
    ----------
    Check more info about the supported platforms and image scaling the
    :ref:`User Guide<Image Scaling>`.

    Parameters
    ----------
    self : ee.ImageCollection (this)
        Image collection to scale.

    Returns
    -------
    ee.ImageCollection
        Scaled image collection.

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> S2 = ee.ImageCollection('COPERNICUS/S2_SR').scale()
    """
    warnings.warn(
        "scale() is deprecated, please use scaleAndOffset() instead",
        DeprecationWarning,
    )

    return ee_extra.STAC.core.scaleAndOffset(self)


@extend(ee.imagecollection.ImageCollection)
def getScaleParams(self):
    """Gets the scale parameters for each band of the image collection.

    Parameters
    ----------
    self : ee.ImageCollection (this)
        Image collection to get the scale parameters from.

    Returns
    -------
    dict
        Dictionary with the scale parameters for each band.

    See Also
    --------
    getOffsetParams : Gets the offset parameters for each band of the image collection.
    scaleAndOffset : Scales bands on an image collection according to their scale and
        offset parameters.

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> ee.ImageCollection('MODIS/006/MOD11A2').getScaleParams()
    {'Clear_sky_days': 1.0,
     'Clear_sky_nights': 1.0,
     'Day_view_angl': 1.0,
     'Day_view_time': 0.1,
     'Emis_31': 0.002,
     'Emis_32': 0.002,
     'LST_Day_1km': 0.02,
     'LST_Night_1km': 0.02,
     'Night_view_angl': 1.0,
     'Night_view_time': 0.1,
     'QC_Day': 1.0,
     'QC_Night': 1.0}
    """
    return ee_extra.STAC.core.getScaleParams(self)


@extend(ee.imagecollection.ImageCollection)
def getOffsetParams(self):
    """Gets the offset parameters for each band of the image collection.

    Parameters
    ----------
    self : ee.ImageCollection (this)
        Image collection to get the offset parameters from.

    Returns
    -------
    dict
        Dictionary with the offset parameters for each band.

    See Also
    --------
    getScaleParams : Gets the scale parameters for each band of the image collection.
    scaleAndOffset : Scales bands on an image collection according to their scale and
        offset parameters.

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> ee.ImageCollection('MODIS/006/MOD11A2').getOffsetParams()
    {'Clear_sky_days': 0.0,
     'Clear_sky_nights': 0.0,
     'Day_view_angl': -65.0,
     'Day_view_time': 0.0,
     'Emis_31': 0.49,
     'Emis_32': 0.49,
     'LST_Day_1km': 0.0,
     'LST_Night_1km': 0.0,
     'Night_view_angl': -65.0,
     'Night_view_time': 0.0,
     'QC_Day': 0.0,
     'QC_Night': 0.0}
    """
    return ee_extra.STAC.core.getOffsetParams(self)


@extend(ee.imagecollection.ImageCollection)
def scaleAndOffset(self):
    """Scales bands on an image collection according to their scale and offset parameters.

    Tip
    ----------
    Check more info about the supported platforms and image scaling the
    :ref:`User Guide<Image Scaling>`.

    Parameters
    ----------
    self : ee.ImageCollection (this)
        Image collection to scale.

    Returns
    -------
    ee.ImageCollection
        Scaled image collection.

    See Also
    --------
    getOffsetParams : Gets the offset parameters for each band of the image collection.
    getScaleParams : Gets the scale parameters for each band of the image collection.

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> S2 = ee.ImageCollection('COPERNICUS/S2_SR').scaleAndOffset()
    """
    return ee_extra.STAC.core.scaleAndOffset(self)


@extend(ee.imagecollection.ImageCollection)
def preprocess(self, **kwargs):
    """Pre-processes the image collection: masks clouds and shadows, and scales and
    offsets the image collection.

    Tip
    ----------
    Check more info here about the supported platforms, :ref:`Image Scaling<Image Scaling>`
    and :ref:`Masking Clouds and Shadows<Masking Clouds and Shadows>`.

    Parameters
    ----------
    self : ee.ImageCollection [this]
        Image Collection to pre-process.
    **kwargs :
        Keywords arguments for maskClouds().

    Returns
    -------
    ee.ImageCollection
        Pre-processed image collection.

    See Also
    --------
    getScaleParams : Gets the scale parameters for each band of the image collection.
    getOffsetParams : Gets the offset parameters for each band of the image collection.
    scaleAndOffset : Scales bands on an image collection according to their scale and
        offset parameters.
    maskClouds : Masks clouds and shadows in an image collection.

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> S2 = ee.ImageCollection('COPERNICUS/S2_SR').preprocess()
    """
    return ee_extra.QA.pipelines.preprocess(self, **kwargs)


@extend(ee.imagecollection.ImageCollection)
def getSTAC(self):
    """Gets the STAC of the image collection.

    Parameters
    ----------
    self : ee.ImageCollection [this]
        Image Collection to get the STAC from.

    Returns
    -------
    dict
        STAC of the image collection.

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> ee.ImageCollection('COPERNICUS/S2_SR').getSTAC()
    {'stac_version': '1.0.0-rc.2',
     'type': 'Collection',
     'stac_extensions': ['https://stac-extensions.github.io/eo/v1.0.0/schema.json'],
     'id': 'COPERNICUS/S2_SR',
     'title': 'Sentinel-2 MSI: MultiSpectral Instrument, Level-2A',
     'gee:type': 'image_collection',
     ...}
    """
    return ee_extra.STAC.core.getSTAC(self)


@extend(ee.imagecollection.ImageCollection)
def getDOI(self):
    """Gets the DOI of the image collection, if available.

    Parameters
    ----------
    self : ee.ImageCollection [this]
        Image Collection to get the DOI from.

    Returns
    -------
    str
        DOI of the ee.ImageCollection dataset.

    See Also
    --------
    getCitation : Gets the citation of the image collection, if available.

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> ee.ImageCollection('NASA/GPM_L3/IMERG_V06').getDOI()
    '10.5067/GPM/IMERG/3B-HH/06'
    """
    return ee_extra.STAC.core.getDOI(self)


@extend(ee.imagecollection.ImageCollection)
def getCitation(self):
    """Gets the citation of the image collection, if available.

    Parameters
    ----------
    self : ee.ImageCollection [this]
        Image Collection to get the citation from.

    Returns
    -------
    str
        Citation of the ee.ImageCollection dataset.

    See Also
    --------
    getDOI : Gets the DOI of the image collection, if available.

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> ee.ImageCollection('NASA/GPM_L3/IMERG_V06').getCitation()
    'Huffman, G.J., E.F. Stocker, D.T. Bolvin, E.J. Nelkin, Jackson Tan (2019),
    GPM IMERG Final Precipitation L3 Half Hourly 0.1 degree x 0.1 degree V06, Greenbelt,
    MD, Goddard Earth Sciences Data and Information Services Center (GES DISC),
    Accessed: [Data Access Date],
    [doi:10.5067/GPM/IMERG/3B-HH/06](https://doi.org/10.5067/GPM/IMERG/3B-HH/06)'
    """
    return ee_extra.STAC.core.getCitation(self)


@extend(ee.imagecollection.ImageCollection)
def panSharpen(self, method="SFIM", qa=None, **kwargs):
    """Apply panchromatic sharpening to each Image in the Image Collection.

    Optionally, run quality assessments between the original and sharpened Images to
    measure spectral distortion and set results as properties of each sharpened Image.

    Parameters
    ----------
    self : ee.ImageCollection [this]
        Image Collection to sharpen.
    method : str, default="SFIM"
        The sharpening algorithm to apply. Current options are "SFIM" (Smoothing
        Filter-based Intensity Modulation), "HPFA" (High Pass Filter Addition), "PCS"
        (Principal Component Substitution), and "SM" (simple mean). Different
        sharpening methods will produce different quality sharpening results in different
        scenarios.
    qa : str | list, default=None
        One or more optional quality assessment names to apply after sharpening, e.g.
        "MSE", "RASE", "UIQI", etc.
    **kwargs :
        Keyword arguments passed to ee.Image.reduceRegion() such as "geometry",
        "maxPixels", "bestEffort", etc. These arguments are only used for PCS sharpening
        and quality assessments.

    Returns
    -------
    ee.ImageCollection
        The Image Collection with all sharpenable bands sharpened to the panchromatic
        resolution and quality assessments run and set as properties.

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> source = ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA")
    >>> sharp = source.panSharpen(method="HPFA", qa=["MSE", "RMSE"], maxPixels=1e13)
    """
    return _panSharpen(self, method, qa, **kwargs)


@extend(ee.imagecollection.ImageCollection)
def tasseledCap(self):
    """Calculates tasseled cap brightness, wetness, and greenness components for all
    images in the collection.

    Tasseled cap transformations are applied using coefficients published for these
    supported platforms:

    * Sentinel-2 MSI Level 1C [1]_
    * Landsat 8 OLI TOA [2]_
    * Landsat 7 ETM+ TOA [3]_
    * Landsat 5 TM Raw DN [4]_
    * Landsat 4 TM Raw DN [5]_
    * Landsat 4 TM Surface Reflectance [6]_
    * MODIS NBAR [7]_

    Parameters
    ----------
    self : ee.ImageCollection
        Image Collection to calculate tasseled cap components for. Must belong to a
        supported platform.

    Returns
    -------
    ee.ImageCollection
        Image Collection with the tasseled cap components as new bands in each image.

    References
    ----------
    .. [1] Shi, T., & Xu, H. (2019). Derivation of Tasseled Cap Transformation
        Coefficients for Sentinel-2 MSI At-Sensor Reflectance Data. IEEE Journal
        of Selected Topics in Applied Earth Observations and Remote Sensing, 1–11.
        doi:10.1109/jstars.2019.2938388
    .. [2] Baig, M.H.A., Zhang, L., Shuai, T. and Tong, Q., 2014. Derivation of a
        tasselled cap transformation based on Landsat 8 at-satellite reflectance.
        Remote Sensing Letters, 5(5), pp.423-431.
    .. [3] Huang, C., Wylie, B., Yang, L., Homer, C. and Zylstra, G., 2002.
        Derivation of a tasselled cap transformation based on Landsat 7 at-satellite
        reflectance. International journal of remote sensing, 23(8), pp.1741-1748.
    .. [4] Crist, E.P., Laurin, R. and Cicone, R.C., 1986, September. Vegetation and
        soils information contained in transformed Thematic Mapper data. In
        Proceedings of IGARSS’86 symposium (pp. 1465-1470). Paris: European Space
        Agency Publications Division.
    .. [5] Crist, E.P. and Cicone, R.C., 1984. A physically-based transformation of
        Thematic Mapper data---The TM Tasseled Cap. IEEE Transactions on Geoscience
        and Remote sensing, (3), pp.256-263.
    .. [6] Crist, E.P., 1985. A TM tasseled cap equivalent transformation for
        reflectance factor data. Remote sensing of Environment, 17(3), pp.301-306.
    .. [7] Lobser, S.E. and Cohen, W.B., 2007. MODIS tasselled cap: land cover
        characteristics expressed through transformed MODIS data. International
        Journal of Remote Sensing, 28(22), pp.5079-5101.

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> col = ee.ImageCollection("LANDSAT/LT05/C01/T1")
    >>> col = col.tasseledCap()
    """
    return ee_extra.Spectral.core.tasseledCap(self)

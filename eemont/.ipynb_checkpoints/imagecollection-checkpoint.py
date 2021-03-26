import ee
import numpy as np
import warnings
from .common import _get_indices
from .common import _get_platform
from .common import _get_scale_method
from .common import _get_expression_map
from .common import _index

def _extend_eeImageCollection():
    """Decorator. Extends the ee.ImageCollection class."""
    return lambda f: (setattr(ee.imagecollection.ImageCollection,f.__name__,f) or f)

@_extend_eeImageCollection()
def closest(self, date, tolerance = 1, unit = 'month'):
    '''Gets the closest image (or set of images if the collection intersects a region that requires multiple scenes) to the specified date.
    
    Parameters
    ----------    
    self : ee.ImageCollection [this]
        Image Collection from which to get the closest image to the specified date.
    date : ee.Date | string
        Date of interest. The method will look for images closest to this date.
    tolerance : float, default = 1
        Filter the collection to [date - tolerance, date + tolerance) before searching the closest image. This speeds up the searching process for collections
        with a high temporal resolution.
    unit : string, default = 'month'
        Units for tolerance. Available units: 'year', 'month', 'week', 'day', 'hour', 'minute' or 'second'.
        
    Returns
    -------    
    ee.ImageCollection
        Closest images to the specified date.
        
    Examples
    --------
    >>> import ee, eemont
    >>> ee.Initialize()
    >>> S2 = ee.ImageCollection('COPERNICUS/S2_SR').closest('2020-10-15')
    ''' 
    if not isinstance(date, ee.ee_date.Date):
        date = ee.Date(date)
    
    startDate = date.advance(-tolerance, unit)
    endDate = date.advance(tolerance, unit)
    self = self.filterDate(startDate, endDate)
    
    def setProperties(img):        
        img = img.set('dateDist',ee.Number(img.get('system:time_start')).subtract(date.millis()).abs())        
        img = img.set('day',ee.Date(img.get('system:time_start')).get('day')) 
        img = img.set('month',ee.Date(img.get('system:time_start')).get('month')) 
        img = img.set('year',ee.Date(img.get('system:time_start')).get('year')) 
        return img
    
    self = self.map(setProperties).sort('dateDist')
    closestImageTime = self.limit(1).first().get('system:time_start')
    dayToFilter = ee.Filter.eq('day',ee.Date(closestImageTime).get('day'))
    monthToFilter = ee.Filter.eq('month',ee.Date(closestImageTime).get('month'))
    yearToFilter = ee.Filter.eq('year',ee.Date(closestImageTime).get('year'))
    self = self.filter(ee.Filter.And(dayToFilter,monthToFilter,yearToFilter))
    
    return self

@_extend_eeImageCollection()
def getTimeSeriesByRegion(self,reducer,bands = None,geometry = None,scale = None,crs = None,crsTransform = None,bestEffort = False,
                          maxPixels = 1e12,tileScale = 1,dateColumn = 'date',dateFormat = 'ISO',naValue = -9999):
    '''Gets the time series by region for the given image collection and geometry (feature or feature collection are also supported) according to the specified reducer (or reducers).
    
    Parameters
    ----------
    self : ee.ImageCollection (this)
        Image collection to get the time series from.
    reducer : ee.Reducer | list[ee.Reducer]
        Reducer or list of reducers to use for region reduction.
    bands : str | list[str], default = None
        Selection of bands to get the time series from. Defaults to all bands in the image collection.    
    geometry : ee.Geometry | ee.Feature | ee.FeatureCollection, default = None
        Geometry to perform the region reduction. If ee.Feature or ee.FeatureCollection, the geometry() method is called. In order to get reductions by each feature please see
        the getTimeSeriesByRegions() method. Defaults to the footprint of the first band for each image in the collection.
    scale : numeric, default = None
        Nomical scale in meters.
    crs : Projection, default = None
        The projection to work in. If unspecified, the projection of the image's first band is used. If specified in addition to scale, rescaled to the specified scale.
    crsTransform : list, default = None
        The list of CRS transform values. This is a row-major ordering of the 3x2 transform matrix.
        This option is mutually exclusive with 'scale', and replaces any transform already set on the projection.
    bestEffort : boolean, default = False
        If the polygon would contain too many pixels at the given scale, compute and use a larger scale which would allow the operation to succeed.
    maxPixels : numeric, default = 1e12
        The maximum number of pixels to reduce.
    tileScale : numeric, default = 1
        A scaling factor used to reduce aggregation tile size; using a larger tileScale (e.g. 2 or 4) may enable computations that run out of memory with the default.
    dateColumn : str, default = 'date'
        Output name of the date column.
    dateFormat : str, default = 'ISO'
        Output format of the date column. Defaults to ISO. Available options: 'ms' (for milliseconds), 'ISO' (for ISO Standard Format) or a custom format pattern.
    naValue : numeric, default = -9999
        Value to use as NA when the region reduction doesn't retrieve a value due to masked pixels.
        
    Returns
    -------
    ee.FeatureCollection
        Time series by region retrieved as a Feature Collection.
        
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
    ...      .scale()
    ...      .index(['EVI','NDVI']))
    >>> ts = S2.getTimeSeriesByRegion(reducer = [ee.Reducer.mean(),ee.Reducer.median()],
    ...                               geometry = fc,
    ...                               bands = ['EVI','NDVI'],
    ...                               scale = 10)
    
    See Also
    --------
    getTimeSeriesByRegions : Gets the time series by regions for the given image collection and feature collection according to the specified reducer (or reducers).
    '''    
    if bands != None:
        if not isinstance(bands,list):
            bands = [bands]
        self = self.select(bands)
    
    if not isinstance(reducer, list):
        reducer = [reducer]
    
    if not isinstance(geometry, ee.geometry.Geometry):
        geometry = geometry.geometry()
    
    collections = []
    
    for red in reducer:
        
        reducerName = red.getOutputs().get(0)
    
        def reduceImageCollectionByRegion(img):
            dictionary = img.reduceRegion(red,geometry,scale,crs,crsTransform,bestEffort,maxPixels,tileScale)
            if dateFormat == 'ms':
                date = ee.Date(img.get('system:time_start')).millis()
            elif dateFormat == 'ISO':
                date = ee.Date(img.get('system:time_start')).format()
            else:
                date = ee.Date(img.get('system:time_start')).format(dateFormat)
            return ee.Feature(None,dictionary).set({dateColumn:date,'reducer':reducerName})
        
        collections.append(ee.FeatureCollection(self.map(reduceImageCollectionByRegion)))
    
    flattenfc = ee.FeatureCollection(collections).flatten()
    
    def setNA(feature):        
        feature = ee.Algorithms.If(condition = feature.propertyNames().size().eq(3),
                                   trueCase = feature.set(ee.Dictionary.fromLists(bands,[naValue] * len(bands))),
                                   falseCase = feature)                    
        feature = ee.Feature(feature) 
        return feature
    
    return flattenfc.map(setNA)

@_extend_eeImageCollection()
def getTimeSeriesByRegions(self,reducer,collection,bands = None,scale = None,crs = None,crsTransform = None,tileScale = 1,dateColumn = 'date',dateFormat = 'ISO',naValue = -9999):
    '''Gets the time series by regions for the given image collection and feature collection according to the specified reducer (or reducers).
    
    Parameters
    ----------
    self : ee.ImageCollection (this)
        Image collection to get the time series from.
    reducer : ee.Reducer | list[ee.Reducer]
        Reducer or list of reducers to use for region reduction.
    collection : ee.FeatureCollection
        Feature Collection to perform the reductions on. Image reductions are applied to each feature in the collection.
    bands : str | list[str], default = None
        Selection of bands to get the time series from. Defaults to all bands in the image collection.
    scale : numeric, default = None
        Nomical scale in meters.
    crs : Projection, default = None
        The projection to work in. If unspecified, the projection of the image's first band is used. If specified in addition to scale, rescaled to the specified scale.
    crsTransform : list, default = None
        The list of CRS transform values. This is a row-major ordering of the 3x2 transform matrix.
        This option is mutually exclusive with 'scale', and replaces any transform already set on the projection.
    tileScale : numeric, default = 1
        A scaling factor used to reduce aggregation tile size; using a larger tileScale (e.g. 2 or 4) may enable computations that run out of memory with the default.
    dateColumn : str, default = 'date'
        Output name of the date column.
    dateFormat : str, default = 'ISO'
        Output format of the date column. Defaults to ISO. Available options: 'ms' (for milliseconds), 'ISO' (for ISO Standard Format) or a custom format pattern.
    naValue : numeric, default = -9999
        Value to use as NA when the region reduction doesn't retrieve a value due to masked pixels.
        
    Returns
    -------
    ee.FeatureCollection
        Time series by regions retrieved as a Feature Collection.
        
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
    ...      .scale()
    ...      .index(['EVI','NDVI']))
    >>> ts = S2.getTimeSeriesByRegions(reducer = [ee.Reducer.mean(),ee.Reducer.median()],
    ...                                collection = fc,
    ...                                bands = ['EVI','NDVI'],
    ...                                scale = 10)
    
    See Also
    --------
    getTimeSeriesByRegion : Gets the time series by region for the given image collection and geometry (feature or feature collection are also supported)
        according to the specified reducer (or reducers).
    ''' 
    if bands != None:
        if not isinstance(bands,list):
            bands = [bands]
        self = self.select(bands)
    
    if not isinstance(reducer, list):
        reducer = [reducer]
    
    if not isinstance(collection,ee.featurecollection.FeatureCollection):
        raise Exception("Parameter collection must be an ee.FeatureCollection!")
    
    props = collection.first().propertyNames()
    
    collections = []
    
    imgList = self.toList(self.size())
    
    for red in reducer:
        
        reducerName = red.getOutputs().get(0)
    
        def reduceImageCollectionByRegions(img):
            
            img = ee.Image(img)
            
            fc = img.reduceRegions(collection,red,scale,crs,crsTransform,tileScale)
                
            if isinstance(bands, list):
                if len(bands) == 1:                              
                    fc = ee.Algorithms.If(condition = fc.first().propertyNames().size().eq(props.size()),
                                          trueCase = fc,
                                          falseCase = fc.select(props.add(reducerName),props.add(bands[0])))                    
                    fc = ee.FeatureCollection(fc) 
                        
            if dateFormat == 'ms':
                date = ee.Date(img.get('system:time_start')).millis()
            elif dateFormat == 'ISO':
                date = ee.Date(img.get('system:time_start')).format()
            else:
                date = ee.Date(img.get('system:time_start')).format(dateFormat)
                
            def setProperties(feature):
                return feature.set({dateColumn:date,'reducer':reducerName})
            
            return fc.map(setProperties)
    
        collections.append(self.map(reduceImageCollectionByRegions).flatten())
    
    flattenfc = ee.FeatureCollection(collections).flatten()
    
    def setNA(feature):        
        feature = ee.Algorithms.If(condition = feature.propertyNames().size().eq(props.size().add(2)),
                                   trueCase = feature.set(ee.Dictionary.fromLists(bands,[naValue] * len(bands))),
                                   falseCase = feature)                    
        feature = ee.Feature(feature) 
        return feature
    
    return flattenfc.map(setNA)

@_extend_eeImageCollection()
def index(self,index = 'NDVI',G = 2.5,C1 = 6.0,C2 = 7.5,L = 1.0,kernel = 'RBF',sigma = '0.5 * (a + b)',p = 2.0,c = 1.0):
    '''Computes one or more spectral indices (indices are added as bands) for an image collection.
    
    Parameters
    ----------     
    self : ee.ImageCollection
        Image collection to compute indices on. Must be scaled to [0,1]. Check the supported platforms in User Guide > Spectral Indices > Supported Platforms.
    index : string | list[string], default = 'NDVI'
        Index or list of indices to compute.\n
        Available options:
            - 'vegetation' : Compute all vegetation indices.
            - 'burn' : Compute all burn indices.
            - 'water' : Compute all water indices.
            - 'snow' : Compute all snow indices.
            - 'drought' : Compute all drought indices.
            - 'kernel' : Compute all kernel indices.
            - 'all' : Compute all indices listed below.
        Vegetation indices:
            - 'BNDVI' : Blue Normalized Difference Vegetation Index.
            - 'CIG' : Chlorophyll Index - Green.
            - 'CVI' : Chlorophyll Vegetation Index.
            - 'EVI' : Enhanced Vegetation Index.
            - 'EVI2' : Two-Band Enhanced Vegetation Index.
            - 'GARI' : Green Atmospherically Resistant Vegetation Index.
            - 'GBNDVI' : Green-Blue Normalized Difference Vegetation Index.
            - 'GEMI' : Global Environment Monitoring Index.
            - 'GLI' : Green Leaf Index.
            - 'GNDVI' : Green Normalized Difference Vegetation Index.
            - 'GRNDVI' : Green-Red Normalized Difference Vegetation Index.
            - 'GVMI' : Global Vegetation Moisture Index.
            - 'MNDVI' : Modified Normalized Difference Vegetation Index.
            - 'NDVI' : Normalized Difference Vegetation Index.
            - 'NGRDI' : Normalized Green Red Difference Index.
            - 'RVI' : Ratio Vegetation Index.
            - 'SAVI' : Soil-Adjusted Vegetation Index.  
            - 'VARI' : Visible Atmospherically Resistant Index.
        Burn and fire indices:     
            - 'BAI' : Burned Area Index.
            - 'BAIS2' : Burned Area Index for Sentinel 2.
            - 'CSIT' : Char Soil Index Thermal.
            - 'NBR' : Normalized Burn Ratio.
            - 'NBRT' : Normalized Burn Ratio Thermal.
            - 'NDVIT' : Normalized Difference Vegetation Index Thermal
            - 'SAVIT' : Soil-Adjusted Vegetation Index Thermal.
        Water indices:            
            - 'MNDWI' : Modified Normalized Difference Water Index.
            - 'NDWI' : Normalized Difference Water Index. 
        Snow indices:     
            - 'NDSI' : Normalized Difference Snow Index.
        Drought indices:     
            - 'NDDI' : Normalized Difference Drought Index.
        Kernel indices:     
            - 'kEVI' : Kernel Enhanced Vegetation Index.
            - 'kNDVI' : Kernel Normalized Difference Vegetation Index.
            - 'kRVI' : Kernel Ratio Vegetation Index.
            - 'kVARI' : Kernel Visible Atmospherically Resistant Index.
    G : float, default = 2.5
        Gain factor. Used just for index = 'EVI'.
    C1 : float, default = 6.0
        Coefficient 1 for the aerosol resistance term. Used just for index = 'EVI'.
    C2 : float, default = 7.5
        Coefficient 2 for the aerosol resistance term. Used just for index = 'EVI'.
    L : float, default = 1.0
        Canopy background adjustment. Used just for index = ['EVI','SAVI'].
    kernel : str, default = 'RBF'
        Kernel used for kernel indices.\n
        Available options:
            - 'linear' : Linear Kernel.
            - 'RBF' : Radial Basis Function (RBF) Kernel.
            - 'poly' : Polynomial Kernel.          
    sigma : str | float, default = '0.5 * (a + b)'
        Length-scale parameter. Used for kernel = 'RBF'. If str, this must be an expression including 'a' and 'b'. If numeric, this must be positive.
    p : float, default = 2.0
        Kernel degree. Used for kernel = 'poly'.
    c : float, default = 1.0
        Free parameter that trades off the influence of higher-order versus lower-order terms in the polynomial kernel.
        Used for kernel = 'poly'. This must be greater than or equal to 0.    
            
    Returns
    -------    
    ee.ImageCollection
        Image collection with the computed spectral index, or indices, as new bands.
        
    Examples
    --------
    >>> import ee, eemont
    >>> ee.Initialize()
    >>> S2 = ee.ImageCollection('COPERNICUS/S2_SR').scale().index(['NDVI','EVI','GNDVI'])
    
    See Also
    --------
    scale : Scales bands on an image collection.
    '''  
    return _index(self,index,G,C1,C2,L,kernel,sigma,p,c)

@_extend_eeImageCollection()
def maskClouds(self, method = 'cloud_prob', prob = 60, maskCirrus = True, maskShadows = True, scaledImage = False, dark = 0.15, cloudDist = 1000, buffer = 250, cdi = None):
    '''Masks clouds and shadows in an image collection (valid just for Surface Reflectance products).
    
    Parameters
    ----------    
    self : ee.ImageCollection [this]
        Image collection to mask. Check the supported platforms in User Guide > Masking Clouds and Shadows > Supported Platforms.
    method : string, default = 'cloud_prob'
        Method used to mask clouds.\n
        Available options:
            - 'cloud_prob' : Use cloud probability.
            - 'qa' : Use Quality Assessment band.
        This parameter is ignored for Landsat products.
    prob : numeric [0, 100], default = 60
        Cloud probability threshold. Valid just for method = 'prob'. This parameter is ignored for Landsat products.
    maskCirrus : boolean, default = True
        Whether to mask cirrus clouds. Valid just for method = 'qa'. This parameter is ignored for Landsat products.
    maskShadows : boolean, default = True
        Whether to mask cloud shadows. For more info see 'Braaten, J. 2020. Sentinel-2 Cloud Masking with s2cloudless. Google Earth Engine, Community Tutorials'.
    scaledImage : boolean, default = False
        Whether the pixel values are scaled to the range [0,1] (reflectance values). This parameter is ignored for Landsat products.
    dark : float [0,1], default = 0.15
        NIR threshold. NIR values below this threshold are potential cloud shadows. This parameter is ignored for Landsat products.
    cloudDist : int, default = 1000
        Maximum distance in meters (m) to look for cloud shadows from cloud edges. This parameter is ignored for Landsat products.
    buffer : int, default = 250
        Distance in meters (m) to dilate cloud and cloud shadows objects. This parameter is ignored for Landsat products.
    cdi : float [-1,1], default = None
        Cloud Displacement Index threshold. Values below this threshold are considered potential clouds.
        A cdi = None means that the index is not used. For more info see
        'Frantz, D., HaS, E., Uhl, A., Stoffels, J., Hill, J. 2018. Improvement of the Fmask algorithm for Sentinel-2 images:
        Separating clouds from bright surfaces based on parallax effects. Remote Sensing of Environment 2015: 471-481'.
        This parameter is ignored for Landsat products.
        
    Returns
    -------    
    ee.ImageCollection
        Cloud-shadow masked image collection.
        
    Examples
    --------
    >>> import ee, eemont
    >>> ee.Initialize()
    >>> S2 = ee.ImageCollection('COPERNICUS/S2_SR').maskClouds(prob = 75,buffer = 300,cdi = -0.5)
        
    Notes
    -----
    This method may mask water as well as clouds for the Sentinel-3 Radiance product.
    '''
    def S3(args):
        qa = args.select('quality_flags')
        notCloud = qa.bitwiseAnd(1 << 27).eq(0);
        return args.updateMask(notCloud)
    
    def S2(args):    

        def cloud_prob(img):
            clouds = ee.Image(img.get('cloud_mask')).select('probability')
            isCloud = clouds.gte(prob).rename('CLOUD_MASK')
            return img.addBands(isCloud)

        def QA(img):
            qa = img.select('QA60')
            cloudBitMask = 1 << 10    
            isCloud = qa.bitwiseAnd(cloudBitMask).eq(0)
            if maskCirrus:
                cirrusBitMask = 1 << 11
                isCloud = isCloud.And(qa.bitwiseAnd(cirrusBitMask).eq(0))
            isCloud = isCloud.Not().rename('CLOUD_MASK')
            return img.addBands(isCloud)

        def CDI(img):
            idx = img.get('system:index')
            S2TOA = ee.ImageCollection('COPERNICUS/S2').filter(ee.Filter.eq('system:index',idx)).first()
            CloudDisplacementIndex = ee.Algorithms.Sentinel2.CDI(S2TOA)
            isCloud = CloudDisplacementIndex.lt(cdi).rename('CLOUD_MASK_CDI')
            return img.addBands(isCloud)

        def get_shadows(img):      
            notWater = img.select('SCL').neq(6)
            if not scaledImage:
                darkPixels = img.select('B8').lt(dark * 1e4).multiply(notWater)
            else:  
                darkPixels = img.select('B8').lt(dark).multiply(notWater)        
            shadowAzimuth = ee.Number(90).subtract(ee.Number(img.get('MEAN_SOLAR_AZIMUTH_ANGLE')))        
            cloudProjection = img.select('CLOUD_MASK').directionalDistanceTransform(shadowAzimuth,cloudDist/10)
            cloudProjection = cloudProjection.reproject(crs = img.select(0).projection(),scale = 10).select('distance').mask()            
            isShadow = cloudProjection.multiply(darkPixels).rename('SHADOW_MASK')        
            return img.addBands(isShadow)

        def clean_dilate(img):        
            isCloudShadow = img.select('CLOUD_MASK')
            if cdi != None:
                isCloudShadow = isCloudShadow.And(img.select('CLOUD_MASK_CDI'))
            if maskShadows:
                isCloudShadow = isCloudShadow.add(img.select('SHADOW_MASK')).gt(0)        
            isCloudShadow = isCloudShadow.focal_min(20,units = 'meters').focal_max(buffer*2/10,units = 'meters').rename('CLOUD_SHADOW_MASK')
            return img.addBands(isCloudShadow)

        def apply_mask(img):
            return img.updateMask(img.select('CLOUD_SHADOW_MASK').Not())
        
        if method == 'cloud_prob':
            S2Clouds = ee.ImageCollection('COPERNICUS/S2_CLOUD_PROBABILITY')                  
            fil = ee.Filter.equals(leftField = 'system:index',rightField = 'system:index')
            S2WithCloudMask = ee.Join.saveFirst('cloud_mask').apply(args,S2Clouds,fil)
            S2Masked = ee.ImageCollection(S2WithCloudMask).map(cloud_prob)
        elif method == 'qa':        
            S2Masked = args.map(QA)
        if cdi != None: 
            S2Masked = S2Masked.map(CDI)
        if maskShadows:
            S2Masked = S2Masked.map(get_shadows)
        S2Masked = S2Masked.map(clean_dilate).map(apply_mask)        
        
        return S2Masked
    
    def L8(args):        
        cloudsBitMask = (1 << 5)
        qa = args.select('pixel_qa')
        mask = qa.bitwiseAnd(cloudsBitMask).eq(0)
        if maskShadows:
            cloudShadowBitMask = (1 << 3)
            mask = mask.And(qa.bitwiseAnd(cloudShadowBitMask).eq(0))
        return args.updateMask(mask)

    def L457(args):
        qa = args.select('pixel_qa')
        cloud = qa.bitwiseAnd(1 << 5).And(qa.bitwiseAnd(1 << 7))
        if maskShadows:
            cloud = cloud.Or(qa.bitwiseAnd(1 << 3))
        mask2 = args.mask().reduce(ee.Reducer.min());
        return args.updateMask(cloud.Not()).updateMask(mask2);
    
    def MOD09GA(args):
        qa = args.select('state_1km')
        notCloud = qa.bitwiseAnd(1 << 0).eq(0)
        if maskShadows:
            notCloud = notCloud.And(qa.bitwiseAnd(1 << 2).eq(0))
        if maskCirrus:
            notCloud = notCloud.And(qa.bitwiseAnd(1 << 8).eq(0))        
        return args.updateMask(notCloud)
    
    def MCD15A3H(args):
        qa = args.select('FparExtra_QC')
        notCloud = qa.bitwiseAnd(1 << 5).eq(0)
        if maskShadows:
            notCloud = notCloud.And(qa.bitwiseAnd(1 << 6).eq(0))
        if maskCirrus:
            notCloud = notCloud.And(qa.bitwiseAnd(1 << 4).eq(0))        
        return args.updateMask(notCloud)
    
    def MOD09Q1(args):
        qa = args.select('State')
        notCloud = qa.bitwiseAnd(1 << 0).eq(0)
        if maskShadows:
            notCloud = notCloud.And(qa.bitwiseAnd(1 << 2).eq(0))
        if maskCirrus:
            notCloud = notCloud.And(qa.bitwiseAnd(1 << 8).eq(0))        
        return args.updateMask(notCloud)
    
    def MOD09A1(args):
        qa = args.select('StateQA')
        notCloud = qa.bitwiseAnd(1 << 0).eq(0)
        if maskShadows:
            notCloud = notCloud.And(qa.bitwiseAnd(1 << 2).eq(0))
        if maskCirrus:
            notCloud = notCloud.And(qa.bitwiseAnd(1 << 8).eq(0))        
        return args.updateMask(notCloud)
    
    def MOD17A2H(args):
        qa = args.select('Psn_QC')
        notCloud = qa.bitwiseAnd(1 << 3).eq(0)
        return args.updateMask(notCloud)
    
    def MOD16A2(args):
        qa = args.select('ET_QC')
        notCloud = qa.bitwiseAnd(1 << 3).eq(0)
        return args.updateMask(notCloud)
    
    def MOD13Q1A1(args):
        qa = args.select('SummaryQA')
        notCloud = qa.bitwiseAnd(1 << 0).eq(0)
        return args.updateMask(notCloud)
    
    def MOD13A2(args):
        qa = args.select('SummaryQA')
        notCloud = qa.eq(0)
        return args.updateMask(notCloud)
    
    lookup = {
        'COPERNICUS/S3': S3,
        'COPERNICUS/S2': S2,
        'LANDSAT/LC08': L8,
        'LANDSAT/LE07': L457,
        'LANDSAT/LT05': L457,
        'LANDSAT/LT04': L457,
        'MODIS/006/MOD09GA': MOD09GA,
        'MODIS/006/MCD15A3H': MCD15A3H,
        'MODIS/006/MOD09Q1': MOD09Q1,
        'MODIS/006/MOD09A1': MOD09A1,
        'MODIS/006/MOD17A2H': MOD17A2H,
        'MODIS/006/MOD16A2': MOD16A2,
        'MODIS/006/MOD13Q1': MOD13Q1A1,
        'MODIS/006/MOD13A1': MOD13Q1A1,
        'MODIS/006/MOD13A2': MOD13A2,
        'MODIS/006/MYD09GA': MOD09GA,
        'MODIS/006/MYD09Q1': MOD09Q1,
        'MODIS/006/MYD09A1': MOD09A1,
        'MODIS/006/MYD17A2H': MOD17A2H,
        'MODIS/006/MYD16A2': MOD16A2,
        'MODIS/006/MYD13Q1': MOD13Q1A1,
        'MODIS/006/MYD13A1': MOD13Q1A1,
        'MODIS/006/MYD13A2': MOD13A2
    }
    
    platformDict = _get_platform(self)
    
    if platformDict['platform'] not in list(lookup.keys()):
        raise Exception("Sorry, satellite platform not supported for cloud masking!")
    
    if platformDict['platform'] == 'COPERNICUS/S2':        
        maskedImageCollection = lookup[platformDict['platform']](self)
    else:        
        maskedImageCollection = self.map(lookup[platformDict['platform']])    
    
    return maskedImageCollection

@_extend_eeImageCollection()
def scale(self):    
    '''Scales bands on an image collection.
    
    Parameters
    ----------
    self : ee.ImageCollection (this)
        Image collection to scale. Check the supported platforms in User Guide > Image Scaling > Supported Platforms.
        
    Returns
    -------
    ee.ImageCollection
        Scaled image collection.
        
    Examples
    --------
    >>> import ee, eemont
    >>> ee.Initialize()
    >>> S2 = ee.ImageCollection('COPERNICUS/S2_SR').scale()
    '''
    platformDict = _get_platform(self)
    lookup = _get_scale_method(platformDict)
    
    if platformDict['platform'] not in list(lookup.keys()):
        raise Exception("Sorry, satellite platform not supported for scaling!")
    
    scaledImageCollection = self.map(lookup[platformDict['platform']])
    
    return scaledImageCollection
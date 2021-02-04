import ee
import numpy as np
import warnings
from .common import _get_indices
from .common import _get_platform
from .common import _get_scale_method
from .common import _get_expression_map

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
def index(self,index = 'NDVI',G = 2.5,C1 = 6.0,C2 = 7.5,L = 1.0):
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
            - 'all' : Compute all indices listed below.
        Vegetation indices:     
            - 'BNDVI' : Blue Normalized Difference Vegetation Index.
            - 'CIG' : Chlorophyll Index - Green.
            - 'CVI' : Chlorophyll Vegetation Index.
            - 'EVI' : Enhanced Vegetation Index.
            - 'GBNDVI' : Green-Blue Normalized Difference Vegetation Index.
            - 'GNDVI' : Green Normalized Difference Vegetation Index.
            - 'GRNDVI' : Green-Red Normalized Difference Vegetation Index.
            - 'MNDVI' : Modified Normalized Difference Vegetation Index.
            - 'NDVI' : Normalized Difference Vegetation Index.
            - 'NGRDI' : Normalized Green Red Difference Index.
            - 'RVI' : Ratio Vegetation Index.
            - 'SAVI' : Soil-Adjusted Vegetation Index.
        Burn and fire indices:       
            - 'BAI' : Burned Area Index.
            - 'BAIS2' : Burned Area Index for Sentinel 2.
            - 'NBR' : Normalized Burn Ratio.
        Water indices:     
            - 'MNDWI' : Modified Normalized Difference Water Index.
            - 'NDWI' : Normalized Difference Water Index.
        Snow indices:     
            - 'NDSI' : Normalized Difference Snow Index.
    G : float, default = 2.5
        Gain factor. Used just for index = 'EVI'.
    C1 : float, default = 6.0
        Coefficient 1 for the aerosol resistance term. Used just for index = 'EVI'.
    C2 : float, default = 7.5
        Coefficient 2 for the aerosol resistance term. Used just for index = 'EVI'.
    L : float, default = 1.0
        Canopy background adjustment. Used just for index = ['EVI','SAVI'].
        
    Returns
    -------    
    ee.ImageCollection
        Image collection with the computed spectral index, or indices, as new bands.
    '''  
    platformDict = _get_platform(self)
    
    additionalParameters = {
        'g': float(G),
        'C1': float(C1),
        'C2': float(C2),
        'L': float(L),
    }
    
    spectralIndices = _get_indices()
    indicesNames = list(spectralIndices.keys())
    
    if not isinstance(index, list):
        if index == 'all':
            index = list(spectralIndices.keys())
        elif index in ['vegetation','burn','water','snow']:
            temporalListOfIndices = []
            for idx in indicesNames:
                if spectralIndices[idx]['type'] == index:
                    temporalListOfIndices.append(idx)
            index = temporalListOfIndices
        else:
            index = [index]        
            
    for idx in index:
        if idx not in list(spectralIndices.keys()):
            warnings.warn("Index " + idx + " is not a built-in index and it won't be computed!",Warning)
        else:
            def temporalIndex(img):
                lookupDic = _get_expression_map(img, platformDict)
                lookupDic = {**lookupDic, **additionalParameters}
                if all(band in list(lookupDic.keys()) for band in spectralIndices[idx]['requires']):
                    return img.addBands(img.expression(spectralIndices[idx]['formula'],lookupDic).rename(idx))                
                else:
                    warnings.warn("This platform doesn't have the required bands for " + idx + " computation!",Warning)
                    return img
            self = self.map(temporalIndex)
            
    return self

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
        'MODIS/006/MOD13A2': MOD13A2
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
    '''
    platformDict = _get_platform(self)
    lookup = _get_scale_method(platformDict)
    
    if platformDict['platform'] not in list(lookup.keys()):
        raise Exception("Sorry, satellite platform not supported for scaling!")
    
    scaledImageCollection = self.map(lookup[platformDict['platform']])
    
    return scaledImageCollection
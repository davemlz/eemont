import ee
import numpy as np

def _get_platform(collection):
    '''Gets the platform (satellite) of an image collection and wheter if it is a Surface Reflectance product.
    
    Parameters
    ----------
    collection : ee.Image.Collection
        Image to get platform.
        
    Returns
    -------
    dict
        Platform and product of the image.
    '''
    platforms = [
        'COPERNICUS/S2',
        'LANDSAT/LC08',
        'LANDSAT/LE07',
        'LANDSAT/LT05',
        'LANDSAT/LT04',
    ]
    
    imgID = collection.first().get('system:id').getInfo()
    plt = None
    
    for platform in platforms:
        if platform in imgID:
            plt = platform
        if '_SR' in imgID:
            platformDict = {'platform': plt, 'sr': True}
        else:
            platformDict = {'platform': plt, 'sr': False}
            
    return platformDict

# Functions to extend the ee.ImageCollection class
def _closest(self, date):
    '''Gets the closest image (or set of images if the collection intersects a region that requires multiple scenes) closest to the specified date.
    
    Parameters
    ----------
    self : ee.ImageCollection
        Image Collection from which to get the closest image to the specified date.
    date : ee.Date | string
        Date of interest. The method will look for images closest to this date.
        
    Returns
    -------
    ee.ImageCollection
        Closest images to the specified date.
    ''' 
    if not isinstance(date, ee.ee_date.Date):
        date = ee.Date(date)
    
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

def _maskClouds(self, method = 'cloud_prob', prob = 60, maskCirrus = True, maskShadows = True, scaledImage = False, dark = 0.15, cloudDist = 1000, buffer = 250, cdi = None):
    '''Masks clouds and shadows in an image collection (valid just for Surface Reflectance products).
    
    Parameters
    ----------
    self : ee.ImageCollection (this)
        Image collection to mask. Accepted platforms:
        - Sentinel-2
        - Landsat 8
        - Landsat 7
        - Landsat 5
        - Landsat 4
    method : string, default = 'cloud_prob'
        - 'cloud_prob' : Use cloud probability. Valid just for Sentinel-2.
        - 'qa' : Use Quality Assessment band. Valid just for Sentinel-2.
        This parameter is ignored for Landsat products.
    prob : numeric [0, 100], default = 60
        Cloud probability threshold. Valid just for method = 'prob'. This parameter is ignored for Landsat products.
    maskCirrus : boolean, default = True
        Whether to mask cirrus clouds. Valid just for method = 'qa'. This parameter is ignored for Landsat products.
    maskShadows : boolean, default = True
        Whether to mask cloud shadows. \n
        For more info see 'Braaten, J. 2020. Sentinel-2 Cloud Masking with s2cloudless. Google Earth Engine, Community Tutorials'.
    scaledImage : boolean, default = False
        Whether the pixel values are scaled to the range [0,1] (reflectance values). This parameter is ignored for Landsat products.
    dark : float [0,1], default = 0.15
        NIR threshold. NIR values below this threshold are potential cloud shadows. This parameter is ignored for Landsat products.
    cloudDist : int, default = 1000
        Maximum distance in meters (m) to look for cloud shadows from cloud edges. This parameter is ignored for Landsat products.
    buffer : int, default = 250
        Distance in meters (m) to dilate cloud and cloud shadows objects. This parameter is ignored for Landsat products.
    cdi : float [-1,1], default = None
        Cloud Displacement Index threshold. Values below this threshold are considered potential clouds.\n
        A cdi = None means that the index is not used. For more info see \n        
        'Frantz, D., HaS, E., Uhl, A., Stoffels, J., Hill, J. 2018. Improvement of the Fmask algorithm for Sentinel-2 images:\n
        Separating clouds from bright surfaces based on parallax effects. Remote Sensing of Environment 2015: 471-481'. \n
        This parameter is ignored for Landsat products.
        
    Returns
    -------
    ee.ImageCollection
        Cloud-shadow masked image collection.
    '''
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
    
    lookup = {
        'COPERNICUS/S2': S2,
        'LANDSAT/LC08': L8,
        'LANDSAT/LE07': L457,
        'LANDSAT/LT05': L457,
        'LANDSAT/LT04': L457
    }
    
    platformDict = _get_platform(self)
    
    if platformDict['platform'] == 'COPERNICUS/S2':
        maskedImageCollection = lookup[platformDict['platform']](self)
    else:
        maskedImageCollection = self.map(lookup[platformDict['platform']])
    
    return maskedImageCollection
    
def _scale(self):    
    '''Scales reflectance bands on an image collection. This also scales temperature in Landsat images and derived bands in Sentinel-2 images\n
    (except for MSK_CLDPRB and MSK_SNWPRB bands that are excluded from the image collection).
    
    Parameters
    ----------
    self : ee.ImageCollection (this)
        Image collection to scale. Accepted platforms:
        - Sentinel-2
        - Landsat 8
        - Landsat 7
        - Landsat 5
        - Landsat 4
        
    Returns
    -------
    ee.ImageCollection
        Scaled image collection.
    '''    
    def S2(img):
        scaled = img.select(['B.*']).divide(1e4)      
        scaled = scaled.addBands(img.select(['Q.*']))
        if platformDict['sr']:            
            scaled = scaled.addBands(img.select(['AOT','WVP']).divide(1e3))
            scaled = scaled.addBands(img.select(['T.*']))            
            scaled = scaled.addBands(img.select('SCL'))
        return ee.Image(scaled.copyProperties(img,img.propertyNames()))
    
    def L8(img):               
        if platformDict['sr']:
            scaled = img.select(['B[1-9]']).divide(1e4)
            scaled = scaled.addBands(img.select(['B10','B11']).divide(10)) 
            scaled = scaled.addBands(img.select(['sr_aerosol','pixel_qa','radsat_qa']))
            return ee.Image(scaled.copyProperties(img,img.propertyNames()))
        else:
            pass
        
    def L457(img):               
        if platformDict['sr']:
            scaled = img.select(['B[1-5]','B7']).divide(1e4)
            scaled = scaled.addBands(img.select(['B6']).divide(10)) 
            scaled = scaled.addBands(img.select(['sr_atmos_opacity']).divide(1e3)) 
            scaled = scaled.addBands(img.select(['sr_cloud_qa','pixel_qa','radsat_qa']))
            return ee.Image(scaled.copyProperties(img,img.propertyNames()))
        else:
            pass
    
    lookup = {
        'COPERNICUS/S2': S2,
        'LANDSAT/LC08': L8,
        'LANDSAT/LE07': L457,
        'LANDSAT/LT05': L457,
        'LANDSAT/LT04': L457
    }
    
    platformDict = _get_platform(self)    
    scaledImageCollection = self.map(lookup[platformDict['platform']])
    
    return scaledImageCollection

# Extend the ee.ImageCollection class with the new functions
setattr(ee.imagecollection.ImageCollection,'closest',_closest)
setattr(ee.imagecollection.ImageCollection,'maskClouds',_maskClouds)
setattr(ee.imagecollection.ImageCollection,'scale',_scale)
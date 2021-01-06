import ee
import numpy as np

def _extend_eeImageCollection():
    """Decorator. Extends the ee.ImageCollection class."""
    return lambda f: (setattr(ee.imagecollection.ImageCollection,f.__name__,f) or f)

def _get_platform(collection):
    '''Gets the platform (satellite) of an image collection and wheter if it is a Surface Reflectance product.
    
    Parameters
    ----------    
    collection : ee.Image.Collection
        Image to get platform.
        
    Returns
    -------
    dict :
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

@_extend_eeImageCollection()
def closest(self, date):
    '''Gets the closest image (or set of images if the collection intersects a region that requires multiple scenes) closest to the specified date.
    
    Parameters
    ----------    
    self : ee.ImageCollection [this]
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

@_extend_eeImageCollection()
def index(self,index = 'NDVI',G = 2.5,C1 = 6.0,C2 = 7.5,L = 1.0):
    '''Computes one or more spectral indices (indices are added as bands) for an image collection.
    
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
            - 'all' : Compute all indices listed below.
        Vegetation indices:     
            - 'BNDVI' : Blue Normalized Difference Vegetation Index.
            - 'CIG' : Chlorophyll Index - Green.
            - 'CVI' : Chlorophyll Vegetation Index.
            - 'EVI' : Enhanced Vegetation Index.
            - 'GNDVI' : Green Normalized Difference Vegetation Index.
            - 'NDVI' : Normalized Difference Vegetation Index.
            - 'NGRDI' : Normalized Green Red Difference Index.
            - 'SR' : Simple Ratio.
            - 'SAVI' : Soil-Adjusted Vegetation Index.
        Burn and fire indices:       
            - 'BAI' : Burned Area Index.
            - 'BAIS2' : Burned Area Index for Sentinel 2.
            - 'NBR' : Normalized Burn Ratio.
        Water indices:     
            - 'MNDWI' : Modified Normalized Difference Water Index.
            - 'NDWI' : Normalized Difference Water Index.        
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
    
    def lookupDic(img):
        
        def lookupS2(img):
            return {
                'G': float(G),
                'C1': float(C1),
                'C2': float(C2),
                'L': float(L),
                'A': img.select('B1'),
                'B': img.select('B2'),
                'G': img.select('B3'),
                'R': img.select('B4'),
                'RE1': img.select('B5'),
                'RE2': img.select('B6'),
                'RE3': img.select('B7'),
                'N' : img.select('B8'),
                'RE4': img.select('B8A'),
                'WV' : img.select('B9'),            
                'S1': img.select('B11'),
                'S2': img.select('B12')
            }
        
        def lookupL8(img):
            return {
                'G': float(G),
                'C1': float(C1),
                'C2': float(C2),
                'L': float(L),
                'A': img.select('B1'),
                'B': img.select('B2'),
                'G': img.select('B3'),
                'R': img.select('B4'),
                'N': img.select('B5'),
                'S1': img.select('B6'),
                'S2': img.select('B7'),                
                'T1' : img.select('B10'),
                'T2': img.select('B11')
            }
        
        def lookupL457(img):
            return {
                'G': float(G),
                'C1': float(C1),
                'C2': float(C2),
                'L': float(L),
                'B': img.select('B1'),
                'G': img.select('B2'),
                'R': img.select('B3'),
                'N': img.select('B4'),
                'S1': img.select('B5'),
                'T1': img.select('B6'),
                'S2': img.select('B7')                
            }
        
        lookupPlatform = {
            'COPERNICUS/S2': lookupS2,
            'LANDSAT/LC08': lookupL8,
            'LANDSAT/LE07': lookupL457,
            'LANDSAT/LT05': lookupL457,
            'LANDSAT/LT04': lookupL457
        }
        
        return lookupPlatform[platformDict['platform']](img)
    
    # VEGETATION INDICES
    
    def BNDVI(img):
        return img.addBands(img.expression('(N - B) / (N + B)',lookupDic(img)).rename('BNDVI'))
    
    def CIG(img):
        return img.addBands(img.expression('(N / G) - 1',lookupDic(img)).rename('CIG'))
    
    def CVI(img):
        return img.addBands(img.expression('(N * R) / (G ** 2)',lookupDic(img)).rename('CVI'))
    
    def EVI(img):
        return img.addBands(img.expression('G * (N - R) / (N + C1 * R - C2 * B + L)',lookupDic(img)).rename('EVI'))
       
    def GNDVI(img):
        return img.addBands(img.expression('(N - G) / (N + G)',lookupDic(img)).rename('GNDVI'))
    
    def NDVI(img):
        return img.addBands(img.expression('(N - R) / (N + R)',lookupDic(img)).rename('NDVI'))
    
    def NGRDI(img):
        return img.addBands(img.expression('(G - R) / (G + R)',lookupDic(img)).rename('NGRDI'))
    
    def SAVI(img):
        return img.addBands(img.expression('(1 + L) * (N - R) / (N + R + L)',lookupDic(img)).rename('SAVI'))
    
    def SR(img):
        return img.addBands(img.expression('N / R',lookupDic(img)).rename('SR'))
    
    lookupVegetation = {
        'BNDVI': BNDVI,
        'CIG': CIG,
        'CVI': CVI,
        'EVI': EVI,
        'GNDVI': GNDVI,
        'NDVI': NDVI,
        'NGRDI': NGRDI,        
        'SAVI': SAVI,
        'SR': SR,
    }
    
    # BURN INDICES
    
    def BAI(img):
        return img.addBands(img.expression('1.0 / ((0.1 - R) ** 2.0 + (0.06 - N) ** 2.0)',lookupDic(img)).rename('BAI'))
    
    def BAIS2(img):
        first = img.expression('(1.0 - ((RE2 * RE3 * RE4) / R) ** 0.5)',lookupDic(img))
        second = img.expression('(((S2 - RE4)/(S2 + RE4) ** 0.5) + 1.0)',lookupDic(img))
        return img.addBands(first.multiply(second).rename('BAIS2'))
    
    def NBR(img):
        return img.addBands(img.expression('(N - S2) / (N + S2)',lookupDic(img)).rename('NBR'))
    
    lookupBurn = {
        'BAI': BAI,
        'BAIS2': BAIS2,
        'NBR': NBR
    }
    
    # WATER INDICES
        
    def MNDWI(img):
        return img.addBands(img.expression('(G - S1) / (G + S1)',lookupDic(img)).rename('MNDWI'))
    
    def NDWI(img):
        return img.addBands(img.expression('(G - N) / (G + N)',lookupDic(img)).rename('NDWI'))
    
    lookupWater = {
        'MNDWI': MNDWI,
        'NDWI': NDWI,
    }
    
    # ALL INDICES
    
    lookup = {**lookupVegetation, **lookupBurn, **lookupWater}
    
    if not isinstance(index, list):
        if index == 'all':
            index = list(lookup.keys())
        elif index == 'vegetation':
            index = list(lookupVegetation.keys())
        elif index == 'burn':
            index = list(lookupBurn.keys())
        elif index == 'water':
            index = list(lookupWater.keys())
        else:
            index = [index]        
    
    if platformDict['platform'] != 'COPERNICUS/S2' and 'BAIS2' in index:
        index.remove('BAIS2')
    
    for idx in index:
        self = self.map(lookup[idx])
    
    return self

@_extend_eeImageCollection()
def maskClouds(self, method = 'cloud_prob', prob = 60, maskCirrus = True, maskShadows = True, scaledImage = False, dark = 0.15, cloudDist = 1000, buffer = 250, cdi = None):
    '''Masks clouds and shadows in an image collection (valid just for Surface Reflectance products).
    
    Parameters
    ----------    
    self : ee.ImageCollection [this]
        Image collection to mask.\n
        Accepted platforms:
            - Sentinel-2
            - Landsat 8
            - Landsat 7
            - Landsat 5
            - Landsat 4
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

@_extend_eeImageCollection()
def scale(self):    
    '''Scales reflectance bands on an image collection. This also scales temperature in Landsat images and derived bands in Sentinel-2 images
    (except for MSK_CLDPRB and MSK_SNWPRB bands that are excluded from the image collection).
    
    Parameters
    ----------
    self : ee.ImageCollection (this)
        Image collection to scale.\n
        Accepted platforms:
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
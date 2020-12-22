import ee

def cloudMask(args,method = 'cloud_prob',prob = 60,maskCirrus = True,maskShadows = True,scaledImage = False,dark = 0.15,
              cloudDist = 1000,buffer = 250,cdi = None):    
    '''Mask clouds and shadows in a Sentinel-2 SR image collection (or image).
    
    Parameters
    ----------
    args : ee.ImageCollection | ee.Image
        Sentinel-2 collection (or image) to mask.
    method : string, default = 'cloud_prob'
        - 'cloud_prob' : Use cloud probability.
        - 'qa' : Use Quality Assessment band.
    prob : numeric [0, 100], default = 60
        Cloud probability threshold.
    maskCirrus : boolean, default = True
        Whether to mask cirrus clouds. Used just for method = 'qa'.
    maskShadows : boolean, default = True
        Whether to mask cloud shadows. \n
        For more info see 'Braaten, J. 2020. Sentinel-2 Cloud Masking with s2cloudless. Google Earth Engine, Community Tutorials'.
    scaledImage : boolean, default = False
        Whether the pixel values are scaled to the range [0,1] (reflectance values).
    dark : float [0,1], default = 0.15
        NIR threshold. NIR values below this threshold are potential cloud shadows. 
    cloudDist : int, default = 1000
        Maximum distance in meters (m) to look for cloud shadows from cloud edges. 
    buffer : int, default = 250
        Distance in meters (m) to dilate cloud and cloud shadows objects.
    cdi : float [-1,1], default = None
        Cloud Displacement Index threshold. Values below this threshold are considered potential clouds.\n
        A cdi = None means that the index is not used. For more info see \n        
        'Frantz, D., HaS, E., Uhl, A., Stoffels, J., Hill, J. 2018. Improvement of the Fmask algorithm for Sentinel-2 images:\n
        Separating clouds from bright surfaces based on parallax effects. Remote Sensing of Environment 2015: 471-481'.
        
    Returns
    -------
    ee.ImageCollection | ee.Image
        Cloud-shadow masked Sentinel-2 collection (or image).
    '''
    def cloud_prob_collection(img):
        clouds = ee.Image(img.get('cloud_mask')).select('probability')
        isCloud = clouds.gte(prob).rename('CLOUD_MASK')
        return img.addBands(isCloud)

    def cloud_prob_image(img):
        clouds = img.select('probability')
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
    
    if isinstance(args,ee.imagecollection.ImageCollection):
    
        if method == 'cloud_prob':
            S2Clouds = ee.ImageCollection('COPERNICUS/S2_CLOUD_PROBABILITY')                  
            fil = ee.Filter.equals(leftField = 'system:index',rightField = 'system:index')
            S2WithCloudMask = ee.Join.saveFirst('cloud_mask').apply(args,S2Clouds,fil)
            S2Masked = ee.ImageCollection(S2WithCloudMask).map(cloud_prob_collection)
        elif method == 'qa':        
            S2Masked = args.map(QA)

        if cdi != None: 
            S2Masked = S2Masked.map(CDI)

        if maskShadows:
            S2Masked = S2Masked.map(get_shadows)

        S2Masked = S2Masked.map(clean_dilate)
        S2Masked = S2Masked.map(apply_mask)
            
    elif isinstance(args,ee.image.Image):
    
        if method == 'cloud_prob':
            idx = args.get('system:index')
            S2Clouds = ee.ImageCollection('COPERNICUS/S2_CLOUD_PROBABILITY').filter(ee.Filter.eq('system:index',idx)).first()
            S2WithCloudMask = args.addBands(S2Clouds)                   
            S2Masked = cloud_prob_image(S2WithCloudMask)
        elif method == 'qa':        
            S2Masked = QA(args)

        if cdi != None:
            S2Masked = CDI(S2Masked)

        if maskShadows:
            S2Masked = get_shadows(S2Masked)

        S2Masked = clean_dilate(S2Masked)
        S2Masked = apply_mask(S2Masked)
        
    return S2Masked

def reflectance(args,surfaceReflectance = True):    
    '''Scale reflectance on a Sentinel-2 image (This also scales the AOT and WVP products in a Surface Reflectance product).
    
    Parameters
    ----------
    args : ee.ImageCollection | ee.Image
        Sentinel-2 Image (or Image Collection) to compute reflectance on.
    surfaceReflectance : boolean, default = True
        Whether the image is the Surface Reflectance product.
        
    Returns
    -------
    ee.ImageCollection | ee.Image
        Sentinel-2 reflectance image (or Image Collection).
    '''    
    def scaleImage(img):
        scaled = img.select(['B.*']).divide(1e4)      
        scaled = scaled.addBands(img.select(['Q.*']))
        if surfaceReflectance:            
            scaled = scaled.addBands(img.select(['AOT','WVP']).divide(1e3))
            scaled = scaled.addBands(img.select(['T.*']))
            scaled = scaled.addBands(img.select(['M.*']))
            scaled = scaled.addBands(img.select('SCL'))
        return scaled
    
    if isinstance(args, ee.imagecollection.ImageCollection):
        scaledArgs = args.map(scaleImage)
        
    elif isinstance(args, ee.image.Image):
        scaledArgs = scaleImage(args)
    
    return scaledArgs

def spectralIndex(args,index = 'NDVI',G = 2.5,C1 = 6.0,C2 = 7.5,L = 1.0):
    '''Compute one or more spectral indices (indices are added as bands) for a Sentinel 2 Image (or Image Collection).
    
    Parameters
    ----------
    args : ee.ImageCollection | ee.Image
        Sentinel-2 reflectance Image (or Image Collection) to compute indices on. Image(s) must be scaled to [0,1].
    index : string | list[string], default = 'NDVI'
        Index or list of indices to compute. Available options:
        - 'vegetation' : Compute all vegetation indices.
        - 'burn' : Compute all burn indices.
        - 'water' : Compute all water indices.
        - 'all' : Compute all indices listed below.
        Vegetation indices:        
        - 'BNDVI' : Blue Normalized Difference Vegetation Index.
        - 'EVI' : Enhanced Vegetation Index.
        - 'GNDVI' : Green Normalized Difference Vegetation Index.
        - 'NDVI' : Normalized Difference Vegetation Index.
        - 'SAVI' : Soil-Adjusted Vegetation Index.
        Burn and fire indices:        
        - 'BAI' : Burned Area Index.
        - 'BAIS2' : Burned Area Index for Sentinel 2.
        - 'NBR' : Normalized Burn Ratio.
        Water indices:        
        - 'AWEInsh' : Automated Water Extraction Index nsh.
        - 'AWEIsh' : Automated Water Extraction Index sh.
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
    ee.ImageCollection | ee.Image
        Sentinel-2 image (or Image Collection) with the computed spectral index, or indices, as new bands.
    '''  
    def lookupDic(img):
        
        lookupDictionary = {
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
        
        return lookupDictionary
    
    # VEGETATION INDICES
    
    def BNDVI(img):
        return img.addBands(img.normalizedDifference(['B8','B2']).rename('BNDVI'))
    
    def EVI(img):
        return img.addBands(img.expression('G * (N - R) / (N + C1 * R - C2 * B + L)',lookupDic(img)).rename('EVI'))
       
    def GNDVI(img):
        return img.addBands(img.normalizedDifference(['B8','B3']).rename('GNDVI'))
    
    def NDVI(img):
        return img.addBands(img.normalizedDifference(['B8','B4']).rename('NDVI'))
    
    def SAVI(img):
        return img.addBands(img.expression('(1 + L) * (N - R) / (N + R + L)',lookupDic(img)).rename('SAVI'))
    
    lookupVegetation = {
        'BNDVI': BNDVI,
        'EVI': EVI,
        'GNDVI': GNDVI,
        'NDVI': NDVI,
        'SAVI': SAVI
    }
    
    # BURN INDICES
    
    def BAI(img):
        return img.addBands(img.expression('1.0 / ((0.1 - R) ** 2.0 + (0.06 - N) ** 2.0)',lookupDic(img)).rename('BAI'))
    
    def BAIS2(img):
        first = img.expression('(1.0 - ((RE2 * RE3 * RE4) / R) ** 0.5)',lookupDic(img))
        second = img.expression('(((S2 - RE4)/(S2 + RE4) ** 0.5) + 1.0)',lookupDic(img))
        return img.addBands(first.multiply(second).rename('BAIS2'))
    
    def NBR(img):
        return img.addBands(img.normalizedDifference(['B8','B12']).rename('NBR'))
    
    lookupBurn = {
        'BAI': BAI,
        'BAIS2': BAIS2,
        'NBR': NBR
    }
    
    # WATER INDICES
    
    def AWEInsh(img):
        return img.addBands(img.expression('4.0 * (G - S1) - (0.25 * N + 2.75 * S1)',lookupDic(img)).rename('AWEInsh'))
    
    def AWEIsh(img):
        return img.addBands(img.expression('B + 2.5 * G - 1.5 * (N + S1) - 0.25 * S2',lookupDic(img)).rename('AWEIsh'))
    
    def MNDWI(img):
        return img.addBands(img.normalizedDifference(['B3','B11']).rename('MNDWI'))
    
    def NDWI(img):
        return img.addBands(img.normalizedDifference(['B3','B8']).rename('NDWI'))
    
    lookupWater = {
        'MNDWI': MNDWI,
        'NDWI': NDWI,
        'AWEInsh': AWEInsh,
        'AWEIsh': AWEIsh,
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
    
    if isinstance(args, ee.imagecollection.ImageCollection):
        for idx in index:
            args = args.map(lookup[idx])
        
    elif isinstance(args, ee.image.Image):
        for idx in index:
            args = lookup[idx](args)
        
    return args
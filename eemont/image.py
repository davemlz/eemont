import ee
import warnings
from .common import _get_indices
from .common import _get_platform
from .common import _get_scale_method
from .common import _get_expression_map
from .common import _index

def _extend_eeImage():
    """Decorator. Extends the ee.ImageCollection class."""
    return lambda f: (setattr(ee.image.Image,f.__name__,f) or f)

@_extend_eeImage()
def __add__(self, other):
    '''Computes the addition between two images.

    Parameters
    ----------
    self : ee.Image
        Left operand.
    other : ee.Image | numeric | list[numeric]
        Right operand. If numeric, an ee.Image is created from its value. If list, an ee.Image with n bands (n = len(list)) is created from its values.

    Returns
    -------
    ee.Image
        Addition of two images.
    '''
    return self.add(other)

@_extend_eeImage()
def __radd__(self, other):
    '''Computes the addition between two images.

    Parameters
    ----------
    self : ee.Image
        Right operand.
    other : ee.Image | numeric | list[numeric]
        Left operand. If numeric, an ee.Image is created from its value. If list, an ee.Image with n bands (n = len(list)) is created from its values.

    Returns
    -------
    ee.Image
        Addition of two images.
    '''
    return self.add(other)

@_extend_eeImage()
def __sub__(self, other):
    '''Computes the subtraction between two images.

    Parameters
    ----------
    self : ee.Image
        Left operand.
    other : ee.Image | numeric | list[numeric]
        Right operand. If numeric, an ee.Image is created from its value. If list, an ee.Image with n bands (n = len(list)) is created from its values.

    Returns
    -------
    ee.Image
        Subtraction of two images.
    '''
    return self.subtract(other)

@_extend_eeImage()
def __rsub__(self, other):
    '''Computes the subtraction between two images.

    Parameters
    ----------
    self : ee.Image
        Right operand.
    other : ee.Image | numeric | list[numeric]
        Left operand. If numeric, an ee.Image is created from its value. If list, an ee.Image with n bands (n = len(list)) is created from its values.

    Returns
    -------
    ee.Image
        Subtraction of two images.
    '''
    return ee.Image(other).subtract(self)

@_extend_eeImage()
def __mul__(self, other):
    '''Computes the multiplication between two images.

    Parameters
    ----------
    self : ee.Image
        Left operand.
    other : ee.Image | numeric | list[numeric]
        Right operand. If numeric, an ee.Image is created from its value. If list, an ee.Image with n bands (n = len(list)) is created from its values.

    Returns
    -------
    ee.Image
        Multiplication of two images.
    '''
    return self.multiply(other)

@_extend_eeImage()
def __rmul__(self, other):
    '''Computes the multiplication between two images.

    Parameters
    ----------
    self : ee.Image
        Right operand.
    other : ee.Image | numeric | list[numeric]
        Left operand. If numeric, an ee.Image is created from its value. If list, an ee.Image with n bands (n = len(list)) is created from its values.

    Returns
    -------
    ee.Image
        Multiplication of two images.
    '''
    return self.multiply(other)

@_extend_eeImage()
def __truediv__(self, other):
    '''Computes the division between two images.

    Parameters
    ----------
    self : ee.Image
        Left operand.
    other : ee.Image | numeric | list[numeric]
        Right operand. If numeric, an ee.Image is created from its value. If list, an ee.Image with n bands (n = len(list)) is created from its values.

    Returns
    -------
    ee.Image
        Division of two images.
    '''
    return self.divide(other)

@_extend_eeImage()
def __rtruediv__(self, other):
    '''Computes the division between two images.

    Parameters
    ----------
    self : ee.Image
        Right operand.
    other : ee.Image | numeric | list[numeric]
        Left operand. If numeric, an ee.Image is created from its value. If list, an ee.Image with n bands (n = len(list)) is created from its values.

    Returns
    -------
    ee.Image
        Division of two images.
    '''
    return ee.Image(other).divide(self)

@_extend_eeImage()
def __floordiv__(self, other):
    '''Computes the floor division of two images.

    Parameters
    ----------
    self : ee.Image
        Left operand.
    other : ee.Image | numeric | list[numeric]
        Right operand. If numeric, an ee.Image is created from its value. If list, an ee.Image with n bands (n = len(list)) is created from its values.

    Returns
    -------
    ee.Image
        Floor division of two images.
    '''
    return self.divide(other).floor()

@_extend_eeImage()
def __rfloordiv__(self, other):
    '''Computes the floor division of two images.

    Parameters
    ----------
    self : ee.Image
        Right operand.
    other : ee.Image | numeric | list[numeric]
        Left operand. If numeric, an ee.Image is created from its value. If list, an ee.Image with n bands (n = len(list)) is created from its values.

    Returns
    -------
    ee.Image
        Floor division of two images.
    '''
    return ee.Image(other).divide(self).floor()

@_extend_eeImage()
def __mod__(self, other):
    '''Computes the modulo of two images.

    Parameters
    ----------
    self : ee.Image
        Left operand.
    other : ee.Image | numeric | list[numeric]
        Right operand. If numeric, an ee.Image is created from its value. If list, an ee.Image with n bands (n = len(list)) is created from its values.

    Returns
    -------
    ee.Image
        Modulo of two images.
    '''
    return self.mod(other)

@_extend_eeImage()
def __rmod__(self, other):
    '''Computes the modulo of two images.

    Parameters
    ----------
    self : ee.Image
        Right operand.
    other : ee.Image | numeric | list[numeric]
        Left operand. If numeric, an ee.Image is created from its value. If list, an ee.Image with n bands (n = len(list)) is created from its values.

    Returns
    -------
    ee.Image
        Modulo of two images.
    '''
    return ee.Image(other).mod(self)

@_extend_eeImage()
def __pow__(self, other):
    '''Computes the base (left operand) to the power (right operand).

    Parameters
    ----------
    self : ee.Image
        Left operand.
    other : ee.Image | numeric | list[numeric]
        Right operand. If numeric, an ee.Image is created from its value. If list, an ee.Image with n bands (n = len(list)) is created from its values.

    Returns
    -------
    ee.Image
        Bsae to the power of two images.
    '''
    return self.pow(other)

@_extend_eeImage()
def __rpow__(self, other):
    '''Computes the base (left operand) to the power (right operand).

    Parameters
    ----------
    self : ee.Image
        Right operand.
    other : ee.Image | numeric | list[numeric]
        Left operand. If numeric, an ee.Image is created from its value. If list, an ee.Image with n bands (n = len(list)) is created from its values.

    Returns
    -------
    ee.Image
        Base to the power of two images.
    '''
    return ee.Image(other).pow(self)

@_extend_eeImage()
def __lshift__(self, other):
    '''Computes the left shift operation between two images.

    Parameters
    ----------
    self : ee.Image
        Left operand.
    other : ee.Image | numeric | list[numeric]
        Right operand. If numeric, an ee.Image is created from its value. If list, an ee.Image with n bands (n = len(list)) is created from its values.

    Returns
    -------
    ee.Image
        Left shift operation.
    '''
    return self.leftShift(other)

@_extend_eeImage()
def __rlshift__(self, other):
    '''Computes the left shift operation between two images.

    Parameters
    ----------
    self : ee.Image
        Right operand.
    other : ee.Image | numeric | list[numeric]
        Left operand. If numeric, an ee.Image is created from its value. If list, an ee.Image with n bands (n = len(list)) is created from its values.

    Returns
    -------
    ee.Image
        Left shift operation.
    '''
    return ee.Image(other).leftShift(self)

@_extend_eeImage()
def __rshift__(self, other):
    '''Computes the right shift operation between two images.

    Parameters
    ----------
    self : ee.Image
        Left operand.
    other : ee.Image | numeric | list[numeric]
        Right operand. If numeric, an ee.Image is created from its value. If list, an ee.Image with n bands (n = len(list)) is created from its values.

    Returns
    -------
    ee.Image
        Right shift operation.
    '''
    return self.rightShift(other)

@_extend_eeImage()
def __rrshift__(self, other):
    '''Computes the right shift operation between two images.

    Parameters
    ----------
    self : ee.Image
        Right operand.
    other : ee.Image | numeric | list[numeric]
        Left operand. If numeric, an ee.Image is created from its value. If list, an ee.Image with n bands (n = len(list)) is created from its values.

    Returns
    -------
    ee.Image
        Right shift operation.
    '''
    return ee.Image(other).rightShift(self)

@_extend_eeImage()
def __and__(self, other):
    '''Computes the binary operator AND between two images.

    Parameters
    ----------
    self : ee.Image
        Left operand.
    other : ee.Image | numeric | list[numeric]
        Right operand. If numeric, an ee.Image is created from its value. If list, an ee.Image with n bands (n = len(list)) is created from its values.

    Returns
    -------
    ee.Image
        Binary operator AND.
    '''
    return self.And(other)

@_extend_eeImage()
def __rand__(self, other):
    '''Computes the binary operator AND between two images.

    Parameters
    ----------
    self : ee.Image
        Right operand.
    other : ee.Image | numeric | list[numeric]
        Left operand. If numeric, an ee.Image is created from its value. If list, an ee.Image with n bands (n = len(list)) is created from its values.

    Returns
    -------
    ee.Image
        Binary operator AND.
    '''
    return ee.Image(other).And(self)

@_extend_eeImage()
def __or__(self, other):
    '''Computes the binary operator OR between two images.

    Parameters
    ----------
    self : ee.Image
        Left operand.
    other : ee.Image | numeric | list[numeric]
        Right operand. If numeric, an ee.Image is created from its value. If list, an ee.Image with n bands (n = len(list)) is created from its values.

    Returns
    -------
    ee.Image
        Binary operator OR.
    '''
    return self.Or(other)

@_extend_eeImage()
def __ror__(self, other):
    '''Computes the binary operator OR between two images.

    Parameters
    ----------
    self : ee.Image
        Right operand.
    other : ee.Image | numeric | list[numeric]
        Left operand. If numeric, an ee.Image is created from its value. If list, an ee.Image with n bands (n = len(list)) is created from its values.

    Returns
    -------
    ee.Image
        Binary operator OR.
    '''
    return ee.Image(other).Or(self)

@_extend_eeImage()
def __lt__(self, other):
    '''Computes the rich comparison LOWER THAN between two images.

    Parameters
    ----------
    self : ee.Image
        Left operand.
    other : ee.Image | numeric | list[numeric]
        Right operand. If numeric, an ee.Image is created from its value. If list, an ee.Image with n bands (n = len(list)) is created from its values.

    Returns
    -------
    ee.Image
        Rich comparison LOWER THAN.
    '''
    return self.lt(other)

@_extend_eeImage()
def __le__(self, other):
    '''Computes the rich comparison LOWER THAN OR EQUAL between two images.

    Parameters
    ----------
    self : ee.Image
        Left operand.
    other : ee.Image | numeric | list[numeric]
        Right operand. If numeric, an ee.Image is created from its value. If list, an ee.Image with n bands (n = len(list)) is created from its values.

    Returns
    -------
    ee.Image
        Rich comparison LOWER THAN OR EQUAL.
    '''
    return self.lte(other)

@_extend_eeImage()
def __eq__(self, other):
    '''Computes the rich comparison EQUAL between two images.

    Parameters
    ----------
    self : ee.Image
        Left operand.
    other : ee.Image | numeric | list[numeric]
        Right operand. If numeric, an ee.Image is created from its value. If list, an ee.Image with n bands (n = len(list)) is created from its values.

    Returns
    -------
    ee.Image
        Rich comparison EQUAL.
    '''
    return self.eq(other)

@_extend_eeImage()
def __ne__(self, other):
    '''Computes the rich comparison NOT EQUAL THAN between two images.

    Parameters
    ----------
    self : ee.Image
        Left operand.
    other : ee.Image | numeric | list[numeric]
        Right operand. If numeric, an ee.Image is created from its value. If list, an ee.Image with n bands (n = len(list)) is created from its values.

    Returns
    -------
    ee.Image
        Rich comparison NOT EQUAL.
    '''
    return self.neq(other)

@_extend_eeImage()
def __gt__(self, other):
    '''Computes the rich comparison GREATER THAN between two images.

    Parameters
    ----------
    self : ee.Image
        Left operand.
    other : ee.Image | numeric | list[numeric]
        Right operand. If numeric, an ee.Image is created from its value. If list, an ee.Image with n bands (n = len(list)) is created from its values.

    Returns
    -------
    ee.Image
        Rich comparison GREATER THAN.
    '''
    return self.gt(other)

@_extend_eeImage()
def __ge__(self, other):
    '''Computes the rich comparison GREATER THAN OR EQUAL between two images.

    Parameters
    ----------
    self : ee.Image
        Left operand.
    other : ee.Image | numeric | list[numeric]
        Right operand. If numeric, an ee.Image is created from its value. If list, an ee.Image with n bands (n = len(list)) is created from its values.

    Returns
    -------
    ee.Image
        Rich comparison GREATER THAN OR EQUAL.
    '''
    return self.gte(other)

@_extend_eeImage()
def __neg__(self):
    '''Computes the unary operator NEGATIVE on an image.

    Parameters
    ----------
    self : ee.Image
        Operand.

    Returns
    -------
    ee.Image
        Unary operator NEGATIVE.
    '''
    return self.multiply(-1)

@_extend_eeImage()
def __invert__(self):
    '''Computes the unary operator NOT on an image.

    Parameters
    ----------
    self : ee.Image
        Operand.

    Returns
    -------
    ee.Image
        Unary operator NOT.
    '''
    return self.Not()

@_extend_eeImage()
def index(self,index = 'NDVI',G = 2.5,C1 = 6.0,C2 = 7.5,L = 1.0,kernel = 'RBF',sigma = '0.5 * (a + b)',p = 2.0,c = 1.0):
    '''Computes one or more spectral indices (indices are added as bands) for an image.
    
    Parameters
    ----------    
    self : ee.Image [this]
        Image to compute indices on. Must be scaled to [0,1]. Check the supported platforms in User Guide > Spectral Indices > Supported Platforms.        
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
    ee.Image
        Image with the computed spectral index, or indices, as new bands.
        
    Examples
    --------
    >>> import ee, eemont
    >>> ee.Initialize()
    >>> S2 = ee.ImageCollection('COPERNICUS/S2_SR').first().scale().index(['NDVI','EVI','GNDVI'])
    
    See Also
    --------
    scale : Scales bands on an image collection.
    '''    
    return _index(self,index,G,C1,C2,L,kernel,sigma,p,c)

@_extend_eeImage()
def maskClouds(self, method = 'cloud_prob', prob = 60, maskCirrus = True, maskShadows = True, scaledImage = False, dark = 0.15, cloudDist = 1000, buffer = 250, cdi = None):
    '''Masks clouds and shadows in an image (valid just for Surface Reflectance products).
    
    Parameters
    ----------    
    self : ee.Image [this]
        Image to mask. Check the supported platforms in User Guide > Masking Clouds and Shadows > Supported Platforms.
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
        A cdi = None means that the index is not used. For more info see 'Frantz, D., HaS, E., Uhl, A., Stoffels, J., Hill, J. 2018. Improvement of the Fmask algorithm for Sentinel-2 images:
        Separating clouds from bright surfaces based on parallax effects. Remote Sensing of Environment 2015: 471-481'.
        This parameter is ignored for Landsat products.
        
    Returns
    -------
    ee.Image
        Cloud-shadow masked image.
        
    Examples
    --------
    >>> import ee, eemont
    >>> ee.Initialize()
    >>> S2 = ee.ImageCollection('COPERNICUS/S2_SR').first().maskClouds(prob = 75,buffer = 300,cdi = -0.5)
        
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
            S2WithCloudMask = ee.Join.saveFirst('cloud_mask').apply(ee.ImageCollection(args),S2Clouds,fil)
            S2Masked = ee.ImageCollection(S2WithCloudMask).map(cloud_prob).first()            
        elif method == 'qa':        
            S2Masked = QA(args)
        if cdi != None:
            S2Masked = CDI(S2Masked)
        if maskShadows:
            S2Masked = get_shadows(S2Masked)
        S2Masked = apply_mask(clean_dilate(S2Masked))        
        
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
        return args.updateMask(notCloud);
    
    def MCD15A3H(args):
        qa = args.select('FparExtra_QC')
        notCloud = qa.bitwiseAnd(1 << 5).eq(0)
        if maskShadows:
            notCloud = notCloud.And(qa.bitwiseAnd(1 << 6).eq(0))
        if maskCirrus:
            notCloud = notCloud.And(qa.bitwiseAnd(1 << 4).eq(0))        
        return args.updateMask(notCloud);
    
    def MOD09Q1(args):
        qa = args.select('State')
        notCloud = qa.bitwiseAnd(1 << 0).eq(0)
        if maskShadows:
            notCloud = notCloud.And(qa.bitwiseAnd(1 << 2).eq(0))
        if maskCirrus:
            notCloud = notCloud.And(qa.bitwiseAnd(1 << 8).eq(0))        
        return args.updateMask(notCloud);
        
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
    
    maskedImage = lookup[platformDict['platform']](self)    
    
    return maskedImage

@_extend_eeImage()
def scale(self):    
    '''Scales bands on an image.
    
    Parameters
    ----------    
    self : ee.Image [this]
        Image to scale. Check the supported platforms in User Guide > Image Scaling > Supported Platforms.
        
    Returns
    -------
    ee.Image
        Scaled image.
    
    Examples
    --------
    >>> import ee, eemont
    >>> ee.Initialize()
    >>> S2 = ee.ImageCollection('COPERNICUS/S2_SR').first().scale()
    '''
    platformDict = _get_platform(self)
    lookup = _get_scale_method(platformDict)
    
    if platformDict['platform'] not in list(lookup.keys()):
        raise Exception("Sorry, satellite platform not supported for scaling!")
    
    scaledImage = lookup[platformDict['platform']](self)
    
    return scaledImage
import ee
import warnings
import requests
from .common import _index
from .common import _maskClouds
from .common import _get_scale_params
from .common import _get_offset_params
from .common import _scale_STAC
from .common import _preprocess


def _extend_eeImage():
    """Decorator. Extends the ee.ImageCollection class."""
    return lambda f: (setattr(ee.image.Image, f.__name__, f) or f)


@_extend_eeImage()
def __add__(self, other):
    """Computes the addition between two images.

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
    """
    return self.add(other)


@_extend_eeImage()
def __radd__(self, other):
    """Computes the addition between two images.

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
    """
    return self.add(other)


@_extend_eeImage()
def __sub__(self, other):
    """Computes the subtraction between two images.

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
    """
    return self.subtract(other)


@_extend_eeImage()
def __rsub__(self, other):
    """Computes the subtraction between two images.

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
    """
    return ee.Image(other).subtract(self)


@_extend_eeImage()
def __mul__(self, other):
    """Computes the multiplication between two images.

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
    """
    return self.multiply(other)


@_extend_eeImage()
def __rmul__(self, other):
    """Computes the multiplication between two images.

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
    """
    return self.multiply(other)


@_extend_eeImage()
def __truediv__(self, other):
    """Computes the division between two images.

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
    """
    return self.divide(other)


@_extend_eeImage()
def __rtruediv__(self, other):
    """Computes the division between two images.

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
    """
    return ee.Image(other).divide(self)


@_extend_eeImage()
def __floordiv__(self, other):
    """Computes the floor division of two images.

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
    """
    return self.divide(other).floor()


@_extend_eeImage()
def __rfloordiv__(self, other):
    """Computes the floor division of two images.

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
    """
    return ee.Image(other).divide(self).floor()


@_extend_eeImage()
def __mod__(self, other):
    """Computes the modulo of two images.

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
    """
    return self.mod(other)


@_extend_eeImage()
def __rmod__(self, other):
    """Computes the modulo of two images.

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
    """
    return ee.Image(other).mod(self)


@_extend_eeImage()
def __pow__(self, other):
    """Computes the base (left operand) to the power (right operand).

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
    """
    return self.pow(other)


@_extend_eeImage()
def __rpow__(self, other):
    """Computes the base (left operand) to the power (right operand).

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
    """
    return ee.Image(other).pow(self)


@_extend_eeImage()
def __lshift__(self, other):
    """Computes the left shift operation between two images.

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
    """
    return self.leftShift(other)


@_extend_eeImage()
def __rlshift__(self, other):
    """Computes the left shift operation between two images.

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
    """
    return ee.Image(other).leftShift(self)


@_extend_eeImage()
def __rshift__(self, other):
    """Computes the right shift operation between two images.

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
    """
    return self.rightShift(other)


@_extend_eeImage()
def __rrshift__(self, other):
    """Computes the right shift operation between two images.

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
    """
    return ee.Image(other).rightShift(self)


@_extend_eeImage()
def __and__(self, other):
    """Computes the binary operator AND between two images.

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
    """
    return self.And(other)


@_extend_eeImage()
def __rand__(self, other):
    """Computes the binary operator AND between two images.

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
    """
    return ee.Image(other).And(self)


@_extend_eeImage()
def __or__(self, other):
    """Computes the binary operator OR between two images.

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
    """
    return self.Or(other)


@_extend_eeImage()
def __ror__(self, other):
    """Computes the binary operator OR between two images.

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
    """
    return ee.Image(other).Or(self)


@_extend_eeImage()
def __lt__(self, other):
    """Computes the rich comparison LOWER THAN between two images.

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
    """
    return self.lt(other)


@_extend_eeImage()
def __le__(self, other):
    """Computes the rich comparison LOWER THAN OR EQUAL between two images.

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
    """
    return self.lte(other)


@_extend_eeImage()
def __eq__(self, other):
    """Computes the rich comparison EQUAL between two images.

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
    """
    return self.eq(other)


@_extend_eeImage()
def __ne__(self, other):
    """Computes the rich comparison NOT EQUAL THAN between two images.

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
    """
    return self.neq(other)


@_extend_eeImage()
def __gt__(self, other):
    """Computes the rich comparison GREATER THAN between two images.

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
    """
    return self.gt(other)


@_extend_eeImage()
def __ge__(self, other):
    """Computes the rich comparison GREATER THAN OR EQUAL between two images.

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
    """
    return self.gte(other)


@_extend_eeImage()
def __neg__(self):
    """Computes the unary operator NEGATIVE on an image.

    Parameters
    ----------
    self : ee.Image
        Operand.

    Returns
    -------
    ee.Image
        Unary operator NEGATIVE.
    """
    return self.multiply(-1)


@_extend_eeImage()
def __invert__(self):
    """Computes the unary operator NOT on an image.

    Parameters
    ----------
    self : ee.Image
        Operand.

    Returns
    -------
    ee.Image
        Unary operator NOT.
    """
    return self.Not()


@_extend_eeImage()
def index(
    self,
    index="NDVI",
    G=2.5,
    C1=6.0,
    C2=7.5,
    L=1.0,
    kernel="RBF",
    sigma="0.5 * (a + b)",
    p=2.0,
    c=1.0,
    online=False,
):
    """Computes one or more spectral indices (indices are added as bands) for an image.

    Warning
    -------------
    **Pending Deprecation:** The :code:`index()` method will no longer be available for future versions. Please use :code:`spectralIndices()` instead.

    Tip
    ----------
    Check more info about the supported platforms and spectral indices in the :ref:`User Guide<Spectral Indices>`.

    Parameters
    ----------
    self : ee.Image [this]
        Image to compute indices on. Must be scaled to [0,1].
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
    online : boolean, default = False
        Wheter to retrieve the most recent list of indices directly from the GitHub repository and not from the local copy.
        
        .. versionadded:: 0.2.0

    Returns
    -------
    ee.Image
        Image with the computed spectral index, or indices, as new bands.

    See Also
    --------
    scale : Scales bands on an image collection.

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> S2 = ee.ImageCollection('COPERNICUS/S2_SR').scale().first()

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
    """
    warnings.warn(
        "index() will be deprecated in future versions, please use spectralIndices() instead",
        PendingDeprecationWarning,
    )

    return _index(self, index, G, C1, C2, L, kernel, sigma, p, c, online)


@_extend_eeImage()
def spectralIndices(
    self,
    index="NDVI",
    G=2.5,
    C1=6.0,
    C2=7.5,
    L=1.0,
    kernel="RBF",
    sigma="0.5 * (a + b)",
    p=2.0,
    c=1.0,
    online=False,
):
    """Computes one or more spectral indices (indices are added as bands) for an image from the Awesome List of Spectral Indices.

    Tip
    ----------
    Check more info about the supported platforms and spectral indices in the :ref:`User Guide<Spectral Indices>`.

    Parameters
    ----------
    self : ee.Image [this]
        Image to compute indices on. Must be scaled to [0,1].
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
    online : boolean, default = False
        Wheter to retrieve the most recent list of indices directly from the GitHub repository and not from the local copy.

    Returns
    -------
    ee.Image
        Image with the computed spectral index, or indices, as new bands.

    See Also
    --------
    scaleAndOffset : Scales bands on an image collection.

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> S2 = ee.ImageCollection('COPERNICUS/S2_SR').scaleAndOffset().first()

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
    return _index(self, index, G, C1, C2, L, kernel, sigma, p, c, online)


@_extend_eeImage()
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
    """Masks clouds and shadows in an image (valid just for Surface Reflectance products).

    Tip
    ----------
    Check more info about the supported platforms and clouds masking in the :ref:`User Guide<Masking Clouds and Shadows>`.

    Parameters
    ----------
    self : ee.Image [this]
        Image to mask.
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

    Notes
    -----
    This method may mask water as well as clouds for the Sentinel-3 Radiance product.

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> S2 = ee.ImageCollection('COPERNICUS/S2_SR').first().maskClouds(prob = 75,buffer = 300,cdi = -0.5)
    """
    return _maskClouds(
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


@_extend_eeImage()
def scale(self):
    """Scales bands on an image.

    Warning
    -------------
    **Pending Deprecation:** The :code:`scale()` method will no longer be available for future versions. Please use :code:`scaleAndOffset()` instead.

    Tip
    ----------
    Check more info about the supported platforms and image scaling the :ref:`User Guide<Image Scaling>`.

    Parameters
    ----------
    self : ee.Image [this]
        Image to scale.

    Returns
    -------
    ee.Image
        Scaled image.

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> S2 = ee.ImageCollection('COPERNICUS/S2_SR').first().scale()
    """
    warnings.warn(
        "scale() will be deprecated in future versions, please use scaleAndOffset() instead",
        PendingDeprecationWarning,
    )

    return _scale_STAC(self)


@_extend_eeImage()
def getScaleParams(self):
    """Gets the scale parameters for each band of the image.

    Parameters
    ----------
    self : ee.Image (this)
        Image to get the scale parameters from.

    Returns
    -------
    dict
        Dictionary with the scale parameters for each band.

    See Also
    --------
    getOffsetParams : Gets the offset parameters for each band of the image.
    scaleAndOffset : Scales bands on an image according to their scale and offset parameters.

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> ee.ImageCollection('MODIS/006/MOD11A2').first().getScaleParams()
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
    return _get_scale_params(self)


@_extend_eeImage()
def getOffsetParams(self):
    """Gets the offset parameters for each band of the image.

    Parameters
    ----------
    self : ee.Image (this)
        Image to get the offset parameters from.

    Returns
    -------
    dict
        Dictionary with the offset parameters for each band.

    See Also
    --------
    getScaleParams : Gets the scale parameters for each band of the image.
    scaleAndOffset : Scales bands on an image according to their scale and offset parameters.

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> ee.ImageCollection('MODIS/006/MOD11A2').first().getOffsetParams()
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
    return _get_offset_params(self)


@_extend_eeImage()
def scaleAndOffset(self):
    """Scales bands on an image according to their scale and offset parameters.

    Tip
    ----------
    Check more info about the supported platforms and image scaling the :ref:`User Guide<Image Scaling>`.

    Parameters
    ----------
    self : ee.Image [this]
        Image to scale.

    Returns
    -------
    ee.Image
        Scaled image.
        
    See Also
    --------
    getScaleParams : Gets the scale parameters for each band of the image.
    getOffsetParams : Gets the offset parameters for each band of the image.

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> S2 = ee.ImageCollection('COPERNICUS/S2_SR').first().scaleAndOffset()
    """
    return _scale_STAC(self)


@_extend_eeImage()
def preprocess(self,**kwargs):
    """Pre-processes the image: masks clouds and shadows, and scales and offsets the image. 

    Tip
    ----------
    Check more info here about the supported platforms, :ref:`Image Scaling<Image Scaling>` and :ref:`Masking Clouds and Shadows<Masking Clouds and Shadows>`.

    Parameters
    ----------
    self : ee.Image [this]
        Image to pre-process.
    **kwargs :
        Keywords arguments for maskClouds().

    Returns
    -------
    ee.Image
        Pre-processed image.
        
    See Also
    --------
    getScaleParams : Gets the scale parameters for each band of the image.
    getOffsetParams : Gets the offset parameters for each band of the image.
    scaleAndOffset : Scales bands on an image according to their scale and offset parameters.
    maskClouds : Masks clouds and shadows in an image.
        
    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> S2 = ee.ImageCollection('COPERNICUS/S2_SR').first().preprocess()
    """ 
    return _preprocess(self,**kwargs)
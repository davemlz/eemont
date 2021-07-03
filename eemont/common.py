import ee
import json
import pkg_resources
import os
import warnings
import requests
from box import Box
from geopy.geocoders import get_geocoder_for_service
import re
import copy

warnings.simplefilter("always", UserWarning)

# STAC
# --------------------------


def _get_platform_STAC(args):
    """Gets the platform (satellite) of an image (or image collection) and wheter if it is a Surface Reflectance product.

    Parameters
    ----------
    args : ee.Image | ee.ImageCollection
        Image or image collection to get the platform from.

    Returns
    -------
    dict
        Platform and product of the image (or image collection).
    """
    eemontDir = os.path.dirname(pkg_resources.resource_filename("eemont", "eemont.py"))
    dataPath = os.path.join(eemontDir, "data/ee-catalog-ids.json")

    f = open(dataPath)
    eeDict = json.load(f)
    platforms = list(eeDict.keys())

    ID = args.get("system:id").getInfo()

    plt = None

    for platform in platforms:

        if eeDict[platform]["gee:type"] == "image_collection" and isinstance(
            args, ee.image.Image
        ):
            pltID = "/".join(ID.split("/")[:-1])
        elif eeDict[platform]["gee:type"] == "image" and isinstance(
            args, ee.imagecollection.ImageCollection
        ):
            pass
        else:
            pltID = ID

        if platform == pltID:
            plt = pltID

        if "_SR" in pltID:
            platformDict = {"platform": plt, "sr": True}
        else:
            platformDict = {"platform": plt, "sr": False}

    if plt is None:
        raise Exception("Sorry, satellite platform not supported!")

    return platformDict


def _getSTAC(args):
    """Gets the STAC of the specified platform.

    Parameters
    ----------
    args : ee.Image | ee.ImageCollection
        Image or image collection to get the STAC from.

    Returns
    -------
    dict
        STAC of the ee.Image or ee.ImageCollection dataset.
    """
    platformDict = _get_platform_STAC(args)

    eemontDir = os.path.dirname(pkg_resources.resource_filename("eemont", "eemont.py"))
    dataPath = os.path.join(eemontDir, "data/ee-catalog-ids.json")

    f = open(dataPath)
    eeDict = json.load(f)

    STAC = requests.get(eeDict[platformDict["platform"]]["href"]).json()

    return STAC


# Spectral Indices
# --------------------------


def _get_expression_map(img, platformDict):
    """Gets the dictionary required for the map parameter in ee.Image.expression() method.

    Parameters
    ----------
    img : ee.Image
        Image to get the dictionary from.
    platformDict : dict
        Dictionary retrieved from the _get_platform() method.

    Returns
    -------
    dict
        Map dictionary for ee.Image.expression.
    """

    def lookupS2(img):
        return {
            "A": img.select("B1"),
            "B": img.select("B2"),
            "G": img.select("B3"),
            "R": img.select("B4"),
            "RE1": img.select("B5"),
            "RE2": img.select("B6"),
            "RE3": img.select("B7"),
            "N": img.select("B8"),
            "RE4": img.select("B8A"),
            "WV": img.select("B9"),
            "S1": img.select("B11"),
            "S2": img.select("B12"),
        }

    def lookupL8(img):
        return {
            "A": img.select("B1"),
            "B": img.select("B2"),
            "G": img.select("B3"),
            "R": img.select("B4"),
            "N": img.select("B5"),
            "S1": img.select("B6"),
            "S2": img.select("B7"),
            "T1": img.select("B10"),
            "T2": img.select("B11"),
        }
    
    def lookupL8C2(img):
        return {
            "A": img.select("SR_B1"),
            "B": img.select("SR_B2"),
            "G": img.select("SR_B3"),
            "R": img.select("SR_B4"),
            "N": img.select("SR_B5"),
            "S1": img.select("SR_B6"),
            "S2": img.select("SR_B7"),
            "T1": img.select("SR_B10"),
            "T2": img.select("SR_B11"),
        }

    def lookupL457(img):
        return {
            "B": img.select("B1"),
            "G": img.select("B2"),
            "R": img.select("B3"),
            "N": img.select("B4"),
            "S1": img.select("B5"),
            "T1": img.select("B6"),
            "S2": img.select("B7"),
        }
    
    def lookupL7C2(img):
        return {
            "B": img.select("SR_B1"),
            "G": img.select("SR_B2"),
            "R": img.select("SR_B3"),
            "N": img.select("SR_B4"),
            "S1": img.select("SR_B5"),
            "T1": img.select("SR_B6"),
            "S2": img.select("SR_B7"),
        }

    def lookupMOD09GQ(img):
        return {"R": img.select("sur_refl_b01"), "N": img.select("sur_refl_b02")}

    def lookupMOD09GA(img):
        return {
            "B": img.select("sur_refl_b03"),
            "G": img.select("sur_refl_b04"),
            "R": img.select("sur_refl_b01"),
            "N": img.select("sur_refl_b02"),
            "S1": img.select("sur_refl_b06"),
            "S2": img.select("sur_refl_b07"),
        }

    def lookupMCD43A4(img):
        return {
            "B": img.select("Nadir_Reflectance_Band3"),
            "G": img.select("Nadir_Reflectance_Band4"),
            "R": img.select("Nadir_Reflectance_Band1"),
            "N": img.select("Nadir_Reflectance_Band2"),
            "S1": img.select("Nadir_Reflectance_Band6"),
            "S2": img.select("Nadir_Reflectance_Band7"),
        }

    lookupPlatform = {
        "COPERNICUS/S2": lookupS2,
        "COPERNICUS/S2_SR": lookupS2,
        "LANDSAT/LC08/C01/T1_SR": lookupL8,
        "LANDSAT/LC08/C01/T2_SR": lookupL8,
        "LANDSAT/LC08/C02/T1_L2": lookupL8C2,
        "LANDSAT/LE07/C01/T1_SR": lookupL457,
        "LANDSAT/LE07/C01/T2_SR": lookupL457,
        "LANDSAT/LE07/C02/T1_L2": lookupL7C2,
        "LANDSAT/LT05/C01/T1_SR": lookupL457,
        "LANDSAT/LT05/C01/T2_SR": lookupL457,
        "LANDSAT/LT04/C01/T1_SR": lookupL457,
        "LANDSAT/LT04/C01/T2_SR": lookupL457,
        "MODIS/006/MOD09GQ": lookupMOD09GQ,
        "MODIS/006/MYD09GQ": lookupMOD09GQ,
        "MODIS/006/MOD09GA": lookupMOD09GA,
        "MODIS/006/MYD09GA": lookupMOD09GA,
        "MODIS/006/MOD09Q1": lookupMOD09GQ,
        "MODIS/006/MYD09Q1": lookupMOD09GQ,
        "MODIS/006/MOD09A1": lookupMOD09GA,
        "MODIS/006/MYD09A1": lookupMOD09GA,
        "MODIS/006/MCD43A4": lookupMCD43A4,
    }

    if platformDict["platform"] not in list(lookupPlatform.keys()):
        raise Exception(
            "Sorry, satellite platform not supported for index computation!"
        )

    return lookupPlatform[platformDict["platform"]](img)


def _get_indices(online):
    """Retrieves the dictionary of indices used for the index() method in ee.Image and ee.ImageCollection classes.

    Parameters
    ----------
    online : boolean
        Wheter to retrieve the most recent list of indices directly from the GitHub repository and not from the local copy.

    Returns
    -------
    dict
        Indices.
    """
    if online:
        indices = requests.get(
            "https://raw.githubusercontent.com/davemlz/awesome-ee-spectral-indices/main/output/spectral-indices-dict.json"
        ).json()
    else:
        eemontDir = os.path.dirname(
            pkg_resources.resource_filename("eemont", "eemont.py")
        )
        dataPath = os.path.join(eemontDir, "data/spectral-indices-dict.json")
        f = open(dataPath)
        indices = json.load(f)

    return indices["SpectralIndices"]


def _get_kernel_image(img, lookup, kernel, sigma, a, b):
    """Creates an ee.Image representing a kernel computed on bands [a] and [b].

    Parameters
    ----------
    img : ee.Image
        Image to compute the kernel on.
    lookup : dict
        Dictionary retrieved from _get_expression_map().
    kernel : str
        Kernel to use.
    sigma : str | float
        Length-scale parameter. Used for kernel = 'RBF'.
    a : str
        Key of the first band to use.
    b : str
        Key of the second band to use.

    Returns
    -------
    ee.Image
        Kernel image.
    """
    if a not in list(lookup.keys()) or b not in list(lookup.keys()):
        return None
    else:
        lookupab = {"a": lookup[a], "b": lookup[b]}
        if isinstance(sigma, str):
            lookup = {**lookup, **lookupab, "sigma": img.expression(sigma, lookupab)}
        else:
            lookup = {**lookup, **lookupab, "sigma": sigma}
        kernels = {
            "linear": "a * b",
            "RBF": "exp((-1.0 * (a - b) ** 2.0)/(2.0 * sigma ** 2.0))",
            "poly": "((a * b) + c) ** p",
        }
        return img.expression(kernels[kernel], lookup)


def _remove_none_dict(dictionary):
    """Removes elements from a dictionary with None values.

    Parameters
    ----------
    dictionary : dict

    Returns
    -------
    dict
        Curated dictionary.
    """
    newDictionary = dict(dictionary)
    for key in dictionary.keys():
        if dictionary[key] is None:
            del newDictionary[key]
    return newDictionary


def _get_kernel_parameters(img, lookup, kernel, sigma):
    """Gets the additional kernel parameters to compute kernel indices.

    Parameters
    ----------
    img : ee.Image
        Image to compute the kernel parameters on.
    lookup : dict
        Dictionary retrieved from _get_expression_map().
    kernel : str
        Kernel to use.
    sigma : str | float
        Length-scale parameter. Used for kernel = 'RBF'.

    Returns
    -------
    dict
        Kernel parameters.
    """
    kernelParameters = {
        "kNN": _get_kernel_image(img, lookup, kernel, sigma, "N", "N"),
        "kNR": _get_kernel_image(img, lookup, kernel, sigma, "N", "R"),
        "kNB": _get_kernel_image(img, lookup, kernel, sigma, "N", "B"),
        "kNL": _get_kernel_image(img, lookup, kernel, sigma, "N", "L"),
        "kGG": _get_kernel_image(img, lookup, kernel, sigma, "G", "G"),
        "kGR": _get_kernel_image(img, lookup, kernel, sigma, "G", "R"),
        "kGB": _get_kernel_image(img, lookup, kernel, sigma, "G", "B"),
        "kBB": _get_kernel_image(img, lookup, kernel, sigma, "B", "B"),
        "kBR": _get_kernel_image(img, lookup, kernel, sigma, "B", "R"),
        "kBL": _get_kernel_image(img, lookup, kernel, sigma, "B", "L"),
        "kRR": _get_kernel_image(img, lookup, kernel, sigma, "R", "R"),
        "kRB": _get_kernel_image(img, lookup, kernel, sigma, "R", "B"),
        "kRL": _get_kernel_image(img, lookup, kernel, sigma, "R", "L"),
        "kLL": _get_kernel_image(img, lookup, kernel, sigma, "L", "L"),
    }

    return kernelParameters


def _index(
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
    kernel,
    sigma,
    p,
    c,
    online,
):
    """Computes one or more spectral indices (indices are added as bands) for an image oir image collection.

    Parameters
    ----------
    self : ee.Image | ee.ImageCollection
        Image to compute indices on. Must be scaled to [0,1]. Check the supported platforms in User Guide > Spectral Indices > Supported Platforms.
    index : string | list[string]
        Index or list of indices to compute.
    G : float
        Gain factor. Used just for index = 'EVI'.
    C1 : float
        Coefficient 1 for the aerosol resistance term. Used just for index = 'EVI'.
    C2 : float
        Coefficient 2 for the aerosol resistance term. Used just for index = 'EVI'.
    L : float
        Canopy background adjustment. Used just for index = ['EVI','SAVI'].
    cexp : float
        Exponent used for OCVI.
    nexp : float
        Exponent used for GDVI.
    alpha : float
        Weighting coefficient  used for WDRVI.
    slope : float
        Soil line slope.
    intercept : float
        Soil line intercept.
    kernel : str
        Kernel used for kernel indices.
    sigma : str | float
        Length-scale parameter. Used for kernel = 'RBF'. If str, this must be an expression including 'a' and 'b'. If numeric, this must be positive.
    p : float
        Kernel degree. Used for kernel = 'poly'.
    c : float
        Free parameter that trades off the influence of higher-order versus lower-order terms. Used for kernel = 'poly'. This must be greater than or equal to 0.
    online : boolean
        Wheter to retrieve the most recent list of indices directly from the GitHub repository and not from the local copy.

    Returns
    -------
    ee.Image | ee.ImageCollection
        Image (or Image Collection) with the computed spectral index, or indices, as new bands.
    """
    platformDict = _get_platform_STAC(self)

    if isinstance(sigma, int) or isinstance(sigma, float):
        if sigma < 0:
            raise Exception("[sigma] must be positive!")

    if p <= 0 or c < 0:
        raise Exception("[p] and [c] must be positive!")

    additionalParameters = {
        "g": float(G),
        "C1": float(C1),
        "C2": float(C2),
        "L": float(L),
        "cexp": float(cexp),
        "nexp": float(nexp),
        "alpha": float(alpha),
        "sla": float(slope),
        "slb": float(intercept),
        "p": float(p),
        "c": float(c),
    }

    spectralIndices = _get_indices(online)
    indicesNames = list(spectralIndices.keys())

    if not isinstance(index, list):
        if index == "all":
            index = list(spectralIndices.keys())
        elif index in [
            "vegetation",
            "burn",
            "water",
            "snow",
            "drought",
            "urban",
            "kernel",
        ]:
            temporalListOfIndices = []
            for idx in indicesNames:
                if spectralIndices[idx]["type"] == index:
                    temporalListOfIndices.append(idx)
            index = temporalListOfIndices
        else:
            index = [index]

    for idx in index:
        if idx not in list(spectralIndices.keys()):
            warnings.warn(
                "Index " + idx + " is not a built-in index and it won't be computed!"
            )
        else:

            def temporalIndex(img):
                lookupDic = _get_expression_map(img, platformDict)
                lookupDic = {**lookupDic, **additionalParameters}
                kernelParameters = _get_kernel_parameters(img, lookupDic, kernel, sigma)
                lookupDic = {**lookupDic, **kernelParameters}
                lookupDicCurated = _remove_none_dict(lookupDic)
                if all(
                    band in list(lookupDicCurated.keys())
                    for band in spectralIndices[idx]["bands"]
                ):
                    return img.addBands(
                        img.expression(
                            spectralIndices[idx]["formula"], lookupDicCurated
                        ).rename(idx)
                    )
                else:
                    warnings.warn(
                        "This platform doesn't have the required bands for "
                        + idx
                        + " computation!"
                    )
                    return img

            if isinstance(self, ee.imagecollection.ImageCollection):
                self = self.map(temporalIndex)
            elif isinstance(self, ee.image.Image):
                self = temporalIndex(self)

    return self


def indices(online=False):
    """Gets the dictionary of available indices as a Box object.

    Parameters
    ----------
    online : boolean
        Wheter to retrieve the most recent list of indices directly from the GitHub repository and not from the local copy.

    Returns
    -------
    Box
        Dictionary of available indices. For each index, the keys 'short_name', 'long_name', 'formula', 'bands', 'reference', 'type', 'date_of_addition' and 'contributor' can be checked.

    See Also
    --------
    listIndices : Gets the list of available indices.

    Examples
    --------
    >>> import eemont
    >>> indices = eemont.indices()
    >>> indices.BAIS2.long_name
    'Burned Area Index for Sentinel 2'
    >>> indices.BAIS2.formula
    '(1.0 - ((RE2 * RE3 * RE4) / R) ** 0.5) * (((S2 - RE4)/(S2 + RE4) ** 0.5) + 1.0)'
    >>> indices.BAIS2.reference
    'https://doi.org/10.3390/ecrs-2-05177'
    """
    return Box(_get_indices(online), frozen_box=True)


def listIndices(online=False):
    """Gets the list of available indices.

    Parameters
    ----------
    online : boolean
        Wheter to retrieve the most recent list of indices directly from the GitHub repository and not from the local copy.

    Returns
    -------
    list
        List of available indices.

    See Also
    --------
    indices : Gets the dictionary of available indices as a Box object.

    Examples
    --------
    >>> import eemont
    >>> eemont.listIndices()
    ['BNDVI','CIG','CVI','EVI','EVI2','GBNDVI','GNDVI',...]
    """
    return list(_get_indices(online).keys())


# Image Scaling
# --------------------------


def _get_scale_params(args):
    """Gets the scale parameters for each band of the image or image collection.

    Parameters
    ----------
    args : ee.Image | ee.ImageCollection
        Image or image collection to get the scale parameters from.

    Returns
    -------
    dict
        Dictionary with the scale parameters for each band.
    """
    platformDict = _get_platform_STAC(args)

    eemontDir = os.path.dirname(pkg_resources.resource_filename("eemont", "eemont.py"))
    dataPath = os.path.join(eemontDir, "data/ee-catalog-scale.json")

    f = open(dataPath)
    eeDict = json.load(f)
    platforms = list(eeDict.keys())

    if platformDict["platform"] not in platforms:
        warnings.warn("This platform is not supported for getting scale parameters.")
        return None
    else:
        return eeDict[platformDict["platform"]]


def _get_offset_params(args):
    """Gets the offset parameters for each band of the image or image collection.

    Parameters
    ----------
    args : ee.Image | ee.ImageCollection
        Image or image collection to get the offset parameters from.

    Returns
    -------
    dict
        Dictionary with the offset parameters for each band.
    """
    platformDict = _get_platform_STAC(args)

    eemontDir = os.path.dirname(pkg_resources.resource_filename("eemont", "eemont.py"))
    dataPath = os.path.join(eemontDir, "data/ee-catalog-offset.json")

    f = open(dataPath)
    eeDict = json.load(f)
    platforms = list(eeDict.keys())

    if platformDict["platform"] not in platforms:
        warnings.warn("This platform is not supported for getting offset parameters.")
        return None
    else:
        return eeDict[platformDict["platform"]]


def _scale_STAC(self):
    """Scales bands on an image or image collection.

    Parameters
    ----------
    self : ee.Image | ee.ImageCollection
        Image or iage collection to scale.

    Returns
    -------
    ee.Image | ee.ImageCollection
        Scaled image or image collection.
    """
    scaleParams = _get_scale_params(self)
    offsetParams = _get_offset_params(self)

    if scaleParams is None or offsetParams is None:
        warnings.warn("This platform is not supported for scaling and offsetting.")
        return self
    else:
        scaleParams = ee.Dictionary(scaleParams).toImage()
        offsetParams = ee.Dictionary(offsetParams).toImage()

        def scaleOffset(img):
            bands = img.bandNames()
            scaleList = scaleParams.bandNames()
            bands = bands.filter(ee.Filter.inList("item", scaleList))
            SOscaleParams = scaleParams.select(bands)
            SOoffsetParams = offsetParams.select(bands)
            scaled = img.select(bands).multiply(SOscaleParams).add(SOoffsetParams)
            return ee.Image(scaled.copyProperties(img, img.propertyNames()))

        if isinstance(self, ee.image.Image):
            scaled = scaleOffset(self)
        elif isinstance(self, ee.imagecollection.ImageCollection):
            scaled = self.map(scaleOffset)

        return scaled


# Cloud Masking
# --------------------------


def _maskClouds(
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
):
    """Masks clouds and shadows in an image or image collection (valid just for Surface Reflectance products).

    Parameters
    ----------
    self : ee.Image | ee.ImageCollection
        Image or image collection to mask.
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
    ee.Image | ee.ImageCollection
        Cloud-shadow masked image or image collection.
    """

    def S3(args):
        qa = args.select("quality_flags")
        notCloud = qa.bitwiseAnd(1 << 27).eq(0)
        return args.updateMask(notCloud)

    def S2(args):
        def cloud_prob(img):
            clouds = ee.Image(img.get("cloud_mask")).select("probability")
            isCloud = clouds.gte(prob).rename("CLOUD_MASK")
            return img.addBands(isCloud)

        def QA(img):
            qa = img.select("QA60")
            cloudBitMask = 1 << 10
            isCloud = qa.bitwiseAnd(cloudBitMask).eq(0)
            if maskCirrus:
                cirrusBitMask = 1 << 11
                isCloud = isCloud.And(qa.bitwiseAnd(cirrusBitMask).eq(0))
            isCloud = isCloud.Not().rename("CLOUD_MASK")
            return img.addBands(isCloud)

        def CDI(img):
            idx = img.get("system:index")
            S2TOA = (
                ee.ImageCollection("COPERNICUS/S2")
                .filter(ee.Filter.eq("system:index", idx))
                .first()
            )
            CloudDisplacementIndex = ee.Algorithms.Sentinel2.CDI(S2TOA)
            isCloud = CloudDisplacementIndex.lt(cdi).rename("CLOUD_MASK_CDI")
            return img.addBands(isCloud)

        def get_shadows(img):
            notWater = img.select("SCL").neq(6)
            if not scaledImage:
                darkPixels = img.select("B8").lt(dark * 1e4).multiply(notWater)
            else:
                darkPixels = img.select("B8").lt(dark).multiply(notWater)
            shadowAzimuth = ee.Number(90).subtract(
                ee.Number(img.get("MEAN_SOLAR_AZIMUTH_ANGLE"))
            )
            cloudProjection = img.select("CLOUD_MASK").directionalDistanceTransform(
                shadowAzimuth, cloudDist / 10
            )
            cloudProjection = (
                cloudProjection.reproject(crs=img.select(0).projection(), scale=10)
                .select("distance")
                .mask()
            )
            isShadow = cloudProjection.multiply(darkPixels).rename("SHADOW_MASK")
            return img.addBands(isShadow)

        def clean_dilate(img):
            isCloudShadow = img.select("CLOUD_MASK")
            if cdi != None:
                isCloudShadow = isCloudShadow.And(img.select("CLOUD_MASK_CDI"))
            if maskShadows:
                isCloudShadow = isCloudShadow.add(img.select("SHADOW_MASK")).gt(0)
            isCloudShadow = (
                isCloudShadow.focal_min(20, units="meters")
                .focal_max(buffer * 2 / 10, units="meters")
                .rename("CLOUD_SHADOW_MASK")
            )
            return img.addBands(isCloudShadow)

        def apply_mask(img):
            return img.updateMask(img.select("CLOUD_SHADOW_MASK").Not())

        if isinstance(self, ee.image.Image):
            if method == "cloud_prob":
                S2Clouds = ee.ImageCollection("COPERNICUS/S2_CLOUD_PROBABILITY")
                fil = ee.Filter.equals(
                    leftField="system:index", rightField="system:index"
                )
                S2WithCloudMask = ee.Join.saveFirst("cloud_mask").apply(
                    ee.ImageCollection(args), S2Clouds, fil
                )
                S2Masked = ee.ImageCollection(S2WithCloudMask).map(cloud_prob).first()
            elif method == "qa":
                S2Masked = QA(args)
            if cdi != None:
                S2Masked = CDI(S2Masked)
            if maskShadows:
                S2Masked = get_shadows(S2Masked)
            S2Masked = apply_mask(clean_dilate(S2Masked))
        elif isinstance(self, ee.imagecollection.ImageCollection):
            if method == "cloud_prob":
                S2Clouds = ee.ImageCollection("COPERNICUS/S2_CLOUD_PROBABILITY")
                fil = ee.Filter.equals(
                    leftField="system:index", rightField="system:index"
                )
                S2WithCloudMask = ee.Join.saveFirst("cloud_mask").apply(
                    args, S2Clouds, fil
                )
                S2Masked = ee.ImageCollection(S2WithCloudMask).map(cloud_prob)
            elif method == "qa":
                S2Masked = args.map(QA)
            if cdi != None:
                S2Masked = S2Masked.map(CDI)
            if maskShadows:
                S2Masked = S2Masked.map(get_shadows)
            S2Masked = S2Masked.map(clean_dilate).map(apply_mask)

        return S2Masked

    def L8(args):
        cloudsBitMask = 1 << 5
        qa = args.select("pixel_qa")
        mask = qa.bitwiseAnd(cloudsBitMask).eq(0)
        if maskShadows:
            cloudShadowBitMask = 1 << 3
            mask = mask.And(qa.bitwiseAnd(cloudShadowBitMask).eq(0))
        return args.updateMask(mask)
    
    def L8C2(args):
        qa = args.select("QA_PIXEL")
        notCloud = qa.bitwiseAnd(1 << 3).eq(0)
        if maskShadows:
            notCloud = notCloud.And(qa.bitwiseAnd(1 << 4).eq(0))
        if maskCirrus:
            notCloud = notCloud.And(qa.bitwiseAnd(1 << 2).eq(0))
        return args.updateMask(notCloud)

    def L457(args):
        qa = args.select("pixel_qa")
        cloud = qa.bitwiseAnd(1 << 5).And(qa.bitwiseAnd(1 << 7))
        if maskShadows:
            cloud = cloud.Or(qa.bitwiseAnd(1 << 3))
        mask2 = args.mask().reduce(ee.Reducer.min())
        return args.updateMask(cloud.Not()).updateMask(mask2)
    
    def L7C2(args):
        qa = args.select("QA_PIXEL")
        notCloud = qa.bitwiseAnd(1 << 3).eq(0)
        if maskShadows:
            notCloud = notCloud.And(qa.bitwiseAnd(1 << 4).eq(0))
        return args.updateMask(notCloud)

    def MOD09GA(args):
        qa = args.select("state_1km")
        notCloud = qa.bitwiseAnd(1 << 0).eq(0)
        if maskShadows:
            notCloud = notCloud.And(qa.bitwiseAnd(1 << 2).eq(0))
        if maskCirrus:
            notCloud = notCloud.And(qa.bitwiseAnd(1 << 8).eq(0))
        return args.updateMask(notCloud)

    def MCD15A3H(args):
        qa = args.select("FparExtra_QC")
        notCloud = qa.bitwiseAnd(1 << 5).eq(0)
        if maskShadows:
            notCloud = notCloud.And(qa.bitwiseAnd(1 << 6).eq(0))
        if maskCirrus:
            notCloud = notCloud.And(qa.bitwiseAnd(1 << 4).eq(0))
        return args.updateMask(notCloud)

    def MOD09Q1(args):
        qa = args.select("State")
        notCloud = qa.bitwiseAnd(1 << 0).eq(0)
        if maskShadows:
            notCloud = notCloud.And(qa.bitwiseAnd(1 << 2).eq(0))
        if maskCirrus:
            notCloud = notCloud.And(qa.bitwiseAnd(1 << 8).eq(0))
        return args.updateMask(notCloud)

    def MOD09A1(args):
        qa = args.select("StateQA")
        notCloud = qa.bitwiseAnd(1 << 0).eq(0)
        if maskShadows:
            notCloud = notCloud.And(qa.bitwiseAnd(1 << 2).eq(0))
        if maskCirrus:
            notCloud = notCloud.And(qa.bitwiseAnd(1 << 8).eq(0))
        return args.updateMask(notCloud)

    def MOD17A2H(args):
        qa = args.select("Psn_QC")
        notCloud = qa.bitwiseAnd(1 << 3).eq(0)
        return args.updateMask(notCloud)

    def MOD16A2(args):
        qa = args.select("ET_QC")
        notCloud = qa.bitwiseAnd(1 << 3).eq(0)
        return args.updateMask(notCloud)

    def MOD13Q1A1(args):
        qa = args.select("SummaryQA")
        notCloud = qa.bitwiseAnd(1 << 0).eq(0)
        return args.updateMask(notCloud)

    def MOD13A2(args):
        qa = args.select("SummaryQA")
        notCloud = qa.eq(0)
        return args.updateMask(notCloud)

    def VNP09GA(args):
        qf1 = args.select("QF1")
        qf2 = args.select("QF2")
        notCloud = qf1.bitwiseAnd(1 << 2).eq(0)
        if maskShadows:
            notCloud = notCloud.And(qf2.bitwiseAnd(1 << 3).eq(0))
        if maskCirrus:
            notCloud = notCloud.And(qf2.bitwiseAnd(1 << 6).eq(0))
            notCloud = notCloud.And(qf2.bitwiseAnd(1 << 7).eq(0))
        return args.updateMask(notCloud)

    def VNP13A1(args):
        qa = args.select("pixel_reliability")
        notCloud = qa.neq(9)
        if maskShadows:
            notCloud = notCloud.And(qa.neq(7))
        return args.updateMask(notCloud)

    lookup = {
        "COPERNICUS/S3/OLCI": S3,
        "COPERNICUS/S2_SR": S2,
        "LANDSAT/LC08/C01/T1_SR": L8,
        "LANDSAT/LC08/C01/T2_SR": L8,
        "LANDSAT/LC08/C02/T1_L2": L8C2,
        "LANDSAT/LE07/C01/T1_SR": L457,
        "LANDSAT/LE07/C01/T2_SR": L457,
        "LANDSAT/LE07/C02/T1_L2": L7C2,
        "LANDSAT/LT05/C01/T1_SR": L457,
        "LANDSAT/LT05/C01/T2_SR": L457,
        "LANDSAT/LT04/C01/T1_SR": L457,
        "LANDSAT/LT04/C01/T2_SR": L457,
        "MODIS/006/MOD09GA": MOD09GA,
        "MODIS/006/MCD15A3H": MCD15A3H,
        "MODIS/006/MOD09Q1": MOD09Q1,
        "MODIS/006/MOD09A1": MOD09A1,
        "MODIS/006/MOD17A2H": MOD17A2H,
        "MODIS/006/MOD16A2": MOD16A2,
        "MODIS/006/MOD13Q1": MOD13Q1A1,
        "MODIS/006/MOD13A1": MOD13Q1A1,
        "MODIS/006/MOD13A2": MOD13A2,
        "MODIS/006/MYD09GA": MOD09GA,
        "MODIS/006/MYD09Q1": MOD09Q1,
        "MODIS/006/MYD09A1": MOD09A1,
        "MODIS/006/MYD17A2H": MOD17A2H,
        "MODIS/006/MYD16A2": MOD16A2,
        "MODIS/006/MYD13Q1": MOD13Q1A1,
        "MODIS/006/MYD13A1": MOD13Q1A1,
        "MODIS/006/MYD13A2": MOD13A2,
        "NOAA/VIIRS/001/VNP09GA": VNP09GA,
        "NOAA/VIIRS/001/VNP13A1": VNP13A1,
    }

    platformDict = _get_platform_STAC(self)

    if platformDict["platform"] not in list(lookup.keys()):
        warnings.warn("This platform is not supported for cloud masking.")
        return self
    else:
        if isinstance(self, ee.image.Image):
            masked = lookup[platformDict["platform"]](self)
        elif isinstance(self, ee.imagecollection.ImageCollection):
            if platformDict["platform"] == "COPERNICUS/S2_SR":
                masked = lookup[platformDict["platform"]](self)
            else:
                masked = self.map(lookup[platformDict["platform"]])
        return masked


# Preprocessing
# --------------------------


def _preprocess(self, **kwargs):
    """Pre-process the image, or image collection: masks clouds and shadows, and scales and offsets the image, or image collection.

    Parameters
    ----------
    self : ee.Image | ee.ImageCollection
        Image or Image Collection to pre-process.
    **kwargs :
        Keywords arguments for maskClouds().

    Returns
    -------
    ee.Image | ee.ImageCollection
        Pre-processed image or image collection.
    """
    maskCloudsDefault = {
        "method": "cloud_prob",
        "prob": 60,
        "maskCirrus": True,
        "maskShadows": True,
        "scaledImage": False,
        "dark": 0.15,
        "cloudDist": 1000,
        "buffer": 250,
        "cdi": None,
    }

    for key, value in maskCloudsDefault.items():
        if key not in kwargs.keys():
            kwargs[key] = value

    self = _maskClouds(self, **kwargs)
    self = _scale_STAC(self)

    return self


# Citation Tools
# --------------------------


def _getDOI(args):
    """Gets the DOI of the specified platform, if available.

    Parameters
    ----------
    args : ee.Image | ee.ImageCollection
        Image or image collection to get the DOI from.

    Returns
    -------
    str
        DOI of the ee.Image or ee.ImageCollection dataset.
    """
    platformDict = _get_platform_STAC(args)

    eemontDir = os.path.dirname(pkg_resources.resource_filename("eemont", "eemont.py"))
    dataPath = os.path.join(eemontDir, "data/ee-catalog-ids.json")

    f = open(dataPath)
    eeDict = json.load(f)

    return eeDict[platformDict["platform"]]["sci:doi"]


def _getCitation(args):
    """Gets the citation of the specified platform, if available.

    Parameters
    ----------
    args : ee.Image | ee.ImageCollection
        Image or image collection to get the citation from.

    Returns
    -------
    str
        Citation of the ee.Image or ee.ImageCollection dataset.
    """
    platformDict = _get_platform_STAC(args)

    eemontDir = os.path.dirname(pkg_resources.resource_filename("eemont", "eemont.py"))
    dataPath = os.path.join(eemontDir, "data/ee-catalog-ids.json")

    f = open(dataPath)
    eeDict = json.load(f)

    return eeDict[platformDict["platform"]]["sci:citation"]


# Geocoding
# --------------------------


def _retrieve_location(query, geocoder, exactly_one, **kwargs):
    """Retrieves a location from a query.

    Parameters
    ----------
    query : str
        Address, query or structured query to geocode.
    geocoder : str
        Geocoder to use. Please visit https://geopy.readthedocs.io/ for more info.
    exactly_one : boolean
        Whether to retrieve just one location.
    **kwargs :
        Keywords arguments for geolocator.geocode(). The user_agent argument is mandatory (this argument can be set as user_agent = 'my-gee-username' or
        user_agent = 'my-gee-app-name'). Please visit https://geopy.readthedocs.io/ for more info.

    Returns
    -------
    Location
        Retrieved location.
    """
    cls = get_geocoder_for_service(geocoder)
    geolocator = cls(**kwargs)
    location = geolocator.geocode(query, exactly_one=exactly_one)
    if location is None:
        raise Exception("No matches were found for your query!")
    else:
        return location


def _lnglat_from_location(location):
    """Returns the longitude and latitude from a location.

    Parameters
    ----------
    location : Location
        Retrieved location. Must be only one location.

    Returns
    -------
    tuple
        The longitude and latitude geocoded from the query.
    """
    return [location.longitude, location.latitude]


# Plus Codes
# --------------------------


def _load_openlocationcode():
    """Attempt to load the openlocationcode.openlocationcode module and return it.

    Because the package is not available through conda-forge, it cannot be made an installation dependency of eemont, so it is only loaded if needed.

    Returns
    -------
    module
        The openlocationcode.openlocationcode module.
    """
    try:
        from openlocationcode import openlocationcode

        return openlocationcode
    except ImportError:
        raise ImportError(
            'openlocationcode could not be loaded. Try installing with "pip install openlocationcode".'
        )


def _convert_lnglat_to_pluscode(lng, lat, code_length):
    """Take a single longitude and latitude coordinate and convert it to a Plus Code.

    Parameters
    ----------
    lng : float
        Longitude.
    lat : float
        Latitude.
    code_length : int
        The number of significant digits in the output code, between 2 and 15. Shorter codes are less precise.

    Returns
    -------
    str
        The Plus Code represented by the coordinate
    """
    olc = _load_openlocationcode()

    return olc.encode(lat, lng, code_length)


def _convert_pluscode_to_lnglat(pluscode, geocoder, **kwargs):
    """Take a single full or shortened Plus Code and convert it to a longitude and latitude.

    Parameters
    ----------
    pluscode : str
        Either a full Plus Code or short Plus Code with a queryable reference location appended to it.
    geocoder : str
        Geocoder to use. Please visit https://geopy.readthedocs.io/ for more info.
    **kwargs :
        Keywords arguments for geolocator.geocode(). The user_agent argument is mandatory (this argument can be set as user_agent = 'my-gee-username' or
        user_agent = 'my-gee-app-name'). Please visit https://geopy.readthedocs.io/ for more info.

    Returns
    -------
    tuple
        The longitude and latitude of the Plus Code centroid.
    """
    olc = _load_openlocationcode()

    if not olc.isFull(pluscode):
        if olc.isShort(pluscode):
            raise ValueError(
                'Short Plus Codes must include a reference location (e.g. "QXGV+XH Denver, CO, USA").'
            )

        shortcode, reference = _parse_code_and_reference_from_pluscode(pluscode)
        location = _retrieve_location(reference, geocoder, exactly_one=True, **kwargs)
        ref_lng, ref_lat = _lnglat_from_location(location)

        pluscode = olc.recoverNearest(shortcode, ref_lat, ref_lng)

    area = olc.decode(pluscode)
    return [area.longitudeCenter, area.latitudeCenter]


def _parse_code_and_reference_from_pluscode(pluscode):
    """Split a short Plus Code into a Plus Code and reference using regex. For example, "QXGV+XH Denver, CO, USA" will
    return ("QXGV+XH", "Denver, CO, USA").

    Parameters
    ----------
    pluscode : str
        A short Plus Code with a queryable reference location appended to it, delimited by whitespace.

    Returns
    -------
    tuple
        The short Plus Code and the reference.
    """
    pattern = r"\w{1,8}\+\w{,7}"
    code = None

    for chunk in pluscode.split(" "):
        match = re.search(pattern, chunk)
        code = match.group(0) if match else code

    if not code:
        raise ValueError("Plus code could not be decoded.")

    reference = pluscode.replace(code, "")

    return (code, reference)


def _is_coordinate_like(x):
    """Test if an object appears to be a longitude, latitude coordinate.

    This doesn't test if the coordinate is valid, only that it has the correct data structure: an iterable containing two
    numbers.

    Parameters
    ----------
    x : Object
        Any object that will be tested for coordinate-like structure.

    Returns
    -------
    bool
        True if the input object resembles a longitude, latitude coordinate.
    """
    if not isinstance(x, (list, tuple)) or len(x) != 2:
        return False
    for element in x:
        if not isinstance(element, (int, float)):
            return False

    return True


def _convert_lnglats_to_pluscodes(arr, code_length):
    """Take an arbitrarily nested array and recursively replace any element that looks like a coordinate with an equivalent
    Plus Code. Raise a ValueError if any non-coordinate elements are found.

    Parameters
    ----------
    arr : iterable
        An arbitrarily nested array containing tuples of longitude, latitude coordinates.
    code_length : int
        The number of significant digits in the output code, between 2 and 15. Shorter codes are less precise.

    Returns
    -------
    iterable
        An array matching the structure of the input array, with coordinate tuples replaced with Plus Code strings.
    """
    converted = copy.deepcopy(arr)

    if not isinstance(arr, (list, tuple)):
        raise ValueError(
            "{} is not a coordinate or iterable of coordinates.".format(arr)
        )

    if _is_coordinate_like(arr):
        converted = _convert_lnglat_to_pluscode(arr[0], arr[1], code_length)
    else:
        for i, element in enumerate(arr):
            converted[i] = _convert_lnglats_to_pluscodes(element, code_length)
    return converted


def _convert_pluscodes_to_lnglats(arr, geocoder, **kwargs):
    """Take an arbitrarily nested array and recursively replace any element that looks like a Plus Code with an equivalent
    longitude, latitude tuple. Raise a ValueError if any non-Plus Code elements are found.

    Parameters
    ----------
    arr : iterable
        An arbitrarily nested array containing Plus Code strings.
    geocoder : str
        Geocoder to use. Please visit https://geopy.readthedocs.io/ for more info.
    **kwargs :
        Keywords arguments for geolocator.geocode(). The user_agent argument is mandatory (this argument can be set as user_agent = 'my-gee-username' or
        user_agent = 'my-gee-app-name'). Please visit https://geopy.readthedocs.io/ for more info.

    Returns
    -------
    iterable
        An array matching the structure of the input array, with Plus Code strings replaced with coordinate tuples.
    """
    converted = copy.deepcopy(arr)

    if not isinstance(arr, (list, tuple, str)):
        raise ValueError("{} is not a Plus Code or iterable of Plus Codes.".format(arr))

    if isinstance(arr, str):
        converted = _convert_pluscode_to_lnglat(arr, geocoder, **kwargs)
    else:
        for i, element in enumerate(arr):
            converted[i] = _convert_pluscodes_to_lnglats(element, geocoder, **kwargs)
    return converted

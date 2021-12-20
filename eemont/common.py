import copy
import json
import os
import re
import warnings
from abc import ABC, abstractmethod

import ee
import ee_extra
import ee_extra.Spectral.core
import ee_extra.STAC.core
import ee_extra.STAC.utils
import pkg_resources
import requests
from box import Box
from ee_extra.STAC.utils import _get_platform_STAC
from geopy.geocoders import get_geocoder_for_service

from .extending import extend

warnings.simplefilter("always", UserWarning)


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
    return Box(ee_extra.Spectral.core.indices(online), frozen_box=True)


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
    return ee_extra.Spectral.core.listIndices(online)


@extend(ee)
def listDatasets():
    """Returns all datasets from the GEE STAC as a list.

    Returns
    -------
    list
        List of all datasets from the GEE STAC.

    Examples
    --------
    >>> import eemont
    >>> eemont.listDatasets()
    """
    return ee_extra.STAC.core.listDatasets()


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


# Histogram Matching
# --------------------------


def _matchHistogram(source_img, target_img, bands, geometry, maxBuckets):
    """Adjust the image's histogram to match a target image.

    Parameters
    ----------
    self : ee.Image [this]
        Image to adjust.
    target : ee.Image
        Image to match.
    bands : dict
        A dictionary of band names to match, with source bands as keys and target bands as values.
    geometry : ee.Geometry, default=None
        The region to match histograms in that overlaps both images. If none is provided, the geometry of the source image will be used.
    maxBuckets : int, default=256
        The maximum number of buckets to use when building histograms. Will be rounded to the nearest power of 2.

    Returns
    -------
    ee.Image
        The adjusted image containing the matched source bands.

    """

    def histogram_lookup(source_hist, target_hist):
        """Build a list of target values with corresponding counts to source values from a source and target histogram.

        Parameters
        ----------
        source_hist : ee.Array
            A histogram for a source image returned by ee.Reducer.autoHistogram
        target_hist : ee.Array
            A histogram for a target image returned by ee.Reducer.autoHistogram

        Returns
        -------
        tuple
            Source histogram values and target histogram values with corresponding counts.
        """
        source_vals = source_hist.slice(1, 0, 1).project([0])
        source_counts = source_hist.slice(1, 1, 2).project([0])
        source_counts = source_counts.divide(source_counts.get([-1]))

        target_vals = target_hist.slice(1, 0, 1).project([0])
        target_counts = target_hist.slice(1, 1, 2).project([0])
        target_counts = target_counts.divide(target_counts.get([-1]))

        def lookup_value(n):
            """Find the first target value with at least n counts."""
            index = target_counts.gte(n).argmax()
            return target_vals.get(index)

        target_lookup_vals = source_counts.toList().map(lookup_value)

        return (source_vals.toList(), target_lookup_vals)

    if not geometry:
        geometry = ee.Element.geometry(source_img)

    bands = ee.Dictionary(bands)
    source_bands = bands.keys()
    target_bands = bands.values()

    source_img = source_img.select(source_bands)
    target_img = target_img.select(target_bands)

    source_histogram = source_img.reduceRegion(
        reducer=ee.Reducer.autoHistogram(maxBuckets=maxBuckets, cumulative=True),
        geometry=geometry,
        scale=30,
        maxPixels=1e13,
        bestEffort=True,
    )

    target_histogram = target_img.updateMask(source_img.mask()).reduceRegion(
        reducer=ee.Reducer.autoHistogram(maxBuckets=maxBuckets, cumulative=True),
        geometry=geometry,
        scale=30,
        maxPixels=1e13,
        bestEffort=True,
    )

    def match_bands(source_band, target_band):
        """Match the histogram of one source band to a target band.

        Parameters
        ----------
        source_band : ee.String
            The name of a band in the source image to adjust.
        target_band : ee.String
            The name of a corresponding band in the target image to match to.

        Returns
        -------
        ee.Image
            The source band histogram-matched to the target band.
        """
        x, y = histogram_lookup(
            source_histogram.getArray(source_band),
            target_histogram.getArray(target_band),
        )
        matched = source_img.select([source_band]).interpolate(x, y)
        return matched

    matched = (
        ee.ImageCollection(bands.map(match_bands).values())
        .toBands()
        .rename(source_bands)
    )

    matched = ee.Image(matched.copyProperties(source_img, source_img.propertyNames()))
    matched = matched.set("eemont:HISTOGRAM_TARGET", target_img)

    return matched


def _filter_image_bands(img, keep_bands):
    """Remove Image bands that aren't in list of bands to keep. Essentially a version of ee.Image.select() that doesn't
    fail if bands are missing.

    Parameters
    ----------
    img : ee.Image
        An Image to select bands from.
    keep_bands : list
        A list of band names to keep in the Image. All other bands will be removed. Any specified bands that do not
        exist will be ignored.

    Returns
    -------
    ee.Image
        The image with specified bands selected.
    """
    bands = img.bandNames().filter(ee.Filter.inList("item", keep_bands))
    return img.select(bands)


def _panSharpen(source, method, qa, **kwargs):
    """Apply panchromatic sharpening to an Image or Image Collection. Optionally, run quality assessments between the
    original and sharpened Image(s) to measure spectral distortion and set results as properties of the sharpened
    Image(s).

    Parameters
    ----------
    source : ee.Image | ee.ImageCollection
        Image or Image Collection to sharpen.
    method : str, default="SFIM"
        The sharpening algorithm to apply. Current options are "SFIM" (Smoothing Filter-based Intensity Modulation),
        "HPFA" (High Pass Filter Addition), "PCS" (Principal Component Substitution), and "SM" (simple mean). Different
        sharpening methods will produce different quality sharpening results in different scenarios.
    qa : str | list, default=None
        One or more optional quality assessment names to apply after sharpening, e.g. "MSE", "RASE", "UIQI", etc.
    **kwargs :
        Keyword arguments passed to ee.Image.reduceRegion() such as "geometry", "maxPixels", "bestEffort", etc. These
        arguments are only used for PCS sharpening and quality assessments.

    Returns
    -------
    ee.Image | ee.ImageCollection
        The Image or ImageCollection with all sharpenable bands sharpened to the panchromatic resolution and quality
        assessments run and set as properties.
    """

    def get_platform(source):
        """Get the correct platform function for sharpening of supported platforms.

        Parameters
        ----------
        source : ee.Image | ee.ImageCollection
            An Image or ImageCollection identify a platform function for.

        Returns
        -------
        function
            A function that accepts Images and ImageCollections from the source platform.
        """
        platform_methods = {
            "LANDSAT/LC08/C01/T1_TOA": L8,
            "LANDSAT/LC08/C01/T1_RT_TOA": L8,
            "LANDSAT/LC08/C01/T2_TOA": L8,
            "LANDSAT/LC08/C01/T1_RT": L8,
            "LANDSAT/LO08/C01/T1": L8,
            "LANDSAT/LC08/C01/T1": L8,
            "LANDSAT/LO08/C01/T2": L8,
            "LANDSAT/LC08/C01/T2": L8,
            "LANDSAT/LE07/C01/T1_TOA": L7,
            "LANDSAT/LE07/C01/T1_RT_TOA": L7,
            "LANDSAT/LE07/C01/T2_TOA": L7,
            "LANDSAT/LE07/C01/T1_RT": L7,
            "LANDSAT/LE07/C01/T1": L7,
            "LANDSAT/LE07/C01/T2": L7,
        }

        platformDict = _get_platform_STAC(source)
        platforms = list(platform_methods.keys())
        platform = platformDict["platform"]

        if platform not in platforms:
            raise Exception(
                "Sharpening is not supported for the {} platform. Use one of the following platforms: {}".format(
                    platform, platforms
                )
            )

        return platform_methods[platform]

    def L7(source):
        """Apply panchromatic sharpening to an Image from a Landsat 7 platform by passing the sharpenable bands and
        panchromatic band to a sharpening function.

        Parameters
        ----------
        source : ee.Image
            Image to sharpen from Landsat 7.

        Returns
        -------
        ee.Image
            The Image with all sharpenable bands sharpened to the panchromatic resolution.
        """
        sharpenable_bands = ee.List(["B1", "B2", "B3", "B4", "B5", "B7"])
        sharpenable_img = _filter_image_bands(source, sharpenable_bands)
        pan_img = source.select("B8")

        return apply_sharpening(sharpenable_img, pan_img)

    def L8(source):
        """Apply panchromatic sharpening to an Image from a Landsat 8 platform by passing the sharpenable bands and
        panchromatic band to a sharpening function.

        Parameters
        ----------
        source : ee.Image
            Image to sharpen from Landsat 8.

        Returns
        -------
        ee.Image
            The Image with all sharpenable bands sharpened to the panchromatic resolution.
        """
        sharpenable_bands = ee.List(["B2", "B3", "B4", "B5", "B6", "B7"])
        sharpenable_img = _filter_image_bands(source, sharpenable_bands)
        pan_img = source.select("B8")

        return apply_sharpening(sharpenable_img, pan_img)

    def apply_sharpening(source, pan):
        """Identify and apply the correct sharpening algorithm to an Image.

        Parameters
        ----------
        source : ee.Image
            Image to sharpen with only sharpenable bands selected.
        pan : ee.Image | ee.ImageCollection
            Image with only the panchromatic band selected.

        Returns
        -------
        ee.Image
            The Image with all sharpenable bands sharpened to the panchromatic resolution.
        """
        sharpener = get_sharpener_by_name(method)
        sharpened = sharpener(source, pan)

        sharpened = ee.Image(sharpened.copyProperties(source, pan.propertyNames()))
        sharpened = sharpened.updateMask(source.mask())

        if qa:
            sharpened = run_and_set_qa(source, sharpened)

        return sharpened

    def get_all_sharpeners():
        """Get the name and class of all supported Sharpener subclasses.

        Returns
        -------
        requests.structures.CaseInsensitiveDict
            A dictionary of Sharpener subclasses with class names as keys and classes as values.
        """
        return requests.structures.CaseInsensitiveDict(
            {cls.__name__: cls for cls in Sharpener.__subclasses__()}
        )

    def get_sharpener_by_name(name):
        """Return a Sharpener subclass that matches a name.

        Parameters
        ----------
        name : str
            The name of a Sharpener, e.g. SFIM.

        Returns
        -------
        Sharpener
            The Sharpener subclass.
        """
        options = get_all_sharpeners()

        try:
            sharpener = options[name]
        except KeyError:
            raise AttributeError(
                '"{}" is not a supported sharpening method. Supported methods: {}'.format(
                    name, list(options.keys())
                )
            )
        return sharpener

    class Sharpener(ABC):
        """The abstract class that is implemented by all sharpening algorithms."""

        def __new__(cls, img, pan):
            """Apply pansharpening and return the sharpened image when the class is instantiated."""
            return cls.sharpen(img, pan)

        @abstractmethod
        def sharpen(img, pan):
            """Abstract method implemented by each Sharpener that applies sharpening."""
            pass

    class SFIM(Sharpener):
        """The Smoothing Filter-based Intensity Modulation (SFIM) sharpener."""

        @staticmethod
        def sharpen(img, pan):
            """Apply Smoothing Filter-based Intensity Modulation (SFIM) sharpening.

            Parameters
            ----------
            img : ee.Image
                Image to sharpen with only sharpenable bands selected.
            pan : ee.Image
                Image with only the panchromatic band selected.

            Returns
            -------
            ee.Image
                The Image with all sharpenable bands sharpened to the panchromatic resolution.

            Reference
            ---------
            Liu, J. G. (2000). Smoothing Filter-based Intensity Modulation: A spectral preserve image fusion technique for improving spatial details. International Journal of Remote Sensing, 21(18), 3461–3472. https://doi.org/10.1080/014311600750037499
            """
            img_scale = img.projection().nominalScale()
            pan_scale = pan.projection().nominalScale()
            kernel_width = img_scale.divide(pan_scale)
            kernel = ee.Kernel.square(radius=kernel_width.divide(2))
            pan_smooth = pan.reduceNeighborhood(
                reducer=ee.Reducer.mean(), kernel=kernel
            )

            img = img.resample("bicubic")
            sharp = img.multiply(pan).divide(pan_smooth)
            sharp = sharp.reproject(pan.projection())
            return sharp

    class HPFA(Sharpener):
        """The High Pass Filter Addition (HPFA) sharpener."""

        @staticmethod
        def sharpen(img, pan):
            """Apply High-Pass Filter Addition sharpening.

            Parameters
            ----------
            img : ee.Image
                Image to sharpen with only sharpenable bands selected.
            pan : ee.Image
                Image with only the panchromatic band selected.

            Returns
            -------
            ee.Image
                The Image with all sharpenable bands sharpened to the panchromatic resolution.

            Reference
            ---------
            Gangkofner, U. G., Pradhan, P. S., & Holcomb, D. W. (2008). Optimizing the High-Pass Filter Addition Technique for Image Fusion. Photogrammetric Engineering & Remote Sensing, 74(9), 1107–1118. https://doi.org/10.14358/pers.74.9.1107
            """
            img_scale = img.projection().nominalScale()
            pan_scale = pan.projection().nominalScale()
            kernel_width = img_scale.divide(pan_scale).multiply(2).add(1)

            img = img.resample("bicubic")

            center_val = kernel_width.pow(2).subtract(1)
            center = kernel_width.divide(2).int()
            kernel_row = ee.List.repeat(-1, kernel_width)
            kernel = ee.List.repeat(kernel_row, kernel_width)
            kernel = kernel.set(
                center, ee.List(kernel.get(center)).set(center, center_val)
            )
            kernel = ee.Kernel.fixed(weights=kernel, normalize=True)

            pan_hpf = pan.convolve(kernel)
            sharp = img.add(pan_hpf)
            sharp = sharp.reproject(pan.projection())

            return sharp

    class PCS(Sharpener):
        """The Principal Component Substitution (PCS) sharpener."""

        @staticmethod
        def sharpen(img, pan):
            """Apply Principal Component Substitution (PCS) sharpening.

            Parameters
            ----------
            img : ee.Image
                Image to sharpen with only sharpenable bands selected.
            pan : ee.Image
                Image with only the panchromatic band selected.

            Returns
            -------
            ee.Image
                The Image with all sharpenable bands sharpened to the panchromatic resolution.
            """
            img = img.resample("bicubic").reproject(pan.projection())
            band_names = img.bandNames()

            band_means = img.reduceRegion(ee.Reducer.mean(), **kwargs)
            img_means = band_means.toImage(band_names)
            img_centered = img.subtract(img_means)

            img_arr = img_centered.toArray()
            covar = img_arr.reduceRegion(ee.Reducer.centeredCovariance(), **kwargs)
            covar_arr = ee.Array(covar.get("array"))
            eigens = covar_arr.eigen()
            eigenvectors = eigens.slice(1, 1)
            img_arr_2d = img_arr.toArray(1)

            principal_components = (
                ee.Image(eigenvectors)
                .matrixMultiply(img_arr_2d)
                .arrayProject([0])
                .arrayFlatten([band_names])
            )

            pc1_name = principal_components.bandNames().get(0)

            # A dictionary can't use an ee.ComputedObject as a key, so set temporary band names
            pc1 = principal_components.select([pc1_name]).rename(["PC1"])
            pan = pan.rename(["pan"])

            pan_matched = pan.matchHistogram(
                pc1, {"pan": "PC1"}, kwargs.get("geometry")
            ).rename([pc1_name])

            principal_components = principal_components.addBands(
                pan_matched, overwrite=True
            )

            sharp_centered = (
                ee.Image(eigenvectors)
                .matrixSolve(principal_components.toArray().toArray(1))
                .arrayProject([0])
                .arrayFlatten([band_names])
            )
            sharp = sharp_centered.add(img_means)

            return sharp

    class SM(Sharpener):
        """The Simple Mean (SM) sharpener."""

        @staticmethod
        def sharpen(img, pan):
            """Apply Simple Mean (SM) sharpening.

            Parameters
            ----------
            img : ee.Image
                Image to sharpen with only sharpenable bands selected.
            pan : ee.Image
                Image with only the panchromatic band selected.

            Returns
            -------
            ee.Image
                The Image with all sharpenable bands sharpened to the panchromatic resolution.
            """
            img = img.resample("bicubic")
            sharp = img.add(pan).multiply(0.5)
            sharp = sharp.reproject(pan.projection())
            return sharp

    def run_and_set_qa(original, modified):
        """Get any valid requested quality assessment functions and run each of them to assess the quality of the
        sharpened Image. Set the results of each quality assessment as a new property (e.g. "eemont:RMSE").

        Parameters
        ----------
        original : ee.Image
            The original, pre-sharpened image.
        modified : ee.Image
            The sharpened image. Quality assessments will be run to quantify distortion between this image and the
            original.

        Results
        -------
        ee.Image
            The modified image with a new property set for each quality assessment.
        """
        selected_metrics = get_qa_metrics_by_names(qa)

        original = original.select(modified.bandNames())

        # Scale should match before calculating QA metrics
        original = original.reproject(modified.projection())

        for metric in selected_metrics:
            values = metric(original, modified)
            modified = modified.set("eemont:{}".format(metric.__name__), values)

        return modified

    def get_all_qa_metrics():
        """Get the name and class of all supported Metric subclasses.

        Returns
        -------
        requests.structures.CaseInsensitiveDict
            A dictionary of Metric subclasses with class names as keys and classes as values.
        """
        return requests.structures.CaseInsensitiveDict(
            {cls.__name__: cls for cls in Metric.__subclasses__()}
        )

    def get_qa_metrics_by_names(names):
        """Take a list of names and return a list of matching Metric subclasses.

        Parameters
        ----------
        names : list | tuple | str
            A list or tuple of strings or a single string with the names of QA metrics.

        Returns
        -------
        list
            A list of Metric subclasses matching the input names.
        """
        names = [names] if not isinstance(names, (list, tuple)) else names

        options = get_all_qa_metrics()
        selected = []

        for name in names:
            try:
                selected.append(options[name])
            except KeyError:
                raise AttributeError(
                    '"{}" is not a supported quality assessment metric. Supported metrics: {}'.format(
                        name, list(options.keys())
                    )
                )

        return selected

    class Metric(ABC):
        """The abstract class that is implemented by all quality assessment metrics."""

        def __new__(cls, original, modified):
            """Calculate and return the QA metric value when the class is instantiated."""
            return cls.calculate(original, modified)

        @abstractmethod
        def calculate(original, modified):
            """Abstract method implemented by each Metric where the metric values are calculated between the input images"""
            return

    class MSE(Metric):
        """The Mean Squared Error (MSE) metric."""

        @staticmethod
        def calculate(original, modified):
            """Calculate band-wise Mean Squared Error (MSE) between an original and modified image of the same spatial
            resolution. A value of 0 represents no error.

            Parameters
            ----------
            original : ee.Image
                The original image to use as a reference.
            modified : ee.Image
                The modified image to compare to the original.

            Returns
            -------
            ee.Dictionary
                A dictionary with band names as keys and MSE values as values.
            """
            mse = (
                original.subtract(modified)
                .pow(2)
                .reduceRegion(reducer=ee.Reducer.mean(), **kwargs)
            )

            return mse

    class RMSE(Metric):
        """The Root-Mean Squared Error (RMSE) metric."""

        @staticmethod
        def calculate(original, modified):
            """Calculate band-wise Root-Mean Squared Error (RMSE) between an original and modified image of the same spatial
            resolution. A value of 0 represents no error.

            Parameters
            ----------
            original : ee.Image
                The original image to use as a reference.
            modified : ee.Image
                The modified image to compare to the original.

            Returns
            -------
            ee.Dictionary
                A dictionary with band names as keys and RMSE values as values.
            """
            mse = MSE()(original, modified)
            sqrt_vals = ee.Array(mse.values()).sqrt().toList()
            rmse = ee.Dictionary.fromLists(mse.keys(), sqrt_vals)

            return rmse

    class RASE(Metric):
        """The Relative Average Spectral Error (RASE) metric."""

        @staticmethod
        def calculate(original, modified):
            """Calculate image-wise Relative Average Spectral Error (RASE) between an original and modified image of the
            same spatial resolution. A value of 0 represents no error.

            Parameters
            ----------
            original : ee.Image
                The original image to use as a reference.
            modified : ee.Image
                The modified image to compare to the original.

            Returns
            -------
            ee.Number
                The RASE value of the modified image.

            Reference
            ---------
            Vaiopoulos, A. D. (2011). Developing Matlab scripts for image analysis and quality assessment. Earth Resources and Environmental Remote Sensing/GIS Applications II. https://doi.org/10.1117/12.897806
            """
            mse = ee.Number(MSE(original, modified).values().reduce(ee.Reducer.mean()))
            xbar = (
                original.reduceRegion(ee.Reducer.mean(), **kwargs)
                .values()
                .reduce(ee.Reducer.mean())
            )
            rase = mse.sqrt().multiply(ee.Number(100).divide(xbar))
            return rase

    class ERGAS(Metric):
        """The Dimensionless Global Relative Error of Synthesis (ERGAS) metric."""

        @staticmethod
        def calculate(original, modified):
            """Calculate image-wise Dimensionless Global Relative Error of Synthesis (ERGAS) between an original and
            modified image of the same spatial resolution. A value of 0 represents no error.

            Parameters
            ----------
            original : ee.Image
                The original image to use as a reference.
            modified : ee.Image
                The modified image to compare to the original.

            Returns
            -------
            ee.Number
                The ERGAS value of the modified image.

            Reference
            ---------
            Vaiopoulos, A. D. (2011). Developing Matlab scripts for image analysis and quality assessment. Earth Resources and Environmental Remote Sensing/GIS Applications II. https://doi.org/10.1117/12.897806
            """
            h = modified.projection().nominalScale()
            l = original.projection().nominalScale()

            msek = ee.Array(MSE(original, modified).values())
            xbark = ee.Array(
                original.reduceRegion(ee.Reducer.mean(), **kwargs).values()
            )

            band_error = ee.Number(
                msek.divide(xbark).toList().reduce(ee.Reducer.mean())
            ).sqrt()
            ergas = band_error.multiply(h.divide(l).multiply(100))

            return ergas

    class DIV(Metric):
        """The Difference in Variance (DIV) metric."""

        @staticmethod
        def calculate(original, modified):
            """Calculate band-wise Difference in Variance (DIV) between an original and modified image of the same spatial
            resolution. A value of 0 represents no change in variance.

            Parameters
            ----------
            original : ee.Image
                The original image to use as a reference.
            modified : ee.Image
                The modified image to compare to the original.

            Returns
            -------
            ee.Dictionary
                A dictionary with band names as keys and DIV values as values.

            Reference
            ---------
            Vaiopoulos, A. D. (2011). Developing Matlab scripts for image analysis and quality assessment. Earth Resources
            and Environmental Remote Sensing/GIS Applications II. https://doi.org/10.1117/12.897806
            """
            var_orig = ee.Array(
                original.reduceRegion(ee.Reducer.variance(), **kwargs).values()
            )
            var_mod = ee.Array(
                modified.reduceRegion(ee.Reducer.variance(), **kwargs).values()
            )

            div = var_mod.divide(var_orig).multiply(-1).add(1)
            return ee.Dictionary.fromLists(original.bandNames(), div.toList())

    class bias(Metric):
        """The bias metric."""

        @staticmethod
        def calculate(original, modified):
            """Calculate band-wise bias between an original and modified image of the same spatial resolution. A value of 0
            represents no bias.

            Parameters
            ----------
            original : ee.Image
                The original image to use as a reference.
            modified : ee.Image
                The modified image to compare to the original.

            Returns
            -------
            ee.Dictionary
                A dictionary with band names as keys and bias values as values.

            Reference
            ---------
            Vaiopoulos, A. D. (2011). Developing Matlab scripts for image analysis and quality assessment. Earth Resources and Environmental Remote Sensing/GIS Applications II. https://doi.org/10.1117/12.897806
            """
            xbar = ee.Array(original.reduceRegion(ee.Reducer.mean(), **kwargs).values())
            ybar = ee.Array(modified.reduceRegion(ee.Reducer.mean(), **kwargs).values())

            bias = ybar.divide(xbar).multiply(-1).add(1)
            return ee.Dictionary.fromLists(original.bandNames(), bias.toList())

    class CC(Metric):
        """The Correlation Coefficient (CC) metric."""

        @staticmethod
        def calculate(original, modified):
            """Calculate band-wise correlation coefficient (CC) between an original and modified image of the same spatial
            resolution. A value of 1 represents perfect correlation.

            Parameters
            ----------
            original : ee.Image
                The original image to use as a reference.
            modified : ee.Image
                The modified image to compare to the original.

            Returns
            -------
            ee.Dictionary
                A dictionary with band names as keys and CC values as values.

            Reference
            ---------
            Gonzalez, R. C., & Woods, R. E. (2018). Digital Image Processing. Pearson.
            """
            xbar = ee.Image.constant(
                original.reduceRegion(ee.Reducer.mean(), **kwargs).values()
            )
            ybar = ee.Image.constant(
                modified.reduceRegion(ee.Reducer.mean(), **kwargs).values()
            )

            x_center = original.subtract(xbar)
            y_center = modified.subtract(ybar)

            numerator = ee.Array(
                x_center.multiply(y_center)
                .reduceRegion(ee.Reducer.sum(), **kwargs)
                .values()
            )

            x_denom = ee.Array(
                x_center.pow(2).reduceRegion(ee.Reducer.sum(), **kwargs).values()
            )
            y_denom = ee.Array(
                y_center.pow(2).reduceRegion(ee.Reducer.sum(), **kwargs).values()
            )

            denom = x_denom.multiply(y_denom).sqrt()

            cc = numerator.divide(denom)

            return ee.Dictionary.fromLists(original.bandNames(), cc.toList())

    class CML(Metric):
        """The Change in Mean Luminance (CML) metric."""

        @staticmethod
        def calculate(original, modified):
            """Calculate band-wise change in mean luminance (CML) between an original and modified image of the same spatial
            resolution. A value of 1 represents no change in luminance.

            Parameters
            ----------
            original : ee.Image
                The original image to use as a reference.
            modified : ee.Image
                The modified image to compare to the original.

            Returns
            -------
            ee.Dictionary
                A dictionary with band names as keys and CML values as values.

            Reference
            ---------
            Wang, Z., & Bovik, A. C. (2002). A universal image quality index. IEEE Signal Processing Letters, 9(3), 81–84. https://doi.org/10.1109/97.995823
            """
            xbar = ee.Array(original.reduceRegion(ee.Reducer.mean(), **kwargs).values())
            ybar = ee.Array(modified.reduceRegion(ee.Reducer.mean(), **kwargs).values())

            l = xbar.multiply(ybar).multiply(2).divide(xbar.pow(2).add(ybar.pow(2)))

            return ee.Dictionary.fromLists(original.bandNames(), l.toList())

    class CMC(Metric):
        """The Change in Mean Contrast (CMC) metric."""

        @staticmethod
        def calculate(original, modified):
            """Calculate band-wise change in mean contrast (CMC) between an original and modified image of the same spatial
            resolution. A value of 1 presents no change in contrast.

            Parameters
            ----------
            original : ee.Image
                The original image to use as a reference.
            modified : ee.Image
                The modified image to compare to the original.

            Returns
            -------
            ee.Dictionary
                A dictionary with band names as keys and CMC values as values.

            Reference
            ---------
            Wang, Z., & Bovik, A. C. (2002). A universal image quality index. IEEE Signal Processing Letters, 9(3), 81–84. https://doi.org/10.1109/97.995823
            """
            xvar = ee.Array(
                original.reduceRegion(ee.Reducer.variance(), **kwargs).values()
            )
            yvar = ee.Array(
                modified.reduceRegion(ee.Reducer.variance(), **kwargs).values()
            )
            xsd = ee.Array(
                original.reduceRegion(ee.Reducer.stdDev(), **kwargs).values()
            )
            ysd = ee.Array(
                modified.reduceRegion(ee.Reducer.stdDev(), **kwargs).values()
            )

            c = xsd.multiply(ysd).multiply(2).divide(xvar.add(yvar))

            return ee.Dictionary.fromLists(original.bandNames(), c.toList())

    class UIQI(Metric):
        """The Universal Image Quality Index (UIQI) metric."""

        @staticmethod
        def calculate(original, modified):
            """Calculate band-wise Universal Image Quality Index (UIQI) between an original and modified image of the same
            spatial resolution. A value of 1 represents perfect quality.

            Parameters
            ----------
            original : ee.Image
                The original image to use as a reference.
            modified : ee.Image
                The modified image to compare to the original.

            Returns
            -------
            ee.Dictionary
                A dictionary with band names as keys and UQI values as values.

            Reference
            ---------
            Wang, Z., & Bovik, A. C. (2002). A universal image quality index. IEEE Signal Processing Letters, 9(3), 81–84. https://doi.org/10.1109/97.995823
            """
            cc = ee.Array(CC(original, modified).values())
            l = ee.Array(CMC(original, modified).values())
            c = ee.Array(CML(original, modified).values())

            uiq = cc.multiply(l).multiply(c)

            return ee.Dictionary.fromLists(original.bandNames(), uiq.toList())

    platform = get_platform(source)

    if isinstance(source, ee.image.Image):
        sharpened = platform(source)
    elif isinstance(source, ee.imagecollection.ImageCollection):
        sharpened = source.map(platform)

    return sharpened

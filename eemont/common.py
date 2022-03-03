import copy
import json
import os
import re
import warnings

import ee
import ee_extra
import ee_extra.Spectral.core
import ee_extra.STAC.core
import ee_extra.STAC.utils
import pkg_resources
import requests
from box import Box
from geopy.geocoders import get_geocoder_for_service

from .extending import extend

warnings.simplefilter("always", UserWarning)


def indices(online=False):
    """Gets the dictionary of available indices as a Box object.

    Parameters
    ----------
    online : boolean
        Whether to retrieve the most recent list of indices directly from the GitHub repository and not from the local copy.

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
        Whether to retrieve the most recent list of indices directly from the GitHub repository and not from the local copy.

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

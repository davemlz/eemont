import ee
import geopy
from geopy.geocoders import get_geocoder_for_service

from .common import _lnglat_from_location, _retrieve_location
from .extending import extend
from .geometry import *


@extend(ee.feature.Feature)
def __getitem__(self, key):
    """Gets the column of the feature according to the specified key.

    Parameters
    ----------
    self : ee.Feature
        Feature to get the columns from.
    key : string | list[string]
        Key used to get the specified column. If string, it gets the column with that name
        or that matches with regex. If list, it gets multiple columns.

    Returns
    -------
    ee.Feature
        Feature with the selected columns.
    """
    if isinstance(key, str):
        key = [key]

    return self.select(key)


@extend(ee.feature.Feature, static=True)
def PointFromQuery(query, geocoder="nominatim", **kwargs):
    """Constructs an ee.Feature describing a point from a query submitted to a geodocer
    using the geopy package.

    This returns exactly one pair of coordinates. The properties of the feature correspond
    to the raw properties retrieved by the location of the query.

    Tip
    ----------
    Check more info about constructors in the :ref:`User Guide<Constructors>`.

    Parameters
    ----------
    query : str
        Address, query or structured query to geocode.
    geocoder : str, default = 'nominatim'
        Geocoder to use. Please visit https://geopy.readthedocs.io/ for more info.
    **kwargs :
        Keywords arguments for geolocator.geocode(). The user_agent argument is mandatory
        (this argument can be set as user_agent = 'my-gee-username' or user_agent =
        'my-gee-app-name'). Please visit https://geopy.readthedocs.io/ for more info.

    Returns
    -------
    ee.Feature
        Feature with a geometry describing a point from the specified query.

    See Also
    --------
    BBoxFromQuery : Constructs an ee.Feature describing a bounding box from a query
        submitted to a geodocer using the geopy package.

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> ee.Feature.PointFromQuery('Mt. Rainier, USA',
    ...                           user_agent = 'my-gee-eemont-query').getInfo()
    {'type': 'Feature',
     'geometry': {'type': 'Point', 'coordinates': [-121.757682, 46.8521484]},
     'properties': {'boundingbox': ['46.8520984',
       '46.8521984',
       '-121.757732',
       '-121.757632'],
      'class': 'natural',
      'display_name': 'Mount Rainier, Pierce County, Washington, United States',
      'importance': 0.5853390667167165,
      'lat': '46.8521484',
      'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright',
      'lon': '-121.757682',
      'osm_id': 1744903493,
      'osm_type': 'node',
      'place_id': 17287419,
      'type': 'volcano'}}
    """
    location = _retrieve_location(query, geocoder, True, **kwargs)
    geometry = ee.Geometry.Point(_lnglat_from_location(location))

    return ee.Feature(geometry, location.raw)


@extend(ee.feature.Feature, static=True)
def BBoxFromQuery(query, geocoder="nominatim", **kwargs):
    """Constructs an ee.Feature describing a bounding box from a query submitted to a
    geodocer using the geopy package.

    The properties of the feature correspond to the raw properties retrieved by the
    location of the query.

    Tip
    ----------
    Check more info about constructors in the :ref:`User Guide<Constructors>`.

    Parameters
    ----------
    query : str
        Address, query or structured query to geocode.
    geocoder : str, default = 'nominatim'
        Geocoder to use. One of 'nominatim' or 'arcgis'. Please visit
        https://geopy.readthedocs.io/ for more info.
    **kwargs :
        Keywords arguments for geolocator.geocode(). The user_agent argument is mandatory
        (this argument can be set as user_agent = 'my-gee-username' or user_agent =
        'my-gee-app-name'). Please visit https://geopy.readthedocs.io/ for more info.

    Returns
    -------
    ee.Feature
        Feature with a geometry describing a bounding box from the specified query.

    See Also
    --------
    PointFromQuery : Constructs an ee.Feature describing a point from a query submitted to
        a geodocer using the geopy package.

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> ee.Feature.BBoxFromQuery('Bogotá',user_agent = 'my-gee-eemont-query').getInfo()
    {'type': 'Feature',
     'geometry': {'geodesic': False,
      'type': 'Polygon',
      'coordinates': [[[-74.22351370000001, 4.4711754],
        [-74.0102483, 4.4711754],
        [-74.0102483, 4.8331695],
        [-74.22351370000001, 4.8331695],
        [-74.22351370000001, 4.4711754]]]},
     'properties': {'boundingbox': ['4.4711754',
       '4.8331695',
       '-74.2235137',
       '-74.0102483'],
      'class': 'boundary',
      'display_name': 'Bogotá, Bogotá Distrito Capital, Región Andina, 11001, Colombia',
      'icon': 'https://nominatim.openstreetmap.org/ui/mapicons//poi_boundary_administrative.p.20.png',
      'importance': 0.7931743429157826,
      'lat': '4.6533326',
      'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright',
      'lon': '-74.083652',
      'osm_id': 7426387,
      'osm_type': 'relation',
      'place_id': 259216862,
      'type': 'administrative'}}
    """
    if geocoder not in ["nominatim", "arcgis"]:
        raise Exception('Invalid geocoder! Use one of "nominatim" or "arcgis".')

    location = _retrieve_location(query, geocoder, True, **kwargs)

    if geocoder == "nominatim":
        BBox = location.raw["boundingbox"]
        geometry = ee.Geometry.BBox(
            float(BBox[2]), float(BBox[0]), float(BBox[3]), float(BBox[1])
        )
        return ee.Feature(geometry, location.raw)
    elif geocoder == "arcgis":
        BBox = location.raw["extent"]
        geometry = ee.Geometry.BBox(
            BBox["xmin"], BBox["ymin"], BBox["xmax"], BBox["ymax"]
        )
        return ee.Feature(geometry, location.raw)
    else:
        raise Exception('Invalid geocoder! Use one of "nominatim" or "arcgis".')


@extend(ee.feature.Feature, static=False)
def plusCodes(self, codeLength=10):
    """Converts the coordinates of the geometry of an ee.Feature to Plus Codes.

    Parameters
    ----------
    self : ee.Feature
        The feature to extract coordinates from.
    codeLength : int, default = 10
        The number of significant digits in the output codes, between 2 and 15. Shorter
        codes are less precise.

    Returns
    -------
    list | str
        The coordinates of the geometry converted to Plus Codes. The structure of the Plus
        Codes array will be identical to the structure returned by ee.Geometry.coordinates().

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> pt = ee.Feature(ee.Geometry.Point([-105, 40]))
    >>> pt.plusCodes()
    '85GQ2222+22'
    """
    return ee.Element.geometry(self).plusCodes(codeLength)

import ee
import geopy
from geopy.geocoders import get_geocoder_for_service
from eemont.common import _convert_lnglats_to_pluscodes, _convert_pluscodes_to_lnglats


def _extend_staticmethod_eeGeometry():
    """Decorator. Extends the ee.Geometry class with a static method."""
    return lambda f: (setattr(ee.geometry.Geometry, f.__name__, staticmethod(f)) or f)


def _extend_eeGeometry():
    """Decorator. Extends the ee.Geometry class."""
    return lambda f: (setattr(ee.geometry.Geometry, f.__name__, f) or f)


@_extend_staticmethod_eeGeometry()
def BBoxFromQuery(query, geocoder="nominatim", **kwargs):
    """Constructs an ee.Geometry describing a bounding box from a query submitted to a geodocer using the geopy package.

    Tip
    ----------
    Check more info about constructors in the :ref:`User Guide<Constructors>`.

    Parameters
    ----------
    query : str
        Address, query or structured query to geocode.
    geocoder : str, default = 'nominatim'
        Geocoder to use. One of 'nominatim' or 'arcgis'. Please visit https://geopy.readthedocs.io/ for more info.
    **kwargs :
        Keywords arguments for geolocator.geocode(). The user_agent argument is mandatory (this argument can be set as user_agent = 'my-gee-username' or
        user_agent = 'my-gee-app-name'). Please visit https://geopy.readthedocs.io/ for more info.

    Returns
    -------
    ee.Geometry.Polygon
        Geometry describing a bounding box from the specified query.

    See Also
    --------
    PointFromQuery : Constructs an ee.Geometry describing a point from a query submitted to a geodocer using the geopy package.
    MultiPointFromQuery : Constructs an ee.Geometry describing a multi-point from a query submitted to a geodocer using the geopy package.

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> ee.Geometry.BBoxFromQuery('Seattle',user_agent = 'my-gee-eemont-query')
    ee.Geometry({
      "functionInvocationValue": {
        "functionName": "GeometryConstructors.Polygon",
        "arguments": {
          "coordinates": {
            "constantValue": [
              [
                [
                  -122.45969600000001,
                  47.7341357
                ],
                [
                  -122.45969600000001,
                  47.4810022
                ],
                [
                  -122.224433,
                  47.4810022
                ],
                [
                  -122.224433,
                  47.7341357
                ]
              ]
            ]
          },
          "geodesic": {
            "constantValue": false
          }
        }
      }
    })
    """
    if geocoder in ["nominatim", "arcgis"]:
        cls = get_geocoder_for_service(geocoder)
    else:
        raise Exception('Invalid geocoder! Use one of "nominatim" or "arcgis".')
    geolocator = cls(**kwargs)
    location = geolocator.geocode(query)
    if location is None:
        raise Exception("No matches were found for your query!")
    else:
        if geocoder == "nominatim":
            BBox = location.raw["boundingbox"]
            return ee.Geometry.BBox(
                float(BBox[2]), float(BBox[0]), float(BBox[3]), float(BBox[1])
            )
        elif geocoder == "arcgis":
            BBox = location.raw["extent"]
            return ee.Geometry.BBox(
                BBox["xmin"], BBox["ymin"], BBox["xmax"], BBox["ymax"]
            )
        else:
            raise Exception('Invalid geocoder! Use one of "nominatim" or "arcgis".')


@_extend_staticmethod_eeGeometry()
def PointFromQuery(query, geocoder="nominatim", **kwargs):
    """Constructs an ee.Geometry describing a point from a query submitted to a geodocer using the geopy package. This returns exactly one pair of coordinates.

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
        Keywords arguments for geolocator.geocode(). The user_agent argument is mandatory (this argument can be set as user_agent = 'my-gee-username' or
        user_agent = 'my-gee-app-name'). Please visit https://geopy.readthedocs.io/ for more info.

    Returns
    -------
    ee.Geometry.Point
        Geometry describing a point from the specified query.

    See Also
    --------
    BBoxFromQuery : Constructs an ee.Geometry describing a bounding box from a query submitted to a geodocer using the geopy package.
    MultiPointFromQuery : Constructs an ee.Geometry describing a multi-point from a query submitted to a geodocer using the geopy package.

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> ee.Geometry.PointFromQuery('Mt. Rainier, USA',user_agent = 'my-gee-eemont-query')
    ee.Geometry({
      "functionInvocationValue": {
        "functionName": "GeometryConstructors.Point",
        "arguments": {
          "coordinates": {
            "constantValue": [
              -121.757682,
              46.8521484
            ]
          }
        }
      }
    })
    """
    cls = get_geocoder_for_service(geocoder)
    geolocator = cls(**kwargs)
    location = geolocator.geocode(query)
    if location is None:
        raise Exception("No matches were found for your query!")
    else:
        return ee.Geometry.Point([location.longitude, location.latitude])


@_extend_staticmethod_eeGeometry()
def MultiPointFromQuery(query, geocoder="nominatim", **kwargs):
    """Constructs an ee.Geometry describing a multi-point from a query submitted to a geodocer using the geopy package. This returns all pairs of coordinates retrieved by the query.

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
        Keywords arguments for geolocator.geocode(). The user_agent argument is mandatory (this argument can be set as user_agent = 'my-gee-username' or
        user_agent = 'my-gee-app-name'). Please visit https://geopy.readthedocs.io/ for more info.

    Returns
    -------
    ee.Geometry.MultiPoint
        Geometry describing a multi-point from the specified query.

    See Also
    --------
    BBoxFromQuery : Constructs an ee.Geometry describing a bounding box from a query submitted to a geodocer using the geopy package.
    PointFromQuery : Constructs an ee.Geometry describing a point from a query submitted to a geodocer using the geopy package.

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> ee.Geometry.MultiPointFromQuery('Mt. Rainier, USA',user_agent = 'my-gee-eemont-query')
    ee.Geometry({
      "functionInvocationValue": {
        "functionName": "GeometryConstructors.MultiPoint",
        "arguments": {
          "coordinates": {
            "constantValue": [
              [
                -121.757682,
                46.8521484
              ],
              [
                -76.9649751,
                38.9415
              ],
              [
                -97.78689,
                30.154197
              ],
              [
                -84.130098,
                39.863452
              ]
            ]
          }
        }
      }
    })
    """
    cls = get_geocoder_for_service(geocoder)
    geolocator = cls(**kwargs)
    locations = geolocator.geocode(query, exactly_one=False)
    if locations is None:
        raise Exception("No matches were found for your query!")
    else:
        coords = []
        for location in locations:
            coords.append([location.longitude, location.latitude])
        return ee.Geometry.MultiPoint(coords)


@_extend_staticmethod_eeGeometry()
def PointFromPlusCode(pluscode, geocoder="nominatim", **kwargs):
    coordinates = _convert_pluscodes_to_lnglats(pluscode, geocoder, **kwargs)
    return ee.Geometry.Point(coordinates)


@_extend_staticmethod_eeGeometry()
def MultiPointFromPlusCodes(pluscodes, geocoder="nominatim", **kwargs):
    coordinates = _convert_pluscodes_to_lnglats(pluscodes, geocoder, **kwargs)
    return ee.Geometry.MultiPoint(coordinates)


@_extend_staticmethod_eeGeometry()
def PolygonFromPlusCodes(pluscodes, geocoder="nominatim", **kwargs):
    coordinates = _convert_pluscodes_to_lnglats(pluscodes, geocoder, **kwargs)
    return ee.Geometry.Polygon(coordinates)


@_extend_staticmethod_eeGeometry()
def MultiPolygonFromPlusCodes(pluscodes, geocoder="nominatim", **kwargs):
    coordinates = _convert_pluscodes_to_lnglats(pluscodes, geocoder, **kwargs)
    return ee.Geometry.MultiPolygon(coordinates)


@_extend_staticmethod_eeGeometry()
def LineStringFromPlusCodes(pluscodes, geocoder="nominatim", **kwargs):
    coordinates = _convert_pluscodes_to_lnglats(pluscodes, geocoder, **kwargs)
    return ee.Geometry.LineString(coordinates)


@_extend_staticmethod_eeGeometry()
def MultiLineStringFromPlusCodes(pluscodes, geocoder="nominatim", **kwargs):
    coordinates = _convert_pluscodes_to_lnglats(pluscodes, geocoder, **kwargs)
    return ee.Geometry.MultiLineString(coordinates)


@_extend_staticmethod_eeGeometry()
def LinearRingFromPlusCodes(pluscodes, geocoder="nominatim", **kwargs):
    coordinates = _convert_pluscodes_to_lnglats(pluscodes, geocoder, **kwargs)
    return ee.Geometry.LinearRing(coordinates)


@_extend_staticmethod_eeGeometry()
def RectangleFromPlusCodes(pluscodes, geocoder="nominatim", **kwargs):
    coordinates = _convert_pluscodes_to_lnglats(pluscodes, geocoder, **kwargs)
    return ee.Geometry.Rectangle(coordinates)


@_extend_eeGeometry()
def plusCodes(self, codeLength=10):
    """Convert the coordinates of an ee.Geometry to plus codes.

    Parameters
    ----------
    self : ee.Geometry
        The geometry to extract coordinates from.
    codeLength : int, default = 10
        The number of significant digits in the output codes, between 2 and 15. Shorter codes are less precise.

    Returns
    -------
    list | str
        The coordinates of the geometry converted to plus codes. The structure of the plus codes array will be 
        identical to the structure returned by ee.Geometry.coordinates().

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> pt = ee.Geometry.Point([-105, 40])
    >>> pt.plusCodes()
    '85GQ2222+22'
    """
    coordinates = self.coordinates().getInfo()
    plus_codes = _convert_lnglats_to_pluscodes(coordinates)
    return plus_codes

import ee
import geopy
from geopy.geocoders import get_geocoder_for_service

from .common import (_convert_lnglats_to_pluscodes,
                     _convert_pluscodes_to_lnglats, _lnglat_from_location,
                     _retrieve_location)
from .extending import extend


@extend(ee.geometry.Geometry, static=True)
def BBoxFromQuery(query, geocoder="nominatim", **kwargs):
    """Constructs an ee.Geometry describing a bounding box from a query submitted to a
    geodocer using the geopy package.

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
    ee.Geometry.Polygon
        Geometry describing a bounding box from the specified query.

    See Also
    --------
    PointFromQuery : Constructs an ee.Geometry describing a point from a query submitted
        to a geodocer using the geopy package.
    MultiPointFromQuery : Constructs an ee.Geometry describing a multi-point from a query
        submitted to a geodocer using the geopy package.

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
    if geocoder not in ["nominatim", "arcgis"]:
        raise Exception('Invalid geocoder! Use one of "nominatim" or "arcgis".')

    location = _retrieve_location(query, geocoder, True, **kwargs)

    if geocoder == "nominatim":
        BBox = location.raw["boundingbox"]
        return ee.Geometry.BBox(
            float(BBox[2]), float(BBox[0]), float(BBox[3]), float(BBox[1])
        )
    elif geocoder == "arcgis":
        BBox = location.raw["extent"]
        return ee.Geometry.BBox(BBox["xmin"], BBox["ymin"], BBox["xmax"], BBox["ymax"])
    else:
        raise Exception('Invalid geocoder! Use one of "nominatim" or "arcgis".')


@extend(ee.geometry.Geometry, static=True)
def PointFromQuery(query, geocoder="nominatim", **kwargs):
    """Constructs an ee.Geometry describing a point from a query submitted to a geodocer
    using the geopy package.

    This returns exactly one pair of coordinates.

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
    ee.Geometry.Point
        Geometry describing a point from the specified query.

    See Also
    --------
    BBoxFromQuery : Constructs an ee.Geometry describing a bounding box from a query
        submitted to a geodocer using the geopy package.
    MultiPointFromQuery : Constructs an ee.Geometry describing a multi-point from a query
        submitted to a geodocer using the geopy package.

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
    location = _retrieve_location(query, geocoder, True, **kwargs)
    return ee.Geometry.Point(_lnglat_from_location(location))


@extend(ee.geometry.Geometry, static=True)
def MultiPointFromQuery(query, geocoder="nominatim", **kwargs):
    """Constructs an ee.Geometry describing a multi-point from a query submitted to a
    geodocer using the geopy package.

    This returns all pairs of coordinates retrieved by the query.

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
    ee.Geometry.MultiPoint
        Geometry describing a multi-point from the specified query.

    See Also
    --------
    BBoxFromQuery : Constructs an ee.Geometry describing a bounding box from a query
        submitted to a geodocer using the geopy package.
    PointFromQuery : Constructs an ee.Geometry describing a point from a query submitted
        to a geodocer using the geopy package.

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
    locations = _retrieve_location(query, geocoder, False, **kwargs)
    coords = []
    for location in locations:
        coords.append([location.longitude, location.latitude])
    return ee.Geometry.MultiPoint(coords)


@extend(ee.geometry.Geometry, static=True)
def PointFromPlusCode(pluscode, geocoder="nominatim", **kwargs):
    """Constructs an ee.Geometry describing a point from a Plus Code.

    If the Plus Code is full, it will be decoded directly using the openlocationcode
    package. If it is a short Code with a reference location, the reference will be
    geocoded using the geopy package.

    Tip
    ----------
    Check more info about constructors in the :ref:`User Guide<Constructors>`.

    Parameters
    ----------
    pluscode : str
        A full Plus Code or a short Plus Code with a geocodable reference location appended to it.
    geocoder : str, default = 'nominatim'
        Geocoder to use. Please visit https://geopy.readthedocs.io/ for more info.
    **kwargs :
        Keywords arguments for geolocator.geocode(). The user_agent argument is mandatory
        (this argument can be set as user_agent = 'my-gee-username' or user_agent =
        'my-gee-app-name'). Please visit https://geopy.readthedocs.io/ for more info.

    Returns
    -------
    ee.Geometry.Point
        Geometry describing a point from the Plus Code centroid.

    See Also
    --------
    MultiPointFromPlusCodes : Constructs an ee.Geometry describing multiple points from a
        list of Plus Codes.
    PolygonFromPlusCodes : Constructs an ee.Geometry describing a polygon from a list of
        Plus Codes.
    MultiPolygonFromPlusCodes : Constructs an ee.Geometry describing multiple polygons
        from a list of lists of Plus Codes.
    LineStringFromPlusCodes : Constructs an ee.Geometry describing a line from a list of
        Plus Codes.
    MultiLineStringFromPlusCodes : Constructs an ee.Geometry describing multiple lines
        from a list of lists of Plus Codes.
    LinearRingFromPlusCodes : Constructs an ee.Geometry describing a linear ring from a
        list of Plus Codes.
    RectangleFromPlusCodes : Constructs an ee.Geometry describing a rectangle from a list
        of two Plus Code corners.

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> geom = ee.Geometry.PointFromPlusCode('QXGV+XH Denver, CO, USA',
    ...                                      user_agent = 'my-gee-eemont-query')
    >>> geom.coordinates().getInfo()
    [-105.0060625, 39.777437500000005]
    """
    coordinates = _convert_pluscodes_to_lnglats(pluscode, geocoder, **kwargs)
    return ee.Geometry.Point(coordinates)


@extend(ee.geometry.Geometry, static=True)
def MultiPointFromPlusCodes(pluscodes, geocoder="nominatim", **kwargs):
    """Constructs an ee.Geometry describing multiple points from a list of Plus Codes.

    If the Plus Codes are full, they will be decoded directly using the openlocationcode
    package. If they are short Codes with reference locations, the references will be
    geocoded using the geopy package.

    Tip
    ----------
    Check more info about constructors in the :ref:`User Guide<Constructors>`.

    Parameters
    ----------
    pluscodes : str
        A list of full Plus Codes or short Plus Codes with geocodable reference locations
        appended to them.
    geocoder : str, default = 'nominatim'
        Geocoder to use. Please visit https://geopy.readthedocs.io/ for more info.
    **kwargs :
        Keywords arguments for geolocator.geocode(). The user_agent argument is mandatory
        (this argument can be set as user_agent = 'my-gee-username' or user_agent =
        'my-gee-app-name'). Please visit https://geopy.readthedocs.io/ for more info.

    Returns
    -------
    ee.Geometry.MultiPoint
        Geometry describing multiple points from the Plus Code centroids.

    See Also
    --------
    PointFromPlusCode : Constructs an ee.Geometry describing a point from a Plus Code.
    PolygonFromPlusCodes : Constructs an ee.Geometry describing a polygon from a list of
        Plus Codes.
    MultiPolygonFromPlusCodes : Constructs an ee.Geometry describing multiple polygons
        from a list of lists of Plus Codes.
    LineStringFromPlusCodes : Constructs an ee.Geometry describing a line from a list of
        Plus Codes.
    MultiLineStringFromPlusCodes : Constructs an ee.Geometry describing multiple lines
        from a list of lists of Plus Codes.
    LinearRingFromPlusCodes : Constructs an ee.Geometry describing a linear ring from a
        list of Plus Codes.
    RectangleFromPlusCodes : Constructs an ee.Geometry describing a rectangle from a list
        of two Plus Code corners.

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> geom = ee.Geometry.MultiPointFromPlusCodes(['85FQ2222+22','85FR2222+22'])
    >>> geom.coordinates().getInfo()
    [[-104.9999375, 39.0000625], [-103.9999375, 39.0000625]]
    """
    coordinates = _convert_pluscodes_to_lnglats(pluscodes, geocoder, **kwargs)
    return ee.Geometry.MultiPoint(coordinates)


@extend(ee.geometry.Geometry, static=True)
def PolygonFromPlusCodes(pluscodes, geocoder="nominatim", **kwargs):
    """Constructs an ee.Geometry describing a polygon from a list of Plus Codes.

    If the Plus Codes are full, they will be decoded directly using the openlocationcode
    package. If they are short Codes with reference locations, the references will be
    geocoded using the geopy package.

    Tip
    ----------
    Check more info about constructors in the :ref:`User Guide<Constructors>`.

    Parameters
    ----------
    pluscodes : str
        A list of full Plus Codes or short Plus Codes with geocodable reference locations
        appended to them.
    geocoder : str, default = 'nominatim'
        Geocoder to use. Please visit https://geopy.readthedocs.io/ for more info.
    **kwargs :
        Keywords arguments for geolocator.geocode(). The user_agent argument is mandatory
        (this argument can be set as user_agent = 'my-gee-username' or user_agent =
        'my-gee-app-name'). Please visit https://geopy.readthedocs.io/ for more info.

    Returns
    -------
    ee.Geometry.Polygon
        Geometry describing a polygon from the Plus Code centroids.

    See Also
    --------
    PointFromPlusCode : Constructs an ee.Geometry describing a point from a Plus Code.
    MultiPointFromPlusCodes : Constructs an ee.Geometry describing multiple points from a
        list of Plus Codes.
    MultiPolygonFromPlusCodes : Constructs an ee.Geometry describing multiple polygons
        from a list of lists of Plus Codes.
    LineStringFromPlusCodes : Constructs an ee.Geometry describing a line from a list of
        Plus Codes.
    MultiLineStringFromPlusCodes : Constructs an ee.Geometry describing multiple lines
        from a list of lists of Plus Codes.
    LinearRingFromPlusCodes : Constructs an ee.Geometry describing a linear ring from a
        list of Plus Codes.
    RectangleFromPlusCodes : Constructs an ee.Geometry describing a rectangle from a list
        of two Plus Code corners.

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> geom = ee.Geometry.PolygonFromPlusCodes(['85FQ2222+22','85FR2222+22','85GR2222+22'])
    >>> geom.coordinates().getInfo()
    [[[-104.9999375, 39.0000625],
      [-103.9999375, 39.0000625],
      [-103.9999375, 40.0000625],
      [-104.9999375, 39.0000625]]]
    """
    coordinates = _convert_pluscodes_to_lnglats(pluscodes, geocoder, **kwargs)
    return ee.Geometry.Polygon(coordinates)


@extend(ee.geometry.Geometry, static=True)
def MultiPolygonFromPlusCodes(pluscodes, geocoder="nominatim", **kwargs):
    """Constructs an ee.Geometry describing multiple polygons from a list of lists of
    Plus Codes.

    If the Plus Codes are full, they will be decoded directly using the openlocationcode
    package. If they are short Codes with reference locations, the references will be
    geocoded using the geopy package.

    Tip
    ----------
    Check more info about constructors in the :ref:`User Guide<Constructors>`.

    Parameters
    ----------
    pluscodes : str
        A list of lists of full Plus Codes or short Plus Codes with geocodable reference
        locations appended to them.
    geocoder : str, default = 'nominatim'
        Geocoder to use. Please visit https://geopy.readthedocs.io/ for more info.
    **kwargs :
        Keywords arguments for geolocator.geocode(). The user_agent argument is mandatory
        (this argument can be set as user_agent = 'my-gee-username' or user_agent =
        'my-gee-app-name'). Please visit https://geopy.readthedocs.io/ for more info.

    Returns
    -------
    ee.Geometry.MultiPolygon
        Geometry describing multiple polygons from the Plus Code centroids.

    See Also
    --------
    PointFromPlusCode : Constructs an ee.Geometry describing a point from a Plus Code.
    MultiPointFromPlusCodes : Constructs an ee.Geometry describing multiple points from a
        list of Plus Codes.
    PolygonFromPlusCodes : Constructs an ee.Geometry describing a polygon from a list of
        Plus Codes.
    LineStringFromPlusCodes : Constructs an ee.Geometry describing a line from a list of
        Plus Codes.
    MultiLineStringFromPlusCodes : Constructs an ee.Geometry describing multiple lines
        from a list of lists of Plus Codes.
    LinearRingFromPlusCodes : Constructs an ee.Geometry describing a linear ring from a
        list of Plus Codes.
    RectangleFromPlusCodes : Constructs an ee.Geometry describing a rectangle from a list
        of two Plus Code corners.

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> geom = ee.Geometry.MultiPolygonFromPlusCodes([
    ...    ['85FQ2222+22', '85FR2222+22', '85GR2222+22'],
    ...    ['85FP8PC2+G2', '85FPJF23+G4', '85FPMW2R+RP']
    ...  ])
    >>> geom.coordinates().getInfo()
    [[[[-104.9999375, 39.0000625],
      [-103.9999375, 39.0000625],
      [-103.9999375, 40.0000625],
      [-104.9999375, 39.0000625]],
      [[-105.2999375, 39.321312500000005],
      [-105.5471875, 39.6013125],
      [-105.0581875, 39.6520625],
      [-105.2999375, 39.321312500000005]]]]
    """
    coordinates = _convert_pluscodes_to_lnglats(pluscodes, geocoder, **kwargs)
    return ee.Geometry.MultiPolygon(coordinates)


@extend(ee.geometry.Geometry, static=True)
def LineStringFromPlusCodes(pluscodes, geocoder="nominatim", **kwargs):
    """Constructs an ee.Geometry describing a line from a list of Plus Codes.

    If the Plus Codes are full, they will be decoded directly using the openlocationcode
    package. If they are short Codes with reference locations, the references will be
    geocoded using the geopy package.

    Tip
    ----------
    Check more info about constructors in the :ref:`User Guide<Constructors>`.

    Parameters
    ----------
    pluscodes : str
        A list of full Plus Codes or short Plus Codes with geocodable reference locations
        appended to them.
    geocoder : str, default = 'nominatim'
        Geocoder to use. Please visit https://geopy.readthedocs.io/ for more info.
    **kwargs :
        Keywords arguments for geolocator.geocode(). The user_agent argument is mandatory
        (this argument can be set as user_agent = 'my-gee-username' or user_agent =
        'my-gee-app-name'). Please visit https://geopy.readthedocs.io/ for more info.

    Returns
    -------
    ee.Geometry.LineString
        Geometry describing a line from the Plus Code centroids.

    See Also
    --------
    PointFromPlusCode : Constructs an ee.Geometry describing a point from a Plus Code.
    MultiPointFromPlusCodes : Constructs an ee.Geometry describing multiple points from a
        list of Plus Codes.
    PolygonFromPlusCodes : Constructs an ee.Geometry describing a polygon from a list of
        Plus Codes.
    MultiPolygonFromPlusCodes : Constructs an ee.Geometry describing multiple polygons
        from a list of lists of Plus Codes.
    MultiLineStringFromPlusCodes : Constructs an ee.Geometry describing multiple lines
        from a list of lists of Plus Codes.
    LinearRingFromPlusCodes : Constructs an ee.Geometry describing a linear ring from a
        list of Plus Codes.
    RectangleFromPlusCodes : Constructs an ee.Geometry describing a rectangle from a list
        of two Plus Code corners.

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> geom = ee.Geometry.LineStringFromPlusCodes(['85FQ2222+22','85FR2222+22'])
    >>> geom.coordinates().getInfo()
    [[-104.9999375, 39.0000625], [-103.9999375, 39.0000625]]
    """
    coordinates = _convert_pluscodes_to_lnglats(pluscodes, geocoder, **kwargs)
    return ee.Geometry.LineString(coordinates)


@extend(ee.geometry.Geometry, static=True)
def MultiLineStringFromPlusCodes(pluscodes, geocoder="nominatim", **kwargs):
    """Constructs an ee.Geometry describing multiple lines from a list of lists of Plus
    Codes.

    If the Plus Codes are full, they will be decoded directly using the openlocationcode
    package. If they are short Codes with reference locations, the references will be
    geocoded using the geopy package.

    Tip
    ----------
    Check more info about constructors in the :ref:`User Guide<Constructors>`.

    Parameters
    ----------
    pluscodes : str
        A list of lists of full Plus Codes or short Plus Codes with geocodable reference
        locations appended to them.
    geocoder : str, default = 'nominatim'
        Geocoder to use. Please visit https://geopy.readthedocs.io/ for more info.
    **kwargs :
        Keywords arguments for geolocator.geocode(). The user_agent argument is mandatory
        (this argument can be set as user_agent = 'my-gee-username' or user_agent =
        'my-gee-app-name'). Please visit https://geopy.readthedocs.io/ for more info.

    Returns
    -------
    ee.Geometry.MultiLineString
        Geometry describing multiple lines from the Plus Code centroids.

    See Also
    --------
    PointFromPlusCode : Constructs an ee.Geometry describing a point from a Plus Code.
    MultiPointFromPlusCodes : Constructs an ee.Geometry describing multiple points from a
        list of Plus Codes.
    PolygonFromPlusCodes : Constructs an ee.Geometry describing a polygon from a list of
        Plus Codes.
    MultiPolygonFromPlusCodes : Constructs an ee.Geometry describing multiple polygons
        from a list of lists of Plus Codes.
    LineStringFromPlusCodes : Constructs an ee.Geometry describing a line from a list of
        Plus Codes.
    LinearRingFromPlusCodes : Constructs an ee.Geometry describing a linear ring from a
        list of Plus Codes.
    RectangleFromPlusCodes : Constructs an ee.Geometry describing a rectangle from a list
        of two Plus Code corners.

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> geom = ee.Geometry.MultiLineStringFromPlusCodes([
    ...    ['85FQ2222+22', '85FR2222+22'],
    ...    ['85FP8PC2+G2', '85FPJF23+G4']
    ... ])
    >>> geom.coordinates().getInfo()
    [[[-104.9999375, 39.0000625], [-103.9999375, 39.0000625]],
    [[-105.2999375, 39.321312500000005], [-105.5471875, 39.6013125]]]
    """
    coordinates = _convert_pluscodes_to_lnglats(pluscodes, geocoder, **kwargs)
    return ee.Geometry.MultiLineString(coordinates)


@extend(ee.geometry.Geometry, static=True)
def LinearRingFromPlusCodes(pluscodes, geocoder="nominatim", **kwargs):
    """Constructs an ee.Geometry describing a linear ring from a list of Plus Codes.

    If the Plus Codes are full, they will be decoded directly using the openlocationcode
    package. If they are short Codes with reference locations, the references will be
    geocoded using the geopy package.

    Tip
    ----------
    Check more info about constructors in the :ref:`User Guide<Constructors>`.

    Parameters
    ----------
    pluscodes : str
        A list of full Plus Codes or short Plus Codes with geocodable reference locations
        appended to them.
    geocoder : str, default = 'nominatim'
        Geocoder to use. Please visit https://geopy.readthedocs.io/ for more info.
    **kwargs :
        Keywords arguments for geolocator.geocode(). The user_agent argument is mandatory
        (this argument can be set as user_agent = 'my-gee-username' or user_agent =
        'my-gee-app-name'). Please visit https://geopy.readthedocs.io/ for more info.

    Returns
    -------
    ee.Geometry.LinearRing
        Geometry describing a linear ring from the Plus Code centroids.

    See Also
    --------
    PointFromPlusCode : Constructs an ee.Geometry describing a point from a Plus Code.
    MultiPointFromPlusCodes : Constructs an ee.Geometry describing multiple points from a
        list of Plus Codes.
    PolygonFromPlusCodes : Constructs an ee.Geometry describing a polygon from a list of
        Plus Codes.
    MultiPolygonFromPlusCodes : Constructs an ee.Geometry describing multiple polygons
        from a list of lists of Plus Codes.
    LineStringFromPlusCodes : Constructs an ee.Geometry describing a line from a list of
        Plus Codes.
    MultiLineStringFromPlusCodes : Constructs an ee.Geometry describing multiple lines
        from a list of lists of Plus Codes.
    RectangleFromPlusCodes : Constructs an ee.Geometry describing a rectangle from a list
        of two Plus Code corners.

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> geom = ee.Geometry.LinearRingFromPlusCodes(['85FQ2222+22',
    ...                                             '85FR2222+22', '85GR2222+22'])
    >>> geom.coordinates().getInfo()
    [[-104.9999375, 39.0000625],
    [-103.9999375, 39.0000625],
    [-103.9999375, 40.0000625],
    [-104.9999375, 39.0000625]]
    """
    coordinates = _convert_pluscodes_to_lnglats(pluscodes, geocoder, **kwargs)
    return ee.Geometry.LinearRing(coordinates)


@extend(ee.geometry.Geometry, static=True)
def RectangleFromPlusCodes(pluscodes, geocoder="nominatim", **kwargs):
    """Constructs an ee.Geometry describing a rectangle from a list of two Plus Code
    corners.

    If the Plus Codes are full, they will be decoded directly using the openlocationcode
    package. If they are short Codes with reference locations, the references will be
    geocoded using the geopy package.

    Tip
    ----------
    Check more info about constructors in the :ref:`User Guide<Constructors>`.

    Parameters
    ----------
    pluscodes : str
        A list of two full Plus Codes or short Plus Codes with geocodable reference
        locations appended to them describing the corners of the rectangle.
    geocoder : str, default = 'nominatim'
        Geocoder to use. Please visit https://geopy.readthedocs.io/ for more info.
    **kwargs :
        Keywords arguments for geolocator.geocode(). The user_agent argument is mandatory
        (this argument can be set as user_agent = 'my-gee-username' or user_agent =
        'my-gee-app-name'). Please visit https://geopy.readthedocs.io/ for more info.

    Returns
    -------
    ee.Geometry.Rectangle
        Geometry describing a rectangle from the Plus Code centroids.

    See Also
    --------
    PointFromPlusCode : Constructs an ee.Geometry describing a point from a Plus Code.
    MultiPointFromPlusCodes : Constructs an ee.Geometry describing multiple points from a
        list of Plus Codes.
    PolygonFromPlusCodes : Constructs an ee.Geometry describing a polygon from a list of
        Plus Codes.
    MultiPolygonFromPlusCodes : Constructs an ee.Geometry describing multiple polygons
        from a list of lists of Plus Codes.
    LineStringFromPlusCodes : Constructs an ee.Geometry describing a line from a list of
        Plus Codes.
    MultiLineStringFromPlusCodes : Constructs an ee.Geometry describing multiple lines
        from a list of lists of Plus Codes.
    LinearRingFromPlusCodes : Constructs an ee.Geometry describing a linear ring from a
        list of Plus Codes.

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> geom = ee.Geometry.RectangleFromPlusCodes(['85FQ2222+22','85FR2222+22'])
    >>> geom.coordinates().getInfo()
    [[[-104.9999375, 39.0000625],
      [-104.9999375, 39.0000625],
      [-103.9999375, 39.0000625],
      [-103.9999375, 39.0000625],
      [-104.9999375, 39.0000625]]]
    """
    coordinates = _convert_pluscodes_to_lnglats(pluscodes, geocoder, **kwargs)
    return ee.Geometry.Rectangle(coordinates)


@extend(ee.geometry.Geometry, static=False)
def plusCodes(self, codeLength=10):
    """Converts the coordinates of an ee.Geometry to Plus Codes.

    Parameters
    ----------
    self : ee.Geometry
        The geometry to extract coordinates from.
    codeLength : int, default = 10
        The number of significant digits in the output codes, between 2 and 15. Shorter
        codes are less precise.

    Returns
    -------
    list | str
        The coordinates of the geometry converted to Plus Codes. The structure of the Plus
        Codes array will be identical to the structure returned by
        ee.Geometry.coordinates().

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
    plus_codes = _convert_lnglats_to_pluscodes(coordinates, codeLength)
    return plus_codes

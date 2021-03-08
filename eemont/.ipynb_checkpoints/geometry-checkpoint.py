import ee
import geopy
from geopy.geocoders import get_geocoder_for_service

def _extend_staticmethod_eeGeometry():
    """Decorator. Extends the ee.Geometry class with a static method."""
    return lambda f: (setattr(ee.geometry.Geometry,f.__name__,staticmethod(f)) or f)

@_extend_staticmethod_eeGeometry()
def BBoxFromQuery(query,geocoder = "nominatim", **kwargs):
    '''Constructs an ee.Geometry describing a bounding box from a query submitted to a geodocer using the geopy package.
    
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
    
    Examples
    --------
    >>> import ee, eemont
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
    
    See Also
    --------
    PointFromQuery : Constructs an ee.Geometry describing a point from a query submitted to a geodocer using the geopy package.
    MultiPointFromQuery : Constructs an ee.Geometry describing a multi-point from a query submitted to a geodocer using the geopy package.
    '''
    if geocoder in ['nominatim','arcgis']:
        cls = get_geocoder_for_service(geocoder)
    else:
        raise Exception('Invalid geocoder! Use one of "nominatim" or "arcgis".')
    geolocator = cls(**kwargs)
    location = geolocator.geocode(query)
    if location is None:
        raise Exception('No matches were found for your query!')
    else:
        if geocoder == 'nominatim':
            BBox = location.raw['boundingbox']
            return ee.Geometry.BBox(float(BBox[2]),float(BBox[0]),float(BBox[3]),float(BBox[1]))
        elif geocoder == 'arcgis':
            BBox = location.raw['extent']
            return ee.Geometry.BBox(BBox['xmin'],BBox['ymin'],BBox['xmax'],BBox['ymax'])
        else:
            raise Exception('Invalid geocoder! Use one of "nominatim" or "arcgis".')

@_extend_staticmethod_eeGeometry()
def PointFromQuery(query,geocoder = "nominatim", **kwargs):
    '''Constructs an ee.Geometry describing a point from a query submitted to a geodocer using the geopy package. This returns exactly one pair of coordinates.
    
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
    
    Examples
    --------
    >>> import ee, eemont
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
    
    See Also
    --------
    BBoxFromQuery : Constructs an ee.Geometry describing a bounding box from a query submitted to a geodocer using the geopy package.
    MultiPointFromQuery : Constructs an ee.Geometry describing a multi-point from a query submitted to a geodocer using the geopy package.
    '''
    cls = get_geocoder_for_service(geocoder)
    geolocator = cls(**kwargs)
    location = geolocator.geocode(query)
    if location is None:
        raise Exception('No matches were found for your query!')
    else:
        return ee.Geometry.Point([location.longitude,location.latitude])
    
@_extend_staticmethod_eeGeometry()
def MultiPointFromQuery(query,geocoder = "nominatim", **kwargs):
    '''Constructs an ee.Geometry describing a multi-point from a query submitted to a geodocer using the geopy package. This returns all pairs of coordinates retrieved by the query.
    
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
    
    Examples
    --------
    >>> import ee, eemont
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
    
    See Also
    --------
    BBoxFromQuery : Constructs an ee.Geometry describing a bounding box from a query submitted to a geodocer using the geopy package.
    PointFromQuery : Constructs an ee.Geometry describing a point from a query submitted to a geodocer using the geopy package.
    '''
    cls = get_geocoder_for_service(geocoder)
    geolocator = cls(**kwargs)
    locations = geolocator.geocode(query,exactly_one = False)
    if locations is None:
        raise Exception('No matches were found for your query!')
    else:
        coords = []
        for location in locations:
            coords.append([location.longitude,location.latitude])
        return ee.Geometry.MultiPoint(coords)
import ee
import geopy
from geopy.geocoders import get_geocoder_for_service
from .geometry import *

def _extend_staticmethod_eeFeature():
    """Decorator. Extends the ee.Feature class with a static method."""
    return lambda f: (setattr(ee.feature.Feature,f.__name__,staticmethod(f)) or f)

@_extend_staticmethod_eeFeature()
def PointFromQuery(query,geocoder = "nominatim",**kwargs):
    '''Constructs an ee.Feature describing a point from a query submitted to a geodocer using the geopy package. This returns exactly one pair of coordinates.
    The properties of the feature correspond to the raw properties retrieved by the location of the query.
    
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
    ee.Feature
        Feature with a geometry describing a point from the specified query.
    
    Examples
    --------
    >>> import ee, eemont
    >>> ee.Initialize()
    >>> ee.Feature.PointFromQuery('Mt. Rainier, USA',user_agent = 'my-gee-eemont-query').getInfo()
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
      
    See Also
    --------
    BBoxFromQuery : Constructs an ee.Feature describing a bounding box from a query submitted to a geodocer using the geopy package.    
    '''
    cls = get_geocoder_for_service(geocoder)
    geolocator = cls(**kwargs)
    location = geolocator.geocode(query)
    if location == None:
        raise Exception('No matches were found for your query!')
    else:
        geometry = ee.Geometry.Point([location.longitude,location.latitude])
    return ee.Feature(geometry,location.raw)

@_extend_staticmethod_eeFeature()
def BBoxFromQuery(query,geocoder = "nominatim",**kwargs):
    '''Constructs an ee.Feature describing a bounding box from a query submitted to a geodocer using the geopy package.
    The properties of the feature correspond to the raw properties retrieved by the location of the query.
    
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
    ee.Feature
        Feature with a geometry describing a bounding box from the specified query.
    
    Examples
    --------
    >>> import ee, eemont
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
      
    See Also
    --------    
    PointFromQuery : Constructs an ee.Feature describing a point from a query submitted to a geodocer using the geopy package.
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
            geometry = ee.Geometry.BBox(float(BBox[2]),float(BBox[0]),float(BBox[3]),float(BBox[1]))
            return ee.Feature(geometry,location.raw)
        elif geocoder == 'arcgis':
            BBox = location.raw['extent']
            geometry = ee.Geometry.BBox(BBox['xmin'],BBox['ymin'],BBox['xmax'],BBox['ymax'])
            return ee.Feature(geometry,location.raw)
        else:
            raise Exception('Invalid geocoder! Use one of "nominatim" or "arcgis".')
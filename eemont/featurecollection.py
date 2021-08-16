import ee
import geopy
from geopy.geocoders import get_geocoder_for_service

from .common import _retrieve_location
from .extending import extend
from .geometry import *


@extend(ee.featurecollection.FeatureCollection)
def __len__(self):
    """Returns the size of the feature collection.

    Parameters
    ----------
    self : ee.FeatureCollection
        Feature Collection to get the size from.

    Returns
    -------
    int
        Size of the feature collection.
    """
    return self.size().getInfo()


@extend(ee.featurecollection.FeatureCollection)
def __getitem__(self, key):
    """Gets the column of each feature in the feature collection according to the
    specified key.

    Parameters
    ----------
    self : ee.FeatureCollection
        Feature Collection to get the columns from.
    key : string | list[string]
        Key used to get the specified column. If string, it gets the column with that name
        or that matches with regex. If list, it gets multiple columns.

    Returns
    -------
    ee.FeatureCollection
        Feature Collection with the selected columns.
    """
    return self.select(key)


@extend(ee.featurecollection.FeatureCollection, static=True)
def MultiPointFromQuery(query, geocoder="nominatim", **kwargs):
    """Constructs an ee.Feature describing a point from a query submitted to a geodocer
    using the geopy package.

    This returns all pairs of coordinates retrieved by the query. The properties of the
    feature collection correspond to the raw properties retrieved by the locations of
    the query.

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
    ee.FeatureCollection
        Feature Collection with point geometries from the specified query.

    Examples
    --------
    >>> import ee, eemont
    >>> ee.Authenticate()
    >>> ee.Initialize()
    >>> ee.FeatureCollection.MultiPointFromQuery('Río Amazonas',
    ...                                     user_agent = 'my-gee-eemont-query').getInfo()
    {'type': 'FeatureCollection',
     'columns': {'boundingbox': 'List<String>',
      'class': 'String',
      'display_name': 'String',
      'importance': 'Float',
      'lat': 'String',
      'licence': 'String',
      'lon': 'String',
      'osm_id': 'Integer',
      'osm_type': 'String',
      'place_id': 'Integer',
      'system:index': 'String',
      'type': 'String'},
     'features': [{'type': 'Feature',
       'geometry': {'type': 'Point', 'coordinates': [-57.4801276, -2.3740229]},
       'id': '0',
       'properties': {'boundingbox': ['-4.4421898',
         '0.7065296',
         '-73.4501259',
         '-49.2759133'],
        'class': 'waterway',
        'display_name': 'Rio Amazonas, Região Norte, 69100-143, Brasil',
        'importance': 0.4,
        'lat': '-2.3740229',
        'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright',
        'lon': '-57.4801276',
        'osm_id': 2295651,
        'osm_type': 'relation',
        'place_id': 258650987,
        'type': 'river'}},
      {'type': 'Feature',
       'geometry': {'type': 'Point',
        'coordinates': [-70.04978704421745, -4.10958645]},
       'id': '1',
       'properties': {'boundingbox': ['-4.2647706',
         '-3.9548576',
         '-70.1817875',
         '-69.9440055'],
        'class': 'natural',
        'display_name': 'Río Amazonas, Ramón Castilla, Mariscal Ramón Castilla, Loreto, Perú',
        'importance': 0.39999999999999997,
        'lat': '-4.10958645',
        'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright',
        'lon': '-70.04978704421745',
        'osm_id': 8495385,
        'osm_type': 'relation',
        'place_id': 297654614,
        'type': 'water'}},
      ...]}
    """
    locations = _retrieve_location(query, geocoder, False, **kwargs)

    features = []

    for location in locations:
        geometry = ee.Geometry.Point([location.longitude, location.latitude])
        feature = ee.Feature(geometry, location.raw)
        features.append(feature)

    return ee.FeatureCollection(features)

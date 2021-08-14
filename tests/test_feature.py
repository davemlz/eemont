import ee
import unittest
from eemont import feature

ee.Initialize()


class Test(unittest.TestCase):
    """Tests for `eemont` package."""

    def test_Container(self):
        """Test the Container Emulation Methods"""
        test = ee.Feature(ee.Geometry.Point([-76.2, 3.21]), {"property": 1})["property"]
        self.assertIsInstance(test, ee.element.Element)

    def test_BBoxFromQuery(self):
        """Test the BBoxFromQuery constructor"""
        test = ee.Feature.BBoxFromQuery("Colombia", user_agent="eemon-feature-test")
        self.assertIsInstance(test, ee.feature.Feature)

    def test_PointFromQuery(self):
        """Test the BBoxFromQuery constructor"""
        test = ee.Feature.PointFromQuery("Colombia", user_agent="eemon-feature-test")
        self.assertIsInstance(test, ee.feature.Feature)

    def test_pluscodes_from_Point_feature(self):
        """Test that the plus codes returned by a Point feature can construct a new Point"""
        geom = ee.Geometry.Point([-105, 40])
        feature = ee.Feature(geom)
        test = ee.Geometry.PointFromPlusCode(feature.plusCodes())
        self.assertIsInstance(test, ee.geometry.Geometry)

    def test_pluscodes_from_MultiPoint_feature(self):
        """Test that the plus codes returned by a MultiPoint feature can construct a new MultiPoint"""
        coords = [
            [-105, 40],
            [-105, 39],
            [-104, 39],
        ]
        geom = ee.Geometry.MultiPoint(coords)
        feature = ee.Feature(geom)
        test = ee.Geometry.MultiPointFromPlusCodes(feature.plusCodes())
        self.assertIsInstance(test, ee.geometry.Geometry)

    def test_pluscodes_from_Polygon_feature(self):
        """Test that the plus codes returned by a Polygon feature can construct a new Polygon"""
        coords = [
            [-105, 40],
            [-105, 39],
            [-104, 39],
            [-105, 40],
        ]
        geom = ee.Geometry.Polygon(coords)
        feature = ee.Feature(geom)
        test = ee.Geometry.PolygonFromPlusCodes(feature.plusCodes())
        self.assertIsInstance(test, ee.geometry.Geometry)

    def test_pluscodes_from_MultiPolygon_feature(self):
        """Test that the plus codes returned by a MultiPolygon feature can construct a new MultiPolygon"""
        coords = [
            [[-105, 40], [-105, 39], [-104, 39]],
            [[-104, 41], [-104, 40], [-103, 40], [-103, 39]],
        ]
        geom = ee.Geometry.MultiPolygon(coords)
        feature = ee.Feature(geom)
        test = ee.Geometry.MultiPolygonFromPlusCodes(feature.plusCodes())
        self.assertIsInstance(test, ee.geometry.Geometry)

    def test_pluscodes_from_LineString_feature(self):
        """Test that the plus codes returned by a LineString feature can construct a new LineString"""
        coords = [
            [-105, 40],
            [-105, 39],
            [-104, 39],
        ]
        geom = ee.Geometry.LineString(coords)
        feature = ee.Feature(geom)
        test = ee.Geometry.LineStringFromPlusCodes(feature.plusCodes())
        self.assertIsInstance(test, ee.geometry.Geometry)

    def test_pluscodes_from_MultiLineString_feature(self):
        """Test that the plus codes returned by a MultiLineString feature can construct a new MultiLineString"""
        coords = [
            [[-105, 40], [-105, 39], [-104, 39]],
            [[-104, 41], [-104, 40], [-103, 40], [-103, 39]],
        ]
        geom = ee.Geometry.MultiLineString(coords)
        feature = ee.Feature(geom)
        test = ee.Geometry.MultiLineStringFromPlusCodes(feature.plusCodes())
        self.assertIsInstance(test, ee.geometry.Geometry)

    def test_pluscodes_from_LinearRing_feature(self):
        """Test that the plus codes returned by a LinearRing feature can construct a new LinearRing"""
        coords = [[-105, 40], [-105, 39], [-104, 39], [-105, 40]]
        geom = ee.Geometry.LinearRing(coords)
        feature = ee.Feature(geom)
        test = ee.Geometry.LinearRingFromPlusCodes(feature.plusCodes())
        self.assertIsInstance(test, ee.geometry.Geometry)

    def test_pluscodes_from_Rectangle_feature(self):
        """Test that the plus codes returned by a Rectangle feature are a list.

        The Rectangle test does not follow the pattern of the other Geometry tests because unlike other Geometries,
        a Rectangle cannot be constructed from the coordinates that it returns.
        """
        coords = [[-105, 40], [-104, 39]]
        geom = ee.Geometry.Rectangle(coords)
        feature = ee.Feature(geom)
        test = feature.plusCodes()
        self.assertIsInstance(test, list)


if __name__ == "__main__":
    unittest.main()

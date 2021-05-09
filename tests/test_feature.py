import ee
import unittest
from eemont import feature

ee.Initialize()

class Test(unittest.TestCase):
    """Tests for `eemont` package."""
    
    def test_BBoxFromQuery(self):
        """Test the BBoxFromQuery constructor"""
        test = ee.Feature.BBoxFromQuery('Colombia',user_agent = 'eemon-feature-test')
        self.assertIsInstance(test, ee.feature.Feature)
        
    def test_PointFromQuery(self):
        """Test the BBoxFromQuery constructor"""
        test = ee.Feature.PointFromQuery('Colombia',user_agent = 'eemon-feature-test')
        self.assertIsInstance(test, ee.feature.Feature)

    def test_pluscodes_from_Polygon(self):
        """Test that the plus codes returned by a Polygon feature can construct a new Polygon geometry"""
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


if __name__ == '__main__':
    unittest.main()
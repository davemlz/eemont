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

    def test_pluscode_from_point(self):
        """Test that a point ee.Feature returns a plus code string"""
        pt = ee.Feature(ee.Geometry.Point([-105, 40]))
        test = pt.plusCode()
        self.assertIsInstance(test, str)

    def test_pluscode_from_polygon(self):
        """Test that a polygon ee.Feature returns a plus code list of correct length"""
        coords = [
            [-105, 40],
            [-105, 39],
            [-104, 39],
            [-105, 40],
        ]

        poly = ee.Feature(ee.Geometry.Polygon(coords))
        test = poly.plusCode()
        self.assertEqual(len(test), len(coords))

if __name__ == '__main__':
    unittest.main()
import ee
import unittest
from eemont import geometry

ee.Initialize()

class Test(unittest.TestCase):
    """Tests for `eemont` package."""
    
    def test_BBoxFromQuery(self):
        """Test the BBoxFromQuery constructor"""
        test = ee.Geometry.BBoxFromQuery('Colombia',user_agent = 'eemon-feature-test')
        self.assertIsInstance(test, ee.geometry.Geometry)
        
    def test_PointFromQuery(self):
        """Test the PointFromQuery constructor"""
        test = ee.Geometry.PointFromQuery('Colombia',user_agent = 'eemon-feature-test')
        self.assertIsInstance(test, ee.geometry.Geometry)
        
    def test_MultiPointFromQuery(self):
        """Test the MultiPointFromQuery constructor"""
        test = ee.Geometry.MultiPointFromQuery('Colombia',user_agent = 'eemon-feature-test')
        self.assertIsInstance(test, ee.geometry.Geometry)
        
    def test_PointFromFullPlusCode(self):
        """Test the PointFromPlusCode constructor with a full plus code"""
        code = "85FPQXGV+XH"
        test = ee.Geometry.PointFromPlusCode(code, user_agent = 'eemont-feature-test')
        self.assertIsInstance(test, ee.geometry.Geometry)
    
    def test_PointFromShortPlusCode(self):
        """Test the PointFromPlusCode constructor with a short plus code"""
        code = "QXGV+XH Denver, CO, USA"
        test = ee.Geometry.PointFromPlusCode(code, user_agent = 'eemont-feature-test')
        self.assertIsInstance(test, ee.geometry.Geometry)
    
    def test_MultiPointFromPlusCode(self):
        """Test the MultiPointFromPlusCode constructor with a list of plus codes"""
        codes = [
            '85FQ2222+22', 
            '85FR2222+22', 
            '85GR2222+22', 
        ]
        test = ee.Geometry.MultiPointFromPlusCode(codes, user_agent = 'eemont-feature-test')
        self.assertIsInstance(test, ee.geometry.Geometry)

    def test_pluscode_from_point(self):
        """Test that an ee.Geometry.Point returns a plus code string"""
        pt = ee.Geometry.Point([-105, 40])
        test = pt.plusCode()
        self.assertIsInstance(test, str)

    def test_pluscode_from_polygon(self):
        """Test that an ee.Geometry.Polygon returns a plus code list of correct length"""
        poly = ee.Geometry.Polygon([
            [-105, 40],
            [-105, 39],
            [-104, 39],
            [-104, 40],
            [-105, 40],
        ])
        test = poly.plusCode()
        self.assertEqual(len(test), 5)


if __name__ == '__main__':
    unittest.main()
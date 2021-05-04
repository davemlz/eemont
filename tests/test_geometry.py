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

if __name__ == '__main__':
    unittest.main()
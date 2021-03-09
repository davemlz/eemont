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
        
if __name__ == '__main__':
    unittest.main()
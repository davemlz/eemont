import ee
import unittest
from eemont import featurecollection

ee.Initialize()

class Test(unittest.TestCase):
    """Tests for `eemont` package."""
        
    def test_MultiPointFromQuery(self):
        """Test the MultiPointFromQuery constructor"""
        test = ee.FeatureCollection.MultiPointFromQuery('Colombia',user_agent = 'eemon-feature-test')
        self.assertIsInstance(test, ee.featurecollection.FeatureCollection)
        
if __name__ == '__main__':
    unittest.main()
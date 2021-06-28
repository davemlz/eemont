import ee
import unittest
from eemont import featurecollection

ee.Initialize()

class Test(unittest.TestCase):
    """Tests for `eemont` package."""
        
    def test_Container_Get_Item(self):
        """Test the Container Emulation Methods"""
        test = ee.FeatureCollection("WCMC/WDPA/current/polygons")[["WDPAID","NAME"]]["NAME"]
        self.assertIsInstance(test, ee.featurecollection.FeatureCollection)
        
    def test_Container_Length(self):
        """Test the Container Emulation Methods"""
        test = len(ee.FeatureCollection("WCMC/WDPA/current/polygons"))
        self.assertIsInstance(test, int)
        
    def test_MultiPointFromQuery(self):
        """Test the MultiPointFromQuery constructor"""
        test = ee.FeatureCollection.MultiPointFromQuery('Colombia',user_agent = 'eemon-feature-test')
        self.assertIsInstance(test, ee.featurecollection.FeatureCollection)
        
if __name__ == '__main__':
    unittest.main()
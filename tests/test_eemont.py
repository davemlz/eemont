import ee
import unittest
from eemont import Sentinel2, visualization

ee.Initialize()

S2 = ee.ImageCollection('COPERNICUS/S2_SR').filterDate('2020-01-01','2020-01-10').limit(10)

class Test(unittest.TestCase):
    """Tests for `eemont` package."""
    
    def test_Sentinel2_cloudMask_01(self):
        """Test the cloud mask function returns an Image Collection"""        
        self.assertIsInstance(Sentinel2.cloudMask(S2), ee.imagecollection.ImageCollection)
        
    def test_Sentinel2_cloudMask_02(self):
        """Test the cloud mask function returns an Image"""        
        self.assertIsInstance(Sentinel2.cloudMask(S2.first()), ee.image.Image)
        
    def test_Sentinel2_reflectance_01(self):
        """Test the cloud mask function returns an Image Collection"""        
        self.assertIsInstance(Sentinel2.reflectance(S2), ee.imagecollection.ImageCollection)
        
    def test_Sentinel2_reflectance_02(self):
        """Test the cloud mask function returns an Image"""        
        self.assertIsInstance(Sentinel2.reflectance(S2.first()), ee.image.Image)
        
    def test_Sentinel2_spectralIndex_01(self):
        """Test the cloud mask function returns an Image Collection"""        
        self.assertIsInstance(Sentinel2.spectralIndex(S2), ee.imagecollection.ImageCollection)
        
    def test_Sentinel2_spectralIndex_02(self):
        """Test the cloud mask function returns an Image"""        
        self.assertIsInstance(Sentinel2.spectralIndex(S2.first()), ee.image.Image)
        
    def test_visualization_rgb(self):
        """Test the visualization function returns a dictionary"""        
        self.assertIsInstance(visualization.rgb(), dict)
        
    def test_visualization_infrared(self):
        """Test the visualization function returns a dictionary"""        
        self.assertIsInstance(visualization.infrared(), dict)
        
    def test_visualization_landwater(self):
        """Test the visualization function returns a dictionary"""        
        self.assertIsInstance(visualization.landwater(), dict)
        
    def test_visualization_vegetation(self):
        """Test the visualization function returns a dictionary"""        
        self.assertIsInstance(visualization.vegetation(), dict)
        
    def test_visualization_index(self):
        """Test the visualization function returns a dictionary"""        
        self.assertIsInstance(visualization.index(), dict)
        
if __name__ == '__main__':
    unittest.main()
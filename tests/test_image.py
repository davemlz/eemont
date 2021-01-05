import ee
import unittest
from eemont import image

ee.Initialize()

S2 = ee.ImageCollection('COPERNICUS/S2_SR').first()
L8 = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR').first()
L7 = ee.ImageCollection('LANDSAT/LE07/C01/T1_SR').first()
L5 = ee.ImageCollection('LANDSAT/LT05/C01/T1_SR').first()
L4 = ee.ImageCollection('LANDSAT/LT04/C01/T1_SR').first()

indices = ['NDVI','BAIS2']

class Test(unittest.TestCase):
    """Tests for `eemont` package."""
    
    def test_S2(self):
        """Test the image module for Sentinel-2"""
        S2_tested = S2.maskClouds().scale().index(indices)
        self.assertIsInstance(S2_tested, ee.image.Image)
        
    def test_L8(self):
        """Test the image module for Landsat 8"""
        L8_tested = L8.maskClouds().scale().index(indices)
        self.assertIsInstance(L8_tested, ee.image.Image)
        
    def test_L7(self):
        """Test the image module for Landsat 7"""
        L7_tested = L7.maskClouds().scale().index(indices)
        self.assertIsInstance(L7_tested, ee.image.Image)
        
    def test_L5(self):
        """Test the image module for Landsat 5"""
        L5_tested = L5.maskClouds().scale().index(indices)
        self.assertIsInstance(L5_tested, ee.image.Image)
        
    def test_L4(self):
        """Test the image module for Landsat 4"""
        L4_tested = L4.maskClouds().scale().index(indices)
        self.assertIsInstance(L4_tested, ee.image.Image)
        
if __name__ == '__main__':
    unittest.main()
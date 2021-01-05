import ee
import unittest
from eemont import imagecollection

ee.Initialize()

point = ee.Geometry.Point([-76.21,3.45])

S2 = ee.ImageCollection('COPERNICUS/S2_SR').filterBounds(point)
L8 = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR').filterBounds(point)
L7 = ee.ImageCollection('LANDSAT/LE07/C01/T1_SR').filterBounds(point)
L5 = ee.ImageCollection('LANDSAT/LT05/C01/T1_SR').filterBounds(point)
L4 = ee.ImageCollection('LANDSAT/LT04/C01/T1_SR').filterBounds(point)

indices = ['NDVI','BAIS2']

class Test(unittest.TestCase):
    """Tests for `eemont` package."""
    
    def test_S2(self):
        """Test the image collection module for Sentinel-2"""
        S2_tested = S2.closest('2020-01-15').maskClouds().scale().index(indices)
        self.assertIsInstance(S2_tested, ee.imagecollection.ImageCollection)
        
    def test_L8(self):
        """Test the image collection module for Landsat 8"""
        L8_tested = L8.closest('2020-01-15').maskClouds().scale().index(indices)
        self.assertIsInstance(L8_tested, ee.imagecollection.ImageCollection)
        
    def test_L7(self):
        """Test the image collection module for Landsat 7"""
        L7_tested = L7.closest('2010-01-15').maskClouds().scale().index(indices)
        self.assertIsInstance(L7_tested, ee.imagecollection.ImageCollection)
        
    def test_L5(self):
        """Test the image collection module for Landsat 5"""
        L5_tested = L5.closest('2000-01-15').maskClouds().scale().index(indices)
        self.assertIsInstance(L5_tested, ee.imagecollection.ImageCollection)
        
    def test_L4(self):
        """Test the image collection module for Landsat 4"""
        L4_tested = L4.closest('1990-01-15').maskClouds().scale().index(indices)
        self.assertIsInstance(L4_tested, ee.imagecollection.ImageCollection)
        
if __name__ == '__main__':
    unittest.main()
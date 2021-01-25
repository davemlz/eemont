import ee
import unittest
from eemont import imagecollection

ee.Initialize()

point = ee.Geometry.Point([-76.21,3.45])

S3 = ee.ImageCollection('COPERNICUS/S3/OLCI').filterBounds(point)
S2 = ee.ImageCollection('COPERNICUS/S2_SR').filterBounds(point)
L8 = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR').filterBounds(point)
L7 = ee.ImageCollection('LANDSAT/LE07/C01/T1_SR').filterBounds(point)
L5 = ee.ImageCollection('LANDSAT/LT05/C01/T1_SR').filterBounds(point)
L4 = ee.ImageCollection('LANDSAT/LT04/C01/T1_SR').filterBounds(point)
MCD43A4 = ee.ImageCollection('MODIS/006/MCD43A4').filterBounds(point)
MCD43A3 = ee.ImageCollection('MODIS/006/MCD43A3').filterBounds(point)
MOD09GQ = ee.ImageCollection('MODIS/006/MOD09GQ').filterBounds(point)
MOD10A1 = ee.ImageCollection('MODIS/006/MOD10A1').filterBounds(point)
MOD11A1 = ee.ImageCollection('MODIS/006/MOD11A1').filterBounds(point)
MOD09GA = ee.ImageCollection('MODIS/006/MOD09GA').filterBounds(point)
MODOCGA = ee.ImageCollection('MODIS/006/MODOCGA').filterBounds(point)
MOD14A1 = ee.ImageCollection('MODIS/006/MOD14A1').filterBounds(point)
MCD43A1 = ee.ImageCollection('MODIS/006/MCD43A1').filterBounds(point)
MCD15A3H = ee.ImageCollection('MODIS/006/MCD15A3H').filterBounds(point)
MOD09Q1 = ee.ImageCollection('MODIS/006/MOD09Q1').filterBounds(point)
MOD09A1 = ee.ImageCollection('MODIS/006/MOD09A1').filterBounds(point)
MOD11A2 = ee.ImageCollection('MODIS/006/MOD11A2').filterBounds(point)
MOD17A2H = ee.ImageCollection('MODIS/006/MOD17A2H').filterBounds(point)
MOD16A2 = ee.ImageCollection('MODIS/006/MOD16A2').filterBounds(point)
MOD13Q1 = ee.ImageCollection('MODIS/006/MOD13Q1').filterBounds(point)
MOD13A1 = ee.ImageCollection('MODIS/006/MOD13A1').filterBounds(point)
MOD13A2 = ee.ImageCollection('MODIS/006/MOD13A2').filterBounds(point)
MOD08_M3 = ee.ImageCollection('MODIS/061/MOD08_M3').filterBounds(point)
MOD17A3HGF = ee.ImageCollection('MODIS/006/MOD17A3HGF').filterBounds(point)

indices = ['NDVI','BAIS2']

class Test(unittest.TestCase):
    """Tests for `eemont` package."""
    
    def test_S3(self):
        """Test the image collection module for Sentinel-3"""
        S3_tested = S3.closest('2020-01-15').maskClouds().scale()
        self.assertIsInstance(S3_tested, ee.imagecollection.ImageCollection)
    
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
        L5_tested = L5.closest('2000-01-15',2,'year').maskClouds().scale().index(indices)
        self.assertIsInstance(L5_tested, ee.imagecollection.ImageCollection)
        
    def test_L4(self):
        """Test the image collection module for Landsat 4"""
        L4_tested = L4.closest('1990-01-15').maskClouds().scale().index(indices)
        self.assertIsInstance(L4_tested, ee.imagecollection.ImageCollection)
        
    def test_MCD43A4(self):
        """Test the image collection module for MCD43A4"""
        MCD43A4_tested = MCD43A4.closest('2020-01-15').scale()
        self.assertIsInstance(MCD43A4_tested, ee.imagecollection.ImageCollection)
        
    def test_MCD43A3(self):
        """Test the image collection module for MCD43A3"""
        MCD43A3_tested = MCD43A3.closest('2020-01-15').scale()
        self.assertIsInstance(MCD43A3_tested, ee.imagecollection.ImageCollection)
        
    def test_MOD09GQ(self):
        """Test the image collection module for MOD09GQ"""
        MOD09GQ_tested = MOD09GQ.closest('2020-01-15').scale()
        self.assertIsInstance(MOD09GQ_tested, ee.imagecollection.ImageCollection)
        
    def test_MOD10A1(self):
        """Test the image collection module for MOD10A1"""
        MOD10A1_tested = MOD10A1.closest('2020-01-15').scale()
        self.assertIsInstance(MOD10A1_tested, ee.imagecollection.ImageCollection)
        
    def test_MOD11A1(self):
        """Test the image collection module for MOD11A1"""
        MOD11A1_tested = MOD11A1.closest('2020-01-15').scale()
        self.assertIsInstance(MOD11A1_tested, ee.imagecollection.ImageCollection)
        
    def test_MOD09GA(self):
        """Test the image collection module for MOD09GA"""
        MOD09GA_tested = MOD09GA.closest('2020-01-15').maskClouds().scale()
        self.assertIsInstance(MOD09GA_tested, ee.imagecollection.ImageCollection)
        
    def test_MODOCGA(self):
        """Test the image collection module for MODOCGA"""
        MODOCGA_tested = MODOCGA.closest('2020-01-15').scale()
        self.assertIsInstance(MODOCGA_tested, ee.imagecollection.ImageCollection)
        
    def test_MOD14A1(self):
        """Test the image collection module for MOD14A1"""
        MOD14A1_tested = MOD14A1.closest('2020-01-15').scale()
        self.assertIsInstance(MOD14A1_tested, ee.imagecollection.ImageCollection)
        
    def test_MCD43A1(self):
        """Test the image collection module for MCD43A1"""
        MCD43A1_tested = MCD43A1.closest('2020-01-15').scale()
        self.assertIsInstance(MCD43A1_tested, ee.imagecollection.ImageCollection)
        
    def test_MCD15A3H(self):
        """Test the image collection module for MCD15A3H"""
        MCD15A3H_tested = MCD15A3H.closest('2020-01-15').maskClouds().scale()
        self.assertIsInstance(MCD15A3H_tested, ee.imagecollection.ImageCollection)
        
    def test_MOD09Q1(self):
        """Test the image collection module for MOD09Q1"""
        MOD09Q1_tested = MOD09Q1.closest('2020-01-15').maskClouds().scale()
        self.assertIsInstance(MOD09Q1_tested, ee.imagecollection.ImageCollection)
        
    def test_MOD09A1(self):
        """Test the image collection module for MOD09A1"""
        MOD09A1_tested = MOD09A1.closest('2020-01-15').maskClouds().scale()
        self.assertIsInstance(MOD09A1_tested, ee.imagecollection.ImageCollection)
        
    def test_MOD11A2(self):
        """Test the image collection module for MOD11A2"""
        MOD11A2_tested = MOD11A2.closest('2020-01-15').scale()
        self.assertIsInstance(MOD11A2_tested, ee.imagecollection.ImageCollection)
        
    def test_MOD17A2H(self):
        """Test the image collection module for MOD17A2H"""
        MOD17A2H_tested = MOD17A2H.closest('2020-01-15').maskClouds().scale()
        self.assertIsInstance(MOD17A2H_tested, ee.imagecollection.ImageCollection)
        
    def test_MOD16A2(self):
        """Test the image collection module for MOD16A2"""
        MOD16A2_tested = MOD16A2.closest('2020-01-15').maskClouds().scale()
        self.assertIsInstance(MOD16A2_tested, ee.imagecollection.ImageCollection)
    
    def test_MOD13Q1(self):
        """Test the image collection module for MOD13Q1"""
        MOD13Q1_tested = MOD13Q1.closest('2020-01-15').maskClouds().scale()
        self.assertIsInstance(MOD13Q1_tested, ee.imagecollection.ImageCollection)
        
    def test_MOD13A1(self):
        """Test the image collection module for MOD13A1"""
        MOD13A1_tested = MOD13A1.closest('2020-01-15').maskClouds().scale()
        self.assertIsInstance(MOD13A1_tested, ee.imagecollection.ImageCollection)
        
    def test_MOD13A2(self):
        """Test the image collection module for MOD13A2"""
        MOD13A2_tested = MOD13A2.closest('2020-01-15').maskClouds().scale()
        self.assertIsInstance(MOD13A2_tested, ee.imagecollection.ImageCollection)
        
    def test_MOD08_M3(self):
        """Test the image collection module for MOD08_M3"""
        MOD08_M3_tested = MOD08_M3.closest('2020-01-15').scale()
        self.assertIsInstance(MOD08_M3_tested, ee.imagecollection.ImageCollection)
        
    def test_MOD17A3HGF(self):
        """Test the image collection module for MOD17A3HGF"""
        MOD17A3HGF_tested = MOD17A3HGF.closest('2019-01-15').scale()
        self.assertIsInstance(MOD17A3HGF_tested, ee.imagecollection.ImageCollection)
        
if __name__ == '__main__':
    unittest.main()
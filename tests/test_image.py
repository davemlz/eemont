import ee
import unittest
from eemont import image

ee.Initialize()

S3 = ee.ImageCollection('COPERNICUS/S3/OLCI').first()
S2 = ee.ImageCollection('COPERNICUS/S2_SR').first()
L8 = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR').first()
L7 = ee.ImageCollection('LANDSAT/LE07/C01/T1_SR').first()
L5 = ee.ImageCollection('LANDSAT/LT05/C01/T1_SR').first()
L4 = ee.ImageCollection('LANDSAT/LT04/C01/T1_SR').first()
MCD43A4 = ee.ImageCollection('MODIS/006/MCD43A4').first()
MCD43A3 = ee.ImageCollection('MODIS/006/MCD43A3').first()
MOD09GQ = ee.ImageCollection('MODIS/006/MOD09GQ').first()
MOD10A1 = ee.ImageCollection('MODIS/006/MOD10A1').first()
MOD11A1 = ee.ImageCollection('MODIS/006/MOD11A1').first()
MOD09GA = ee.ImageCollection('MODIS/006/MOD09GA').first()
MODOCGA = ee.ImageCollection('MODIS/006/MODOCGA').first()
MOD14A1 = ee.ImageCollection('MODIS/006/MOD14A1').first()
MCD43A1 = ee.ImageCollection('MODIS/006/MCD43A1').first()
MCD15A3H = ee.ImageCollection('MODIS/006/MCD15A3H').first()
MOD09Q1 = ee.ImageCollection('MODIS/006/MOD09Q1').first()
MOD09A1 = ee.ImageCollection('MODIS/006/MOD09A1').first()
MOD11A2 = ee.ImageCollection('MODIS/006/MOD11A2').first()
MOD17A2H = ee.ImageCollection('MODIS/006/MOD17A2H').first()
MOD16A2 = ee.ImageCollection('MODIS/006/MOD16A2').first()
MOD13Q1 = ee.ImageCollection('MODIS/006/MOD13Q1').first()
MOD13A1 = ee.ImageCollection('MODIS/006/MOD13A1').first()
MOD13A2 = ee.ImageCollection('MODIS/006/MOD13A2').first()
MOD08_M3 = ee.ImageCollection('MODIS/061/MOD08_M3').first()
MOD17A3HGF = ee.ImageCollection('MODIS/006/MOD17A3HGF').first()

indices = ['NDVI','BAIS2']

class Test(unittest.TestCase):
    """Tests for `eemont` package."""
    
    def test_S3(self):
        """Test the image module for Sentinel-3"""
        S3_tested = S3.maskClouds().scale()
        self.assertIsInstance(S3_tested, ee.image.Image)
    
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
    
    def test_MCD43A4(self):
        """Test the image module for MCD43A4"""
        MCD43A4_tested = MCD43A4.scale()
        self.assertIsInstance(MCD43A4_tested, ee.image.Image)
        
    def test_MCD43A3(self):
        """Test the image module for MCD43A3"""
        MCD43A3_tested = MCD43A3.scale()
        self.assertIsInstance(MCD43A3_tested, ee.image.Image)
        
    def test_MOD09GQ(self):
        """Test the image module for MOD09GQ"""
        MOD09GQ_tested = MOD09GQ.scale()
        self.assertIsInstance(MOD09GQ_tested, ee.image.Image)
        
    def test_MOD10A1(self):
        """Test the image module for MOD10A1"""
        MOD10A1_tested = MOD10A1.scale()
        self.assertIsInstance(MOD10A1_tested, ee.image.Image)
        
    def test_MOD11A1(self):
        """Test the image module for MOD11A1"""
        MOD11A1_tested = MOD11A1.scale()
        self.assertIsInstance(MOD11A1_tested, ee.image.Image)
        
    def test_MOD09GA(self):
        """Test the image module for MOD09GA"""
        MOD09GA_tested = MOD09GA.maskClouds().scale()
        self.assertIsInstance(MOD09GA_tested, ee.image.Image)
        
    def test_MODOCGA(self):
        """Test the image module for MODOCGA"""
        MODOCGA_tested = MODOCGA.scale()
        self.assertIsInstance(MODOCGA_tested, ee.image.Image)
        
    def test_MOD14A1(self):
        """Test the image module for MOD14A1"""
        MOD14A1_tested = MOD14A1.scale()
        self.assertIsInstance(MOD14A1_tested, ee.image.Image)
        
    def test_MCD43A1(self):
        """Test the image module for MCD43A1"""
        MCD43A1_tested = MCD43A1.scale()
        self.assertIsInstance(MCD43A1_tested, ee.image.Image)
        
    def test_MCD15A3H(self):
        """Test the image module for MCD15A3H"""
        MCD15A3H_tested = MCD15A3H.maskClouds().scale()
        self.assertIsInstance(MCD15A3H_tested, ee.image.Image)
        
    def test_MOD09Q1(self):
        """Test the image module for MOD09Q1"""
        MOD09Q1_tested = MOD09Q1.maskClouds().scale()
        self.assertIsInstance(MOD09Q1_tested, ee.image.Image)
        
    def test_MOD09A1(self):
        """Test the image module for MOD09A1"""
        MOD09A1_tested = MOD09A1.maskClouds().scale()
        self.assertIsInstance(MOD09A1_tested, ee.image.Image)
        
    def test_MOD11A2(self):
        """Test the image module for MOD11A2"""
        MOD11A2_tested = MOD11A2.scale()
        self.assertIsInstance(MOD11A2_tested, ee.image.Image)
        
    def test_MOD17A2H(self):
        """Test the image module for MOD17A2H"""
        MOD17A2H_tested = MOD17A2H.maskClouds().scale()
        self.assertIsInstance(MOD17A2H_tested, ee.image.Image)
        
    def test_MOD16A2(self):
        """Test the image module for MOD16A2"""
        MOD16A2_tested = MOD16A2.maskClouds().scale()
        self.assertIsInstance(MOD16A2_tested, ee.image.Image)
    
    def test_MOD13Q1(self):
        """Test the image module for MOD13Q1"""
        MOD13Q1_tested = MOD13Q1.maskClouds().scale()
        self.assertIsInstance(MOD13Q1_tested, ee.image.Image)
        
    def test_MOD13A1(self):
        """Test the image module for MOD13A1"""
        MOD13A1_tested = MOD13A1.maskClouds().scale()
        self.assertIsInstance(MOD13A1_tested, ee.image.Image)
        
    def test_MOD13A2(self):
        """Test the image module for MOD13A2"""
        MOD13A2_tested = MOD13A2.maskClouds().scale()
        self.assertIsInstance(MOD13A2_tested, ee.image.Image)
        
    def test_MOD08_M3(self):
        """Test the image module for MOD08_M3"""
        MOD08_M3_tested = MOD08_M3.scale()
        self.assertIsInstance(MOD08_M3_tested, ee.image.Image)
        
    def test_MOD17A3HGF(self):
        """Test the image module for MOD17A3HGF"""
        MOD17A3HGF_tested = MOD17A3HGF.scale()
        self.assertIsInstance(MOD17A3HGF_tested, ee.image.Image)
        
if __name__ == '__main__':
    unittest.main()
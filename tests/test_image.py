import ee
import unittest
from eemont import image

ee.Initialize()

# SENTINEL MISSIONS
S3 = ee.ImageCollection('COPERNICUS/S3/OLCI').first()
S2 = ee.ImageCollection('COPERNICUS/S2_SR').first()

# LANDSAT MISSIONS
L8 = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR').first()
L8C2 = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2').first()
L7 = ee.ImageCollection('LANDSAT/LE07/C01/T1_SR').first()
L7C2 = ee.ImageCollection('LANDSAT/LE07/C02/T1_L2').first()
L5 = ee.ImageCollection('LANDSAT/LT05/C01/T1_SR').first()
L4 = ee.ImageCollection('LANDSAT/LT04/C01/T1_SR').first()

# MODIS (TERRA + AQUA)
MCD43A4 = ee.ImageCollection('MODIS/006/MCD43A4').first()
MCD43A3 = ee.ImageCollection('MODIS/006/MCD43A3').first()
MCD43A1 = ee.ImageCollection('MODIS/006/MCD43A1').first()
MCD15A3H = ee.ImageCollection('MODIS/006/MCD15A3H').first()

# MODIS (TERRA)
MOD09GQ = ee.ImageCollection('MODIS/006/MOD09GQ').first()
MOD10A1 = ee.ImageCollection('MODIS/006/MOD10A1').first()
MOD11A1 = ee.ImageCollection('MODIS/006/MOD11A1').first()
MOD09GA = ee.ImageCollection('MODIS/006/MOD09GA').first()
MODOCGA = ee.ImageCollection('MODIS/006/MODOCGA').first()
MOD14A1 = ee.ImageCollection('MODIS/006/MOD14A1').first()
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

# MODIS (AQUA)
MYD09GQ = ee.ImageCollection('MODIS/006/MYD09GQ').first()
MYD10A1 = ee.ImageCollection('MODIS/006/MYD10A1').first()
MYD11A1 = ee.ImageCollection('MODIS/006/MYD11A1').first()
MYD09GA = ee.ImageCollection('MODIS/006/MYD09GA').first()
MYDOCGA = ee.ImageCollection('MODIS/006/MYDOCGA').first()
MYD14A1 = ee.ImageCollection('MODIS/006/MYD14A1').first()
MYD09Q1 = ee.ImageCollection('MODIS/006/MYD09Q1').first()
MYD09A1 = ee.ImageCollection('MODIS/006/MYD09A1').first()
MYD11A2 = ee.ImageCollection('MODIS/006/MYD11A2').first()
MYD17A2H = ee.ImageCollection('MODIS/006/MYD17A2H').first()
MYD16A2 = ee.ImageCollection('MODIS/006/MYD16A2').first()
MYD13Q1 = ee.ImageCollection('MODIS/006/MYD13Q1').first()
MYD13A1 = ee.ImageCollection('MODIS/006/MYD13A1').first()
MYD13A2 = ee.ImageCollection('MODIS/006/MYD13A2').first()
MYD08_M3 = ee.ImageCollection('MODIS/061/MYD08_M3').first()
MYD17A3HGF = ee.ImageCollection('MODIS/006/MYD17A3HGF').first()

indices = 'all'

class Test(unittest.TestCase):
    """Tests for `eemont` package."""

    # CONTAINER EMULATION METHODS
    
    def test_Container_Get_Item_By_Key(self):
        """Test the Container Emulation Methods"""
        test = S2[['B.*']]['B1']
        self.assertIsInstance(test, ee.image.Image)
        
    def test_Container_Get_Item_By_Index(self):
        """Test the Container Emulation Methods"""
        test = S2[1]
        self.assertIsInstance(test, ee.image.Image)
        
    def test_Container_Get_Item_By_Slice(self):
        """Test the Container Emulation Methods"""
        test = S2[0:3]
        self.assertIsInstance(test, ee.image.Image)
    
    # OVERLOADED OPERATIONS
    
    def test_binary1(self):
        """Test the image module for binary operators 1"""
        binary1_tested = ee.Image(1) + 0 - 0 * 1 / 1 // 1 % 1 ** 1 << 1 >> 1
        self.assertIsInstance(binary1_tested, ee.image.Image)
        
    def test_binary2(self):
        """Test the image module for binary operators 2"""
        binary2_tested_a = (ee.Image(1) > 1) & (ee.Image(1) < 1)
        binary2_tested_b = (ee.Image(1) >= 1) | (ee.Image(1) <= 1)
        binary2_tested_c = (ee.Image(1) == 1) & (ee.Image(1) != 1)
        binary2_tested = binary2_tested_a + binary2_tested_b + binary2_tested_c
        self.assertIsInstance(binary2_tested, ee.image.Image)
        
    def test_unary(self):
        """Test the image module for unary operators"""
        unary_tested_a = - ee.Image(1)
        unary_tested_b = ~ ee.Image(1)
        unary_tested = unary_tested_a + unary_tested_b
        self.assertIsInstance(unary_tested, ee.image.Image)
    
    # SENTINEL MISSIONS
    
    def test_S3(self):
        """Test the image module for Sentinel-3"""
        S3_tested = S3.maskClouds().scaleAndOffset()
        self.assertIsInstance(S3_tested, ee.image.Image)
    
    def test_S2(self):
        """Test the image module for Sentinel-2"""
        S2_tested = S2.maskClouds().scaleAndOffset().spectralIndices(indices)
        self.assertIsInstance(S2_tested, ee.image.Image)
        
    def test_S2_STAC(self):
        """Test the image module for Sentinel-2"""
        S2_tested = S2.getSTAC()
        self.assertIsInstance(S2_tested, dict)
        
    def test_S2_DOI(self):
        """Test the image module for Sentinel-2"""
        S2_tested = S2.getDOI()
        self.assertIsInstance(S2_tested, str)
        
    def test_S2_Citation(self):
        """Test the image module for Sentinel-2"""
        S2_tested = S2.getCitation()
        self.assertIsInstance(S2_tested, str)
        
    def test_S2_online(self):
        """Test the image module for Sentinel-2"""
        S2_tested = S2.maskClouds().scaleAndOffset().spectralIndices(indices,online = True)
        self.assertIsInstance(S2_tested, ee.image.Image)
        
    def test_S2_previous(self):
        """Test the image module for Sentinel-2"""
        S2_tested = S2.maskClouds().scale().index(indices,online = True)
        self.assertIsInstance(S2_tested, ee.image.Image)
        
    # LANDSAT MISSIONS
        
    def test_L8(self):
        """Test the image module for Landsat 8"""
        L8_tested = L8.maskClouds().scaleAndOffset().spectralIndices(indices)
        self.assertIsInstance(L8_tested, ee.image.Image)
        
    def test_L8C2(self):
        """Test the image module for Landsat 8"""
        L8_tested = L8C2.maskClouds().scaleAndOffset().spectralIndices(indices)
        self.assertIsInstance(L8_tested, ee.image.Image)
        
    def test_L7(self):
        """Test the image module for Landsat 7"""
        L7_tested = L7.maskClouds().scaleAndOffset().spectralIndices(indices)
        self.assertIsInstance(L7_tested, ee.image.Image)
        
    def test_L7C2(self):
        """Test the image module for Landsat 7"""
        L7_tested = L7C2.maskClouds().scaleAndOffset().spectralIndices(indices)
        self.assertIsInstance(L7_tested, ee.image.Image)
        
    def test_L5(self):
        """Test the image module for Landsat 5"""
        L5_tested = L5.maskClouds().scaleAndOffset().spectralIndices(indices)
        self.assertIsInstance(L5_tested, ee.image.Image)
                
    def test_L4(self):
        """Test the image module for Landsat 4"""
        L4_tested = L4.maskClouds().scaleAndOffset().spectralIndices(indices)
        self.assertIsInstance(L4_tested, ee.image.Image)
    
    # MODIS (TERRA + AQUA)
    
    def test_MCD43A4(self):
        """Test the image module for MCD43A4"""
        MCD43A4_tested = MCD43A4.scaleAndOffset().spectralIndices(indices)
        self.assertIsInstance(MCD43A4_tested, ee.image.Image)
        
    def test_MCD43A3(self):
        """Test the image module for MCD43A3"""
        MCD43A3_tested = MCD43A3.scaleAndOffset()
        self.assertIsInstance(MCD43A3_tested, ee.image.Image)
        
    def test_MCD43A1(self):
        """Test the image module for MCD43A1"""
        MCD43A1_tested = MCD43A1.scaleAndOffset()
        self.assertIsInstance(MCD43A1_tested, ee.image.Image)
        
    def test_MCD15A3H(self):
        """Test the image module for MCD15A3H"""
        MCD15A3H_tested = MCD15A3H.maskClouds().scaleAndOffset()
        self.assertIsInstance(MCD15A3H_tested, ee.image.Image)
        
    # MODIS (TERRA)
        
    def test_MOD09GQ(self):
        """Test the image module for MOD09GQ"""
        MOD09GQ_tested = MOD09GQ.scaleAndOffset().spectralIndices(indices)
        self.assertIsInstance(MOD09GQ_tested, ee.image.Image)
        
    def test_MOD10A1(self):
        """Test the image module for MOD10A1"""
        MOD10A1_tested = MOD10A1.scaleAndOffset()
        self.assertIsInstance(MOD10A1_tested, ee.image.Image)
        
    def test_MOD11A1(self):
        """Test the image module for MOD11A1"""
        MOD11A1_tested = MOD11A1.scaleAndOffset()
        self.assertIsInstance(MOD11A1_tested, ee.image.Image)
        
    def test_MOD09GA(self):
        """Test the image module for MOD09GA"""
        MOD09GA_tested = MOD09GA.maskClouds().scaleAndOffset().spectralIndices(indices)
        self.assertIsInstance(MOD09GA_tested, ee.image.Image)
        
    def test_MODOCGA(self):
        """Test the image module for MODOCGA"""
        MODOCGA_tested = MODOCGA.scaleAndOffset()
        self.assertIsInstance(MODOCGA_tested, ee.image.Image)
        
    def test_MOD14A1(self):
        """Test the image module for MOD14A1"""
        MOD14A1_tested = MOD14A1.scaleAndOffset()
        self.assertIsInstance(MOD14A1_tested, ee.image.Image)
        
    def test_MOD09Q1(self):
        """Test the image module for MOD09Q1"""
        MOD09Q1_tested = MOD09Q1.maskClouds().scaleAndOffset().spectralIndices(indices)
        self.assertIsInstance(MOD09Q1_tested, ee.image.Image)
        
    def test_MOD09A1(self):
        """Test the image module for MOD09A1"""
        MOD09A1_tested = MOD09A1.maskClouds().scaleAndOffset().spectralIndices(indices)
        self.assertIsInstance(MOD09A1_tested, ee.image.Image)
        
    def test_MOD11A2(self):
        """Test the image module for MOD11A2"""
        MOD11A2_tested = MOD11A2.scaleAndOffset()
        self.assertIsInstance(MOD11A2_tested, ee.image.Image)
        
    def test_MOD17A2H(self):
        """Test the image module for MOD17A2H"""
        MOD17A2H_tested = MOD17A2H.maskClouds().scaleAndOffset()
        self.assertIsInstance(MOD17A2H_tested, ee.image.Image)
        
    def test_MOD16A2(self):
        """Test the image module for MOD16A2"""
        MOD16A2_tested = MOD16A2.maskClouds().scaleAndOffset()
        self.assertIsInstance(MOD16A2_tested, ee.image.Image)
    
    def test_MOD13Q1(self):
        """Test the image module for MOD13Q1"""
        MOD13Q1_tested = MOD13Q1.maskClouds().scaleAndOffset()
        self.assertIsInstance(MOD13Q1_tested, ee.image.Image)
        
    def test_MOD13A1(self):
        """Test the image module for MOD13A1"""
        MOD13A1_tested = MOD13A1.maskClouds().scaleAndOffset()
        self.assertIsInstance(MOD13A1_tested, ee.image.Image)
        
    def test_MOD13A2(self):
        """Test the image module for MOD13A2"""
        MOD13A2_tested = MOD13A2.maskClouds().scaleAndOffset()
        self.assertIsInstance(MOD13A2_tested, ee.image.Image)
        
    def test_MOD08_M3(self):
        """Test the image module for MOD08_M3"""
        MOD08_M3_tested = MOD08_M3.scaleAndOffset()
        self.assertIsInstance(MOD08_M3_tested, ee.image.Image)
        
    def test_MOD17A3HGF(self):
        """Test the image module for MOD17A3HGF"""
        MOD17A3HGF_tested = MOD17A3HGF.scaleAndOffset()
        self.assertIsInstance(MOD17A3HGF_tested, ee.image.Image)
        
    # MODIS (AQUA)
        
    def test_MYD09GQ(self):
        """Test the image module for MYD09GQ"""
        MYD09GQ_tested = MYD09GQ.scaleAndOffset().spectralIndices(indices)
        self.assertIsInstance(MYD09GQ_tested, ee.image.Image)
        
    def test_MYD10A1(self):
        """Test the image module for MYD10A1"""
        MYD10A1_tested = MYD10A1.scaleAndOffset()
        self.assertIsInstance(MYD10A1_tested, ee.image.Image)
        
    def test_MYD11A1(self):
        """Test the image module for MYD11A1"""
        MYD11A1_tested = MYD11A1.scaleAndOffset()
        self.assertIsInstance(MYD11A1_tested, ee.image.Image)
        
    def test_MYD09GA(self):
        """Test the image module for MYD09GA"""
        MYD09GA_tested = MYD09GA.maskClouds().scaleAndOffset().spectralIndices(indices)
        self.assertIsInstance(MYD09GA_tested, ee.image.Image)
        
    def test_MYDOCGA(self):
        """Test the image module for MYDOCGA"""
        MYDOCGA_tested = MYDOCGA.scaleAndOffset()
        self.assertIsInstance(MYDOCGA_tested, ee.image.Image)
        
    def test_MYD14A1(self):
        """Test the image module for MYD14A1"""
        MYD14A1_tested = MYD14A1.scaleAndOffset()
        self.assertIsInstance(MYD14A1_tested, ee.image.Image)
        
    def test_MYD09Q1(self):
        """Test the image module for MYD09Q1"""
        MYD09Q1_tested = MYD09Q1.maskClouds().scaleAndOffset().spectralIndices(indices)
        self.assertIsInstance(MYD09Q1_tested, ee.image.Image)
        
    def test_MYD09A1(self):
        """Test the image module for MYD09A1"""
        MYD09A1_tested = MYD09A1.maskClouds().scaleAndOffset().spectralIndices(indices)
        self.assertIsInstance(MYD09A1_tested, ee.image.Image)
        
    def test_MYD11A2(self):
        """Test the image module for MYD11A2"""
        MYD11A2_tested = MYD11A2.scaleAndOffset()
        self.assertIsInstance(MYD11A2_tested, ee.image.Image)
        
    def test_MYD17A2H(self):
        """Test the image module for MYD17A2H"""
        MYD17A2H_tested = MYD17A2H.maskClouds().scaleAndOffset()
        self.assertIsInstance(MYD17A2H_tested, ee.image.Image)
    
    # CURRENTLY UNAVAILABLE
    #def test_MYD16A2(self):
    #    """Test the image module for MYD16A2"""
    #    MYD16A2_tested = MYD16A2.maskClouds().scaleAndOffset()
    #    self.assertIsInstance(MYD16A2_tested, ee.image.Image)
    
    def test_MYD13Q1(self):
        """Test the image module for MYD13Q1"""
        MYD13Q1_tested = MYD13Q1.maskClouds().scaleAndOffset()
        self.assertIsInstance(MYD13Q1_tested, ee.image.Image)
        
    def test_MYD13A1(self):
        """Test the image module for MYD13A1"""
        MYD13A1_tested = MYD13A1.maskClouds().scaleAndOffset()
        self.assertIsInstance(MYD13A1_tested, ee.image.Image)
        
    def test_MYD13A2(self):
        """Test the image module for MYD13A2"""
        MYD13A2_tested = MYD13A2.maskClouds().scaleAndOffset()
        self.assertIsInstance(MYD13A2_tested, ee.image.Image)
        
    def test_MYD08_M3(self):
        """Test the image module for MYD08_M3"""
        MYD08_M3_tested = MYD08_M3.scaleAndOffset()
        self.assertIsInstance(MYD08_M3_tested, ee.image.Image)
        
    def test_MYD17A3HGF(self):
        """Test the image module for MYD17A3HGF"""
        MYD17A3HGF_tested = MYD17A3HGF.scaleAndOffset()
        self.assertIsInstance(MYD17A3HGF_tested, ee.image.Image)

    # ----------------------
    # CHECKING PREPROCESS
    # ----------------------
        
    # SENTINEL MISSIONS
    
    def test_S3_preprocess(self):
        """Test the image module for Sentinel-3"""
        S3_tested = S3.preprocess()
        self.assertIsInstance(S3_tested, ee.image.Image)
    
    def test_S2_preprocess(self):
        """Test the image module for Sentinel-2"""
        S2_tested = S2.preprocess().spectralIndices(indices)
        self.assertIsInstance(S2_tested, ee.image.Image)
        
    def test_S2_online_preprocess(self):
        """Test the image module for Sentinel-2"""
        S2_tested = S2.preprocess().spectralIndices(indices,online = True)
        self.assertIsInstance(S2_tested, ee.image.Image)
        
    # LANDSAT MISSIONS
        
    def test_L8_preprocess(self):
        """Test the image module for Landsat 8"""
        L8_tested = L8.preprocess().spectralIndices(indices)
        self.assertIsInstance(L8_tested, ee.image.Image)
        
    def test_L8C2_preprocess(self):
        """Test the image module for Landsat 8"""
        L8_tested = L8C2.preprocess().spectralIndices(indices)
        self.assertIsInstance(L8_tested, ee.image.Image)
        
    def test_L7_preprocess(self):
        """Test the image module for Landsat 7"""
        L7_tested = L7.preprocess().spectralIndices(indices)
        self.assertIsInstance(L7_tested, ee.image.Image)
        
    def test_L7C2_preprocess(self):
        """Test the image module for Landsat 7"""
        L7_tested = L7C2.preprocess().spectralIndices(indices)
        self.assertIsInstance(L7_tested, ee.image.Image)
        
    def test_L5_preprocess(self):
        """Test the image module for Landsat 5"""
        L5_tested = L5.preprocess().spectralIndices(indices)
        self.assertIsInstance(L5_tested, ee.image.Image)
                
    def test_L4_preprocess(self):
        """Test the image module for Landsat 4"""
        L4_tested = L4.preprocess().spectralIndices(indices)
        self.assertIsInstance(L4_tested, ee.image.Image)
    
    # MODIS (TERRA + AQUA)
    
    def test_MCD43A4_preprocess(self):
        """Test the image module for MCD43A4"""
        MCD43A4_tested = MCD43A4.preprocess().spectralIndices(indices)
        self.assertIsInstance(MCD43A4_tested, ee.image.Image)
        
    def test_MCD43A3_preprocess(self):
        """Test the image module for MCD43A3"""
        MCD43A3_tested = MCD43A3.preprocess()
        self.assertIsInstance(MCD43A3_tested, ee.image.Image)
        
    def test_MCD43A1_preprocess(self):
        """Test the image module for MCD43A1"""
        MCD43A1_tested = MCD43A1.preprocess()
        self.assertIsInstance(MCD43A1_tested, ee.image.Image)
        
    def test_MCD15A3H_preprocess(self):
        """Test the image module for MCD15A3H"""
        MCD15A3H_tested = MCD15A3H.preprocess()
        self.assertIsInstance(MCD15A3H_tested, ee.image.Image)
        
    # MODIS (TERRA)
        
    def test_MOD09GQ_preprocess(self):
        """Test the image module for MOD09GQ"""
        MOD09GQ_tested = MOD09GQ.preprocess().spectralIndices(indices)
        self.assertIsInstance(MOD09GQ_tested, ee.image.Image)
        
    def test_MOD10A1_preprocess(self):
        """Test the image module for MOD10A1"""
        MOD10A1_tested = MOD10A1.preprocess()
        self.assertIsInstance(MOD10A1_tested, ee.image.Image)
        
    def test_MOD11A1_preprocess(self):
        """Test the image module for MOD11A1"""
        MOD11A1_tested = MOD11A1.preprocess()
        self.assertIsInstance(MOD11A1_tested, ee.image.Image)
        
    def test_MOD09GA_preprocess(self):
        """Test the image module for MOD09GA"""
        MOD09GA_tested = MOD09GA.preprocess().spectralIndices(indices)
        self.assertIsInstance(MOD09GA_tested, ee.image.Image)
        
    def test_MODOCGA_preprocess(self):
        """Test the image module for MODOCGA"""
        MODOCGA_tested = MODOCGA.preprocess()
        self.assertIsInstance(MODOCGA_tested, ee.image.Image)
        
    def test_MOD14A1_preprocess(self):
        """Test the image module for MOD14A1"""
        MOD14A1_tested = MOD14A1.preprocess()
        self.assertIsInstance(MOD14A1_tested, ee.image.Image)
        
    def test_MOD09Q1_preprocess(self):
        """Test the image module for MOD09Q1"""
        MOD09Q1_tested = MOD09Q1.preprocess().spectralIndices(indices)
        self.assertIsInstance(MOD09Q1_tested, ee.image.Image)
        
    def test_MOD09A1_preprocess(self):
        """Test the image module for MOD09A1"""
        MOD09A1_tested = MOD09A1.preprocess().spectralIndices(indices)
        self.assertIsInstance(MOD09A1_tested, ee.image.Image)
        
    def test_MOD11A2_preprocess(self):
        """Test the image module for MOD11A2"""
        MOD11A2_tested = MOD11A2.preprocess()
        self.assertIsInstance(MOD11A2_tested, ee.image.Image)
        
    def test_MOD17A2H_preprocess(self):
        """Test the image module for MOD17A2H"""
        MOD17A2H_tested = MOD17A2H.preprocess()
        self.assertIsInstance(MOD17A2H_tested, ee.image.Image)
        
    def test_MOD16A2_preprocess(self):
        """Test the image module for MOD16A2"""
        MOD16A2_tested = MOD16A2.preprocess()
        self.assertIsInstance(MOD16A2_tested, ee.image.Image)
    
    def test_MOD13Q1_preprocess(self):
        """Test the image module for MOD13Q1"""
        MOD13Q1_tested = MOD13Q1.preprocess()
        self.assertIsInstance(MOD13Q1_tested, ee.image.Image)
        
    def test_MOD13A1_preprocess(self):
        """Test the image module for MOD13A1"""
        MOD13A1_tested = MOD13A1.preprocess()
        self.assertIsInstance(MOD13A1_tested, ee.image.Image)
        
    def test_MOD13A2_preprocess(self):
        """Test the image module for MOD13A2"""
        MOD13A2_tested = MOD13A2.preprocess()
        self.assertIsInstance(MOD13A2_tested, ee.image.Image)
        
    def test_MOD08_M3_preprocess(self):
        """Test the image module for MOD08_M3"""
        MOD08_M3_tested = MOD08_M3.preprocess()
        self.assertIsInstance(MOD08_M3_tested, ee.image.Image)
        
    def test_MOD17A3HGF_preprocess(self):
        """Test the image module for MOD17A3HGF"""
        MOD17A3HGF_tested = MOD17A3HGF.preprocess()
        self.assertIsInstance(MOD17A3HGF_tested, ee.image.Image)
        
    # MODIS (AQUA)
        
    def test_MYD09GQ_preprocess(self):
        """Test the image module for MYD09GQ"""
        MYD09GQ_tested = MYD09GQ.preprocess().spectralIndices(indices)
        self.assertIsInstance(MYD09GQ_tested, ee.image.Image)
        
    def test_MYD10A1_preprocess(self):
        """Test the image module for MYD10A1"""
        MYD10A1_tested = MYD10A1.preprocess()
        self.assertIsInstance(MYD10A1_tested, ee.image.Image)
        
    def test_MYD11A1_preprocess(self):
        """Test the image module for MYD11A1"""
        MYD11A1_tested = MYD11A1.preprocess()
        self.assertIsInstance(MYD11A1_tested, ee.image.Image)
        
    def test_MYD09GA_preprocess(self):
        """Test the image module for MYD09GA"""
        MYD09GA_tested = MYD09GA.preprocess().spectralIndices(indices)
        self.assertIsInstance(MYD09GA_tested, ee.image.Image)
        
    def test_MYDOCGA_preprocess(self):
        """Test the image module for MYDOCGA"""
        MYDOCGA_tested = MYDOCGA.preprocess()
        self.assertIsInstance(MYDOCGA_tested, ee.image.Image)
        
    def test_MYD14A1_preprocess(self):
        """Test the image module for MYD14A1"""
        MYD14A1_tested = MYD14A1.preprocess()
        self.assertIsInstance(MYD14A1_tested, ee.image.Image)
        
    def test_MYD09Q1_preprocess(self):
        """Test the image module for MYD09Q1"""
        MYD09Q1_tested = MYD09Q1.preprocess().spectralIndices(indices)
        self.assertIsInstance(MYD09Q1_tested, ee.image.Image)
        
    def test_MYD09A1_preprocess(self):
        """Test the image module for MYD09A1"""
        MYD09A1_tested = MYD09A1.preprocess().spectralIndices(indices)
        self.assertIsInstance(MYD09A1_tested, ee.image.Image)
        
    def test_MYD11A2_preprocess(self):
        """Test the image module for MYD11A2"""
        MYD11A2_tested = MYD11A2.preprocess()
        self.assertIsInstance(MYD11A2_tested, ee.image.Image)
        
    def test_MYD17A2H_preprocess(self):
        """Test the image module for MYD17A2H"""
        MYD17A2H_tested = MYD17A2H.preprocess()
        self.assertIsInstance(MYD17A2H_tested, ee.image.Image)
    
    # CURRENTLY UNAVAILABLE
    #def test_MYD16A2_preprocess(self):
    #    """Test the image module for MYD16A2"""
    #    MYD16A2_tested = MYD16A2.preprocess()
    #    self.assertIsInstance(MYD16A2_tested, ee.image.Image)
    
    def test_MYD13Q1_preprocess(self):
        """Test the image module for MYD13Q1"""
        MYD13Q1_tested = MYD13Q1.preprocess()
        self.assertIsInstance(MYD13Q1_tested, ee.image.Image)
        
    def test_MYD13A1_preprocess(self):
        """Test the image module for MYD13A1"""
        MYD13A1_tested = MYD13A1.preprocess()
        self.assertIsInstance(MYD13A1_tested, ee.image.Image)
        
    def test_MYD13A2_preprocess(self):
        """Test the image module for MYD13A2"""
        MYD13A2_tested = MYD13A2.preprocess()
        self.assertIsInstance(MYD13A2_tested, ee.image.Image)
        
    def test_MYD08_M3_preprocess(self):
        """Test the image module for MYD08_M3"""
        MYD08_M3_tested = MYD08_M3.preprocess()
        self.assertIsInstance(MYD08_M3_tested, ee.image.Image)
        
    def test_MYD17A3HGF_preprocess(self):
        """Test the image module for MYD17A3HGF"""
        MYD17A3HGF_tested = MYD17A3HGF.preprocess()
        self.assertIsInstance(MYD17A3HGF_tested, ee.image.Image)
    
    def test_matchHistogram(self):
        """Test that histogram matching returns an image"""
        source = ee.Image("LANDSAT/LC08/C01/T1_TOA/LC08_047027_20160819")
        target = ee.Image("LANDSAT/LE07/C01/T1_TOA/LE07_046027_20150701")
        bands = {
           "B4": "B3", 
           "B3": "B2", 
           "B2": "B1"
        }
        matched = source.matchHistogram(target, bands)
        self.assertIsInstance(matched, ee.image.Image)

    def test_panSharpen(self):
        """Test that pan-sharpening returns an image"""
        source = ee.Image("LANDSAT/LC08/C01/T1_TOA/LC08_047027_20160819")
        sharp = source.panSharpen(qa=["DIV"])
        self.assertIsInstance(sharp, ee.image.Image)
        
if __name__ == '__main__':
    unittest.main()
import unittest

import ee

from eemont import imagecollection

ee.Initialize()

point = ee.Geometry.Point([-76.21, 3.45])
point2 = ee.Geometry.Point([-76.3, 4])
points = ee.FeatureCollection(
    [ee.Feature(point, {"id": 1}), ee.Feature(point2, {"id": 2})]
)

# SENTINEL MISSIONS
S3 = ee.ImageCollection("COPERNICUS/S3/OLCI").filterBounds(point)
S2 = ee.ImageCollection("COPERNICUS/S2_SR").filterBounds(point)

# LANDSAT MISSIONS
L8 = ee.ImageCollection("LANDSAT/LC08/C01/T1_SR").filterBounds(point)
L8C2 = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2").filterBounds(point)
L7 = ee.ImageCollection("LANDSAT/LE07/C01/T1_SR").filterBounds(point)
L7C2 = ee.ImageCollection("LANDSAT/LE07/C02/T1_L2").filterBounds(point)
L5 = ee.ImageCollection("LANDSAT/LT05/C01/T1_SR").filterBounds(point)
L4 = ee.ImageCollection("LANDSAT/LT04/C01/T1_SR").filterBounds(point)

# MODIS (TERRA + AQUA)
MCD43A4 = ee.ImageCollection("MODIS/006/MCD43A4").filterBounds(point)
MCD43A3 = ee.ImageCollection("MODIS/006/MCD43A3").filterBounds(point)
MCD43A1 = ee.ImageCollection("MODIS/006/MCD43A1").filterBounds(point)
MCD15A3H = ee.ImageCollection("MODIS/006/MCD15A3H").filterBounds(point)

# MODIS (TERRA)
MOD09GQ = ee.ImageCollection("MODIS/006/MOD09GQ").filterBounds(point)
MOD10A1 = ee.ImageCollection("MODIS/006/MOD10A1").filterBounds(point)
MOD11A1 = ee.ImageCollection("MODIS/006/MOD11A1").filterBounds(point)
MOD09GA = ee.ImageCollection("MODIS/006/MOD09GA").filterBounds(point)
MODOCGA = ee.ImageCollection("MODIS/006/MODOCGA").filterBounds(point)
MOD14A1 = ee.ImageCollection("MODIS/006/MOD14A1").filterBounds(point)
MOD09Q1 = ee.ImageCollection("MODIS/006/MOD09Q1").filterBounds(point)
MOD09A1 = ee.ImageCollection("MODIS/006/MOD09A1").filterBounds(point)
MOD11A2 = ee.ImageCollection("MODIS/006/MOD11A2").filterBounds(point)
MOD17A2H = ee.ImageCollection("MODIS/006/MOD17A2H").filterBounds(point)
MOD16A2 = ee.ImageCollection("MODIS/006/MOD16A2").filterBounds(point)
MOD13Q1 = ee.ImageCollection("MODIS/006/MOD13Q1").filterBounds(point)
MOD13A1 = ee.ImageCollection("MODIS/006/MOD13A1").filterBounds(point)
MOD13A2 = ee.ImageCollection("MODIS/006/MOD13A2").filterBounds(point)
MOD08_M3 = ee.ImageCollection("MODIS/061/MOD08_M3").filterBounds(point)
MOD17A3HGF = ee.ImageCollection("MODIS/006/MOD17A3HGF").filterBounds(point)

# MODIS (AQUA)
MYD09GQ = ee.ImageCollection("MODIS/006/MYD09GQ").filterBounds(point)
MYD10A1 = ee.ImageCollection("MODIS/006/MYD10A1").filterBounds(point)
MYD11A1 = ee.ImageCollection("MODIS/006/MYD11A1").filterBounds(point)
MYD09GA = ee.ImageCollection("MODIS/006/MYD09GA").filterBounds(point)
MYDOCGA = ee.ImageCollection("MODIS/006/MYDOCGA").filterBounds(point)
MYD14A1 = ee.ImageCollection("MODIS/006/MYD14A1").filterBounds(point)
MYD09Q1 = ee.ImageCollection("MODIS/006/MYD09Q1").filterBounds(point)
MYD09A1 = ee.ImageCollection("MODIS/006/MYD09A1").filterBounds(point)
MYD11A2 = ee.ImageCollection("MODIS/006/MYD11A2").filterBounds(point)
MYD17A2H = ee.ImageCollection("MODIS/006/MYD17A2H").filterBounds(point)
MYD16A2 = ee.ImageCollection("MODIS/006/MYD16A2").filterBounds(point)
MYD13Q1 = ee.ImageCollection("MODIS/006/MYD13Q1").filterBounds(point)
MYD13A1 = ee.ImageCollection("MODIS/006/MYD13A1").filterBounds(point)
MYD13A2 = ee.ImageCollection("MODIS/006/MYD13A2").filterBounds(point)
MYD08_M3 = ee.ImageCollection("MODIS/061/MYD08_M3").filterBounds(point)
MYD17A3HGF = ee.ImageCollection("MODIS/006/MYD17A3HGF").filterBounds(point)

indices = "all"


class Test(unittest.TestCase):
    """Tests for `eemont` package."""

    # TIME SERIES BY REGION

    def test_TS_Region(self):
        """Test the Container Emulation Methods"""
        test = S2.getTimeSeriesByRegion(ee.Reducer.mean(), "B2", point, 100)
        self.assertIsInstance(test, ee.featurecollection.FeatureCollection)

    def test_TS_Regions(self):
        """Test the Container Emulation Methods"""
        test = S2.getTimeSeriesByRegions(ee.Reducer.mean(), points, "B2", 100)
        self.assertIsInstance(test, ee.featurecollection.FeatureCollection)

    # CONTAINER EMULATION METHODS

    def test_Container_Get_Item_By_Key(self):
        """Test the Container Emulation Methods"""
        test = S2[["B.*"]]["B1"]
        self.assertIsInstance(test, ee.imagecollection.ImageCollection)

    def test_Container_Get_Item_By_Index(self):
        """Test the Container Emulation Methods"""
        test = S2[1]
        self.assertIsInstance(test, ee.imagecollection.ImageCollection)

    def test_Container_Get_Item_By_Slice(self):
        """Test the Container Emulation Methods"""
        test = S2[0:3]
        self.assertIsInstance(test, ee.imagecollection.ImageCollection)

    def test_Container_Length(self):
        """Test the Container Emulation Methods"""
        test = len(S2)
        self.assertIsInstance(test, int)

    # SENTINEL MISSIONS

    def test_S3(self):
        """Test the image collection module for Sentinel-3"""
        S3_tested = S3.closest("2020-01-15").maskClouds().scaleAndOffset()
        self.assertIsInstance(S3_tested, ee.imagecollection.ImageCollection)

    def test_S2(self):
        """Test the image collection module for Sentinel-2"""
        S2_tested = (
            S2.closest("2020-01-15")
            .maskClouds()
            .scaleAndOffset()
            .spectralIndices(indices)
        )
        self.assertIsInstance(S2_tested, ee.imagecollection.ImageCollection)

    def test_S2_STAC(self):
        """Test the image collection module for Sentinel-2"""
        S2_tested = S2.getSTAC()
        self.assertIsInstance(S2_tested, dict)

    def test_S2_DOI(self):
        """Test the image collection module for Sentinel-2"""
        S2_tested = S2.getDOI()
        self.assertIsInstance(S2_tested, str)

    def test_S2_Citation(self):
        """Test the image collection module for Sentinel-2"""
        S2_tested = S2.getCitation()
        self.assertIsInstance(S2_tested, str)

    def test_S2_online(self):
        """Test the image collection module for Sentinel-2"""
        S2_tested = (
            S2.closest("2020-01-15")
            .maskClouds()
            .scaleAndOffset()
            .spectralIndices(indices, online=True)
        )
        self.assertIsInstance(S2_tested, ee.imagecollection.ImageCollection)

    # LANDSAT MISSIONS

    def test_L8(self):
        """Test the image collection module for Landsat 8"""
        L8_tested = (
            L8.closest("2020-01-15")
            .maskClouds()
            .scaleAndOffset()
            .spectralIndices(indices)
        )
        self.assertIsInstance(L8_tested, ee.imagecollection.ImageCollection)

    def test_L8C2(self):
        """Test the image collection module for Landsat 8"""
        L8_tested = (
            L8C2.closest("2020-01-15")
            .maskClouds()
            .scaleAndOffset()
            .spectralIndices(indices)
        )
        self.assertIsInstance(L8_tested, ee.imagecollection.ImageCollection)

    def test_L7(self):
        """Test the image collection module for Landsat 7"""
        L7_tested = (
            L7.closest("2010-01-15")
            .maskClouds()
            .scaleAndOffset()
            .spectralIndices(indices)
        )
        self.assertIsInstance(L7_tested, ee.imagecollection.ImageCollection)

    def test_L7C2(self):
        """Test the image collection module for Landsat 7"""
        L7_tested = (
            L7C2.closest("2010-01-15")
            .maskClouds()
            .scaleAndOffset()
            .spectralIndices(indices)
        )
        self.assertIsInstance(L7_tested, ee.imagecollection.ImageCollection)

    def test_L5(self):
        """Test the image collection module for Landsat 5"""
        L5_tested = (
            L5.closest("2000-01-15", 2, "year")
            .maskClouds()
            .scaleAndOffset()
            .spectralIndices(indices)
        )
        self.assertIsInstance(L5_tested, ee.imagecollection.ImageCollection)

    def test_L4(self):
        """Test the image collection module for Landsat 4"""
        L4_tested = (
            L4.closest("1990-01-15")
            .maskClouds()
            .scaleAndOffset()
            .spectralIndices(indices)
        )
        self.assertIsInstance(L4_tested, ee.imagecollection.ImageCollection)

    # MODIS (TERRA + AQUA)

    def test_MCD43A4(self):
        """Test the image collection module for MCD43A4"""
        MCD43A4_tested = (
            MCD43A4.closest("2020-01-15").scaleAndOffset().spectralIndices(indices)
        )
        self.assertIsInstance(MCD43A4_tested, ee.imagecollection.ImageCollection)

    def test_MCD43A3(self):
        """Test the image collection module for MCD43A3"""
        MCD43A3_tested = MCD43A3.closest("2020-01-15").scaleAndOffset()
        self.assertIsInstance(MCD43A3_tested, ee.imagecollection.ImageCollection)

    def test_MCD43A1(self):
        """Test the image collection module for MCD43A1"""
        MCD43A1_tested = MCD43A1.closest("2020-01-15").scaleAndOffset()
        self.assertIsInstance(MCD43A1_tested, ee.imagecollection.ImageCollection)

    def test_MCD15A3H(self):
        """Test the image collection module for MCD15A3H"""
        MCD15A3H_tested = MCD15A3H.closest("2020-01-15").maskClouds().scaleAndOffset()
        self.assertIsInstance(MCD15A3H_tested, ee.imagecollection.ImageCollection)

    # MODIS (TERRA)

    def test_MOD09GQ(self):
        """Test the image collection module for MOD09GQ"""
        MOD09GQ_tested = (
            MOD09GQ.closest("2020-01-15").scaleAndOffset().spectralIndices(indices)
        )
        self.assertIsInstance(MOD09GQ_tested, ee.imagecollection.ImageCollection)

    def test_MOD10A1(self):
        """Test the image collection module for MOD10A1"""
        MOD10A1_tested = MOD10A1.closest("2020-01-15").scaleAndOffset()
        self.assertIsInstance(MOD10A1_tested, ee.imagecollection.ImageCollection)

    def test_MOD11A1(self):
        """Test the image collection module for MOD11A1"""
        MOD11A1_tested = MOD11A1.closest("2020-01-15").scaleAndOffset()
        self.assertIsInstance(MOD11A1_tested, ee.imagecollection.ImageCollection)

    def test_MOD09GA(self):
        """Test the image collection module for MOD09GA"""
        MOD09GA_tested = (
            MOD09GA.closest("2020-01-15")
            .maskClouds()
            .scaleAndOffset()
            .spectralIndices(indices)
        )
        self.assertIsInstance(MOD09GA_tested, ee.imagecollection.ImageCollection)

    def test_MODOCGA(self):
        """Test the image collection module for MODOCGA"""
        MODOCGA_tested = MODOCGA.closest("2020-01-15").scaleAndOffset()
        self.assertIsInstance(MODOCGA_tested, ee.imagecollection.ImageCollection)

    def test_MOD14A1(self):
        """Test the image collection module for MOD14A1"""
        MOD14A1_tested = MOD14A1.closest("2020-01-15").scaleAndOffset()
        self.assertIsInstance(MOD14A1_tested, ee.imagecollection.ImageCollection)

    def test_MOD09Q1(self):
        """Test the image collection module for MOD09Q1"""
        MOD09Q1_tested = (
            MOD09Q1.closest("2020-01-15")
            .maskClouds()
            .scaleAndOffset()
            .spectralIndices(indices)
        )
        self.assertIsInstance(MOD09Q1_tested, ee.imagecollection.ImageCollection)

    def test_MOD09A1(self):
        """Test the image collection module for MOD09A1"""
        MOD09A1_tested = (
            MOD09A1.closest("2020-01-15")
            .maskClouds()
            .scaleAndOffset()
            .spectralIndices(indices)
        )
        self.assertIsInstance(MOD09A1_tested, ee.imagecollection.ImageCollection)

    def test_MOD11A2(self):
        """Test the image collection module for MOD11A2"""
        MOD11A2_tested = MOD11A2.closest("2020-01-15").scaleAndOffset()
        self.assertIsInstance(MOD11A2_tested, ee.imagecollection.ImageCollection)

    def test_MOD17A2H(self):
        """Test the image collection module for MOD17A2H"""
        MOD17A2H_tested = MOD17A2H.closest("2020-01-15").maskClouds().scaleAndOffset()
        self.assertIsInstance(MOD17A2H_tested, ee.imagecollection.ImageCollection)

    def test_MOD16A2(self):
        """Test the image collection module for MOD16A2"""
        MOD16A2_tested = MOD16A2.closest("2020-01-15").maskClouds().scaleAndOffset()
        self.assertIsInstance(MOD16A2_tested, ee.imagecollection.ImageCollection)

    def test_MOD13Q1(self):
        """Test the image collection module for MOD13Q1"""
        MOD13Q1_tested = MOD13Q1.closest("2020-01-15").maskClouds().scaleAndOffset()
        self.assertIsInstance(MOD13Q1_tested, ee.imagecollection.ImageCollection)

    def test_MOD13A1(self):
        """Test the image collection module for MOD13A1"""
        MOD13A1_tested = MOD13A1.closest("2020-01-15").maskClouds().scaleAndOffset()
        self.assertIsInstance(MOD13A1_tested, ee.imagecollection.ImageCollection)

    def test_MOD13A2(self):
        """Test the image collection module for MOD13A2"""
        MOD13A2_tested = MOD13A2.closest("2020-01-15").maskClouds().scaleAndOffset()
        self.assertIsInstance(MOD13A2_tested, ee.imagecollection.ImageCollection)

    def test_MOD08_M3(self):
        """Test the image collection module for MOD08_M3"""
        MOD08_M3_tested = MOD08_M3.closest("2020-01-15").scaleAndOffset()
        self.assertIsInstance(MOD08_M3_tested, ee.imagecollection.ImageCollection)

    def test_MOD17A3HGF(self):
        """Test the image collection module for MOD17A3HGF"""
        MOD17A3HGF_tested = MOD17A3HGF.closest("2019-01-15").scaleAndOffset()
        self.assertIsInstance(MOD17A3HGF_tested, ee.imagecollection.ImageCollection)

    # MODIS (AQUA)
    # CURRENTLY UNAVAILABLE

    # def test_MYD09GQ(self):
    #     """Test the image collection module for MYD09GQ"""
    #     MYD09GQ_tested = (
    #         MYD09GQ.closest("2020-01-15").scaleAndOffset().spectralIndices(indices)
    #     )
    #     self.assertIsInstance(MYD09GQ_tested, ee.imagecollection.ImageCollection)

    # def test_MYD10A1(self):
    #     """Test the image collection module for MYD10A1"""
    #     MYD10A1_tested = MYD10A1.closest("2020-01-15").scaleAndOffset()
    #     self.assertIsInstance(MYD10A1_tested, ee.imagecollection.ImageCollection)

    # def test_MYD11A1(self):
    #     """Test the image collection module for MYD11A1"""
    #     MYD11A1_tested = MYD11A1.closest("2020-01-15").scaleAndOffset()
    #     self.assertIsInstance(MYD11A1_tested, ee.imagecollection.ImageCollection)

    # def test_MYD09GA(self):
    #     """Test the image collection module for MYD09GA"""
    #     MYD09GA_tested = (
    #         MYD09GA.closest("2020-01-15")
    #         .maskClouds()
    #         .scaleAndOffset()
    #         .spectralIndices(indices)
    #     )
    #     self.assertIsInstance(MYD09GA_tested, ee.imagecollection.ImageCollection)

    # def test_MYDOCGA(self):
    #     """Test the image collection module for MYDOCGA"""
    #     MYDOCGA_tested = MYDOCGA.closest("2020-01-15").scaleAndOffset()
    #     self.assertIsInstance(MYDOCGA_tested, ee.imagecollection.ImageCollection)

    # def test_MYD14A1(self):
    #     """Test the image collection module for MYD14A1"""
    #     MYD14A1_tested = MYD14A1.closest("2020-01-15").scaleAndOffset()
    #     self.assertIsInstance(MYD14A1_tested, ee.imagecollection.ImageCollection)

    # def test_MYD09Q1(self):
    #     """Test the image collection module for MYD09Q1"""
    #     MYD09Q1_tested = (
    #         MYD09Q1.closest("2020-01-15")
    #         .maskClouds()
    #         .scaleAndOffset()
    #         .spectralIndices(indices)
    #     )
    #     self.assertIsInstance(MYD09Q1_tested, ee.imagecollection.ImageCollection)

    # def test_MYD09A1(self):
    #     """Test the image collection module for MYD09A1"""
    #     MYD09A1_tested = (
    #         MYD09A1.closest("2020-01-15")
    #         .maskClouds()
    #         .scaleAndOffset()
    #         .spectralIndices(indices)
    #     )
    #     self.assertIsInstance(MYD09A1_tested, ee.imagecollection.ImageCollection)

    # def test_MYD11A2(self):
    #     """Test the image collection module for MYD11A2"""
    #     MYD11A2_tested = MYD11A2.closest("2020-01-15").scaleAndOffset()
    #     self.assertIsInstance(MYD11A2_tested, ee.imagecollection.ImageCollection)

    # def test_MYD17A2H(self):
    #     """Test the image collection module for MYD17A2H"""
    #     MYD17A2H_tested = MYD17A2H.closest("2020-01-15").maskClouds().scaleAndOffset()
    #     self.assertIsInstance(MYD17A2H_tested, ee.imagecollection.ImageCollection)

    # def test_MYD16A2(self):
    #    """Test the image collection module for MYD16A2"""
    #    MYD16A2_tested = MYD16A2.closest('2020-01-15').maskClouds().scaleAndOffset()
    #    self.assertIsInstance(MYD16A2_tested, ee.imagecollection.ImageCollection)

    # def test_MYD13Q1(self):
    #     """Test the image collection module for MYD13Q1"""
    #     MYD13Q1_tested = MYD13Q1.closest("2020-01-15").maskClouds().scaleAndOffset()
    #     self.assertIsInstance(MYD13Q1_tested, ee.imagecollection.ImageCollection)

    # def test_MYD13A1(self):
    #     """Test the image collection module for MYD13A1"""
    #     MYD13A1_tested = MYD13A1.closest("2020-01-15").maskClouds().scaleAndOffset()
    #     self.assertIsInstance(MYD13A1_tested, ee.imagecollection.ImageCollection)

    # def test_MYD13A2(self):
    #     """Test the image collection module for MYD13A2"""
    #     MYD13A2_tested = MYD13A2.closest("2020-01-15").maskClouds().scaleAndOffset()
    #     self.assertIsInstance(MYD13A2_tested, ee.imagecollection.ImageCollection)

    # def test_MYD08_M3(self):
    #     """Test the image collection module for MYD08_M3"""
    #     MYD08_M3_tested = MYD08_M3.closest("2020-01-15").scaleAndOffset()
    #     self.assertIsInstance(MYD08_M3_tested, ee.imagecollection.ImageCollection)

    # def test_MYD17A3HGF(self):
    #     """Test the image collection module for MYD17A3HGF"""
    #     MYD17A3HGF_tested = MYD17A3HGF.closest("2019-01-15").scaleAndOffset()
    #     self.assertIsInstance(MYD17A3HGF_tested, ee.imagecollection.ImageCollection)

    # ----------------------
    # CHECKING PREPROCESS
    # ----------------------

    # SENTINEL MISSIONS

    def test_S3(self):
        """Test the image collection module for Sentinel-3"""
        S3_tested = S3.closest("2020-01-15").preprocess()
        self.assertIsInstance(S3_tested, ee.imagecollection.ImageCollection)

    def test_S2(self):
        """Test the image collection module for Sentinel-2"""
        S2_tested = S2.closest("2020-01-15").preprocess().spectralIndices(indices)
        self.assertIsInstance(S2_tested, ee.imagecollection.ImageCollection)

    def test_S2_online(self):
        """Test the image collection module for Sentinel-2"""
        S2_tested = (
            S2.closest("2020-01-15").preprocess().spectralIndices(indices, online=True)
        )
        self.assertIsInstance(S2_tested, ee.imagecollection.ImageCollection)

    # LANDSAT MISSIONS

    def test_L8(self):
        """Test the image collection module for Landsat 8"""
        L8_tested = L8.closest("2020-01-15").preprocess().spectralIndices(indices)
        self.assertIsInstance(L8_tested, ee.imagecollection.ImageCollection)

    def test_L8C2(self):
        """Test the image collection module for Landsat 8"""
        L8_tested = L8C2.closest("2020-01-15").preprocess().spectralIndices(indices)
        self.assertIsInstance(L8_tested, ee.imagecollection.ImageCollection)

    def test_L7(self):
        """Test the image collection module for Landsat 7"""
        L7_tested = L7.closest("2010-01-15").preprocess().spectralIndices(indices)
        self.assertIsInstance(L7_tested, ee.imagecollection.ImageCollection)

    def test_L7C2(self):
        """Test the image collection module for Landsat 7"""
        L7_tested = L7C2.closest("2010-01-15").preprocess().spectralIndices(indices)
        self.assertIsInstance(L7_tested, ee.imagecollection.ImageCollection)

    def test_L5(self):
        """Test the image collection module for Landsat 5"""
        L5_tested = (
            L5.closest("2000-01-15", 2, "year").preprocess().spectralIndices(indices)
        )
        self.assertIsInstance(L5_tested, ee.imagecollection.ImageCollection)

    def test_L4(self):
        """Test the image collection module for Landsat 4"""
        L4_tested = L4.closest("1990-01-15").preprocess().spectralIndices(indices)
        self.assertIsInstance(L4_tested, ee.imagecollection.ImageCollection)

    # MODIS (TERRA + AQUA)

    def test_MCD43A4(self):
        """Test the image collection module for MCD43A4"""
        MCD43A4_tested = (
            MCD43A4.closest("2020-01-15").preprocess().spectralIndices(indices)
        )
        self.assertIsInstance(MCD43A4_tested, ee.imagecollection.ImageCollection)

    def test_MCD43A3(self):
        """Test the image collection module for MCD43A3"""
        MCD43A3_tested = MCD43A3.closest("2020-01-15").preprocess()
        self.assertIsInstance(MCD43A3_tested, ee.imagecollection.ImageCollection)

    def test_MCD43A1(self):
        """Test the image collection module for MCD43A1"""
        MCD43A1_tested = MCD43A1.closest("2020-01-15").preprocess()
        self.assertIsInstance(MCD43A1_tested, ee.imagecollection.ImageCollection)

    def test_MCD15A3H(self):
        """Test the image collection module for MCD15A3H"""
        MCD15A3H_tested = MCD15A3H.closest("2020-01-15").preprocess()
        self.assertIsInstance(MCD15A3H_tested, ee.imagecollection.ImageCollection)

    # MODIS (TERRA)

    def test_MOD09GQ(self):
        """Test the image collection module for MOD09GQ"""
        MOD09GQ_tested = (
            MOD09GQ.closest("2020-01-15").preprocess().spectralIndices(indices)
        )
        self.assertIsInstance(MOD09GQ_tested, ee.imagecollection.ImageCollection)

    def test_MOD10A1(self):
        """Test the image collection module for MOD10A1"""
        MOD10A1_tested = MOD10A1.closest("2020-01-15").preprocess()
        self.assertIsInstance(MOD10A1_tested, ee.imagecollection.ImageCollection)

    def test_MOD11A1(self):
        """Test the image collection module for MOD11A1"""
        MOD11A1_tested = MOD11A1.closest("2020-01-15").preprocess()
        self.assertIsInstance(MOD11A1_tested, ee.imagecollection.ImageCollection)

    def test_MOD09GA(self):
        """Test the image collection module for MOD09GA"""
        MOD09GA_tested = (
            MOD09GA.closest("2020-01-15").preprocess().spectralIndices(indices)
        )
        self.assertIsInstance(MOD09GA_tested, ee.imagecollection.ImageCollection)

    def test_MODOCGA(self):
        """Test the image collection module for MODOCGA"""
        MODOCGA_tested = MODOCGA.closest("2020-01-15").preprocess()
        self.assertIsInstance(MODOCGA_tested, ee.imagecollection.ImageCollection)

    def test_MOD14A1(self):
        """Test the image collection module for MOD14A1"""
        MOD14A1_tested = MOD14A1.closest("2020-01-15").preprocess()
        self.assertIsInstance(MOD14A1_tested, ee.imagecollection.ImageCollection)

    def test_MOD09Q1(self):
        """Test the image collection module for MOD09Q1"""
        MOD09Q1_tested = (
            MOD09Q1.closest("2020-01-15").preprocess().spectralIndices(indices)
        )
        self.assertIsInstance(MOD09Q1_tested, ee.imagecollection.ImageCollection)

    def test_MOD09A1(self):
        """Test the image collection module for MOD09A1"""
        MOD09A1_tested = (
            MOD09A1.closest("2020-01-15").preprocess().spectralIndices(indices)
        )
        self.assertIsInstance(MOD09A1_tested, ee.imagecollection.ImageCollection)

    def test_MOD11A2(self):
        """Test the image collection module for MOD11A2"""
        MOD11A2_tested = MOD11A2.closest("2020-01-15").preprocess()
        self.assertIsInstance(MOD11A2_tested, ee.imagecollection.ImageCollection)

    def test_MOD17A2H(self):
        """Test the image collection module for MOD17A2H"""
        MOD17A2H_tested = MOD17A2H.closest("2020-01-15").preprocess()
        self.assertIsInstance(MOD17A2H_tested, ee.imagecollection.ImageCollection)

    def test_MOD16A2(self):
        """Test the image collection module for MOD16A2"""
        MOD16A2_tested = MOD16A2.closest("2020-01-15").preprocess()
        self.assertIsInstance(MOD16A2_tested, ee.imagecollection.ImageCollection)

    def test_MOD13Q1(self):
        """Test the image collection module for MOD13Q1"""
        MOD13Q1_tested = MOD13Q1.closest("2020-01-15").preprocess()
        self.assertIsInstance(MOD13Q1_tested, ee.imagecollection.ImageCollection)

    def test_MOD13A1(self):
        """Test the image collection module for MOD13A1"""
        MOD13A1_tested = MOD13A1.closest("2020-01-15").preprocess()
        self.assertIsInstance(MOD13A1_tested, ee.imagecollection.ImageCollection)

    def test_MOD13A2(self):
        """Test the image collection module for MOD13A2"""
        MOD13A2_tested = MOD13A2.closest("2020-01-15").preprocess()
        self.assertIsInstance(MOD13A2_tested, ee.imagecollection.ImageCollection)

    def test_MOD08_M3(self):
        """Test the image collection module for MOD08_M3"""
        MOD08_M3_tested = MOD08_M3.closest("2020-01-15").preprocess()
        self.assertIsInstance(MOD08_M3_tested, ee.imagecollection.ImageCollection)

    def test_MOD17A3HGF(self):
        """Test the image collection module for MOD17A3HGF"""
        MOD17A3HGF_tested = MOD17A3HGF.closest("2019-01-15").preprocess()
        self.assertIsInstance(MOD17A3HGF_tested, ee.imagecollection.ImageCollection)

    # MODIS (AQUA)

    # def test_MYD09GQ(self):
    #     """Test the image collection module for MYD09GQ"""
    #     MYD09GQ_tested = (
    #         MYD09GQ.closest("2020-01-15").preprocess().spectralIndices(indices)
    #     )
    #     self.assertIsInstance(MYD09GQ_tested, ee.imagecollection.ImageCollection)

    # def test_MYD10A1(self):
    #     """Test the image collection module for MYD10A1"""
    #     MYD10A1_tested = MYD10A1.closest("2020-01-15").preprocess()
    #     self.assertIsInstance(MYD10A1_tested, ee.imagecollection.ImageCollection)

    # def test_MYD11A1(self):
    #     """Test the image collection module for MYD11A1"""
    #     MYD11A1_tested = MYD11A1.closest("2020-01-15").preprocess()
    #     self.assertIsInstance(MYD11A1_tested, ee.imagecollection.ImageCollection)

    # def test_MYD09GA(self):
    #     """Test the image collection module for MYD09GA"""
    #     MYD09GA_tested = (
    #         MYD09GA.closest("2020-01-15").preprocess().spectralIndices(indices)
    #     )
    #     self.assertIsInstance(MYD09GA_tested, ee.imagecollection.ImageCollection)

    # def test_MYDOCGA(self):
    #     """Test the image collection module for MYDOCGA"""
    #     MYDOCGA_tested = MYDOCGA.closest("2020-01-15").preprocess()
    #     self.assertIsInstance(MYDOCGA_tested, ee.imagecollection.ImageCollection)

    # def test_MYD14A1(self):
    #     """Test the image collection module for MYD14A1"""
    #     MYD14A1_tested = MYD14A1.closest("2020-01-15").preprocess()
    #     self.assertIsInstance(MYD14A1_tested, ee.imagecollection.ImageCollection)

    # def test_MYD09Q1(self):
    #     """Test the image collection module for MYD09Q1"""
    #     MYD09Q1_tested = (
    #         MYD09Q1.closest("2020-01-15").preprocess().spectralIndices(indices)
    #     )
    #     self.assertIsInstance(MYD09Q1_tested, ee.imagecollection.ImageCollection)

    # def test_MYD09A1(self):
    #     """Test the image collection module for MYD09A1"""
    #     MYD09A1_tested = (
    #         MYD09A1.closest("2020-01-15").preprocess().spectralIndices(indices)
    #     )
    #     self.assertIsInstance(MYD09A1_tested, ee.imagecollection.ImageCollection)

    # def test_MYD11A2(self):
    #     """Test the image collection module for MYD11A2"""
    #     MYD11A2_tested = MYD11A2.closest("2020-01-15").preprocess()
    #     self.assertIsInstance(MYD11A2_tested, ee.imagecollection.ImageCollection)

    # def test_MYD17A2H(self):
    #     """Test the image collection module for MYD17A2H"""
    #     MYD17A2H_tested = MYD17A2H.closest("2020-01-15").preprocess()
    #     self.assertIsInstance(MYD17A2H_tested, ee.imagecollection.ImageCollection)

    # # CURRENTLY UNAVAILABLE
    # # def test_MYD16A2(self):
    # #    """Test the image collection module for MYD16A2"""
    # #    MYD16A2_tested = MYD16A2.closest('2020-01-15').preprocess()
    # #    self.assertIsInstance(MYD16A2_tested, ee.imagecollection.ImageCollection)

    # def test_MYD13Q1(self):
    #     """Test the image collection module for MYD13Q1"""
    #     MYD13Q1_tested = MYD13Q1.closest("2020-01-15").preprocess()
    #     self.assertIsInstance(MYD13Q1_tested, ee.imagecollection.ImageCollection)

    # def test_MYD13A1(self):
    #     """Test the image collection module for MYD13A1"""
    #     MYD13A1_tested = MYD13A1.closest("2020-01-15").preprocess()
    #     self.assertIsInstance(MYD13A1_tested, ee.imagecollection.ImageCollection)

    # def test_MYD13A2(self):
    #     """Test the image collection module for MYD13A2"""
    #     MYD13A2_tested = MYD13A2.closest("2020-01-15").preprocess()
    #     self.assertIsInstance(MYD13A2_tested, ee.imagecollection.ImageCollection)

    # def test_MYD08_M3(self):
    #     """Test the image collection module for MYD08_M3"""
    #     MYD08_M3_tested = MYD08_M3.closest("2020-01-15").preprocess()
    #     self.assertIsInstance(MYD08_M3_tested, ee.imagecollection.ImageCollection)

    # def test_MYD17A3HGF(self):
    #     """Test the image collection module for MYD17A3HGF"""
    #     MYD17A3HGF_tested = MYD17A3HGF.closest("2019-01-15").preprocess()
    #     self.assertIsInstance(MYD17A3HGF_tested, ee.imagecollection.ImageCollection)

    def test_panSharpen(self):
        """Test that pan-sharpening returns an Image Collection"""
        source = ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA")
        sharp = source.panSharpen(qa=["DIV"])
        self.assertIsInstance(sharp, ee.imagecollection.ImageCollection)

    def test_tasseledCap(self):
        """Test that tasseledCap returns an image collection"""
        col = ee.ImageCollection("COPERNICUS/S2")
        col = col.tasseledCap()
        self.assertIsInstance(col, ee.imagecollection.ImageCollection)


if __name__ == "__main__":
    unittest.main()

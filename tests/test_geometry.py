import ee
import unittest
from eemont import geometry

ee.Initialize()

class Test(unittest.TestCase):
    """Tests for `eemont` package."""
    
    def test_BBoxFromQuery(self):
        """Test the BBoxFromQuery constructor"""
        test = ee.Geometry.BBoxFromQuery('Colombia',user_agent = 'eemon-feature-test')
        self.assertIsInstance(test, ee.geometry.Geometry)
        
    def test_PointFromQuery(self):
        """Test the PointFromQuery constructor"""
        test = ee.Geometry.PointFromQuery('Colombia',user_agent = 'eemon-feature-test')
        self.assertIsInstance(test, ee.geometry.Geometry)
        
    def test_MultiPointFromQuery(self):
        """Test the MultiPointFromQuery constructor"""
        test = ee.Geometry.MultiPointFromQuery('Colombia',user_agent = 'eemon-feature-test')
        self.assertIsInstance(test, ee.geometry.Geometry)
        
    def test_PointFromFullPlusCode(self):
        """Test the PointFromPlusCode constructor with a full plus code"""
        code = "85FPQXGV+XH"
        test = ee.Geometry.PointFromPlusCode(code)
        self.assertIsInstance(test, ee.geometry.Geometry)
    
    def test_PointFromShortPlusCode(self):
        """Test the PointFromPlusCode constructor with a short plus code"""
        code = "QXGV+XH Denver, CO, USA"
        test = ee.Geometry.PointFromPlusCode(code, user_agent = 'eemont-feature-test')
        self.assertIsInstance(test, ee.geometry.Geometry)
    
    def test_MultiPointFromPlusCode(self):
        """Test the MultiPointFromPlusCode constructor with a list of plus codes"""
        codes = [
            '85FQ2222+22', 
            '85FR2222+22', 
            '85GR2222+22', 
        ]
        test = ee.Geometry.MultiPointFromPlusCode(codes)
        self.assertIsInstance(test, ee.geometry.Geometry)
    
    def test_PolygonFromPlusCode(self):
        """Test the PolygonFromPlusCode constructor with a list of plus codes"""
        codes = [
            '85FQ2222+22', 
            '85FR2222+22', 
            '85GR2222+22', 
        ]
        test = ee.Geometry.PolygonFromPlusCode(codes)
        self.assertIsInstance(test, ee.geometry.Geometry)

    def test_MultiPolygonFromPlusCode(self):
        """Test the MultiPolygonFromPlusCode constructor with a list of lists of plus codes"""
        codes = [
            ['85FQ2222+22', '85FR2222+22', '85GR2222+22'], 
            ['85FP8PC2+G2', '85FPJF23+G4', '85FPMW2R+RP'],
            ['85FPRJ5W+82', '85GP3M67+CP', '85GQ2R7C+38', '85FQC5X6+FJ', '85FPPXQJ+F3'],
        ]
        test = ee.Geometry.MultiPolygonFromPlusCode(codes)
        self.assertIsInstance(test, ee.geometry.Geometry)

    def test_LineStringFromPlusCode(self):
        """Test the LineStringFromPlusCode constructor with a list of plus codes"""
        codes = [
            '85FQ2222+22', 
            '85FR2222+22', 
            '85GR2222+22', 
        ]
        test = ee.Geometry.LineStringFromPlusCode(codes)
        self.assertIsInstance(test, ee.geometry.Geometry)

    def test_MultiLineStringFromPlusCode(self):
        """Test the MultiLineStringFromPlusCode constructor with a list of lists of plus codes"""
        codes = [
            ['85FQ2222+22', '85FR2222+22', '85GR2222+22'], 
            ['85FP8PC2+G2', '85FPJF23+G4', '85FPMW2R+RP'],
            ['85FPRJ5W+82', '85GP3M67+CP', '85GQ2R7C+38', '85FQC5X6+FJ', '85FPPXQJ+F3'],
        ]
        test = ee.Geometry.MultiLineStringFromPlusCode(codes)
        self.assertIsInstance(test, ee.geometry.Geometry)

    def test_LinearRingFromPlusCode(self):
        """Test the LinearRingFromPlusCode constructor with a list of plus codes"""
        codes = [
            '85FQ2222+22', 
            '85FR2222+22', 
            '85GR2222+22', 
        ]
        test = ee.Geometry.LinearRingFromPlusCode(codes)
        self.assertIsInstance(test, ee.geometry.Geometry)

    def test_RectangleFromPlusCode(self):
        """Test the RectangleFromPlusCode constructor with a list of plus codes"""
        codes = [
            '85FQ2222+22', 
            '85GR2222+22', 
        ]
        test = ee.Geometry.RectangleFromPlusCode(codes)
        self.assertIsInstance(test, ee.geometry.Geometry)

    def test_pluscode_from_Point(self):
        """Test that an ee.Geometry.Point returns a plus code string"""
        geom = ee.Geometry.Point([-105, 40])
        test = geom.plusCode()
        self.assertIsInstance(test, str)
    
    def test_pluscode_from_MultiPoint(self):
        """Test that an ee.Geometry.MultiPoint returns a plus code list of correct length"""
        coords = [
            [-105, 40],
            [-105, 39],
            [-104, 39],
        ]
        geom = ee.Geometry.MultiPoint(coords)
        test = geom.plusCode()
        self.assertEqual(len(test), len(coords))

    def test_pluscode_from_Polygon(self):
        """Test that an ee.Geometry.Polygon returns a plus code list of correct length"""
        coords = [
            [-105, 40],
            [-105, 39],
            [-104, 39],
            [-105, 40],
        ]
        geom = ee.Geometry.Polygon(coords)
        test = geom.plusCode()
        self.assertEqual(len(test), len(coords))

    def test_pluscode_from_MultiPolygon(self):
        """Test that an ee.Geometry.MultiPolygon returns a plus code list of correct length"""
        coords = [
            [[-105, 40], [-105, 39], [-104, 39]],
            [[-104, 41], [-104, 40], [-103, 40], [-103, 39]]
        ]
        geom = ee.Geometry.MultiPolygon(coords)
        test = geom.plusCode()
        self.assertEqual(len(test), len(coords))

    def test_pluscode_from_LineString(self):
        """Test that an ee.Geometry.LineString returns a plus code list of correct length"""
        coords = [
            [-105, 40],
            [-105, 39],
            [-104, 39],
        ]
        geom = ee.Geometry.LineString(coords)
        test = geom.plusCode()
        self.assertEqual(len(test), len(coords))

    def test_pluscode_from_MultiLineString(self):
        """Test that an ee.Geometry.MultiLineString returns a plus code list of correct length"""
        coords = [
            [[-105, 40], [-105, 39], [-104, 39]],
            [[-104, 41], [-104, 40], [-103, 40], [-103, 39]]
        ]
        geom = ee.Geometry.MultiLineString(coords)
        test = geom.plusCode()
        self.assertEqual(len(test), len(coords))

    def test_pluscode_from_LinearRing(self):
        """Test that an ee.Geometry.LinearRing returns a plus code list of correct length"""
        coords = [
            [-105, 40],
            [-105, 39],
            [-104, 39],
            [-105, 40]
        ]
        geom = ee.Geometry.LinearRing(coords)
        test = geom.plusCode()
        self.assertEqual(len(test), len(coords))

    def test_pluscode_from_Rectangle(self):
        """Test that an ee.Geometry.Rectangle returns a plus code list of correct length"""
        coords = [
            [-105, 40],
            [-104, 39]
        ]
        geom = ee.Geometry.Rectangle(coords)
        test = geom.plusCode()
        self.assertEqual(len(test), 5)


if __name__ == '__main__':
    unittest.main()
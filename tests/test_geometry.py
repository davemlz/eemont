import unittest

import ee

from eemont import geometry

ee.Initialize()


class Test(unittest.TestCase):
    """Tests for `eemont` package."""

    def test_BBoxFromQuery(self):
        """Test the BBoxFromQuery constructor"""
        test = ee.Geometry.BBoxFromQuery("Colombia", user_agent="eemon-feature-test")
        self.assertIsInstance(test, ee.geometry.Geometry)

    def test_PointFromQuery(self):
        """Test the PointFromQuery constructor"""
        test = ee.Geometry.PointFromQuery("Colombia", user_agent="eemon-feature-test")
        self.assertIsInstance(test, ee.geometry.Geometry)

    def test_MultiPointFromQuery(self):
        """Test the MultiPointFromQuery constructor"""
        test = ee.Geometry.MultiPointFromQuery(
            "Colombia", user_agent="eemon-feature-test"
        )
        self.assertIsInstance(test, ee.geometry.Geometry)

    def test_PointFromFullPlusCode(self):
        """Test the PointFromPlusCode constructor with a full plus code"""
        code = "85FPQXGV+XH"
        test = ee.Geometry.PointFromPlusCode(code)
        self.assertIsInstance(test, ee.geometry.Geometry)

    def test_PointFromShortPlusCode(self):
        """Test the PointFromPlusCode constructor with a short plus code"""
        code = "QXGV+XH Denver, CO, USA"
        test = ee.Geometry.PointFromPlusCode(code, user_agent="eemont-feature-test")
        self.assertIsInstance(test, ee.geometry.Geometry)

    def test_MultiPointFromPlusCodes(self):
        """Test the MultiPointFromPlusCodes constructor with a list of plus codes"""
        codes = [
            "85FQ2222+22",
            "85FR2222+22",
            "85GR2222+22",
        ]
        test = ee.Geometry.MultiPointFromPlusCodes(codes)
        self.assertIsInstance(test, ee.geometry.Geometry)

    def test_PolygonFromPlusCodes(self):
        """Test the PolygonFromPlusCodes constructor with a list of plus codes"""
        codes = [
            "85FQ2222+22",
            "85FR2222+22",
            "85GR2222+22",
        ]
        test = ee.Geometry.PolygonFromPlusCodes(codes)
        self.assertIsInstance(test, ee.geometry.Geometry)

    def test_MultiPolygonFromPlusCodes(self):
        """Test the MultiPolygonFromPlusCodes constructor with a list of lists of plus codes"""
        codes = [
            ["85FQ2222+22", "85FR2222+22", "85GR2222+22"],
            ["85FP8PC2+G2", "85FPJF23+G4", "85FPMW2R+RP"],
            ["85FPRJ5W+82", "85GP3M67+CP", "85GQ2R7C+38", "85FQC5X6+FJ", "85FPPXQJ+F3"],
        ]
        test = ee.Geometry.MultiPolygonFromPlusCodes(codes)
        self.assertIsInstance(test, ee.geometry.Geometry)

    def test_LineStringFromPlusCodes(self):
        """Test the LineStringFromPlusCodes constructor with a list of plus codes"""
        codes = [
            "85FQ2222+22",
            "85FR2222+22",
            "85GR2222+22",
        ]
        test = ee.Geometry.LineStringFromPlusCodes(codes)
        self.assertIsInstance(test, ee.geometry.Geometry)

    def test_MultiLineStringFromPlusCodes(self):
        """Test the MultiLineStringFromPlusCodes constructor with a list of lists of plus codes"""
        codes = [
            ["85FQ2222+22", "85FR2222+22", "85GR2222+22"],
            ["85FP8PC2+G2", "85FPJF23+G4", "85FPMW2R+RP"],
            ["85FPRJ5W+82", "85GP3M67+CP", "85GQ2R7C+38", "85FQC5X6+FJ", "85FPPXQJ+F3"],
        ]
        test = ee.Geometry.MultiLineStringFromPlusCodes(codes)
        self.assertIsInstance(test, ee.geometry.Geometry)

    def test_LinearRingFromPlusCodes(self):
        """Test the LinearRingFromPlusCodes constructor with a list of plus codes"""
        codes = [
            "85FQ2222+22",
            "85FR2222+22",
            "85GR2222+22",
        ]
        test = ee.Geometry.LinearRingFromPlusCodes(codes)
        self.assertIsInstance(test, ee.geometry.Geometry)

    def test_RectangleFromPlusCodes(self):
        """Test the RectangleFromPlusCodes constructor with a list of plus codes"""
        codes = [
            "85FQ2222+22",
            "85GR2222+22",
        ]
        test = ee.Geometry.RectangleFromPlusCodes(codes)
        self.assertIsInstance(test, ee.geometry.Geometry)

    def test_pluscodes_from_Point(self):
        """Test that the plus codes returned by a Point can construct a new Point"""
        geom = ee.Geometry.Point([-105, 40])
        test = ee.Geometry.PointFromPlusCode(geom.plusCodes())
        self.assertIsInstance(test, ee.geometry.Geometry)

    def test_pluscodes_from_MultiPoint(self):
        """Test that the plus codes returned by a MultiPoint can construct a new MultiPoint"""
        coords = [
            [-105, 40],
            [-105, 39],
            [-104, 39],
        ]
        geom = ee.Geometry.MultiPoint(coords)
        test = ee.Geometry.MultiPointFromPlusCodes(geom.plusCodes())
        self.assertIsInstance(test, ee.geometry.Geometry)

    def test_pluscodes_from_Polygon(self):
        """Test that the plus codes returned by a Polygon can construct a new Polygon"""
        coords = [
            [-105, 40],
            [-105, 39],
            [-104, 39],
            [-105, 40],
        ]
        geom = ee.Geometry.Polygon(coords)
        test = ee.Geometry.PolygonFromPlusCodes(geom.plusCodes())
        self.assertIsInstance(test, ee.geometry.Geometry)

    def test_pluscodes_from_MultiPolygon(self):
        """Test that the plus codes returned by a MultiPolygon can construct a new MultiPolygon"""
        coords = [
            [[-105, 40], [-105, 39], [-104, 39]],
            [[-104, 41], [-104, 40], [-103, 40], [-103, 39]],
        ]
        geom = ee.Geometry.MultiPolygon(coords)
        test = ee.Geometry.MultiPolygonFromPlusCodes(geom.plusCodes())
        self.assertIsInstance(test, ee.geometry.Geometry)

    def test_pluscodes_from_LineString(self):
        """Test that the plus codes returned by a LineString can construct a new LineString"""
        coords = [
            [-105, 40],
            [-105, 39],
            [-104, 39],
        ]
        geom = ee.Geometry.LineString(coords)
        test = ee.Geometry.LineStringFromPlusCodes(geom.plusCodes())
        self.assertIsInstance(test, ee.geometry.Geometry)

    def test_pluscodes_from_MultiLineString(self):
        """Test that the plus codes returned by a MultiLineString can construct a new MultiLineString"""
        coords = [
            [[-105, 40], [-105, 39], [-104, 39]],
            [[-104, 41], [-104, 40], [-103, 40], [-103, 39]],
        ]
        geom = ee.Geometry.MultiLineString(coords)
        test = ee.Geometry.MultiLineStringFromPlusCodes(geom.plusCodes())
        self.assertIsInstance(test, ee.geometry.Geometry)

    def test_pluscodes_from_LinearRing(self):
        """Test that the plus codes returned by a LinearRing can construct a new LinearRing"""
        coords = [[-105, 40], [-105, 39], [-104, 39], [-105, 40]]
        geom = ee.Geometry.LinearRing(coords)
        test = ee.Geometry.LinearRingFromPlusCodes(geom.plusCodes())
        self.assertIsInstance(test, ee.geometry.Geometry)

    def test_pluscodes_from_Rectangle(self):
        """Test that the plus codes returned by a Rectangle are a list.

        The Rectangle test does not follow the pattern of the other Geometry tests because unlike other Geometries,
        a Rectangle cannot be constructed from the coordinates that it returns.
        """
        coords = [[-105, 40], [-104, 39]]
        geom = ee.Geometry.Rectangle(coords)
        test = geom.plusCodes()
        self.assertIsInstance(test, list)


if __name__ == "__main__":
    unittest.main()

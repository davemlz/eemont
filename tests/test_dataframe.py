import ee
import pandas as pd
import unittest
from eemont import dataframe

ee.Initialize()

df = pd.DataFrame()
df["x"] = [-76.4, -76.5]
df["y"] = [4.3, 4.2]
df["z"] = [1, 2]
df["obs"] = ["a", "b"]


class Test(unittest.TestCase):
    """Tests for `eemont` package."""

    def test_dataframe(self):
        """Test the image module for pd.DataFrame"""
        dataframe_tested = df.toEEFeatureCollection("y", "x")
        self.assertIsInstance(dataframe_tested, ee.featurecollection.FeatureCollection)


if __name__ == "__main__":
    unittest.main()

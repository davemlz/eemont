import ee
import unittest
from eemont import eeDictionary

ee.Initialize()


class Test(unittest.TestCase):
    """Tests for `eemont` package."""

    # CONTAINER EMULATION METHODS

    def test_Container_Get_Item_By_Key(self):
        """Test the Container Emulation Methods"""
        test = ee.Dictionary({"key1": 1, "key2": 2})["key1"]
        self.assertIsInstance(test, ee.computedobject.ComputedObject)

    def test_Container_Contains(self):
        """Test the Container Emulation Methods"""
        test = "key3" in ee.Dictionary({"key1": 1, "key2": 2})
        self.assertIsInstance(test, bool)


if __name__ == "__main__":
    unittest.main()

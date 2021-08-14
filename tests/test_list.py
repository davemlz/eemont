import ee
import unittest
from eemont import eeList

ee.Initialize()


class Test(unittest.TestCase):
    """Tests for `eemont` package."""

    # CONTAINER EMULATION METHODS

    def test_Container_Get_Item_By_Index(self):
        """Test the Container Emulation Methods"""
        test = ee.List([1, 2, 3])[0]
        self.assertIsInstance(test, ee.computedobject.ComputedObject)

    def test_Container_Get_Item_By_Slice(self):
        """Test the Container Emulation Methods"""
        test = ee.List([1, 2, 3])[0:2]
        self.assertIsInstance(test, ee.ee_list.List)

    def test_Container_Length(self):
        """Test the Container Emulation Methods"""
        test = len(ee.List([1, 2, 3]))
        self.assertIsInstance(test, int)

    def test_Container_Contains(self):
        """Test the Container Emulation Methods"""
        test = 2 in ee.List([1, 2, 3])
        self.assertIsInstance(test, bool)

    # OVERLOADED OPERATIONS

    def test_binary1(self):
        """Test the eeList module for binary operators 1"""
        binary1_tested = ee.List([1, 2, 3]) + ee.List([4, 5, 6]) * 5
        self.assertIsInstance(binary1_tested, ee.ee_list.List)


if __name__ == "__main__":
    unittest.main()

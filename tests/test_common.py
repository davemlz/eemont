import unittest

import box
import ee

import eemont

ee.Initialize()


class Test(unittest.TestCase):
    """Tests for `eemont` package."""

    def test_indices(self):
        """Test the indices function"""
        test = eemont.indices()
        self.assertIsInstance(test, box.box.Box)

    def test_indices_online(self):
        """Test the indices function"""
        test = eemont.indices(online=True)
        self.assertIsInstance(test, box.box.Box)

    def test_listIndices(self):
        """Test the listIndices function"""
        test = eemont.listIndices()
        self.assertIsInstance(test, list)

    def test_listIndices_online(self):
        """Test the listIndices function"""
        test = eemont.listIndices(online=True)
        self.assertIsInstance(test, list)


if __name__ == "__main__":
    unittest.main()

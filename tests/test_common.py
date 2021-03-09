import ee
import unittest
import eemont
import box

ee.Initialize()

class Test(unittest.TestCase):
    """Tests for `eemont` package."""
    
    def test_indices(self):
        """Test the indices function"""
        test = eemont.indices()
        self.assertIsInstance(test, box.box.Box)
        
    def test_listIndices(self):
        """Test the listIndices function"""
        test = eemont.listIndices()
        self.assertIsInstance(test, list)        
        
if __name__ == '__main__':
    unittest.main()
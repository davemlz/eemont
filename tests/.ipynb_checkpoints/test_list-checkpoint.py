import ee
import unittest
from eemont import eeList

ee.Initialize()

class Test(unittest.TestCase):
    """Tests for `eemont` package."""
    
    # OVERLOADED OPERATIONS
    
    def test_binary1(self):
        """Test the eeList module for binary operators 1"""
        binary1_tested = ee.List([1,2,3]) + ee.List([4,5,6]) * 5
        self.assertIsInstance(binary1_tested, ee.ee_list.List)
        
if __name__ == '__main__':
    unittest.main()
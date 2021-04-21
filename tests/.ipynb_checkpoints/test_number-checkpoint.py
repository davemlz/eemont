import ee
import unittest
from eemont import number

ee.Initialize()

class Test(unittest.TestCase):
    """Tests for `eemont` package."""
    
    # OVERLOADED OPERATIONS
    
    def test_binary1(self):
        """Test the number module for binary operators 1"""
        binary1_tested = ee.Number(1) + 0 - 0 * 1 / 1 // 1 % 1 ** 1 << 1 >> 1
        self.assertIsInstance(binary1_tested, ee.ee_number.Number)
        
    def test_binary2(self):
        """Test the number module for binary operators 2"""
        binary2_tested_a = (ee.Number(1) > 1) & (ee.Number(1) < 1)
        binary2_tested_b = (ee.Number(1) >= 1) | (ee.Number(1) <= 1)
        binary2_tested_c = (ee.Number(1) == 1) & (ee.Number(1) != 1)
        binary2_tested = binary2_tested_a + binary2_tested_b + binary2_tested_c
        self.assertIsInstance(binary2_tested, ee.ee_number.Number)
        
    def test_unary(self):
        """Test the number module for unary operators"""
        unary_tested_a = - ee.Number(1)
        unary_tested_b = ~ ee.Number(1)
        unary_tested = unary_tested_a + unary_tested_b
        self.assertIsInstance(unary_tested, ee.ee_number.Number)
        
if __name__ == '__main__':
    unittest.main()
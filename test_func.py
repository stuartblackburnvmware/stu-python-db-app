import unittest
from func import main  # Import the main function to test

class TestFunc(unittest.TestCase):
    def test_main_returns_expected_output(self):
        # Test the main function
        result = main(None)  # You can pass None for the 'req' argument
        expected_output = "This is the greatest PUBLIC python app ever written. Trust me."
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()

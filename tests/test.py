import os
import sys
import unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spycis import wrappers
from spycis.wrappers.example import ExampleWrapper


class WrappersTests(unittest.TestCase):

    def test_get_all_returns_example_wrapper_class(self):
        example_wrapper = ExampleWrapper
        wrapper_list = wrappers.get_all()
        self.assertIn(example_wrapper, wrapper_list)

    def test_get_instances_result_contains_an_example_wrapper_instance(self):
        instance_list = wrappers.get_instances()
        self.assertNotEqual([], [i for i in instance_list if isinstance(i, ExampleWrapper)])

    def test_get_example_wrapper_instance_by_name_returns_valid_instance(self):
        self.assertTrue(isinstance(wrappers.get_by_name("example"), ExampleWrapper))


if __name__ == "__main__":
    unittest.main()

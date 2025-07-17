#!/usr/bin/env python3
"""Test module for utils.access_nested_map function."""
import unittest
from utils import access_nested_map

class TestAccessNestedMapBase(unittest.TestCase):
    """Base test cases for the access_nested_map function."""
    
    def test_access_nested_map_one(self):
        """Test that access_nested_map returns 1 for {'a': 1} with path ('a',)."""
        self.assertEqual(access_nested_map({"a": 1}, ("a",)), 1)

    def test_access_nested_map_two(self):
        """Test that access_nested_map returns {'b': 2} for {'a': {'b': 2}} with path ('a',)."""
        self.assertEqual(access_nested_map({"a": {"b": 2}}, ("a",)), {"b": 2})

    def test_access_nested_map_three(self):
        """Test that access_nested_map returns 2 for {'a': {'b': 2}} with path ('a', 'b')."""
        self.assertEqual(access_nested_map({"a": {"b": 2}}, ("a", "b")), 2)

    def test_access_nested_map_exception_one(self):
        """Test that access_nested_map raises KeyError with 'a' for {} with path ('a',)."""
        with self.assertRaises(KeyError) as context:
            access_nested_map({}, ("a",))
        self.assertEqual(str(context.exception), "a")

    def test_access_nested_map_exception_two(self):
        """Test that access_nested_map raises KeyError with 'b' for {'a': 1} with path ('a', 'b')."""
        with self.assertRaises(KeyError) as context:
            access_nested_map({"a": 1}, ("a", "b"))
        self.assertEqual(str(context.exception), "b")

if __name__ == '__main__':
    unittest.main()
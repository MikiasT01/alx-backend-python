#!/usr/bin/env python3
"""Test module for utils.access_nested_map and utils.get_json functions."""
import unittest
from unittest.mock import Mock, patch
from utils import access_nested_map, get_json

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
        self.assertEqual(str(context.exception), "'a'")

    def test_access_nested_map_exception_two(self):
        """Test that access_nested_map raises KeyError with 'b' for {'a': 1} with path ('a', 'b')."""
        with self.assertRaises(KeyError) as context:
            access_nested_map({"a": 1}, ("a", "b"))
        self.assertEqual(str(context.exception), "'b'")

class TestGetJson(unittest.TestCase):
    """Test cases for the get_json function."""
    
    @patch('utils.requests.get')
    def test_get_json_example_com(self, mock_get):
        """Test get_json with http://example.com returns {'payload': True}."""
        mock_response = Mock()
        mock_response.json.return_value = {"payload": True}
        mock_get.return_value = mock_response
        
        result = get_json("http://example.com")
        self.assertEqual(result, {"payload": True})
        mock_get.assert_called_once_with("http://example.com")

    @patch('utils.requests.get')
    def test_get_json_holberton_io(self, mock_get):
        """Test get_json with http://holberton.io returns {'payload': False}."""
        mock_response = Mock()
        mock_response.json.return_value = {"payload": False}
        mock_get.return_value = mock_response
        
        result = get_json("http://holberton.io")
        self.assertEqual(result, {"payload": False})
        mock_get.assert_called_once_with("http://holberton.io")

if __name__ == '__main__':
    unittest.main()
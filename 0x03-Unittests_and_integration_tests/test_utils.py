#!/usr/bin/env python3
"""Test module for utils module functions."""
import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from unittest.mock import patch

class TestAccessNestedMap(unittest.TestCase):
    """Test class for access_nested_map function."""
    
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: dict, path: tuple, expected: any) -> None:
        """Test that access_nested_map returns the expected result.
        
        Args:
            nested_map (dict): The nested dictionary to access.
            path (tuple): The path to the desired value.
            expected (any): The expected output value.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "'a'"),
        ({"a": 1}, ("a", "b"), "'b'"),
    ])
    def test_access_nested_map_exception(self, nested_map: dict, path: tuple, expected_msg: str) -> None:
        """Test that access_nested_map raises KeyError with expected message.
        
        Args:
            nested_map (dict): The nested dictionary to access.
            path (tuple): The path that should raise an error.
            expected_msg (str): The expected error message.
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), expected_msg)

class TestGetJson(unittest.TestCase):
    """Test class for get_json function."""
    
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url: str, test_payload: dict) -> None:
        """Test that get_json returns the expected payload with mocked HTTP call.
        
        Args:
            test_url (str): The URL to mock the HTTP request.
            test_payload (dict): The expected JSON payload.
        """
        with patch('requests.get') as mock_get:
            mock_get.return_value.json.return_value = test_payload
            mock_get.return_value.status_code = 200
            result = get_json(test_url)
            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)

class TestMemoize(unittest.TestCase):
    """Test class for memoize decorator."""
    
    def test_memoize(self) -> None:
        """Test that memoize calls the method only once."""
        class TestClass:
            """Test class with memoized property."""
            def a_method(self) -> int:
                """Return a constant value.
                
                Returns:
                    int: The value 42.
                """
                return 42
            @memoize
            def a_property(self) -> int:
                """Return the result of a_method.
                
                Returns:
                    int: The cached result of a_method.
                """
                return self.a_method()
        
        with patch.object(TestClass, 'a_method') as mock_method:
            mock_method.return_value = 42
            test_class = TestClass()
            result1 = test_class.a_property
            result2 = test_class.a_property
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()

if __name__ == '__main__':
    unittest.main()
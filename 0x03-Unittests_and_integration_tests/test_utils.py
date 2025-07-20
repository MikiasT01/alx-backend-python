#!/usr/bin/env python3
"""Test module for utils.access_nested_map."""
import unittest
from parameterized import parameterized
from utils import access_nested_map

class TestAccessNestedMap(unittest.TestCase):
    """Test class for access_nested_map function."""
    
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test that access_nested_map returns the expected result."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

if __name__ == '__main__':
    unittest.main()#!/usr/bin/env python3
"""Test module for utils.access_nested_map."""
import unittest
from parameterized import parameterized
from utils import access_nested_map

class TestAccessNestedMap(unittest.TestCase):
    """Test class for access_nested_map function."""
    
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test that access_nested_map returns the expected result."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

   
    @parameterized.expand([
        ({}, ("a",), "'a'"),
        ({"a": 1}, ("a", "b"), "'b'"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_msg):
        """Test that access_nested_map raises KeyError with expected message."""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), expected_msg)

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """Test that get_json returns the expected payload with mocked HTTP call."""
        with unittest.mock.patch('requests.get') as mock_get:
            mock_get.return_value.json.return_value = test_payload
            mock_get.return_value.status_code = 200
            result = get_json(test_url)
            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)

    def test_memoize(self):
        """Test that memoize calls the method only once."""
        class TestClass:
            """Test class with memoized property."""
            def a_method(self):
                """Return a constant value."""
                return 42
            @memoize
            def a_property(self):
                """Return the result of a_method."""
                return self.a_method()
        
        with unittest.mock.patch.object(TestClass, 'a_method') as mock_method:
            mock_method.return_value = 42
            test_class = TestClass()
            result1 = test_class.a_property
            result2 = test_class.a_property
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()


    #!/usr/bin/env python3
"""Test module for client.GithubOrgClient."""
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that org returns the correct value with mocked get_json."""
        mock_get_json.return_value = {"name": org_name}
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, {"name": org_name})
        mock_get_json.assert_called_once()

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the expected URL."""
        with patch('client.GithubOrgClient.org', new_callable=unittest.mock.PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "http://example.com/repos"}
            client = GithubOrgClient("test")
            result = client._public_repos_url
            self.assertEqual(result, "http://example.com/repos")

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns the expected list."""
        with patch('client.GithubOrgClient._public_repos_url', new_callable=unittest.mock.PropertyMock) as mock_url:
            mock_url.return_value = "http://example.com/repos"
            mock_get_json.return_value = ["repo1", "repo2"]
            client = GithubOrgClient("test")
            result = client.public_repos()
            self.assertEqual(result, ["repo1", "repo2"])
            mock_get_json.assert_called_once()
            mock_url.assert_called_once()



    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license returns the expected boolean."""
        client = GithubOrgClient("test")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)
    

    import fixtures

class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class for GithubOrgClient."""

    @classmethod
    def setUpClass(cls):
        """Set up class with mocked requests.get."""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()
        cls.mock_get.side_effect = lambda url: unittest.mock.Mock(
            json=lambda: fixtures.ORG_PAYLOAD if "orgs/test" in url else fixtures.REPOS_PAYLOAD
        )

    @classmethod
    def tearDownClass(cls):
        """Tear down class by stopping the patcher."""
        cls.get_patcher.stop()

    @parameterized_class([
        {
            'org_payload': fixtures.ORG_PAYLOAD,
            'repos_payload': fixtures.REPOS_PAYLOAD,
            'expected_repos': fixtures.EXPECTED_REPOS,
            'apache2_repos': fixtures.APACE2_REPOS,
        }
    ])
    def test_public_repos(self):
        """Test public_repos with integration setup."""
        client = GithubOrgClient("test")
        result = client.public_repos()
        self.assertEqual(result, self.expected_repos)
if __name__ == '__main__':
    unittest.main()
    
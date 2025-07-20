#!/usr/bin/env python3
"""Test module for client.GithubOrgClient class."""
import unittest
from unittest.mock import patch
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
import fixtures

class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name: str, mock_get_json) -> None:
        """Test that org returns the correct value with mocked get_json.

        Args:
            org_name (str): The organization name to test.
            mock_get_json: Mock object for get_json function.
        """
        mock_get_json.return_value = {"name": org_name}
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, {"name": org_name})
        mock_get_json.assert_called_once()

    def test_public_repos_url(self) -> None:
        """Test that _public_repos_url returns the expected URL."""
        with patch('client.GithubOrgClient.org', new_callable=unittest.mock.PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "http://example.com/repos"}
            client = GithubOrgClient("test")
            result = client._public_repos_url
            self.assertEqual(result, "http://example.com/repos")

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json) -> None:
        """Test that public_repos returns the expected list.

        Args:
            mock_get_json: Mock object for get_json function.
        """
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
    def test_has_license(self, repo: dict, license_key: str, expected: bool) -> None:
        """Test that has_license returns the expected boolean.

        Args:
            repo (dict): The repository dictionary with license info.
            license_key (str): The license key to check.
            expected (bool): The expected return value.
        """
        client = GithubOrgClient("test")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)

@parameterized_class([
    {
        'org_payload': fixtures.ORG_PAYLOAD,
        'repos_payload': fixtures.REPOS_PAYLOAD,
        'expected_repos': fixtures.EXPECTED_REPOS,
        'apache2_repos': fixtures.APACE2_REPOS,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class for GithubOrgClient."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set up class with mocked requests.get."""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()
        cls.mock_get.side_effect = lambda url: unittest.mock.Mock(
            json=lambda: fixtures.ORG_PAYLOAD if "orgs/test" in url else fixtures.REPOS_PAYLOAD
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """Tear down class by stopping the patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """Test public_repos with integration setup."""
        client = GithubOrgClient("test")
        result = client.public_repos()
        self.assertEqual(result, self.expected_repos)

if __name__ == '__main__':
    unittest.main()
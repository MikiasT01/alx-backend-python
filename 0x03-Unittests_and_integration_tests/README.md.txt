# 0x03-Unittests_and_integration_tests

This directory contains code and tests for the "Unittests and Integration Tests" project as part of the ALX Software Engineering curriculum. The focus is on writing unit tests and understanding integration testing concepts using Python 3.7.

## Project Overview
- **Objective**: Learn to create unit tests with the `unittest` framework, use parameterized testing, and differentiate between unit and integration tests.
- **Tools**: `unittest`, `parameterized`, and mocking techniques.
- **Requirements**: All files must comply with Ubuntu 18.04, Python 3.7, pycodestyle (version 2.5), and include proper documentation and type annotations.

## Files
- `utils.py`: Contains utility functions like `access_nested_map`, `get_json`, and `memoize` for handling nested dictionaries, JSON data, and method memoization.
- `client.py`: Implements a `GithubOrgClient` class to interact with GitHub API data.
- `fixtures.py`: Provides test data (e.g., GitHub repository payloads) for testing.
- `test_utils.py`: Unit tests for the `utils` module, starting with parameterized tests for `access_nested_map`.


"""
Tests package for SIGMA Project

This module contains all automated tests for the SIGMA school management system.

Test Structure:
- tests/conftest.py: Pytest configuration and shared fixtures
- tests/factories.py: Factory Boy factories for test data creation
- tests/example_tests.py: Example test cases (models, views, forms, integration)
- tests/test_models.py: Model unit tests (after migration)
- tests/test_views.py: View/endpoint tests (after migration)
- tests/test_forms.py: Form validation tests (after migration)
- tests/test_integration.py: Integration/workflow tests (after migration)

Running Tests:
    pytest                          # Run all tests
    pytest -v                       # Verbose output
    pytest tests/test_models.py    # Run specific file
    pytest -m unit                  # Run unit tests only
    pytest --cov=apps              # With coverage report
    pytest -x                       # Stop on first failure

See example_tests.py for test examples and patterns.
See conftest.py for available fixtures.
See factories.py for creating test data.
"""

# Make this directory a Python package

"""
Pytest Configuration for SIGMA Project

This file configures pytest behavior and provides shared fixtures.
Place this file in the project root as pytest.ini or pyproject.toml [tool.pytest.ini_options]

Reference: https://docs.pytest.org/en/latest/reference.html
"""

# ============================================================================
# pytest.ini content
# ============================================================================

"""
[pytest]
# Django settings module
DJANGO_SETTINGS_MODULE = config.settings

# Python path (where to find manage.py)
python_files = tests.py test_*.py *_tests.py

# Patterns for test discovery
python_classes = Test*
python_functions = test_*

# Minimum Python version
minversion = 7.0

# Add current directory to Python path
pythonpath = .

# Show extra info
addopts = -v --strict-markers --tb=short --disable-warnings

# Database settings
# Django will use in-memory SQLite by default, which is fast
# Alternatively, use PostgreSQL:
# [testenv:django]
# setenv =
#     DATABASE_URL = postgresql://user:password@localhost:5432/sigma_test

# Markers for test categorization
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests
    smoke: marks tests as smoke tests
    database: marks tests that require database access
    django_db: marks tests that access the database
"""

import os
import django
from django.conf import settings

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import pytest
from django.test.utils import get_unique_databases_and_mirrors
from django.db import connections

# ============================================================================
# PYTEST CONFIGURATION
# ============================================================================

def pytest_configure(config):
    """
    Configure pytest
    This runs before test collection begins
    """
    config.addinivalue_line(
        "markers",
        "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers",
        "integration: integration tests"
    )
    config.addinivalue_line(
        "markers",
        "unit: unit tests"
    )
    config.addinivalue_line(
        "markers",
        "smoke: smoke tests"
    )


# ============================================================================
# SESSION-SCOPED FIXTURES (Run once per test session)
# ============================================================================

@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    """
    Setup database for testing
    This is called once at the start of the test session
    """
    with django_db_blocker.unblock():
        # Create the test database
        # (Django handles this automatically with pytest-django)
        pass


@pytest.fixture(scope='session')
def django_db_keepdb():
    """
    Keep test database between test runs for faster execution
    Set to False to recreate database each time
    """
    return False


# ============================================================================
# MODULE-SCOPED FIXTURES (Run once per test module)
# ============================================================================

@pytest.fixture(scope='module')
def db_setup(django_db_blocker):
    """Setup database before module tests"""
    with django_db_blocker.unblock():
        # Run migrations or setup
        pass


# ============================================================================
# FUNCTION-SCOPED FIXTURES (Run before each test function)
# ============================================================================

@pytest.fixture
def db_reset(db):
    """
    Ensure database is clean before each test
    (db fixture from pytest-django already does this)
    """
    yield db
    # Cleanup after test (if needed)


# ============================================================================
# COMMAND LINE OPTIONS
# ============================================================================

def pytest_addoption(parser):
    """Add custom command-line options"""
    parser.addoption(
        "--slow",
        action="store_true",
        default=False,
        help="run slow tests"
    )
    parser.addoption(
        "--integration",
        action="store_true",
        default=False,
        help="run integration tests"
    )
    parser.addoption(
        "--coverage",
        action="store_true",
        default=False,
        help="collect coverage data"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection based on markers"""
    
    # Skip slow tests unless --slow is passed
    if not config.getoption("--slow"):
        skip_slow = pytest.mark.skip(reason="need --slow option to run")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)
    
    # Skip integration tests unless --integration is passed
    if not config.getoption("--integration"):
        skip_integration = pytest.mark.skip(reason="need --integration option to run")
        for item in items:
            if "integration" in item.keywords:
                item.add_marker(skip_integration)


# ============================================================================
# FIXTURES FOR DJANGO
# ============================================================================

@pytest.fixture
def settings_override(settings):
    """
    Override settings for specific test
    
    Usage:
        def test_something(settings_override):
            settings_override.DEBUG = False
            ...
    """
    return settings


# ============================================================================
# FIXTURES FOR COMMON OPERATIONS
# ============================================================================

@pytest.fixture
def api_client():
    """Django test API client"""
    from django.test import Client
    return Client()


@pytest.fixture
def authenticated_client():
    """API client with authenticated user"""
    from django.test import Client
    from tests.factories import AkunFactory
    
    client = Client()
    user = AkunFactory()
    client.force_login(user)
    return client


# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

import logging

# Configure logging for tests
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Suppress noisy loggers
logging.getLogger('django').setLevel(logging.WARNING)
logging.getLogger('django.db.backends').setLevel(logging.WARNING)
logging.getLogger('factory').setLevel(logging.WARNING)


# ============================================================================
# TEST RUNNING TIPS
# ============================================================================

"""
RUNNING TESTS:

1. Run all tests:
   pytest
   pytest tests/

2. Run specific test file:
   pytest tests/test_models.py
   pytest tests/example_tests.py

3. Run specific test class:
   pytest tests/example_tests.py::TestAkunModel

4. Run specific test function:
   pytest tests/example_tests.py::TestAkunModel::test_akun_creation

5. Run with verbose output:
   pytest -v
   pytest -vv

6. Run with coverage:
   pytest --cov=apps --cov-report=html
   pytest --cov=apps --cov-report=term-missing

7. Run with coverage for specific file:
   pytest --cov=apps.users --cov-report=html tests/test_models.py

8. Run marked tests:
   pytest -m unit
   pytest -m integration
   pytest -m "not slow"

9. Run slow tests:
   pytest --slow

10. Run integration tests:
    pytest --integration

11. Stop on first failure:
    pytest -x
    pytest --exitfirst

12. Show print statements:
    pytest -s
    pytest --capture=no

13. Run last failed tests:
    pytest --lf
    pytest --last-failed

14. Run failed first, then others:
    pytest --ff

15. Parallel execution (requires pytest-xdist):
    pytest -n 4  # Run on 4 workers
    pytest -n auto

16. Run tests matching keyword:
    pytest -k test_akun
    pytest -k "not test_slow"

17. Run with specific database:
    pytest --ds=config.settings

18. Create test report:
    pytest --html=report.html --self-contained-html
    pytest --junit-xml=report.xml

USEFUL PYTEST PLUGINS:
- pytest-django: Django integration (required)
- pytest-cov: Coverage reporting
- pytest-xdist: Parallel execution
- pytest-html: HTML reports
- freezegun: Time mocking
- pytest-factoryboy: Factory Boy integration

INSTALL:
pip install pytest pytest-django pytest-cov pytest-xdist pytest-html freezegun
"""

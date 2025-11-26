# SIGMA Project - Testing Guide

Complete testing setup with pytest, Factory Boy, and Django test utilities.

## Quick Start

### 1. Install Test Dependencies

```bash
pip install pytest pytest-django pytest-cov factory-boy freezegun pytest-factoryboy
```

Or from the pyproject.toml dev dependencies:

```bash
pip install -e ".[dev]"
```

### 2. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=apps --cov-report=html

# Run specific test file
pytest tests/example_tests.py -v

# Run specific test class
pytest tests/example_tests.py::TestAkunModel -v

# Run specific test
pytest tests/example_tests.py::TestAkunModel::test_akun_creation -v
```

### 3. View Coverage Report

```bash
# After running with --cov-report=html
open htmlcov/index.html
```

## Project Structure

```
tests/
├── __init__.py              # Package marker
├── conftest.py             # Pytest configuration and shared fixtures
├── factories.py            # Factory Boy factories for test data
├── example_tests.py        # Example test cases (read this first!)
├── test_models.py          # Model tests (to be created)
├── test_views.py           # View tests (to be created)
├── test_forms.py           # Form tests (to be created)
└── test_integration.py     # Integration tests (to be created)

conftest.py                 # Root pytest configuration
pytest.ini                  # Pytest settings
```

## Files Explained

### conftest.py
Root pytest configuration file with:
- Django settings configuration
- Shared pytest fixtures
- Custom command-line options
- Logging configuration

**Key fixtures:**
```python
@pytest.fixture
def admin_user()        # Admin account for testing
@pytest.fixture
def teacher_user()      # Teacher account for testing
@pytest.fixture
def student_user()      # Student account for testing
@pytest.fixture
def school_data()       # Complete school structure
```

### factories.py
Factory Boy factories for creating test objects:

```python
# Create single instance
akun = AkunFactory(email='test@test.id')

# Create multiple instances
siswa_list = SiswaFactory.create_batch(5)

# Build without saving
akun = AkunFactory.build()
```

**Available factories:**
- `AkunFactory`, `AdminAkunFactory` - Users
- `SiswaFactory`, `GuruFactory`, `WaliFactory` - Persons
- `TahunAjaranFactory`, `JurusanFactory`, `KelasFactory` - Academic structure
- `MapelFactory`, `JadwalFactory` - Subjects and schedules
- `TugasFactory`, `NilaiFactory`, `PresensiFactory` - Grades
- `SchoolBatchFactory` - Complete school structure

### example_tests.py
Comprehensive test examples covering:
- **Model tests** - Testing model methods, constraints, relationships
- **Form tests** - Testing form validation
- **View tests** - Testing endpoints, permissions, rendering
- **Integration tests** - Testing workflows across models

Read this file to understand the testing patterns.

## Test Categories

### Unit Tests
Test individual model methods, form validation, etc.

```python
@pytest.mark.unit
def test_akun_creation():
    akun = AkunFactory(email='test@test.id')
    assert akun.email == 'test@test.id'
```

Run with: `pytest -m unit`

### Integration Tests
Test workflows across multiple models/views.

```python
@pytest.mark.integration
def test_student_enrollment_workflow():
    # Create student, enroll in class, assign grades, etc.
    pass
```

Run with: `pytest -m integration`

### Smoke Tests
Quick tests to verify basic functionality.

```python
@pytest.mark.smoke
def test_akun_model_exists():
    assert Akun is not None
```

Run with: `pytest -m smoke`

## Common Patterns

### Testing Models

```python
class TestAkunModel:
    def test_akun_creation(self):
        akun = AkunFactory(email='test@test.id')
        assert akun.email == 'test@test.id'
        assert akun.check_password('testpassword123')
    
    def test_email_unique(self):
        AkunFactory(email='same@test.id')
        with pytest.raises(Exception):  # IntegrityError
            AkunFactory(email='same@test.id')
```

### Testing Views

```python
class TestAkunListView:
    @pytest.fixture
    def client(self):
        return Client()
    
    @pytest.fixture
    def admin_user(self):
        return AdminAkunFactory()
    
    def test_requires_login(self, client):
        response = client.get(reverse('users:akun_list'))
        assert response.status_code == 302  # Redirect
    
    def test_admin_can_view(self, client, admin_user):
        client.login(username=admin_user.email, password='testpassword123')
        response = client.get(reverse('users:akun_list'))
        assert response.status_code == 200
```

### Testing with Database Transactions

```python
@pytest.mark.django_db
def test_with_database():
    # This test has access to the database
    akun = AkunFactory()
    assert Akun.objects.filter(email=akun.email).exists()
```

### Parametrized Tests (Test Multiple Values)

```python
@pytest.mark.parametrize('status', ['Hadir', 'Sakit', 'Izin', 'Alpha'])
def test_presensi_status_choices(status):
    presensi = PresensiFactory(status=status)
    assert presensi.status == status
```

### Using Fixtures

```python
@pytest.fixture
def sample_school():
    """Create complete school structure"""
    return SchoolBatchFactory.create()

def test_with_school_data(sample_school):
    # sample_school contains tahun_ajaran, kelas_list, siswa_list, etc.
    assert len(sample_school['kelas_list']) > 0
```

## Command Reference

### Running Tests

```bash
# Run all tests
pytest

# Run specific file
pytest tests/example_tests.py

# Run specific test
pytest tests/example_tests.py::TestAkunModel::test_akun_creation

# Run with markers
pytest -m unit              # Only unit tests
pytest -m integration       # Only integration tests
pytest -m "not slow"        # Skip slow tests

# Run with options
pytest -v                   # Verbose
pytest -vv                  # Very verbose
pytest -s                   # Show print statements
pytest -x                   # Stop on first failure
pytest --lf                 # Run last failed
pytest --ff                 # Failed first, then others
```

### Coverage Reports

```bash
# Generate coverage report
pytest --cov=apps --cov-report=html

# View specific app
pytest --cov=apps.users --cov-report=html

# Terminal report
pytest --cov=apps --cov-report=term-missing

# With branch coverage
pytest --cov=apps --cov-branch --cov-report=html
```

### Performance

```bash
# Parallel execution (requires pytest-xdist)
pytest -n 4              # Run on 4 workers
pytest -n auto           # Auto-detect workers

# Timing information
pytest --durations=10    # Show slowest 10 tests

# Profile tests
pytest --profile         # Requires pytest-profiling
```

### Reporting

```bash
# HTML report
pytest --html=report.html --self-contained-html

# JUnit XML (CI/CD)
pytest --junit-xml=report.xml

# Coverage XML (CI/CD)
pytest --cov=apps --cov-report=xml
```

## Best Practices

### 1. Use Factories Instead of Fixtures

❌ **Bad:** Create objects in fixtures
```python
@pytest.fixture
def akun():
    return Akun.objects.create(email='test@test.id', ...)
```

✅ **Good:** Use factories
```python
def test_something():
    akun = AkunFactory(email='test@test.id')
```

### 2. Test One Thing Per Test

❌ **Bad:** Multiple assertions for different behaviors
```python
def test_akun():
    akun = AkunFactory()
    assert akun.email
    assert akun.is_active
    assert akun.check_password('testpassword123')
```

✅ **Good:** Separate tests
```python
def test_akun_has_email():
    akun = AkunFactory()
    assert akun.email

def test_akun_is_active():
    akun = AkunFactory()
    assert akun.is_active

def test_akun_password_hashing():
    akun = AkunFactory()
    assert akun.check_password('testpassword123')
```

### 3. Use Descriptive Names

❌ **Bad:** `test_1`, `test_akun`, `test_fail`
✅ **Good:** `test_akun_creation`, `test_email_unique`, `test_invalid_password_raises_error`

### 4. Use pytest Markers

```python
@pytest.mark.slow
def test_complex_calculation():
    pass

@pytest.mark.integration
def test_complete_workflow():
    pass
```

Run with: `pytest -m "not slow"`, `pytest -m integration`

### 5. Test Edge Cases

```python
def test_empty_name():
    siswa = SiswaFactory(first_name='', last_name='')
    # Test behavior

def test_future_birthday():
    siswa = SiswaFactory(tanggal_lahir=date(2099, 1, 1))
    # Test behavior

def test_null_optional_field():
    jadwal = JadwalFactory(ruangan=None)
    # Test behavior
```

## Troubleshooting

### "Module not found" Errors

Ensure `pythonpath = .` is set in pytest.ini and run tests from project root:
```bash
cd c:\Users\fatha\sigma
pytest
```

### Database Lock Errors

Django test database is locked. Clear temp files:
```bash
rm -rf db.sqlite3-journal
pytest
```

### "django.core.exceptions.ImproperlyConfigured"

Ensure `DJANGO_SETTINGS_MODULE` is set correctly in pytest.ini or conftest.py.

### Import Errors in Factories

Ensure factories.py imports are correct. Run:
```bash
python -c "from tests.factories import AkunFactory"
```

## Next Steps

1. **Copy example_tests.py patterns** to create test files for each app
2. **Run pytest --cov** to see coverage gaps
3. **Aim for 80%+ coverage** on critical models and views
4. **Add CI/CD pipeline** to run tests on every commit
5. **Expand tests** as new features are added

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [pytest-django Documentation](https://pytest-django.readthedocs.io/)
- [Factory Boy Documentation](https://factoryboy.readthedocs.io/)
- [Django Testing Documentation](https://docs.djangoproject.com/en/stable/topics/testing/)

## Support

For issues or questions about the test setup, refer to:
- `conftest.py` - Configuration
- `factories.py` - Factory definitions
- `example_tests.py` - Test examples and patterns
- Documentation files in `/docs/` folder

# SIGMA - Test Plan & Example Test Cases

**Document Date**: November 26, 2025  
**Current Coverage**: 0% (No tests exist yet)  
**Target Coverage**: 80%+

---

## 1. Testing Strategy

### **1.1 Testing Pyramid**

```
         /\
        /  \    E2E Tests (10%)
       /____\   - Full workflows
      /      \  - Selenium/Playwright
     /        \
    /          \ Integration Tests (20%)
   /____________\ - Multiple models
  /              \ - View + Form + Model
 /                \
/____Unit Tests____\ Unit Tests (70%)
- Models: 90%      - Single function
- Forms: 85%       - No DB/network
- Views: 80%       - Fast feedback
- Utils: 90%
```

### **1.2 Test Scope**

| Layer | What to Test | Coverage Goal |
|-------|-------------|--------------|
| Models | Validations, relationships, methods | 90% |
| Forms | Field validation, save logic | 85% |
| Views | Permission checks, data filtering, context | 80% |
| Integration | User workflows, CRUD operations | 60% |
| E2E | Full scenarios (login → create → view) | 40% |

### **1.3 Testing Stack**

**Tools**:
- **pytest**: Test runner
- **pytest-django**: Django integration
- **factory-boy**: Test data generation
- **pytest-cov**: Coverage reporting
- **responses**: Mock external APIs (if needed)
- **faker**: Fake data generation

**Installation**:
```bash
pip install pytest pytest-django factory-boy faker pytest-cov
```

**Configuration** (`pytest.ini`):
```ini
[pytest]
DJANGO_SETTINGS_MODULE = config.settings
python_files = tests.py test_*.py *_tests.py
addopts = --cov=apps --cov-report=html --cov-report=term
testpaths = tests
```

---

## 2. Unit Tests

### **2.1 Model Tests** (`tests/test_models.py`)

**Test Coverage for Key Models**:

#### **PersonModel (Abstract Base)**
- ✅ `get_full_name()` returns correct format
- ✅ `get_age()` calculates correctly
- ✅ Fields required: first_name, last_name, alamat, tanggal_lahir, nomor_handphone
- ✅ Gender choices validation
- ✅ Timestamps auto_now and auto_now_add

#### **Akun (User)**
- ✅ Email-based authentication (not username)
- ✅ Password hashing (set_password)
- ✅ Role properties: is_guru, is_siswa, is_admin, etc.
- ✅ Unique email constraint
- ✅ Created_at timestamp

#### **Peran (Role)**
- ✅ Unique role names
- ✅ Foreign key relationship with Akun

#### **Siswa (Student)**
- ✅ OneToOne relationship with Akun
- ✅ NIS unique
- ✅ Inherits Person fields
- ✅ Related objects (KelasSiswa, SiswaWali, Nilai, Presensi)

#### **Guru (Teacher)**
- ✅ OneToOne relationship with Akun
- ✅ NIP unique
- ✅ Jabatan field
- ✅ Related objects (Kelas, Jadwal)

#### **TahunAjaran (Academic Year)**
- ✅ Unique together (tahun, semester)
- ✅ is_active boolean
- ✅ Date range validation (mulai < selesai)

#### **Kelas (Class)**
- ✅ Unique together (nama, tahun_ajaran)
- ✅ Foreign key validations (jurusan, wali_kelas, tahun_ajaran)
- ✅ Related objects (KelasSiswa, Jadwal)

#### **Jadwal (Schedule)**
- ✅ Unique constraints on (kelas, hari, jam_mulai) and (guru, hari, jam_mulai)
- ✅ Time validation (jam_mulai < jam_selesai)
- ✅ Related objects (Tugas, Nilai, Presensi)

#### **Nilai (Grade)**
- ✅ Tipe_penilaian choices validation
- ✅ Nilai range validation (0-100)
- ✅ Unique validation per tipe (except Tugas)
- ✅ Tugas required for tipe='Tugas'
- ✅ Foreign key constraints

#### **Presensi (Attendance)**
- ✅ Status choices validation
- ✅ Unique together (siswa, jadwal, tanggal)
- ✅ Date validation

### **2.2 Form Tests** (`tests/test_forms.py`)

#### **AkunCreationForm**
- ✅ Valid form with correct email, password, password2
- ✅ Password mismatch validation
- ✅ Password strength validation
- ✅ Email unique validation
- ✅ Save method sets password correctly

#### **AkunChangeForm**
- ✅ Valid form with all fields
- ✅ Email update
- ✅ Role assignment
- ✅ Permission assignment
- ✅ is_active/is_staff/is_superuser toggle

### **2.3 View Tests** (`tests/test_views.py`)

#### **Authentication Views**
- ✅ Unauthenticated users redirect to login
- ✅ LoginRequiredMixin enforced
- ✅ PermissionRequiredMixin enforced (403 if no permission)

#### **AkunListView**
- ✅ Requires 'users.view_akun' permission
- ✅ Returns paginated list (10 per page)
- ✅ Search filter by email/peran__nama works
- ✅ HTMX requests return partial template
- ✅ Non-HTMX requests return full template

#### **AkunCreateView**
- ✅ Requires 'users.add_akun' permission
- ✅ GET returns form
- ✅ POST with valid data creates Akun
- ✅ POST invalid data returns form with errors
- ✅ Redirects to akun_list on success

#### **AkunUpdateView**
- ✅ Requires 'users.change_akun' permission
- ✅ Can update email, role, permissions
- ✅ Shows success message on save
- ✅ HTMX support

#### **DashboardView**
- ✅ Requires authentication
- ✅ Superuser sees counts (total_akun, total_peran, etc.)
- ✅ Non-superuser doesn't see counts
- ✅ Context has role flags (is_admin, is_guru)

#### **KelasListView**
- ✅ Filters to active academic year only
- ✅ Uses select_related('jurusan', 'wali_kelas', 'tahun_ajaran')
- ✅ Annotates student count
- ✅ Search by class name works

#### **JadwalListView**
- ✅ Students see only their class schedule
- ✅ Teachers see all schedules
- ✅ Uses multiple select_related for performance
- ✅ Ordered by day, time

---

## 3. Integration Tests

### **3.1 User Creation & Authentication Flow**

**Scenario**: Admin creates student account, student logs in, sees dashboard

```python
def test_student_account_creation_and_login():
    # Setup
    peran = PeranFactory(nama='Siswa')
    
    # Admin creates student account
    admin = AkunFactory(is_superuser=True, peran=PeranFactory(nama='Admin'))
    form_data = {
        'email': 'student@school.id',
        'password': 'SecurePassword123!',
        'password2': 'SecurePassword123!',
        'peran': peran.id
    }
    form = AkunCreationForm(data=form_data)
    assert form.is_valid()
    
    student_akun = form.save()
    assert student_akun.email == 'student@school.id'
    assert student_akun.peran == peran
    
    # Student logs in
    login_successful = client.login(username='student@school.id', password='SecurePassword123!')
    assert login_successful
    
    # Student accesses dashboard
    response = client.get('/dashboard/')
    assert response.status_code == 200
    assert 'dashboard' in response.context
```

### **3.2 Class Assignment Workflow**

**Scenario**: Teacher is assigned to class, students enrolled, schedule created

```python
def test_class_assignment_workflow():
    # Create academic year
    tahun_ajaran = TahunAjaranFactory(is_active=True)
    
    # Create jurusan
    jurusan = JurusanFactory()
    
    # Create guru (teacher)
    guru = GuruFactory()
    
    # Create class
    kelas = KelasFactory(
        jurusan=jurusan,
        wali_kelas=guru,
        tahun_ajaran=tahun_ajaran
    )
    
    # Enroll students
    siswa1, siswa2 = SiswaFactory(), SiswaFactory()
    KelasSiswaFactory(siswa=siswa1, kelas=kelas, tahun_ajaran=tahun_ajaran)
    KelasSiswaFactory(siswa=siswa2, kelas=kelas, tahun_ajaran=tahun_ajaran)
    
    # Verify class has 2 students
    assert kelas.kelassiswa_set.count() == 2
    
    # Create schedule
    mapel = MapelFactory(nama='Mathematics')
    jadwal = JadwalFactory(
        kelas=kelas,
        mapel=mapel,
        guru=guru,
        hari='Senin',
        jam_mulai=datetime.time(7, 0),
        jam_selesai=datetime.time(8, 0)
    )
    
    # Verify schedule exists
    assert Jadwal.objects.filter(kelas=kelas).count() == 1
```

### **3.3 Grade Entry & Retrieval**

**Scenario**: Teacher enters grades, student views grades

```python
def test_grade_entry_and_viewing():
    # Setup
    jadwal = JadwalFactory()
    siswa = jadwal.kelas.kelassiswa_set.first().siswa
    
    # Teacher creates grade
    nilai = NilaiFactory(
        siswa=siswa,
        jadwal=jadwal,
        tipe_penilaian='Ujian Harian',
        nilai=85.5,
        tanggal_penilaian=date.today()
    )
    
    # Verify grade created
    assert nilai.siswa == siswa
    assert nilai.nilai == 85.5
    
    # Student views grades
    client.login(username=siswa.akun.email, password='password')
    response = client.get('/grades/nilai/')
    
    # Verify student sees their grade
    assert 85.5 in str(response.content)
```

---

## 4. Test Fixtures & Factories

### **4.1 Factory Pattern** (`tests/factories.py`)

```python
import factory
from factory.django import DjangoModelFactory
from faker import Faker

fake = Faker()

class PeranFactory(DjangoModelFactory):
    class Meta:
        model = 'users.Peran'
    nama = factory.Sequence(lambda n: f'Peran_{n}')

class AkunFactory(DjangoModelFactory):
    class Meta:
        model = 'users.Akun'
    email = factory.Faker('email')
    peran = factory.SubFactory(PeranFactory)
    is_active = True
    
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        obj = model_class(*args, **kwargs)
        obj.set_password('testpassword123')
        obj.save()
        return obj

class SiswaFactory(DjangoModelFactory):
    class Meta:
        model = 'users.Siswa'
    akun = factory.SubFactory(AkunFactory)
    nis = factory.Sequence(lambda n: f'NIS{n:06d}')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    alamat = factory.Faker('address')
    tanggal_lahir = factory.Faker('date_of_birth')
    nomor_handphone = factory.Faker('phone_number')

class TahunAjaranFactory(DjangoModelFactory):
    class Meta:
        model = 'academics.TahunAjaran'
    tahun = '2024/2025'
    semester = 'Ganjil'
    tanggal_mulai = date(2024, 7, 1)
    tanggal_selesai = date(2024, 12, 31)
    is_active = False

class KelasFactory(DjangoModelFactory):
    class Meta:
        model = 'academics.Kelas'
    nama = factory.Sequence(lambda n: f'XI IPA-{n}')
    jurusan = factory.SubFactory(JurusanFactory)
    wali_kelas = factory.SubFactory(GuruFactory)
    tahun_ajaran = factory.SubFactory(TahunAjaranFactory)

# ... More factories for other models
```

### **4.2 Test Data Fixtures** (`tests/fixtures.py`)

**Predefined Test Data**:
- Sample Peran (Admin, Guru, Siswa)
- Sample Akun (admin, teacher, student)
- Sample TahunAjaran (2024/2025 Ganjil + Genap)
- Sample Jurusan (IPA, IPS, Bisnis)
- Sample Mapel (Math, Physics, etc.)

**Usage**:
```python
@pytest.fixture
def sample_school_data():
    """Creates a complete sample school structure"""
    tahun = TahunAjaranFactory(is_active=True)
    admin = AkunFactory(is_superuser=True)
    guru = GuruFactory()
    kelas = KelasFactory(wali_kelas=guru, tahun_ajaran=tahun)
    siswa_list = [SiswaFactory() for _ in range(10)]
    
    return {
        'tahun_ajaran': tahun,
        'admin': admin,
        'guru': guru,
        'kelas': kelas,
        'siswa_list': siswa_list
    }
```

---

## 5. Test Execution

### **5.1 Run All Tests**

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=apps --cov-report=html

# Run specific app tests
pytest tests/test_users_views.py

# Run specific test
pytest tests/test_models.py::test_siswa_full_name

# Run with verbose output
pytest -v

# Run and stop on first failure
pytest -x

# Run last failed tests
pytest --lf
```

### **5.2 Coverage Reports**

```bash
# Generate HTML report
pytest --cov=apps --cov-report=html

# View coverage summary
pytest --cov=apps --cov-report=term

# Coverage by module
pytest --cov=apps --cov-report=term-missing
```

### **5.3 CI/CD Integration**

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest --cov=apps
      - uses: codecov/codecov-action@v2
```

---

## 6. Example Test File Structure

### **File: `tests/test_models.py`**

```python
import pytest
from datetime import date, datetime
from django.core.exceptions import ValidationError
from django.test import TestCase
from factory.django import DjangoModelFactory

from apps.users.models import Akun, Siswa, Guru, Peran
from apps.academics.models import Kelas, TahunAjaran, Jurusan
from apps.grades.models import Nilai, Presensi

from .factories import (
    AkunFactory, SiswaFactory, GuruFactory, PeranFactory,
    KelasFactory, TahunAjaranFactory, JurusanFactory,
    NilaiFactory, PresensiFactory, JadwalFactory, MapelFactory
)

pytestmark = pytest.mark.django_db  # All tests in this module use DB

# --- AKUN TESTS ---

def test_akun_creation():
    """Test creating an account with email and password"""
    akun = AkunFactory(email='test@school.id')
    assert akun.email == 'test@school.id'
    assert akun.check_password('testpassword123')

def test_akun_unique_email():
    """Test email uniqueness constraint"""
    AkunFactory(email='duplicate@school.id')
    with pytest.raises(Exception):  # IntegrityError
        AkunFactory(email='duplicate@school.id')

def test_akun_role_properties():
    """Test role-based properties"""
    peran_guru = PeranFactory(nama='Guru')
    akun = AkunFactory(peran=peran_guru)
    
    assert akun.is_guru is True
    assert akun.is_siswa is False
    assert akun.is_admin is False

# --- SISWA TESTS ---

def test_siswa_full_name():
    """Test get_full_name method"""
    siswa = SiswaFactory(first_name='John', last_name='Doe')
    assert siswa.get_full_name() == 'John Doe'

def test_siswa_age_calculation():
    """Test get_age method"""
    birth_date = datetime(2007, 1, 15)
    siswa = SiswaFactory(tanggal_lahir=birth_date)
    expected_age = date.today().year - 2007
    assert siswa.get_age() == expected_age

def test_siswa_nis_unique():
    """Test NIS uniqueness"""
    SiswaFactory(nis='12345')
    with pytest.raises(Exception):
        SiswaFactory(nis='12345')

# --- KELAS TESTS ---

def test_kelas_unique_per_year():
    """Test unique constraint on (nama, tahun_ajaran)"""
    tahun = TahunAjaranFactory()
    KelasFactory(nama='XI IPA-1', tahun_ajaran=tahun)
    
    # Same name, same year should fail
    with pytest.raises(Exception):
        KelasFactory(nama='XI IPA-1', tahun_ajaran=tahun)
    
    # Different year should work
    tahun2 = TahunAjaranFactory(tahun='2025/2026')
    kelas2 = KelasFactory(nama='XI IPA-1', tahun_ajaran=tahun2)
    assert kelas2.id is not None

# --- NILAI TESTS ---

def test_nilai_validation_non_tugas():
    """Test unique validation for non-Tugas grades"""
    jadwal = JadwalFactory()
    siswa = SiswaFactory()
    
    # Create first grade
    nilai1 = NilaiFactory(
        siswa=siswa,
        jadwal=jadwal,
        tipe_penilaian='Ujian Harian'
    )
    
    # Create second grade of same type should fail validation
    nilai2 = Nilai(
        siswa=siswa,
        jadwal=jadwal,
        tipe_penilaian='Ujian Harian'
    )
    
    with pytest.raises(ValidationError):
        nilai2.clean()

def test_nilai_tugas_requires_tugas_id():
    """Test that Tugas type requires tugas_id"""
    jadwal = JadwalFactory()
    siswa = SiswaFactory()
    
    nilai = Nilai(
        siswa=siswa,
        jadwal=jadwal,
        tipe_penilaian='Tugas',
        tugas=None  # Missing tugas
    )
    
    with pytest.raises(ValidationError):
        nilai.clean()
```

### **File: `tests/test_views.py`**

```python
import pytest
from django.test import Client
from django.urls import reverse

from apps.users.models import Akun, Peran
from .factories import AkunFactory, PeranFactory, SiswaFactory, KelasFactory

pytestmark = pytest.mark.django_db

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def admin_user():
    peran = PeranFactory(nama='Admin')
    return AkunFactory(email='admin@test.id', is_superuser=True, peran=peran)

@pytest.fixture
def student_user():
    peran = PeranFactory(nama='Siswa')
    return AkunFactory(email='student@test.id', peran=peran)

class TestAkunListView:
    def test_requires_login(self, client):
        """Test unauthenticated users are redirected"""
        response = client.get(reverse('users:akun_list'))
        assert response.status_code == 302  # Redirect
        assert 'login' in response.url
    
    def test_requires_permission(self, client, student_user):
        """Test permission_required decorator"""
        client.login(username=student_user.email, password='testpassword123')
        response = client.get(reverse('users:akun_list'))
        assert response.status_code == 403  # Forbidden
    
    def test_list_displays_accounts(self, client, admin_user):
        """Test list view displays accounts"""
        client.login(username=admin_user.email, password='testpassword123')
        
        # Create some test accounts
        AkunFactory.create_batch(3)
        
        response = client.get(reverse('users:akun_list'))
        assert response.status_code == 200
        assert 'object_list' in response.context
        assert len(response.context['object_list']) >= 3
    
    def test_search_by_email(self, client, admin_user):
        """Test search functionality"""
        client.login(username=admin_user.email, password='testpassword123')
        
        akun = AkunFactory(email='john@test.id')
        
        response = client.get(reverse('users:akun_list'), {'q': 'john'})
        assert response.status_code == 200
        assert akun in response.context['object_list']
    
    def test_htmx_returns_partial(self, client, admin_user):
        """Test HTMX request returns partial template"""
        client.login(username=admin_user.email, password='testpassword123')
        
        response = client.get(
            reverse('users:akun_list'),
            HTTP_HX_REQUEST='true'
        )
        
        # Should return partial template (no full HTML structure)
        assert response.status_code == 200
        # Partial templates typically don't include <html> tag
        assert b'<html>' not in response.content or response.context.get('is_htmx')

class TestAkunCreateView:
    def test_create_valid_account(self, client, admin_user):
        """Test creating account with valid data"""
        client.login(username=admin_user.email, password='testpassword123')
        
        form_data = {
            'email': 'newuser@test.id',
            'password': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'peran': PeranFactory(nama='Guru').id
        }
        
        response = client.post(reverse('users:akun_add'), form_data)
        
        # Should redirect on success
        assert response.status_code == 302
        
        # Account should be created
        assert Akun.objects.filter(email='newuser@test.id').exists()
    
    def test_password_mismatch(self, client, admin_user):
        """Test password mismatch validation"""
        client.login(username=admin_user.email, password='testpassword123')
        
        form_data = {
            'email': 'newuser@test.id',
            'password': 'SecurePass123!',
            'password2': 'DifferentPass123!',
            'peran': PeranFactory(nama='Guru').id
        }
        
        response = client.post(reverse('users:akun_add'), form_data)
        
        # Should return form with errors
        assert response.status_code == 200
        assert 'form' in response.context
        assert response.context['form'].errors

class TestDashboardView:
    def test_superuser_sees_counts(self, client, admin_user):
        """Test admin dashboard shows counts"""
        client.login(username=admin_user.email, password='testpassword123')
        
        response = client.get(reverse('core:dashboard'))
        
        assert response.status_code == 200
        assert 'total_akun' in response.context
        assert 'total_peran' in response.context
        assert isinstance(response.context['total_akun'], int)
    
    def test_non_superuser_no_counts(self, client, student_user):
        """Test student doesn't see counts"""
        client.login(username=student_user.email, password='testpassword123')
        
        response = client.get(reverse('core:dashboard'))
        
        assert response.status_code == 200
        # Non-superuser shouldn't have counts in context
        assert response.context.get('total_akun') is None
```

---

## 7. Test Execution Checklist

Before deploying to production:

- [ ] All unit tests passing (models, forms, views)
- [ ] All integration tests passing
- [ ] Coverage report ≥ 80% for critical code
- [ ] Security tests running (SQL injection, XSS, CSRF)
- [ ] Performance tests on large datasets
- [ ] Manual testing on staging environment
- [ ] User acceptance testing (UAT) sign-off

---

## 8. Continuous Integration Setup

**GitHub Actions Workflow** (`.github/workflows/test.yml`):

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      mysql:
        image: mysql:8.0
        env:
          MYSQL_ROOT_PASSWORD: root
          MYSQL_DATABASE: test_db
        options: >-
          --health-cmd="mysqladmin ping"
          --health-interval=10s
          --health-timeout=5s
          --health-retries=3
        ports:
          - 3306:3306
    
    steps:
      - uses: actions/checkout@v2
      
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      
      - name: Run migrations
        run: python manage.py migrate
        env:
          DATABASE_URL: mysql://root:root@127.0.0.1:3306/test_db
      
      - name: Run tests
        run: pytest --cov=apps --cov-report=xml
        env:
          DATABASE_URL: mysql://root:root@127.0.0.1:3306/test_db
      
      - uses: codecov/codecov-action@v2
        with:
          files: ./coverage.xml
```

---

**Next Steps**:
1. Create `tests/` directory structure
2. Create `factories.py` with all model factories
3. Write unit tests for all models
4. Write integration tests for workflows
5. Setup pytest and run tests
6. Integrate with GitHub Actions
7. Monitor coverage and improve to 80%+

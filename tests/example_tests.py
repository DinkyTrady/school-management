"""
Example Test File for SIGMA Project

This file demonstrates how to write tests for Django apps.
Copy this as a template to tests/ directory and expand.

Usage:
    pytest tests/example_tests.py -v
    pytest tests/example_tests.py::test_akun_creation -v
    pytest tests/ --cov=apps --cov-report=html
"""

import pytest
from datetime import date, datetime, time
from django.core.exceptions import ValidationError
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model

# Import models
from apps.users.models import Akun, Peran, Siswa, Guru, Wali, SiswaWali
from apps.academics.models import (
    TahunAjaran, Jurusan, Kelas, Mapel, KelasSiswa, Jadwal
)
from apps.grades.models import Tugas, Nilai, Presensi

# Import factories (you'll create these in tests/factories.py)
from tests.factories import (
    AkunFactory, PeranFactory, SiswaFactory, GuruFactory, WaliFactory,
    TahunAjaranFactory, JurusanFactory, KelasFactory, MapelFactory,
    KelasSiswaFactory, JadwalFactory, TugasFactory, NilaiFactory, PresensiFactory
)

User = get_user_model()

# Mark all tests in this module as using database
pytestmark = pytest.mark.django_db

# ============================================================================
# MODEL TESTS
# ============================================================================

class TestAkunModel:
    """Tests for Akun (User) model"""
    
    def test_akun_creation(self):
        """Test creating an Akun with email"""
        akun = AkunFactory(email='student@school.id')
        assert akun.email == 'student@school.id'
        assert akun.check_password('testpassword123')
        assert akun.is_active is True
    
    def test_akun_email_unique(self):
        """Test that email must be unique"""
        AkunFactory(email='john@school.id')
        with pytest.raises(Exception):  # IntegrityError
            AkunFactory(email='john@school.id')
    
    def test_akun_role_properties(self):
        """Test role property methods"""
        peran_guru = PeranFactory(nama='Guru')
        peran_siswa = PeranFactory(nama='Siswa')
        
        guru_akun = AkunFactory(peran=peran_guru)
        siswa_akun = AkunFactory(peran=peran_siswa)
        
        assert guru_akun.is_guru is True
        assert guru_akun.is_siswa is False
        
        assert siswa_akun.is_siswa is True
        assert siswa_akun.is_guru is False
    
    def test_akun_superuser_creation(self):
        """Test creating a superuser"""
        akun = Akun.objects.create_superuser(
            email='admin@school.id',
            password='AdminPass123!'
        )
        assert akun.is_superuser is True
        assert akun.is_staff is True
        assert akun.check_password('AdminPass123!')
    
    def test_akun_password_hashing(self):
        """Test that password is hashed, not stored in plaintext"""
        akun = AkunFactory(email='test@school.id')
        # Get from database to verify it was saved correctly
        akun_from_db = Akun.objects.get(email='test@school.id')
        assert not akun_from_db.password == 'testpassword123'  # Not plaintext
        assert akun_from_db.check_password('testpassword123')  # But can verify


class TestSiswaModel:
    """Tests for Siswa (Student) model"""
    
    def test_siswa_creation(self):
        """Test creating a Siswa"""
        siswa = SiswaFactory(
            first_name='John',
            last_name='Doe',
            nis='12345'
        )
        assert siswa.get_full_name() == 'John Doe'
        assert siswa.nis == '12345'
    
    def test_siswa_nis_unique(self):
        """Test that NIS is unique per student"""
        SiswaFactory(nis='67890')
        with pytest.raises(Exception):  # IntegrityError
            SiswaFactory(nis='67890')
    
    def test_siswa_age_calculation(self):
        """Test age calculation from birth date"""
        birth_date = datetime(2007, 6, 15)
        siswa = SiswaFactory(tanggal_lahir=birth_date)
        
        current_year = date.today().year
        expected_age = current_year - 2007
        # Note: age might be off by 1 if birthday hasn't occurred
        assert abs(siswa.get_age() - expected_age) <= 1
    
    def test_siswa_full_name_with_spaces(self):
        """Test full name with extra spaces is trimmed"""
        siswa = SiswaFactory(first_name='  John  ', last_name='  Doe  ')
        assert siswa.get_full_name() == 'John Doe'


class TestGuruModel:
    """Tests for Guru (Teacher) model"""
    
    def test_guru_creation(self):
        """Test creating a Guru"""
        guru = GuruFactory(
            first_name='Jane',
            last_name='Smith',
            nip='NIP123',
            jabatan='Kepala Sekolah'
        )
        assert guru.get_full_name() == 'Jane Smith'
        assert guru.jabatan == 'Kepala Sekolah'
    
    def test_guru_nip_unique(self):
        """Test that NIP is unique"""
        GuruFactory(nip='NIP999')
        with pytest.raises(Exception):  # IntegrityError
            GuruFactory(nip='NIP999')


class TestKelasModel:
    """Tests for Kelas (Class) model"""
    
    def test_kelas_creation(self):
        """Test creating a Kelas"""
        tahun = TahunAjaranFactory(tahun='2024/2025')
        jurusan = JurusanFactory(nama='IPA')
        guru = GuruFactory()
        
        kelas = KelasFactory(
            nama='XI IPA-1',
            jurusan=jurusan,
            wali_kelas=guru,
            tahun_ajaran=tahun
        )
        assert kelas.nama == 'XI IPA-1'
        assert kelas.tahun_ajaran == tahun
    
    def test_kelas_unique_per_year(self):
        """Test that class name must be unique per year"""
        tahun = TahunAjaranFactory(tahun='2024/2025')
        
        KelasFactory(nama='XI IPA-1', tahun_ajaran=tahun)
        
        # Same name, same year should fail
        with pytest.raises(Exception):  # IntegrityError
            KelasFactory(nama='XI IPA-1', tahun_ajaran=tahun)
        
        # But same name, different year should work
        tahun2 = TahunAjaranFactory(tahun='2025/2026')
        kelas2 = KelasFactory(nama='XI IPA-1', tahun_ajaran=tahun2)
        assert kelas2.id is not None


class TestNilaiModel:
    """Tests for Nilai (Grade) model"""
    
    def test_nilai_creation(self):
        """Test creating a grade"""
        jadwal = JadwalFactory()
        siswa = SiswaFactory()
        
        nilai = NilaiFactory(
            siswa=siswa,
            jadwal=jadwal,
            tipe_penilaian='Ujian Harian',
            nilai=85.5
        )
        assert nilai.siswa == siswa
        assert nilai.nilai == 85.5
    
    def test_nilai_tugas_type_requires_tugas(self):
        """Test that Tugas type requires tugas_id"""
        jadwal = JadwalFactory()
        siswa = SiswaFactory()
        
        nilai = Nilai(
            siswa=siswa,
            jadwal=jadwal,
            tipe_penilaian='Tugas',
            nilai=80,
            tanggal_penilaian=date.today(),
            tugas=None  # Missing tugas
        )
        
        with pytest.raises(ValidationError):
            nilai.clean()
    
    def test_nilai_with_tugas(self):
        """Test creating grade for assignment"""
        jadwal = JadwalFactory()
        siswa = SiswaFactory()
        tugas = TugasFactory(jadwal=jadwal)
        
        nilai = NilaiFactory(
            siswa=siswa,
            jadwal=jadwal,
            tugas=tugas,
            tipe_penilaian='Tugas'
        )
        assert nilai.tugas == tugas


class TestPresensiModel:
    """Tests for Presensi (Attendance) model"""
    
    def test_presensi_creation(self):
        """Test creating an attendance record"""
        jadwal = JadwalFactory()
        siswa = SiswaFactory()
        
        presensi = PresensiFactory(
            siswa=siswa,
            jadwal=jadwal,
            tanggal=date.today(),
            status='Hadir'
        )
        assert presensi.status == 'Hadir'
    
    def test_presensi_unique_per_date(self):
        """Test unique constraint on (siswa, jadwal, tanggal)"""
        jadwal = JadwalFactory()
        siswa = SiswaFactory()
        
        PresensiFactory(
            siswa=siswa,
            jadwal=jadwal,
            tanggal=date.today(),
            status='Hadir'
        )
        
        # Same student, same schedule, same date should fail
        with pytest.raises(Exception):  # IntegrityError
            PresensiFactory(
                siswa=siswa,
                jadwal=jadwal,
                tanggal=date.today(),
                status='Sakit'
            )


# ============================================================================
# FORM TESTS (if using Django Forms)
# ============================================================================

class TestAkunCreationForm:
    """Tests for account creation form (from apps/users/forms.py)"""
    
    @pytest.mark.skip(reason="Requires forms.py import")
    def test_form_valid(self):
        """Test valid form submission"""
        from apps.users.forms import AkunCreationForm
        
        form_data = {
            'email': 'newuser@school.id',
            'password': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'peran': PeranFactory().id
        }
        form = AkunCreationForm(data=form_data)
        assert form.is_valid()
    
    @pytest.mark.skip(reason="Requires forms.py import")
    def test_password_mismatch(self):
        """Test password mismatch validation"""
        from apps.users.forms import AkunCreationForm
        
        form_data = {
            'email': 'newuser@school.id',
            'password': 'SecurePass123!',
            'password2': 'DifferentPass123!',
            'peran': PeranFactory().id
        }
        form = AkunCreationForm(data=form_data)
        assert not form.is_valid()
        assert 'password2' in form.errors


# ============================================================================
# VIEW TESTS
# ============================================================================

class TestAkunListView:
    """Tests for account list view"""
    
    @pytest.fixture
    def client(self):
        """Create a test client"""
        return Client()
    
    @pytest.fixture
    def admin_user(self):
        """Create an admin user"""
        peran = PeranFactory(nama='Admin')
        return AkunFactory(
            email='admin@test.id',
            is_superuser=True,
            peran=peran
        )
    
    @pytest.fixture
    def regular_user(self):
        """Create a non-admin user"""
        peran = PeranFactory(nama='Guru')
        return AkunFactory(
            email='guru@test.id',
            peran=peran
        )
    
    def test_requires_login(self, client):
        """Test unauthenticated users are redirected to login"""
        response = client.get(reverse('users:akun_list'))
        assert response.status_code == 302
        assert 'login' in response.url
    
    def test_requires_permission(self, client, regular_user):
        """Test non-admin users get 403 Forbidden"""
        client.login(username=regular_user.email, password='testpassword123')
        response = client.get(reverse('users:akun_list'))
        assert response.status_code == 403
    
    def test_admin_can_view_list(self, client, admin_user):
        """Test admin can view account list"""
        client.login(username=admin_user.email, password='testpassword123')
        response = client.get(reverse('users:akun_list'))
        assert response.status_code == 200
        assert 'object_list' in response.context or 'akun_list' in response.context
    
    def test_list_displays_accounts(self, client, admin_user):
        """Test list view displays accounts"""
        client.login(username=admin_user.email, password='testpassword123')
        
        # Create test accounts
        AkunFactory.create_batch(3)
        
        response = client.get(reverse('users:akun_list'))
        assert response.status_code == 200
        
        # Check if accounts are in context
        object_list = response.context.get('object_list') or response.context.get('akun_list')
        assert len(object_list) >= 3
    
    def test_search_filter(self, client, admin_user):
        """Test search functionality"""
        client.login(username=admin_user.email, password='testpassword123')
        
        # Create a specific user
        akun = AkunFactory(email='searchme@test.id')
        
        # Search for this user
        response = client.get(reverse('users:akun_list'), {'q': 'searchme'})
        assert response.status_code == 200
        
        object_list = response.context.get('object_list') or response.context.get('akun_list')
        assert akun in object_list or any(a.email == akun.email for a in object_list)


class TestDashboardView:
    """Tests for dashboard view"""
    
    @pytest.fixture
    def client(self):
        return Client()
    
    def test_requires_login(self, client):
        """Test unauthenticated users redirected"""
        response = client.get(reverse('core:dashboard'))
        assert response.status_code == 302
    
    def test_superuser_sees_stats(self, client):
        """Test superuser sees statistics"""
        admin = AkunFactory(is_superuser=True)
        client.login(username=admin.email, password='testpassword123')
        
        response = client.get(reverse('core:dashboard'))
        assert response.status_code == 200
        assert 'total_akun' in response.context
        assert 'total_peran' in response.context


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestStudentLoginAndDashboard:
    """Integration test: Student login and view dashboard"""
    
    @pytest.fixture
    def client(self):
        return Client()
    
    def test_student_can_login_and_view_dashboard(self, client):
        """Test complete student login flow"""
        # Create student account
        peran = PeranFactory(nama='Siswa')
        siswa = SiswaFactory()
        siswa.akun.peran = peran
        siswa.akun.save()
        
        # Login
        login_success = client.login(
            username=siswa.akun.email,
            password='testpassword123'
        )
        assert login_success
        
        # Can access dashboard
        response = client.get(reverse('core:dashboard'))
        assert response.status_code == 200


class TestClassEnrollmentWorkflow:
    """Integration test: Class enrollment workflow"""
    
    def test_enroll_students_in_class(self):
        """Test enrolling multiple students in a class"""
        # Create academic year
        tahun = TahunAjaranFactory(is_active=True)
        
        # Create class
        kelas = KelasFactory(tahun_ajaran=tahun)
        
        # Enroll students
        siswa_list = [SiswaFactory() for _ in range(3)]
        for siswa in siswa_list:
            KelasSiswaFactory(
                siswa=siswa,
                kelas=kelas,
                tahun_ajaran=tahun
            )
        
        # Verify enrollment
        enrolled = kelas.kelassiswa_set.all()
        assert enrolled.count() == 3
        assert all(ks.tahun_ajaran == tahun for ks in enrolled)


class TestGradeEntryWorkflow:
    """Integration test: Teacher enters grades, student views them"""
    
    def test_teacher_enters_grade_student_views(self):
        """Test grade entry and viewing workflow"""
        # Setup
        jadwal = JadwalFactory()
        kelas = jadwal.kelas
        siswa = SiswaFactory()
        
        # Enroll student
        KelasSiswaFactory(
            siswa=siswa,
            kelas=kelas,
            tahun_ajaran=kelas.tahun_ajaran
        )
        
        # Teacher enters grade
        nilai = NilaiFactory(
            siswa=siswa,
            jadwal=jadwal,
            nilai=92.5
        )
        
        # Verify grade exists
        assert Nilai.objects.filter(siswa=siswa, jadwal=jadwal).exists()
        assert nilai.nilai == 92.5


# ============================================================================
# FIXTURES (Reusable test data)
# ============================================================================

@pytest.fixture
def sample_school():
    """Create a complete sample school structure"""
    tahun = TahunAjaranFactory(is_active=True)
    jurusan = JurusanFactory()
    guru = GuruFactory()
    kelas = KelasFactory(jurusan=jurusan, wali_kelas=guru, tahun_ajaran=tahun)
    siswa_list = [SiswaFactory() for _ in range(5)]
    
    for siswa in siswa_list:
        KelasSiswaFactory(siswa=siswa, kelas=kelas, tahun_ajaran=tahun)
    
    return {
        'tahun_ajaran': tahun,
        'jurusan': jurusan,
        'guru': guru,
        'kelas': kelas,
        'siswa_list': siswa_list
    }


# ============================================================================
# PARAMETRIZED TESTS (Test multiple scenarios)
# ============================================================================

@pytest.mark.parametrize('status', ['Hadir', 'Sakit', 'Izin', 'Alpha'])
def test_presensi_status_choices(status):
    """Test all attendance status choices are valid"""
    jadwal = JadwalFactory()
    siswa = SiswaFactory()
    
    presensi = PresensiFactory(
        siswa=siswa,
        jadwal=jadwal,
        status=status
    )
    assert presensi.status == status


@pytest.mark.parametrize('tipe', ['Tugas', 'Ujian Harian', 'UTS', 'UAS'])
def test_nilai_tipe_penilaian_choices(tipe):
    """Test all grade type choices are valid"""
    jadwal = JadwalFactory()
    siswa = SiswaFactory()
    
    # Skip Tugas type validation for non-Tugas
    if tipe != 'Tugas':
        nilai = NilaiFactory(
            siswa=siswa,
            jadwal=jadwal,
            tipe_penilaian=tipe
        )
        assert nilai.tipe_penilaian == tipe


# ============================================================================
# INSTRUCTIONS
# ============================================================================

"""
HOW TO USE THIS FILE:

1. Copy this file to tests/example_tests.py
2. Create tests/factories.py with all factory definitions (see test_plan.md)
3. Create tests/__init__.py (empty file)
4. Run tests:
   
   pytest tests/example_tests.py -v
   pytest tests/example_tests.py::TestAkunModel -v
   pytest tests/example_tests.py::TestAkunModel::test_akun_creation -v
   
5. Run with coverage:
   
   pytest tests/ --cov=apps --cov-report=html
   
6. Run all tests:
   
   pytest tests/ -v

FIXTURES:
- Use @pytest.fixture for reusable test data
- Use @pytest.mark.parametrize for testing multiple scenarios
- Use pytestmark = pytest.mark.django_db for database access

ASSERTIONS:
- Use assert statements instead of self.assert* (pytest style)
- Use pytest.raises() for exception testing
- Use pytest.skip() to skip tests

MOCKING:
- Use unittest.mock for mocking external services
- Use responses library for mocking HTTP requests
- Use factory_boy for creating test objects
"""

"""
Factory Boy Factories for SIGMA Project

This file defines factory classes for creating test data.
Factory Boy automatically creates model instances with sensible defaults.

Usage:
    from tests.factories import AkunFactory, SiswaFactory
    
    # Create single instance
    akun = AkunFactory(email='test@test.id')
    
    # Create multiple instances
    siswa_list = SiswaFactory.create_batch(5)
    
    # Build without saving to DB (for testing)
    akun = AkunFactory.build()
    
Reference: https://github.com/FactoryBoy/factory_boy
"""

import factory
from factory import fuzzy, Faker
from datetime import date, time, timedelta, datetime
from django.utils import timezone

from apps.users.models import Akun, Peran, Siswa, Guru, Wali, SiswaWali
from apps.academics.models import (
    TahunAjaran, Jurusan, Kelas, Mapel, KelasSiswa, Jadwal
)
from apps.grades.models import Tugas, Nilai, Presensi


# ============================================================================
# PERAN FACTORY (Role)
# ============================================================================

class PeranFactory(factory.django.DjangoModelFactory):
    """Factory for Peran (Role) model"""
    
    class Meta:
        model = Peran
    
    nama = factory.Faker('word')
    deskripsi = factory.Faker('paragraph', nb_sentences=2)
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)


# ============================================================================
# AKUN FACTORY (User)
# ============================================================================

class AkunFactory(factory.django.DjangoModelFactory):
    """Factory for Akun (User/Account) model"""
    
    class Meta:
        model = Akun
    
    email = factory.Sequence(lambda n: f'user{n}@school.id')
    peran = factory.SubFactory(PeranFactory)
    is_active = True
    is_staff = False
    is_superuser = False
    
    @factory.post_generation
    def password(obj, create, extracted, **kwargs):
        """Set password after object creation"""
        if not create:
            return
        
        if extracted:
            obj.set_password(extracted)
        else:
            # Default test password
            obj.set_password('testpassword123')
        
        obj.save()
    
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override creation to handle password correctly"""
        password = kwargs.pop('password', 'testpassword123')
        obj = model_class(*args, **kwargs)
        obj.set_password(password)
        obj.save()
        return obj


class AdminAkunFactory(AkunFactory):
    """Factory for admin user"""
    is_staff = True
    is_superuser = True
    peran = factory.SubFactory(
        PeranFactory,
        nama='Admin'
    )


# ============================================================================
# PERSON SUBCLASS FACTORIES (Siswa, Guru, Wali)
# ============================================================================

class SiswaFactory(factory.django.DjangoModelFactory):
    """Factory for Siswa (Student) model"""
    
    class Meta:
        model = Siswa
    
    akun = factory.SubFactory(AkunFactory)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    nis = factory.Sequence(lambda n: f'{n:06d}')
    
    jenis_kelamin = factory.fuzzy.FuzzyChoice(['L', 'P'])
    tanggal_lahir = factory.Faker(
        'date_of_birth',
        minimum_age=14,
        maximum_age=18
    )
    alamat = factory.Faker('address')
    no_telepon = factory.Faker('phone_number')
    

class GuruFactory(factory.django.DjangoModelFactory):
    """Factory for Guru (Teacher) model"""
    
    class Meta:
        model = Guru
    
    akun = factory.SubFactory(AkunFactory)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    nip = factory.Sequence(lambda n: f'NIP{n:08d}')
    
    jenis_kelamin = factory.fuzzy.FuzzyChoice(['L', 'P'])
    tanggal_lahir = factory.Faker(
        'date_of_birth',
        minimum_age=25,
        maximum_age=60
    )
    alamat = factory.Faker('address')
    no_telepon = factory.Faker('phone_number')
    jabatan = factory.Faker('job')


class WaliFactory(factory.django.DjangoModelFactory):
    """Factory for Wali (Guardian) model"""
    
    class Meta:
        model = Wali
    
    akun = factory.SubFactory(AkunFactory)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    
    jenis_kelamin = factory.fuzzy.FuzzyChoice(['L', 'P'])
    tanggal_lahir = factory.Faker('date_of_birth', minimum_age=30)
    alamat = factory.Faker('address')
    no_telepon = factory.Faker('phone_number')
    pekerjaan = factory.Faker('job')


class SiswaWaliFactory(factory.django.DjangoModelFactory):
    """Factory for SiswaWali (Student-Guardian relation)"""
    
    class Meta:
        model = SiswaWali
    
    siswa = factory.SubFactory(SiswaFactory)
    wali = factory.SubFactory(WaliFactory)
    hubungan = factory.fuzzy.FuzzyChoice(['Ayah', 'Ibu', 'Kakek', 'Nenek', 'Wali Lain'])


# ============================================================================
# ACADEMICS FACTORIES
# ============================================================================

class TahunAjaranFactory(factory.django.DjangoModelFactory):
    """Factory for TahunAjaran (Academic Year) model"""
    
    class Meta:
        model = TahunAjaran
    
    tahun = factory.Sequence(lambda n: f'{2024+n}/{2025+n}')
    is_active = False
    tanggal_mulai = factory.Faker('date_this_year', after_today=False)
    tanggal_selesai = factory.Faker('date_this_year', after_today=True)
    
    @factory.lazy_attribute
    def tanggal_selesai(self):
        """Ensure end date is after start date"""
        return self.tanggal_mulai + timedelta(days=365)


class JurusanFactory(factory.django.DjangoModelFactory):
    """Factory for Jurusan (Major) model"""
    
    class Meta:
        model = Jurusan
    
    nama = factory.fuzzy.FuzzyChoice(['IPA', 'IPS', 'Bahasa'])
    deskripsi = factory.Faker('paragraph', nb_sentences=2)


class KelasFactory(factory.django.DjangoModelFactory):
    """Factory for Kelas (Class) model"""
    
    class Meta:
        model = Kelas
    
    nama = factory.Sequence(lambda n: f'XI-{n}')
    jurusan = factory.SubFactory(JurusanFactory)
    wali_kelas = factory.SubFactory(GuruFactory)
    tahun_ajaran = factory.SubFactory(TahunAjaranFactory)
    kapasitas = 35


class MapelFactory(factory.django.DjangoModelFactory):
    """Factory for Mapel (Subject) model"""
    
    class Meta:
        model = Mapel
    
    nama = factory.Faker('word')
    deskripsi = factory.Faker('paragraph', nb_sentences=2)
    kkm = 75  # Minimum completion score


class KelasSiswaFactory(factory.django.DjangoModelFactory):
    """Factory for KelasSiswa (Class-Student enrollment) model"""
    
    class Meta:
        model = KelasSiswa
    
    siswa = factory.SubFactory(SiswaFactory)
    kelas = factory.SubFactory(KelasFactory)
    tahun_ajaran = factory.SubFactory(TahunAjaranFactory)


class JadwalFactory(factory.django.DjangoModelFactory):
    """Factory for Jadwal (Schedule) model"""
    
    class Meta:
        model = Jadwal
    
    kelas = factory.SubFactory(KelasFactory)
    mapel = factory.SubFactory(MapelFactory)
    guru = factory.SubFactory(GuruFactory)
    
    hari = factory.fuzzy.FuzzyChoice(['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat'])
    jam_mulai = factory.LazyFunction(lambda: time(7, 0))
    jam_selesai = factory.LazyFunction(lambda: time(8, 30))
    ruangan = factory.Sequence(lambda n: f'Ruang {n}')


# ============================================================================
# GRADES FACTORIES
# ============================================================================

class TugasFactory(factory.django.DjangoModelFactory):
    """Factory for Tugas (Assignment) model"""
    
    class Meta:
        model = Tugas
    
    jadwal = factory.SubFactory(JadwalFactory)
    judul = factory.Faker('sentence', nb_words=5)
    deskripsi = factory.Faker('paragraph', nb_sentences=3)
    
    tanggal_dibuat = factory.LazyFunction(lambda: timezone.now().date())
    tanggal_deadline = factory.LazyFunction(
        lambda: (timezone.now() + timedelta(days=7)).date()
    )
    bobot = 20  # Weight/percentage


class NilaiFactory(factory.django.DjangoModelFactory):
    """Factory for Nilai (Grade) model"""
    
    class Meta:
        model = Nilai
    
    siswa = factory.SubFactory(SiswaFactory)
    jadwal = factory.SubFactory(JadwalFactory)
    tugas = None  # Optional, depends on tipe_penilaian
    
    tipe_penilaian = factory.fuzzy.FuzzyChoice(['Tugas', 'Ujian Harian', 'UTS', 'UAS'])
    nilai = factory.fuzzy.FuzzyInteger(60, 100)
    tanggal_penilaian = factory.LazyFunction(lambda: timezone.now().date())


class PresensiFactory(factory.django.DjangoModelFactory):
    """Factory for Presensi (Attendance) model"""
    
    class Meta:
        model = Presensi
    
    siswa = factory.SubFactory(SiswaFactory)
    jadwal = factory.SubFactory(JadwalFactory)
    
    tanggal = factory.LazyFunction(lambda: timezone.now().date())
    status = factory.fuzzy.FuzzyChoice(['Hadir', 'Sakit', 'Izin', 'Alpha'])
    keterangan = factory.Faker('sentence', nb_words=3)


# ============================================================================
# BATCH FACTORIES (Create multiple related objects)
# ============================================================================

class SchoolBatchFactory:
    """Helper class to create a complete school structure"""
    
    @staticmethod
    def create():
        """Create a complete school year with classes and students"""
        
        # Create academic year
        tahun_ajaran = TahunAjaranFactory(
            tahun='2024/2025',
            is_active=True
        )
        
        # Create majors
        jurusan_ipa = JurusanFactory(nama='IPA')
        jurusan_ips = JurusanFactory(nama='IPS')
        
        # Create teachers
        guru_list = GuruFactory.create_batch(5)
        
        # Create classes
        kelas_list = [
            KelasFactory(
                nama=f'XI IPA-{i}',
                jurusan=jurusan_ipa,
                wali_kelas=guru_list[i],
                tahun_ajaran=tahun_ajaran
            )
            for i in range(2)
        ]
        kelas_list += [
            KelasFactory(
                nama=f'XI IPS-{i}',
                jurusan=jurusan_ips,
                wali_kelas=guru_list[2+i],
                tahun_ajaran=tahun_ajaran
            )
            for i in range(2)
        ]
        
        # Create subjects
        mapel_list = [
            MapelFactory(nama='Matematika'),
            MapelFactory(nama='Bahasa Inggris'),
            MapelFactory(nama='Fisika'),
            MapelFactory(nama='Kimia'),
        ]
        
        # Create schedules
        jadwal_list = []
        for kelas in kelas_list:
            for mapel in mapel_list:
                jadwal = JadwalFactory(
                    kelas=kelas,
                    mapel=mapel,
                    guru=factory.random.choice(guru_list)
                )
                jadwal_list.append(jadwal)
        
        # Create students and enroll
        siswa_list = SiswaFactory.create_batch(30)
        for i, siswa in enumerate(siswa_list):
            kelas = kelas_list[i % len(kelas_list)]
            KelasSiswaFactory(
                siswa=siswa,
                kelas=kelas,
                tahun_ajaran=tahun_ajaran
            )
        
        # Create guardians for students
        wali_list = WaliFactory.create_batch(15)
        for i, siswa in enumerate(siswa_list):
            wali = wali_list[i % len(wali_list)]
            SiswaWaliFactory(
                siswa=siswa,
                wali=wali,
                hubungan=factory.random.choice(['Ayah', 'Ibu'])
            )
        
        # Create assignments for schedules
        tugas_list = []
        for jadwal in jadwal_list[:5]:  # Create assignments for first 5 schedules
            tugas = TugasFactory(jadwal=jadwal)
            tugas_list.append(tugas)
        
        # Create grades for students
        for siswa in siswa_list[:10]:  # Grades for first 10 students
            for jadwal in jadwal_list[:5]:
                NilaiFactory(
                    siswa=siswa,
                    jadwal=jadwal,
                    tipe_penilaian=factory.random.choice(['Tugas', 'Ujian Harian'])
                )
        
        # Create attendance records
        for siswa in siswa_list[:10]:
            for jadwal in jadwal_list[:3]:
                PresensiFactory(
                    siswa=siswa,
                    jadwal=jadwal
                )
        
        return {
            'tahun_ajaran': tahun_ajaran,
            'jurusan_list': [jurusan_ipa, jurusan_ips],
            'guru_list': guru_list,
            'kelas_list': kelas_list,
            'mapel_list': mapel_list,
            'jadwal_list': jadwal_list,
            'siswa_list': siswa_list,
            'wali_list': wali_list,
            'tugas_list': tugas_list,
        }


# ============================================================================
# PYTEST FIXTURES
# ============================================================================

import pytest

@pytest.fixture
def admin_user():
    """Create an admin user for tests"""
    return AdminAkunFactory(email='admin@test.id')


@pytest.fixture
def teacher_user():
    """Create a teacher user for tests"""
    peran = PeranFactory(nama='Guru')
    guru = GuruFactory()
    guru.akun.peran = peran
    guru.akun.save()
    return guru.akun


@pytest.fixture
def student_user():
    """Create a student user for tests"""
    peran = PeranFactory(nama='Siswa')
    siswa = SiswaFactory()
    siswa.akun.peran = peran
    siswa.akun.save()
    return siswa.akun


@pytest.fixture
def school_data():
    """Create complete school structure"""
    return SchoolBatchFactory.create()

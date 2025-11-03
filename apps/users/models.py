from typing import override

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from apps.core.models import Person

from .managers import AkunManager


class Peran(models.Model):
    nama = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name_plural = 'Peran Akun'


class Akun(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    peran = models.ForeignKey(Peran, on_delete=models.PROTECT, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True, auto_created=True, editable=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AkunManager()

    @override
    def __str__(self):
        return self.email

    @property
    def get_user_peran(self):
        if not self.peran:
            return ''
        return self.peran.nama

    @property
    def is_guru(self):
        if not self.peran:
            return False
        return self.peran.nama == 'Guru'

    @property
    def is_siswa(self):
        if not self.peran:
            return False
        return self.peran.nama == 'Siswa'

    @property
    def is_tata_usaha(self):
        if not self.peran:
            return False
        return self.peran.nama == 'Tata Usaha'

    @property
    def is_kepala_sekolah(self):
        if not self.peran:
            return False
        return self.peran.nama == 'Kepala Sekolah'

    @property
    def is_admin(self):
        if not self.peran:
            return False
        return self.peran.nama == 'Admin'

    class Meta:
        verbose_name_plural = 'Akun'


class Siswa(Person):
    nis = models.CharField(max_length=255, unique=True)
    akun = models.OneToOneField(
        Akun, on_delete=models.CASCADE, primary_key=True, related_name='siswa_profile'
    )

    @override
    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name_plural = 'Siswa'


class Guru(Person):
    nip = models.CharField(max_length=255, unique=True)
    jabatan = models.CharField(max_length=100)
    akun = models.OneToOneField(
        Akun, on_delete=models.CASCADE, primary_key=True, related_name='guru_profile'
    )

    @override
    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name_plural = 'Guru'
        indexes = [models.Index(fields=['jabatan'])]


class Wali(Person):
    @override
    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name_plural = 'Wali Murid'


class SiswaWali(models.Model):
    HUBUNGAN_CHOICES = [
        ('Ayah', 'Ayah'),
        ('Ibu', 'Ibu'),
        ('Wali', 'Wali'),
    ]
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    wali = models.ForeignKey(Wali, on_delete=models.CASCADE)
    hubungan = models.CharField(max_length=10, choices=HUBUNGAN_CHOICES)

    class Meta:
        unique_together = ('siswa', 'wali')
        indexes = [models.Index(fields=['wali', 'siswa'])]
        verbose_name_plural = 'Hubungan Siswa-Wali'

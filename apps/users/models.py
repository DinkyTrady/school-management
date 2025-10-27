# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from typing import ClassVar
from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.core.models import Person


class Peran(models.Model):
    nama = models.CharField(max_length=255)


class Akun(AbstractUser):
    email = models.EmailField(unique=True)
    peran = models.ForeignKey(Peran, on_delete=models.CASCADE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']


class Siswa(Person):
    nis = models.CharField(max_length=255, unique=True)
    akun = models.ForeignKey(Akun, on_delete=models.CASCADE)


class Guru(Person):
    nip = models.CharField(max_length=255)
    jabatan = models.CharField(max_length=100)
    akun = models.ForeignKey(Akun, on_delete=models.CASCADE)


class Wali(Person):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SiswaWali(models.Model):
    HUBUNGAN_CHOICES: ClassVar[list[tuple[str, str]]] = [
        ('Ayah', 'Ayah'),
        ('Ibu', 'Ibu'),
        ('Wali', 'Wali'),
    ]
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    wali = models.ForeignKey(Wali, on_delete=models.CASCADE)
    hubungan = models.CharField(max_length=10, choices=HUBUNGAN_CHOICES)

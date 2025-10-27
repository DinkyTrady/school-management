# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Gender(models.TextChoices):
    LAKI_LAKI = 'L', 'Laki-laki'
    PEREMPUAN = 'P', 'Perempuan'


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    alamat = models.TextField()
    tanggal_lahir = models.DateTimeField()
    nomor_handphone = models.CharField(max_length=20)
    gender = models.CharField(
        max_length=10, choices=Gender.choices, default=Gender.LAKI_LAKI
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

from datetime import date
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
        indexes = [
            models.Index(fields=['first_name', 'last_name', 'nomor_handphone'])
        ]

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_age(self):
        today= date.today()
        birth_date = self.tanggal_lahir.date()
        age = (
            today.year
            - birth_date.year
            - ((today.month, today.day) < (birth_date.month, birth_date.year))
        )

        return age
from django.db import models

from apps.users.models import Guru, Siswa


# Create your models here.
class TahunAjaran(models.Model):
    SEMESTER_CHOICES = [('Ganjil', 'Ganjil'), ('Genap', 'Genap')]

    tahun = models.CharField(max_length=10)
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES)
    tanggal_mulai = models.DateField()
    tanggal_selesai = models.DateField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.tahun} - {self.semester}'

    class Meta:
        verbose_name_plural = 'Tahun Ajaran'
        constraints = [
            models.UniqueConstraint(
                fields=['tahun', 'semester'], name='unique_academic_period'
            )
        ]


class Jurusan(models.Model):
    nama = models.CharField(max_length=255,db_index=True)
    deskripsi = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name_plural = 'Jurusan'


class Kelas(models.Model):
    nama = models.CharField(max_length=255, db_index=True)
    jurusan = models.ForeignKey(Jurusan, on_delete=models.PROTECT, db_index=True)
    wali_kelas = models.ForeignKey(
        Guru,
        on_delete=models.PROTECT,
        related_name='kelas_diampu',
        db_index=True,
        limit_choices_to={'akun__peran__nama': 'Guru'},
    )
    tahun_ajaran = models.ForeignKey(
        TahunAjaran, on_delete=models.PROTECT, db_index=True
    )

    def __str__(self):
        return f'{self.nama} ({self.tahun_ajaran})'

    class Meta:
        verbose_name_plural = 'Kelas'
        constraints = [
            models.UniqueConstraint(
                fields=['nama', 'tahun_ajaran'], name='unique_class_period'
            )
        ]


class Mapel(models.Model):
    nama = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name_plural = 'Mata Pelajaran'


class KelasSiswa(models.Model):
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE, db_index=True)
    tahun_ajaran = models.ForeignKey(
        TahunAjaran, on_delete=models.CASCADE, db_index=True
    )

    class Meta:
        unique_together = ('siswa', 'kelas', 'tahun_ajaran')
        verbose_name_plural = 'Pendaftaran Kelas Siswa'
        indexes = [models.Index(fields=['kelas', 'tahun_ajaran'])]

class Jadwal(models.Model):
    HARI_CHOICES = [
        ('Senin', 'Senin'),
        ('Selasa', 'Selasa'),
        ('Rabu', 'Rabu'),
        ('Kamis', 'Kamis'),
        ("Jum'at", "Jum'at"),
        ('Sabtu', 'Sabtu'),
        ('Minggu', 'Minggu'),
    ]
    
    hari = models.CharField(max_length=10, choices=HARI_CHOICES)
    jam_mulai = models.TimeField()
    jam_selesai = models.TimeField()
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE, db_index=True)
    mapel = models.ForeignKey(Mapel, on_delete=models.PROTECT, db_index=True)
    guru = models.ForeignKey(Guru, on_delete=models.PROTECT, db_index=True)

    def __str__(self):
        return f'{self.mapel.nama} - {self.kelas.nama} ({self.hari} {self.jam_mulai})'

    class Meta:
        verbose_name_plural = 'Jadwal Pelajaran'
        constraints = [
            models.UniqueConstraint(
                fields=['kelas', 'hari', 'jam_mulai'], name='unique_class_schedule_time'
            ),
            models.UniqueConstraint(
                fields=['guru', 'hari', 'jam_mulai'],
                name='unique_teacher_schedule_time',
            ),
        ]

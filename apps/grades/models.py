from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.academics.models import Jadwal
from apps.users.models import Siswa


# Create your models here.
class Tugas(models.Model):
    nama = models.CharField(max_length=255, db_index=True)
    deskripsi = models.TextField()
    mulai = models.DateTimeField()
    tenggat = models.DateTimeField()
    jadwal = models.ForeignKey(Jadwal, on_delete=models.CASCADE, db_index=True)

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name_plural = 'Tugas'


class Nilai(models.Model):
    TIPE_CHOICES = [
        ('Tugas', 'Tugas'),
        ('Ujian Harian', 'Ujian Harian'),
        ('UTS', 'UTS'),
        ('UAS', 'UAS'),
    ]

    tipe_penilaian = models.CharField(max_length=20, choices=TIPE_CHOICES)
    nilai = models.DecimalField(max_digits=5, decimal_places=2, db_index=True)
    tanggal_penilaian = models.DateField()
    siswa = models.ForeignKey(Siswa, on_delete=models.PROTECT, db_index=True)
    jadwal = models.ForeignKey(
        Jadwal,
        on_delete=models.CASCADE,
        db_index=True,
        help_text='Konteks mapel/kelas/guru',
    )
    tugas = models.ForeignKey(
        Tugas,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_index=True,
        help_text='Isi jika tipe penilaian adalah Tugas',
    )

    class Meta:
        verbose_name_plural = 'Nilai Siswa'

    def __str__(self):
        mapel_name = (
            self.jadwal.mapel.nama if self.jadwal and self.jadwal.mapel else 'N/A'
        )
        return f'Nilai {self.siswa.get_full_name()} - {mapel_name} ({self.tipe_penilaian}: {self.nilai})'  # noqa: E501

    def clean(self):
        super().clean()

        queryset = Nilai.objects.filter(
            siswa = self.siswa,
            jadwal = self.jadwal,
            tipe_penilaian=self.tipe_penilaian
        )

        if self.pk:
            queryset = queryset.exclude(pk=self.pk)

        if self.tipe_penilaian != 'Tugas':
            if queryset.exists():
                raise ValidationError(
                    _(
                        'Nilai untuk tipe penilaian ini sudah ada untuk siswa pada jadwal yang sama'  # noqa: E501
                    )
                )
        else:
            if not self.tugas:
                raise ValidationError(
                    _(
                        'Nilai untuk tipe penilaian "Tugas", field tugas tidak boleh kosong.'  # noqa: E501
                    )
                )

            tugas_queryset = Nilai.objects.filter(siswa=self.siswa, tugas=self.tugas)
            if self.pk:
                tugas_queryset = tugas_queryset.exclude(pk=self.pk)

            if tugas_queryset.exists():
                raise ValidationError(
                    _('Siswa ini sudah memiliki nilai tugas yang sama.')
                )


class Presensi(models.Model):
    STATUS_CHOICES = [
        ('Hadir', 'Hadir'),
        ('Sakit', 'Sakit'),
        ('Izin', 'Izin'),
        ('Alpha', 'Alpha'),
    ]

    tanggal = models.DateField(db_index=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    keterangan = models.TextField(
        null=True,
        blank=True,
        help_text="Penjelasan terkait status kehadiran selain 'Hadir'",
    )
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    jadwal = models.ForeignKey(Jadwal, on_delete=models.CASCADE)

    def __str__(self):
        return f'Presensi {self.siswa.get_full_name()} - {self.tanggal} ({self.status})'

    class Meta:
        verbose_name_plural = 'Presensi Siswa'
        unique_together = ('siswa', 'jadwal', 'tanggal')
        indexes = [models.Index(fields=['jadwal', 'tanggal'])]

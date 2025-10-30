from django.contrib import admin
from .models import Tugas, Nilai, Presensi


@admin.register(Tugas)
class TugasAdmin(admin.ModelAdmin):
    list_display = ('nama', 'jadwal', 'mulai', 'tenggat')
    list_filter = ('jadwal__kelas__jurusan', 'jadwal__mapel', 'mulai', 'tenggat')
    search_fields = ('nama', 'deskripsi', 'jadwal__kelas__nama', 'jadwal__mapel__nama')
    autocomplete_fields = ('jadwal',)
    list_select_related = ('jadwal__kelas', 'jadwal__mapel')


@admin.register(Nilai)
class NilaiAdmin(admin.ModelAdmin):
    list_display = (
        'siswa',
        'get_mapel',
        'tipe_penilaian',
        'nilai',
        'tanggal_penilaian',
        'tugas',
    )
    list_filter = ('tipe_penilaian', 'tanggal_penilaian', 'jadwal__kelas__jurusan', 'jadwal__mapel')
    search_fields = ('siswa__first_name', 'siswa__last_name', 'jadwal__mapel__nama', 'tugas__nama')
    autocomplete_fields = ('siswa', 'jadwal', 'tugas')
    list_select_related = ('siswa', 'jadwal__mapel', 'tugas')

    @admin.display(description='Mata Pelajaran', ordering='jadwal__mapel__nama')
    def get_mapel(self, obj):
        if obj.jadwal:
            return obj.jadwal.mapel
        return "-"


@admin.register(Presensi)
class PresensiAdmin(admin.ModelAdmin):
    list_display = (
        'siswa',
        'get_mapel',
        'tanggal',
        'status',
        'keterangan',
    )
    list_filter = ('status', 'tanggal', 'jadwal__kelas__jurusan', 'jadwal__mapel')
    search_fields = ('siswa__first_name', 'siswa__last_name', 'keterangan')
    autocomplete_fields = ('siswa', 'jadwal')
    list_select_related = ('siswa', 'jadwal__mapel')

    @admin.display(description='Mata Pelajaran', ordering='jadwal__mapel__nama')
    def get_mapel(self, obj):
        if obj.jadwal:
            return obj.jadwal.mapel
        return "-"

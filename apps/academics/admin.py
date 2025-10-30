from django.contrib import admin

from .models import Jadwal, Jurusan, Kelas, KelasSiswa, Mapel, TahunAjaran


@admin.register(TahunAjaran)
class TahunAjaranAdmin(admin.ModelAdmin):
    list_display = (
        'tahun',
        'semester',
        'is_active',
        'tanggal_mulai',
        'tanggal_selesai',
    )
    search_fields = ('tahun',)
    list_filter = ('is_active', 'tahun')
    list_editable = ('is_active',)


@admin.register(Jurusan)
class JurusanAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama', 'deskripsi')
    search_fields = ('nama',)


@admin.register(Kelas)
class KelasAdmin(admin.ModelAdmin):
    list_display = ('nama', 'jurusan', 'get_wali_kelas_nama', 'tahun_ajaran')
    list_filter = ('jurusan', 'tahun_ajaran__is_active', 'tahun_ajaran')
    search_fields = ('nama', 'jurusan__nama', 'wali_kelas__first_name', 'wali_kelas__last_name', 'tahun_ajaran__tahun')
    autocomplete_fields = ('jurusan', 'wali_kelas', 'tahun_ajaran')
    list_select_related = ('jurusan', 'wali_kelas', 'tahun_ajaran')

    @admin.display(description='Wali Kelas', ordering='wali_kelas__first_name')
    def get_wali_kelas_nama(self, obj):
        return obj.wali_kelas.get_full_name()


@admin.register(Mapel)
class MapelAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama')
    search_fields = ('nama',)


@admin.register(KelasSiswa)
class KelasSiswaAdmin(admin.ModelAdmin):
    list_display = ('get_nama_siswa', 'get_nama_kelas', 'tahun_ajaran')
    list_filter = ('tahun_ajaran__is_active', 'kelas__jurusan', 'tahun_ajaran')
    search_fields = ('siswa__first_name', 'siswa__last_name', 'kelas__nama', 'tahun_ajaran__tahun')
    autocomplete_fields = ('siswa', 'kelas', 'tahun_ajaran')
    list_select_related = ('siswa', 'kelas', 'tahun_ajaran')

    @admin.display(description='Siswa', ordering='siswa__first_name')
    def get_nama_siswa(self, obj):
        return obj.siswa.get_full_name()

    @admin.display(description='Kelas', ordering='kelas__nama')
    def get_nama_kelas(self, obj):
        return obj.kelas.nama


@admin.register(Jadwal)
class JadwalAdmin(admin.ModelAdmin):
    list_display = (
        'get_nama_kelas',
        'mapel',
        'get_nama_guru',
        'hari',
        'jam_mulai',
        'jam_selesai',
    )
    list_filter = ('hari', 'kelas__jurusan', 'mapel', 'guru', 'kelas__tahun_ajaran__is_active')
    search_fields = ('kelas__nama', 'mapel__nama', 'guru__first_name', 'guru__last_name')
    autocomplete_fields = ('kelas', 'mapel', 'guru')
    list_select_related = ('kelas', 'mapel', 'guru')

    @admin.display(description='Guru', ordering='guru__first_name')
    def get_nama_guru(self, obj):
        return obj.guru.get_full_name()

    @admin.display(description='Kelas', ordering='kelas__nama')
    def get_nama_kelas(self, obj):
        return obj.kelas.nama

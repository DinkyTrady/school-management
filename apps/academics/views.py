# apps/academics/views.py
from django.db.models import Count

from apps.core.views import BaseListView
from .models import Kelas, TahunAjaran, Jurusan, Mapel, Jadwal


class KelasListView(BaseListView):
    """
    Menampilkan halaman penuh daftar kelas.
    Hanya untuk Staf Internal (Admin, Guru, Kepsek, TU).
    """
    model = Kelas
    permission_required = ['academics.view_kelas']
    full_template_name = 'academics/kelas_list.html'
    partial_template_name = 'academics/partials/academics/_kelas_table_rows.html'
    context_object_name = 'daftar_kelas'
    success_url_name = 'academics:kelas_list'
    search_fields = ['nama']
    table_body_id = 'kelas-table-body'

    def get_queryset(self):
        """
        Override queryset untuk mengoptimalkan N+1 query
        dan hanya mengambil kelas yang aktif.
        """
        # Apply base search first
        qs = super().get_queryset()
        
        # Filter active classes
        qs = qs.filter(tahun_ajaran__is_active=True)
        
        # OPTIMASI N+1 QUERY:
        # Gunakan select_related untuk ForeignKey (M:1)
        # Ambil data jurusan, wali_kelas, dan tahun_ajaran dalam satu query JOIN
        qs = qs.select_related('jurusan', 'wali_kelas', 'tahun_ajaran')
        
        # OPTIMASI N+1 QUERY:
        # Gunakan annotate untuk menghitung jumlah siswa (M:N)
        # Ini melakukan GROUP BY di level database, sangat efisien.
        qs = qs.annotate(
            jumlah_siswa=Count('kelassiswa') # 'kelassiswa' adalah related_name
        )
        
        return qs.order_by('nama')


class TahunAjaranListView(BaseListView):
    """ListView untuk manajemen tahun ajaran"""
    model = TahunAjaran
    permission_required = ['academics.view_tahunajar']
    full_template_name = 'academics/tahun_ajaran_list.html'
    partial_template_name = 'academics/partials/tahun_ajaran_table_body.html'
    context_object_name = 'tahun_ajaran_list'
    success_url_name = 'academics:tahun_ajaran_list'
    search_fields = ['tahun', 'semester']
    table_body_id = 'tahun-ajaran-table-body'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.order_by('-is_active', '-tahun', 'semester')


class JurusanListView(BaseListView):
    """ListView untuk manajemen jurusan"""
    model = Jurusan
    permission_required = ['academics.view_jurusan']
    full_template_name = 'academics/jurusan_list.html'
    partial_template_name = 'academics/partials/jurusan_table_body.html'
    context_object_name = 'jurusan_list'
    success_url_name = 'academics:jurusan_list'
    search_fields = ['nama', 'deskripsi']
    table_body_id = 'jurusan-table-body'


class MapelListView(BaseListView):
    """ListView untuk manajemen mata pelajaran"""
    model = Mapel
    permission_required = ['academics.view_mapel']
    full_template_name = 'academics/mapel_list.html'
    partial_template_name = 'academics/partials/mapel_table_body.html'
    context_object_name = 'mapel_list'
    success_url_name = 'academics:mapel_list'
    search_fields = ['nama']
    table_body_id = 'mapel-table-body'


class JadwalListView(BaseListView):
    """ListView untuk melihat jadwal pelajaran"""
    model = Jadwal
    permission_required = ['academics.view_jadwal']
    full_template_name = 'academics/jadwal_list.html'
    partial_template_name = 'academics/partials/jadwal_table_body.html'
    context_object_name = 'jadwal_list'
    success_url_name = 'academics:jadwal_list'
    search_fields = ['kelas__nama', 'mapel__nama', 'guru__first_name', 'guru__last_name']
    table_body_id = 'jadwal-table-body'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('kelas', 'mapel', 'guru', 'kelas__tahun_ajaran')
        return qs.filter(kelas__tahun_ajaran__is_active=True).order_by('hari', 'jam_mulai')

# HTMX search functionality now handled by BaseListView

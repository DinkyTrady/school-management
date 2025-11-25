from apps.academics.models import KelasSiswa
from apps.core.views import BaseListView
from .models import Tugas, Nilai, Presensi


class TugasListView(BaseListView):
    """ListView untuk manajemen tugas"""
    model = Tugas
    permission_required = ['grades.view_tugas']
    full_template_name = 'grades/tugas_list.html'
    partial_template_name = 'grades/partials/tugas_table_body.html'
    context_object_name = 'tugas_list'
    success_url_name = 'grades:tugas_list'
    search_fields = ['nama', 'deskripsi', 'jadwal__kelas__nama', 'jadwal__mapel__nama']
    table_body_id = 'tugas-table-body'

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user

        qs = qs.select_related(
            'jadwal', 'jadwal__kelas', 'jadwal__mapel', 'jadwal__guru',
            'jadwal__kelas__tahun_ajaran'
        ).filter(jadwal__kelas__tahun_ajaran__is_active=True).order_by('-tenggat')
        
        if user.is_siswa:
            try:
                siswa_profile = user.siswa_profile
                kelas_siswa = KelasSiswa.objects.filter(
                    siswa=siswa_profile,
                    tahun_ajaran__is_active=True
                ).select_related('kelas').first()

                if kelas_siswa:
                    return qs.filter(jadwal__kelas=kelas_siswa.kelas)
                return qs.none() 
            except AttributeError:
                return qs.none()

        return qs


class NilaiListView(BaseListView):
    """ListView untuk melihat nilai siswa"""
    model = Nilai
    permission_required = ['grades.view_nilai']
    full_template_name = 'grades/nilai_list.html'
    partial_template_name = 'grades/partials/nilai_table_body.html'
    context_object_name = 'nilai_list'
    success_url_name = 'grades:nilai_list'
    search_fields = [
        'siswa__first_name', 'siswa__last_name', 'siswa__nis',
        'jadwal__kelas__nama', 'jadwal__mapel__nama', 'tipe_penilaian'
    ]
    table_body_id = 'nilai-table-body'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related(
            'siswa', 'siswa__akun', 'jadwal', 'jadwal__kelas', 'jadwal__mapel',
            'jadwal__guru', 'tugas', 'jadwal__kelas__tahun_ajaran'
        )
        return qs.filter(jadwal__kelas__tahun_ajaran__is_active=True).order_by('-tanggal_penilaian')


class PresensiListView(BaseListView):
    """ListView untuk melihat presensi siswa"""
    model = Presensi
    permission_required = ['grades.view_presensi']
    full_template_name = 'grades/presensi_list.html'
    partial_template_name = 'grades/partials/presensi_table_body.html'
    context_object_name = 'presensi_list'
    success_url_name = 'grades:presensi_list'
    search_fields = [
        'siswa__first_name', 'siswa__last_name', 'siswa__nis',
        'jadwal__kelas__nama', 'jadwal__mapel__nama', 'status'
    ]
    table_body_id = 'presensi-table-body'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related(
            'siswa', 'siswa__akun', 'jadwal', 'jadwal__kelas', 'jadwal__mapel',
            'jadwal__guru', 'jadwal__kelas__tahun_ajaran'
        )
        return qs.filter(jadwal__kelas__tahun_ajaran__is_active=True).order_by('-tanggal')

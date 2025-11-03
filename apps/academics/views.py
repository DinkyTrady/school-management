# apps/academics/views.py
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Count
from django.shortcuts import render
from django.views.generic import ListView

from .models import Kelas


class KelasListView(LoginRequiredMixin,  ListView):
    """
    Menampilkan halaman penuh daftar kelas.
    Hanya untuk Staf Internal (Admin, Guru, Kepsek, TU).
    """
    model = Kelas
    # permission_required = ['academics.view_kelas']
    template_name = 'academics/kelas_list.html'
    context_object_name = 'daftar_kelas'

    def get_queryset(self):
        """
        Override queryset untuk mengoptimalkan N+1 query
        dan hanya mengambil kelas yang aktif.
        """
        # Mulai dengan queryset dasar
        qs = Kelas.objects.filter(tahun_ajaran__is_active=True)
        
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

# --- View untuk HTMX ---

@login_required
@permission_required('academics.view_kelas', 'users:login', True)
def htmx_search_kelas(request):
    """
    View ini HANYA merender partial HTML untuk isi tabel.
    Dipanggil oleh HTMX dari search bar.
    """
    search_text = request.GET.get('q', '').strip()
    
    # Mulai dengan queryset yang SAMA persis dengan CBV
    qs = Kelas.objects.filter(tahun_ajaran__is_active=True)
    qs = qs.select_related('jurusan', 'wali_kelas', 'tahun_ajaran')
    qs = qs.annotate(jumlah_siswa=Count('kelassiswa'))
    
    # Terapkan filter pencarian
    if search_text:
        qs = qs.filter(nama__icontains=search_text)
        
    context = {'daftar_kelas': qs.order_by('nama')}
    
    # Render HANYA partial-nya
    return render(request, 'partials/academics/_kelas_table_rows.html', context)

# apps/academics/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import render
from django.views.generic import ListView

from apps.users.decorators import staff_internal_required
from apps.users.mixins import StaffInternalRequiredMixin

from .models import Kelas


class KelasListView(LoginRequiredMixin, StaffInternalRequiredMixin, ListView):
    """
    Menampilkan halaman penuh daftar kelas.
    Hanya untuk Staf Internal (Admin, Guru, Kepsek, TU).
    """
    model = Kelas
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

@staff_internal_required # Amankan endpoint HTMX Anda
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

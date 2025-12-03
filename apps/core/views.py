from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q, Case, When, Value, IntegerField, Count, Avg
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.utils import timezone

from apps.users.models import Peran
from apps.academics.models import Kelas, Mapel, KelasSiswa, Jadwal
from apps.grades.models import Tugas, Presensi, Nilai

User = get_user_model()

class BaseCrudMixin(LoginRequiredMixin, PermissionRequiredMixin):
    '''
    Mixin dasar untuk semua CRUD View.
    Menangani Hak Akses, URL sukses, dan logika HTMX
    '''
    success_url_name = None
    partial_template_name = None
    full_template_name = None
    search_fields = []

    def get_success_url(self):
        if not self.success_url_name:
            raise ImproperlyConfigured('"success_url_name" not defined correctly')
        return reverse_lazy(self.success_url_name)

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')

        if query and self.search_fields:
            q_objects = Q()
            for field in self.search_fields:
                q_objects |= Q(**{f'{field}__icontains': query})
            qs = qs.filter(q_objects)
        
        return qs

    def get_template_names(self):
        if self.request.htmx:
            if not self.partial_template_name:
                raise ImproperlyConfigured(
                    '"partial_template_name" not defined correctly'
                )
            return [self.partial_template_name]

        print(self.request.htmx)
        if not self.full_template_name:
            raise ImproperlyConfigured(
                '"full_template_name" not defined correctly'
            )

        return [self.full_template_name]

class BaseListView(BaseCrudMixin, ListView):
    paginate_by = 10
    table_body_id = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.table_body_id:
            context['table_body_id'] = self.table_body_id
        
        if self.request.htmx:
            pagination_html = render_to_string(
                'core/partials/_paginate.html',
                context,
                request=self.request
            )
            context['pagination'] = (
                f'<div id="pagination-container" hx-swap-oob="true">{pagination_html}</div>'
            )
        return context

class BaseDetailView(BaseCrudMixin, DetailView):
    pass

class BaseCreateView(BaseCrudMixin, CreateView):
    full_template_name = 'core/partials/_generic_form.html'
    partial_template_name = 'core/partials/_form_content.html'

class BaseUpdateView(BaseCrudMixin, UpdateView):
    full_template_name = 'core/partials/_generic_form.html'
    partial_template_name = 'core/partials/_form_content.html'

class BaseDeleteView(BaseCrudMixin, DeleteView):
    full_template_name = 'core/partials/_generic_form.html'
    partial_template_name = 'core/partials/_generic_form.html'


class IntroPageView(TemplateView):
    '''
    View untuk halaman intro/perkenalan SIGMA sebelum login
    '''
    template_name = 'core/intro.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Jika user sudah login, redirect ke dashboard
        if request.user.is_authenticated:
            return redirect('core:dashboard')
        return super().dispatch(request, *args, **kwargs)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['is_admin'] = user.is_admin
        context['is_guru'] = user.is_guru
        context['card_akun_url'] = reverse(
            'users:akun_list'
        )  # Change 'users:list' to your actual URL name
        context['card_peran_url'] = reverse(
            'users:peran_list'
        )  # Change 'peran:list' to your actual URL name
        context['card_kelas_url'] = reverse(
            'academics:kelas_list'
        )  # Change 'kelas:list' to your actual URL name
        # context['card_mapel_url'] = reverse(
        #     'academics:mapel_list'
        # )  # Change 'mapel:list' to your actual URL name

        # Hanya hitung dan tambahkan data ini jika pengguna adalah admin
        if user.is_superuser:
            # Cukup ambil data untuk kartu ringkasan
            context['total_akun'] = User.objects.count()
            context['total_peran'] = Peran.objects.count()
            context['total_kelas'] = Kelas.objects.count()
            context['total_mapel'] = Mapel.objects.count()

        # Data khusus untuk Siswa
        if user.is_siswa and hasattr(user, 'siswa_profile'):
            siswa = user.siswa_profile
            # Ambil kelas aktif siswa
            kelas_siswa = KelasSiswa.objects.filter(
                siswa=siswa,
                tahun_ajaran__is_active=True
            ).select_related('kelas', 'kelas__wali_kelas', 'kelas__jurusan').first()

            if kelas_siswa:
                context['kelas_siswa'] = kelas_siswa.kelas
                
                # Ambil Jadwal Minggu Ini (Diurutkan berdasarkan Hari dan Jam)
                # Mapping hari ke angka untuk sorting
                hari_ordering = Case(
                    When(hari='Senin', then=Value(1)),
                    When(hari='Selasa', then=Value(2)),
                    When(hari='Rabu', then=Value(3)),
                    When(hari='Kamis', then=Value(4)),
                    When(hari="Jum'at", then=Value(5)),
                    When(hari='Sabtu', then=Value(6)),
                    When(hari='Minggu', then=Value(7)),
                    output_field=IntegerField(),
                )
                
                jadwal_list = Jadwal.objects.filter(
                    kelas=kelas_siswa.kelas
                ).annotate(
                    hari_order=hari_ordering
                ).order_by('hari_order', 'jam_mulai').select_related('mapel', 'guru')
                
                context['jadwal_list'] = jadwal_list
                
                # Ambil 2 Tugas Terbaru yang belum tenggat
                tugas_list = Tugas.objects.filter(
                    jadwal__kelas=kelas_siswa.kelas,
                    tenggat__gte=timezone.now()
                ).select_related('jadwal', 'jadwal__mapel').order_by('tenggat')[:2]
                
                context['tugas_list'] = tugas_list

                # Attendance Summary
                presensi_stats = Presensi.objects.filter(
                    siswa=siswa,
                    jadwal__kelas__tahun_ajaran__is_active=True
                ).values('status').annotate(count=Count('status'))
                
                attendance_data = {
                    'Hadir': 0,
                    'Sakit': 0,
                    'Izin': 0,
                    'Alpha': 0
                }
                for stat in presensi_stats:
                    if stat['status'] in attendance_data:
                        attendance_data[stat['status']] = stat['count']
                
                context['attendance_data'] = attendance_data

                # Grades Chart Data (Average per Subject)
                nilai_stats = Nilai.objects.filter(
                    siswa=siswa,
                    jadwal__kelas__tahun_ajaran__is_active=True
                ).values('jadwal__mapel__nama').annotate(
                    avg_nilai=Avg('nilai')
                ).order_by('jadwal__mapel__nama')

                context['chart_labels'] = [stat['jadwal__mapel__nama'] for stat in nilai_stats]
                context['chart_data'] = [float(stat['avg_nilai']) for stat in nilai_stats]

        # Data khusus untuk Guru
        if user.is_guru and hasattr(user, 'guru_profile'):
            guru = user.guru_profile
            today = timezone.now()
            
            # Mapping hari Inggris ke Indonesia
            day_mapping = {
                'Monday': 'Senin',
                'Tuesday': 'Selasa',
                'Wednesday': 'Rabu',
                'Thursday': 'Kamis',
                'Friday': "Jum'at",
                'Saturday': 'Sabtu',
                'Sunday': 'Minggu',
            }
            hari_ini = day_mapping.get(today.strftime('%A'))
            
            # Jadwal Mengajar Hari Ini
            jadwal_hari_ini = Jadwal.objects.filter(
                guru=guru,
                hari=hari_ini,
                kelas__tahun_ajaran__is_active=True
            ).select_related('kelas', 'mapel').order_by('jam_mulai')
            
            context['jadwal_hari_ini'] = jadwal_hari_ini
            
            # Tugas Terbaru (yang dibuat oleh guru ini)
            tugas_terbaru = Tugas.objects.filter(
                jadwal__guru=guru,
                jadwal__kelas__tahun_ajaran__is_active=True
            ).select_related('jadwal', 'jadwal__kelas', 'jadwal__mapel').order_by('-tenggat')[:5]
            
            context['tugas_terbaru'] = tugas_terbaru
            
            # Presensi Terbaru (Siswa yang tidak hadir di kelas yang diajar guru ini)
            presensi_terbaru = Presensi.objects.filter(
                jadwal__guru=guru,
                jadwal__kelas__tahun_ajaran__is_active=True
            ).exclude(status='Hadir').select_related('siswa', 'jadwal', 'jadwal__kelas').order_by('-tanggal')[:5]
            
            context['presensi_terbaru'] = presensi_terbaru

        return context


class PermissionTestView(LoginRequiredMixin, TemplateView):
    """
    View to test the role-based permission system
    Shows permission matrix for different roles based on intro.html
    """
    template_name = 'core/permission_test.html'

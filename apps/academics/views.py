# apps/academics/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DeleteView, DetailView
from django.urls import reverse_lazy
from django.template.response import TemplateResponse
from django.db.models import Count

from apps.core.views import BaseListView, BaseCreateView, BaseUpdateView
from apps.core.mixins import AcademicViewOnlyMixin, FullAccessMixin
from .models import Kelas, TahunAjaran, Jurusan, Mapel, Jadwal, KelasSiswa
from .forms import KelasForm, TahunAjaranForm, JurusanForm, MapelForm, JadwalForm


class KelasListView(AcademicViewOnlyMixin, BaseListView):
    """
    Menampilkan halaman penuh daftar kelas.
    Admin: Full access, Guru/Siswa: View only
    """
    model = Kelas
    required_permission = 'view'
    model_name = 'kelas'
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


class KelasDetailView(AcademicViewOnlyMixin, DetailView):
    """DetailView for Kelas"""
    model = Kelas
    template_name = 'academics/kelas_detail.html'
    context_object_name = 'kelas'
    required_permission = 'view'

    def get_queryset(self):
        return Kelas.objects.select_related('jurusan', 'wali_kelas', 'tahun_ajaran').annotate(
            jumlah_siswa=Count('kelassiswa')
        )


# CRUD Views untuk Kelas (Admin only)
class KelasCreateView(FullAccessMixin, BaseCreateView):
    """CreateView for Kelas - Admin only"""
    model = Kelas
    form_class = KelasForm
    success_url_name = 'academics:kelas_list'


class KelasUpdateView(FullAccessMixin, BaseUpdateView):
    """UpdateView for Kelas - Admin only"""  
    model = Kelas
    form_class = KelasForm
    success_url_name = 'academics:kelas_list'
    
    def form_valid(self, form):
        self.object = form.save()
        context = self.get_context_data(form=form)
        context['success_message'] = "Kelas berhasil diperbarui."
        return TemplateResponse(self.request, self.get_template_names(), context)


class KelasDeleteView(FullAccessMixin, LoginRequiredMixin, DeleteView):
    """DeleteView for Kelas - Admin only"""
    model = Kelas
    template_name = 'academics/kelas_confirm_delete.html'
    success_url = reverse_lazy('academics:kelas_list')
    
    def get_template_names(self):
        if self.request.htmx:
            return ['academics/partials/kelas_delete_modal.html']
        return ['academics/kelas_confirm_delete.html']


class TahunAjaranListView(AcademicViewOnlyMixin, BaseListView):
    """ListView untuk manajemen tahun ajaran"""
    model = TahunAjaran
    required_permission = 'view'
    model_name = 'tahunajar'
    full_template_name = 'academics/tahun_ajaran_list.html'
    partial_template_name = 'academics/partials/tahun_ajaran_table_body.html'
    context_object_name = 'tahun_ajaran_list'
    success_url_name = 'academics:tahun_ajaran_list'
    search_fields = ['tahun', 'semester']
    table_body_id = 'tahun-ajaran-table-body'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.order_by('-is_active', '-tahun', 'semester')


class TahunAjaranDetailView(AcademicViewOnlyMixin, DetailView):
    """DetailView for TahunAjaran"""
    model = TahunAjaran
    template_name = 'academics/tahun_ajaran_detail.html'
    context_object_name = 'tahun_ajaran'
    required_permission = 'view'


# CRUD Views untuk Tahun Ajaran (Admin only)
class TahunAjaranCreateView(FullAccessMixin, BaseCreateView):
    """CreateView for TahunAjaran - Admin only"""
    model = TahunAjaran
    form_class = TahunAjaranForm
    success_url_name = 'academics:tahun_ajaran_list'


class TahunAjaranUpdateView(FullAccessMixin, BaseUpdateView):
    """UpdateView for TahunAjaran - Admin only"""  
    model = TahunAjaran
    form_class = TahunAjaranForm
    success_url_name = 'academics:tahun_ajaran_list'
    
    def form_valid(self, form):
        self.object = form.save()
        context = self.get_context_data(form=form)
        context['success_message'] = "Tahun Ajaran berhasil diperbarui."
        return TemplateResponse(self.request, self.get_template_names(), context)


class TahunAjaranDeleteView(FullAccessMixin, LoginRequiredMixin, DeleteView):
    """DeleteView for TahunAjaran - Admin only"""
    model = TahunAjaran
    template_name = 'academics/tahun_ajaran_confirm_delete.html'
    success_url = reverse_lazy('academics:tahun_ajaran_list')
    
    def get_template_names(self):
        if self.request.htmx:
            return ['academics/partials/tahun_ajaran_delete_modal.html']
        return ['academics/tahun_ajaran_confirm_delete.html']


class JurusanListView(AcademicViewOnlyMixin, BaseListView):
    """ListView untuk manajemen jurusan"""
    model = Jurusan
    required_permission = 'view'
    model_name = 'jurusan'
    full_template_name = 'academics/jurusan_list.html'
    partial_template_name = 'academics/partials/jurusan_table_body.html'
    context_object_name = 'jurusan_list'
    success_url_name = 'academics:jurusan_list'
    search_fields = ['nama', 'deskripsi']
    table_body_id = 'jurusan-table-body'


class JurusanDetailView(AcademicViewOnlyMixin, DetailView):
    """DetailView for Jurusan"""
    model = Jurusan
    template_name = 'academics/jurusan_detail.html'
    context_object_name = 'jurusan'
    required_permission = 'view'


# CRUD Views untuk Jurusan (Admin only)
class JurusanCreateView(FullAccessMixin, BaseCreateView):
    """CreateView for Jurusan - Admin only"""
    model = Jurusan
    form_class = JurusanForm
    success_url_name = 'academics:jurusan_list'


class JurusanUpdateView(FullAccessMixin, BaseUpdateView):
    """UpdateView for Jurusan - Admin only"""  
    model = Jurusan
    form_class = JurusanForm
    success_url_name = 'academics:jurusan_list'
    
    def form_valid(self, form):
        self.object = form.save()
        context = self.get_context_data(form=form)
        context['success_message'] = "Jurusan berhasil diperbarui."
        return TemplateResponse(self.request, self.get_template_names(), context)


class JurusanDeleteView(FullAccessMixin, LoginRequiredMixin, DeleteView):
    """DeleteView for Jurusan - Admin only"""
    model = Jurusan
    template_name = 'academics/jurusan_confirm_delete.html'
    success_url = reverse_lazy('academics:jurusan_list')
    
    def get_template_names(self):
        if self.request.htmx:
            return ['academics/partials/jurusan_delete_modal.html']
        return ['academics/jurusan_confirm_delete.html']


class MapelListView(AcademicViewOnlyMixin, BaseListView):
    """ListView untuk manajemen mata pelajaran"""
    model = Mapel
    required_permission = 'view'
    model_name = 'mapel'
    full_template_name = 'academics/mapel_list.html'
    partial_template_name = 'academics/partials/mapel_table_body.html'
    context_object_name = 'mapel_list'
    success_url_name = 'academics:mapel_list'
    search_fields = ['nama']
    table_body_id = 'mapel-table-body'


class MapelDetailView(AcademicViewOnlyMixin, DetailView):
    """DetailView for Mapel"""
    model = Mapel
    template_name = 'academics/mapel_detail.html'
    context_object_name = 'mapel'
    required_permission = 'view'


# CRUD Views untuk Mapel (Admin only)
class MapelCreateView(FullAccessMixin, BaseCreateView):
    """CreateView for Mapel - Admin only"""
    model = Mapel
    form_class = MapelForm
    success_url_name = 'academics:mapel_list'


class MapelUpdateView(FullAccessMixin, BaseUpdateView):
    """UpdateView for Mapel - Admin only"""  
    model = Mapel
    form_class = MapelForm
    success_url_name = 'academics:mapel_list'
    
    def form_valid(self, form):
        self.object = form.save()
        context = self.get_context_data(form=form)
        context['success_message'] = "Mata Pelajaran berhasil diperbarui."
        return TemplateResponse(self.request, self.get_template_names(), context)


class MapelDeleteView(FullAccessMixin, LoginRequiredMixin, DeleteView):
    """DeleteView for Mapel - Admin only"""
    model = Mapel
    template_name = 'academics/mapel_confirm_delete.html'
    success_url = reverse_lazy('academics:mapel_list')
    
    def get_template_names(self):
        if self.request.htmx:
            return ['academics/partials/mapel_delete_modal.html']
        return ['academics/mapel_confirm_delete.html']


class JadwalListView(AcademicViewOnlyMixin, BaseListView):
    """ListView untuk melihat jadwal pelajaran"""
    model = Jadwal
    required_permission = 'view'
    model_name = 'jadwal'
    full_template_name = 'academics/jadwal_list.html'
    partial_template_name = 'academics/partials/jadwal_table_body.html'
    context_object_name = 'jadwal_list'
    success_url_name = 'academics:jadwal_list'
    search_fields = ['kelas__nama', 'mapel__nama', 'guru__first_name', 'guru__last_name']
    table_body_id = 'jadwal-table-body'

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user

        qs = qs.select_related(
            'kelas', 'mapel', 'guru', 'kelas__tahun_ajaran'
        ).filter(kelas__tahun_ajaran__is_active=True)

        if user.is_siswa:
            try:
                siswa_profile = user.siswa_profile
                kelas_siswa = KelasSiswa.objects.filter(
                    siswa=siswa_profile,
                    tahun_ajaran__is_active=True
                ).select_related('kelas').first()

                if kelas_siswa:
                    return qs.filter(kelas=kelas_siswa.kelas).order_by('hari', 'jam_mulai')
                return qs.none()
            except AttributeError:
                return qs.none()
        
        return qs.order_by('hari', 'jam_mulai')


class JadwalDetailView(AcademicViewOnlyMixin, DetailView):
    """DetailView for Jadwal"""
    model = Jadwal
    template_name = 'academics/jadwal_detail.html'
    context_object_name = 'jadwal'
    required_permission = 'view'

    def get_queryset(self):
        return Jadwal.objects.select_related('kelas', 'mapel', 'guru', 'kelas__tahun_ajaran')


# CRUD Views untuk Jadwal (Admin only)
class JadwalCreateView(FullAccessMixin, BaseCreateView):
    """CreateView for Jadwal - Admin only"""
    model = Jadwal
    form_class = JadwalForm
    success_url_name = 'academics:jadwal_list'


class JadwalUpdateView(FullAccessMixin, BaseUpdateView):
    """UpdateView for Jadwal - Admin only"""  
    model = Jadwal
    form_class = JadwalForm
    success_url_name = 'academics:jadwal_list'
    
    def form_valid(self, form):
        self.object = form.save()
        context = self.get_context_data(form=form)
        context['success_message'] = "Jadwal berhasil diperbarui."
        return TemplateResponse(self.request, self.get_template_names(), context)


class JadwalDeleteView(FullAccessMixin, LoginRequiredMixin, DeleteView):
    """DeleteView for Jadwal - Admin only"""
    model = Jadwal
    template_name = 'academics/jadwal_confirm_delete.html'
    success_url = reverse_lazy('academics:jadwal_list')
    
    def get_template_names(self):
        if self.request.htmx:
            return ['academics/partials/jadwal_delete_modal.html']
        return ['academics/jadwal_confirm_delete.html']

# HTMX search functionality now handled by BaseListView

from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import DeleteView, DetailView
from django.urls import reverse_lazy
from django.template.response import TemplateResponse

from apps.academics.models import KelasSiswa, Jadwal
from apps.core.views import BaseListView, BaseCreateView, BaseUpdateView
from apps.core.mixins import TugasPermissionMixin, NilaiPermissionMixin, PresensiPermissionMixin
from .models import Tugas, Nilai, Presensi
from .forms import TugasForm, NilaiForm, PresensiForm


class TugasListView(TugasPermissionMixin, BaseListView):
    """ListView untuk manajemen tugas - Role-based access from intro.html"""
    model = Tugas
    required_permission = 'view'
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


class TugasDetailView(TugasPermissionMixin, DetailView):
    """DetailView for Tugas"""
    model = Tugas
    template_name = 'grades/tugas_detail.html'
    context_object_name = 'tugas'
    required_permission = 'view'

    def get_queryset(self):
        return Tugas.objects.select_related(
            'jadwal', 'jadwal__kelas', 'jadwal__mapel', 'jadwal__guru',
            'jadwal__kelas__tahun_ajaran'
        )


class NilaiListView(NilaiPermissionMixin, BaseListView):
    """ListView untuk melihat nilai siswa - Role-based access from intro.html"""
    model = Nilai
    required_permission = 'view'
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
        user = self.request.user
        
        qs = qs.select_related(
            'siswa', 'siswa__akun', 'jadwal', 'jadwal__kelas', 'jadwal__mapel',
            'jadwal__guru', 'tugas', 'jadwal__kelas__tahun_ajaran'
        ).filter(jadwal__kelas__tahun_ajaran__is_active=True).order_by('-tanggal_penilaian')

        if user.is_siswa:
            try:
                siswa_profile = user.siswa_profile
                kelas_siswa = KelasSiswa.objects.filter(
                    siswa=siswa_profile,
                    tahun_ajaran__is_active=True
                ).select_related('kelas').first()

                if kelas_siswa:
                    # Siswa hanya melihat nilai mereka sendiri
                    return qs.filter(siswa=siswa_profile)
                return qs.none() 
            except AttributeError:
                return qs.none()

        return qs


class NilaiDetailView(NilaiPermissionMixin, DetailView):
    """DetailView for Nilai"""
    model = Nilai
    template_name = 'grades/nilai_detail.html'
    context_object_name = 'nilai'
    required_permission = 'view'

    def get_queryset(self):
        return Nilai.objects.select_related(
            'siswa', 'siswa__akun', 'jadwal', 'jadwal__kelas', 'jadwal__mapel',
            'jadwal__guru', 'tugas', 'jadwal__kelas__tahun_ajaran'
        )


class PresensiListView(PresensiPermissionMixin, BaseListView):
    """ListView untuk melihat presensi siswa - Role-based access from intro.html"""
    model = Presensi
    required_permission = 'view'
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
        user = self.request.user
        
        qs = qs.select_related(
            'siswa', 'siswa__akun', 'jadwal', 'jadwal__kelas', 'jadwal__mapel',
            'jadwal__guru', 'jadwal__kelas__tahun_ajaran'
        ).filter(jadwal__kelas__tahun_ajaran__is_active=True).order_by('-tanggal')

        if user.is_siswa:
            try:
                siswa_profile = user.siswa_profile
                kelas_siswa = KelasSiswa.objects.filter(
                    siswa=siswa_profile,
                    tahun_ajaran__is_active=True
                ).select_related('kelas').first()

                if kelas_siswa:
                    # Siswa hanya melihat presensi mereka sendiri
                    return qs.filter(siswa=siswa_profile)
                return qs.none() 
            except AttributeError:
                return qs.none()

        return qs


class PresensiDetailView(PresensiPermissionMixin, DetailView):
    """DetailView for Presensi"""
    model = Presensi
    template_name = 'grades/presensi_detail.html'
    context_object_name = 'presensi'
    required_permission = 'view'

    def get_queryset(self):
        return Presensi.objects.select_related(
            'siswa', 'siswa__akun', 'jadwal', 'jadwal__kelas', 'jadwal__mapel',
            'jadwal__guru', 'jadwal__kelas__tahun_ajaran'
        )


# CRUD Views for Guru to manage grades data (based on intro.html permissions)

class TugasCreateView(TugasPermissionMixin, BaseCreateView):
    """CreateView for Tugas - Guru can create assignments"""
    model = Tugas
    form_class = TugasForm
    required_permission = 'add'
    success_url_name = 'grades:tugas_list'


class TugasUpdateView(TugasPermissionMixin, BaseUpdateView):
    """UpdateView for Tugas - Guru can edit assignments"""  
    model = Tugas
    form_class = TugasForm
    required_permission = 'change'
    success_url_name = 'grades:tugas_list'
    
    def form_valid(self, form):
        self.object = form.save()
        context = self.get_context_data(form=form)
        context['success_message'] = "Tugas berhasil diperbarui."
        return TemplateResponse(self.request, self.get_template_names(), context)


class TugasDeleteView(TugasPermissionMixin, LoginRequiredMixin, DeleteView):
    """DeleteView for Tugas - Guru can delete assignments"""
    model = Tugas  
    template_name = 'grades/tugas_confirm_delete.html'
    success_url = reverse_lazy('grades:tugas_list')
    
    def get_template_names(self):
        if self.request.htmx:
            return ['grades/partials/tugas_delete_modal.html']
        return ['grades/tugas_confirm_delete.html']
    
    def has_permission(self):
        return (
            self.request.user.is_authenticated and 
            self.request.user.can_edit_delete_model('tugas')
        )


class NilaiCreateView(NilaiPermissionMixin, BaseCreateView):
    """CreateView for Nilai - Guru can input grades"""
    model = Nilai
    form_class = NilaiForm
    required_permission = 'add'
    success_url_name = 'grades:nilai_list'


class NilaiUpdateView(NilaiPermissionMixin, BaseUpdateView):
    """UpdateView for Nilai - Guru can edit grades"""
    model = Nilai
    form_class = NilaiForm
    required_permission = 'change' 
    success_url_name = 'grades:nilai_list'
    
    def form_valid(self, form):
        self.object = form.save()
        context = self.get_context_data(form=form)
        context['success_message'] = "Nilai berhasil diperbarui."
        return TemplateResponse(self.request, self.get_template_names(), context)


class NilaiDeleteView(NilaiPermissionMixin, LoginRequiredMixin, DeleteView):
    """DeleteView for Nilai - Guru can delete grades"""
    model = Nilai
    template_name = 'grades/nilai_confirm_delete.html'
    success_url = reverse_lazy('grades:nilai_list')
    
    def get_template_names(self):
        if self.request.htmx:
            return ['grades/partials/nilai_delete_modal.html']
        return ['grades/nilai_confirm_delete.html']
    
    def has_permission(self):
        return (
            self.request.user.is_authenticated and 
            self.request.user.can_edit_delete_model('nilai')
        )


class PresensiCreateView(PresensiPermissionMixin, BaseCreateView):
    """CreateView for Presensi - Guru can record attendance"""
    model = Presensi
    form_class = PresensiForm
    required_permission = 'add'
    success_url_name = 'grades:presensi_list'


class PresensiUpdateView(PresensiPermissionMixin, BaseUpdateView):
    """UpdateView for Presensi - Guru can edit attendance"""
    model = Presensi
    form_class = PresensiForm
    required_permission = 'change'
    success_url_name = 'grades:presensi_list'
    
    def form_valid(self, form):
        self.object = form.save()
        context = self.get_context_data(form=form)
        context['success_message'] = "Presensi berhasil diperbarui."
        return TemplateResponse(self.request, self.get_template_names(), context)


class PresensiDeleteView(PresensiPermissionMixin, LoginRequiredMixin, DeleteView):
    """DeleteView for Presensi - Guru can delete attendance"""
    model = Presensi
    template_name = 'grades/presensi_confirm_delete.html'
    success_url = reverse_lazy('grades:presensi_list')
    
    def get_template_names(self):
        if self.request.htmx:
            return ['grades/partials/presensi_delete_modal.html']
        return ['grades/presensi_confirm_delete.html']
    
    def has_permission(self):
        return (
            self.request.user.is_authenticated and 
            self.request.user.can_edit_delete_model('presensi')
        )


class JadwalAbsensiView(LoginRequiredMixin, View):
    template_name = 'grades/jadwal_absensi.html'

    def get(self, request, jadwal_id):
        if not request.user.is_guru and not request.user.is_admin:
             messages.error(request, "Anda tidak memiliki izin untuk mengakses halaman ini.")
             return redirect('academics:jadwal_list')
        
        jadwal = get_object_or_404(Jadwal, pk=jadwal_id)
        # Get students in the class
        students = KelasSiswa.objects.filter(
            kelas=jadwal.kelas,
            tahun_ajaran=jadwal.kelas.tahun_ajaran
        ).select_related('siswa', 'siswa__akun').order_by('siswa__first_name')
        
        # Check if attendance already exists for today
        today = timezone.now().date()
        existing_presensi = {
            p.siswa_id: p 
            for p in Presensi.objects.filter(jadwal=jadwal, tanggal=today)
        }
        
        student_data = []
        for ks in students:
            presensi = existing_presensi.get(ks.siswa.pk)
            student_data.append({
                'siswa': ks.siswa,
                'presensi': presensi
            })
            
        context = {
            'jadwal': jadwal,
            'student_data': student_data,
            'today': today
        }
        return render(request, self.template_name, context)

    def post(self, request, jadwal_id):
        if not request.user.is_guru and not request.user.is_admin:
             messages.error(request, "Anda tidak memiliki izin untuk melakukan aksi ini.")
             return redirect('academics:jadwal_list')

        jadwal = get_object_or_404(Jadwal, pk=jadwal_id)
        today = timezone.now().date()
        
        students = KelasSiswa.objects.filter(
            kelas=jadwal.kelas,
            tahun_ajaran=jadwal.kelas.tahun_ajaran
        )
        
        for ks in students:
            siswa_id = ks.siswa.pk
            status = request.POST.get(f'status_{siswa_id}')
            keterangan = request.POST.get(f'keterangan_{siswa_id}')
            
            if status:
                Presensi.objects.update_or_create(
                    siswa=ks.siswa,
                    jadwal=jadwal,
                    tanggal=today,
                    defaults={
                        'status': status,
                        'keterangan': keterangan
                    }
                )
        
        messages.success(request, 'Presensi berhasil disimpan.')
        return redirect('academics:jadwal_list')

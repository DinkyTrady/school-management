from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Permission
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views.generic import (
    DeleteView,
    DetailView,
    UpdateView,
)

from apps.core.views import BaseCreateView, BaseListView, BaseUpdateView
from apps.core.mixins import UserManagementMixin, ViewOnlyMixin

from .forms import (
    AkunChangeForm,
    AkunCreationForm,
    SiswaForm,
    GuruForm,
    SiswaProfileForm,
    GuruProfileForm,
    SelfAkunChangeForm,
)
from .models import Akun as AkunType, Peran, Siswa, Guru

Akun: AkunType = get_user_model()


def search_permissions(request):
    query = request.GET.get('q', '')
    permissions = Permission.objects.filter(name__icontains=query)

    if 'akun_pk' in request.GET and request.GET.get('akun_pk'):
        akun = Akun.objects.get(pk=request.GET.get('akun_pk'))
        form = AkunChangeForm(instance=akun)
    else:
        form = AkunCreationForm()

    field = form['user_permissions']
    field.field.queryset = permissions

    return HttpResponse(
        render_to_string(
            'users/partials/_permission_checkboxes.html',
            {'field': field},
        )
    )


class AkunListView(UserManagementMixin, BaseListView):
    model = Akun
    required_permission = 'view'
    context_object_name = 'akun_list'
    full_template_name = 'users/akun_list.html'
    partial_template_name = 'users/partials/akun_table_body.html'
    success_url_name = 'users:akun_list'
    search_fields = ['email', 'peran__nama']
    table_body_id = 'akun-table-body'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('peran').all().order_by('id')


class AkunCreateView(UserManagementMixin, BaseCreateView):
    model = Akun
    form_class = AkunCreationForm
    success_url_name = 'users:akun_list'


class AkunDetailView(UserManagementMixin, LoginRequiredMixin, DetailView):
    model = Akun
    template_name = 'users/akun_detail.html'
    context_object_name = 'akun'

    def get_queryset(self):
        return Akun.objects.select_related('peran').all()


class AkunUpdateView(UserManagementMixin, BaseUpdateView):
    model = Akun
    form_class = AkunChangeForm
    success_url_name = 'users:akun_list'

    def form_valid(self, form):
        self.object = form.save()
        context = self.get_context_data(form=form)
        context['success_message'] = "Akun Berhasil diperbarui."
        return TemplateResponse(self.request, self.get_template_names(), context)


class AkunDeleteView(UserManagementMixin, LoginRequiredMixin, DeleteView):
    model = Akun
    template_name = 'users/akun_confirm_delete.html'
    success_url = reverse_lazy('users:akun_list')

    def get_template_names(self):
        if self.request.htmx:
            return ['users/partials/akun_delete_modal.html']
        return ['users/akun_confirm_delete.html']


# -- Views peran
class PeranListView(UserManagementMixin, BaseListView):
    model = Peran
    required_permission = 'view'
    context_object_name = 'peran_list'
    full_template_name = 'users/peran_list.html'
    partial_template_name = 'users/partials/peran_table_body.html'
    success_url_name = 'users:peran_list'
    search_fields = ['nama']
    table_body_id = 'peran-table-body'


class PeranCreateView(UserManagementMixin, BaseCreateView):
    model = Peran
    fields = ['nama']
    success_url_name = 'users:peran_list'


class PeranUpdateView(UserManagementMixin, BaseUpdateView):
    model = Peran
    fields = ['nama']
    success_url_name = 'users:peran_list'


class PeranDeleteView(UserManagementMixin, LoginRequiredMixin, DeleteView):
    model = Peran
    template_name = 'users/peran_confirm_delete.html'
    success_url = reverse_lazy('users:peran_list')

    def get_template_names(self):
        if self.request.htmx:
            return ['users/partials/peran_delete_modal.html']
        return ['users/peran_confirm_delete.html']


class SiswaListView(ViewOnlyMixin, BaseListView):
    """ListView untuk manajemen data siswa - All can view"""
    model = Siswa
    required_permission = 'view'
    model_name = 'siswa'
    full_template_name = 'users/siswa_list.html'
    partial_template_name = 'users/partials/siswa_table_body.html'
    context_object_name = 'siswa_list'
    success_url_name = 'users:siswa_list'
    search_fields = ['first_name', 'last_name', 'nis', 'akun__email']
    table_body_id = 'siswa-table-body'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('akun').order_by('first_name', 'last_name')


class GuruListView(ViewOnlyMixin, BaseListView):
    """ListView untuk manajemen data guru - All can view"""
    model = Guru
    required_permission = 'view'
    model_name = 'guru'
    full_template_name = 'users/guru_list.html'
    partial_template_name = 'users/partials/guru_table_body.html'
    context_object_name = 'guru_list'
    success_url_name = 'users:guru_list'
    search_fields = ['first_name', 'last_name', 'nip', 'jabatan', 'akun__email']
    table_body_id = 'guru-table-body'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('akun').order_by('first_name', 'last_name')


class SiswaDetailView(UserManagementMixin, LoginRequiredMixin, DetailView):
    """DetailView for Siswa - All authenticated users can view"""
    model = Siswa
    template_name = 'users/siswa_detail.html'
    context_object_name = 'siswa'

    def get_queryset(self):
        return Siswa.objects.select_related('akun').all()


# CRUD Views untuk Siswa (Admin only)
class SiswaCreateView(UserManagementMixin, BaseCreateView):
    """CreateView for Siswa - Admin only"""
    model = Siswa
    form_class = SiswaForm
    success_url_name = 'users:siswa_list'


class SiswaUpdateView(UserManagementMixin, BaseUpdateView):
    """UpdateView for Siswa - Admin only"""
    model = Siswa
    form_class = SiswaForm
    success_url_name = 'users:siswa_list'

    def form_valid(self, form):
        self.object = form.save()
        context = self.get_context_data(form=form)
        context['success_message'] = "Data siswa berhasil diperbarui."
        return TemplateResponse(self.request, self.get_template_names(), context)


class SiswaDeleteView(UserManagementMixin, LoginRequiredMixin, DeleteView):
    """DeleteView for Siswa - Admin only"""
    model = Siswa
    template_name = 'users/siswa_confirm_delete.html'
    success_url = reverse_lazy('users:siswa_list')

    def get_template_names(self):
        if self.request.htmx:
            return ['users/partials/siswa_delete_modal.html']
        return ['users/siswa_confirm_delete.html']


# CRUD Views untuk Guru (Admin only)
class GuruDetailView(UserManagementMixin, LoginRequiredMixin, DetailView):
    """DetailView for Guru - All authenticated users can view"""
    model = Guru
    template_name = 'users/guru_detail.html'
    context_object_name = 'guru'

    def get_queryset(self):
        return Guru.objects.select_related('akun').all()


class GuruCreateView(UserManagementMixin, BaseCreateView):
    """CreateView for Guru - Admin only"""
    model = Guru
    form_class = GuruForm
    success_url_name = 'users:guru_list'


class GuruUpdateView(UserManagementMixin, BaseUpdateView):
    """UpdateView for Guru - Admin only"""
    model = Guru
    form_class = GuruForm
    success_url_name = 'users:guru_list'

    def form_valid(self, form):
        self.object = form.save()
        context = self.get_context_data(form=form)
        context['success_message'] = "Data guru berhasil diperbarui."
        return TemplateResponse(self.request, self.get_template_names(), context)


class GuruDeleteView(UserManagementMixin, LoginRequiredMixin, DeleteView):
    """DeleteView for Guru - Admin only"""
    model = Guru
    template_name = 'users/guru_confirm_delete.html'
    success_url = reverse_lazy('users:guru_list')

    def get_template_names(self):
        if self.request.htmx:
            return ['users/partials/guru_delete_modal.html']
        return ['users/guru_confirm_delete.html']


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('core:dashboard')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ubah Password'
        return context
    
    def form_valid(self, form):
        # Add a success message if you have a message framework set up, 
        # or pass it to the template via session or URL params if needed.
        # For now, just redirect.
        return super().form_valid(form)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'users/profile_update.html'
    success_url = reverse_lazy('core:dashboard')

    def get_object(self):
        user = self.request.user
        if hasattr(user, 'siswa_profile'):
            return user.siswa_profile
        elif hasattr(user, 'guru_profile'):
            return user.guru_profile
        return user

    def get_form_class(self):
        user = self.request.user
        if hasattr(user, 'siswa_profile'):
            return SiswaProfileForm
        elif hasattr(user, 'guru_profile'):
            return GuruProfileForm
        return SelfAkunChangeForm # Fallback for admin/staff without profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Pengaturan Akun'
        return context

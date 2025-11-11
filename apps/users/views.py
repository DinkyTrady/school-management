from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Permission
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from apps.core.views import BaseCreateView, BaseListView, BaseUpdateView

from .forms import AkunChangeForm, AkunCreationForm
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


class AkunListView(BaseListView):
    model = Akun
    permission_required = 'users.view_akun'
    context_object_name = 'akun_list'
    full_template_name = 'users/akun_list.html'
    partial_template_name = 'users/partials/akun_table_body.html'
    success_url_name = 'users:akun_list'
    search_fields = ['email', 'peran__nama']
    table_body_id = 'akun-table-body'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('peran').all().order_by('id')


class AkunCreateView(BaseCreateView):
    model = Akun
    form_class = AkunCreationForm
    success_url_name = 'users:akun_list'
    permission_required = 'users.add_akun'


class AkunDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Akun
    template_name = 'users/akun_detail.html'
    context_object_name = 'akun'
    permission_required = 'users.view_akun'

    def get_queryset(self):
        return Akun.objects.select_related('peran').all()


class AkunUpdateView(BaseUpdateView):
    model = Akun
    form_class = AkunChangeForm
    success_url_name = 'users:akun_list'
    permission_required = 'users.change_akun'

    def form_valid(self, form):
        self.object = form.save()
        context = self.get_context_data(form=form)
        context['success_message'] = "Akun Berhasil diperbarui."
        return TemplateResponse(self.request, self.get_template_names(), context)


class AkunDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Akun
    template_name = 'users/akun_confirm_delete.html'
    success_url = reverse_lazy('users:akun_list')
    permission_required = 'users.delete_akun'

    def get_template_names(self):
        if self.request.htmx:
            return ['users/partials/akun_delete_modal.html']
        return ['users/akun_confirm_delete.html']


# -- Views peran
class PeranListView(BaseListView):
    model = Peran
    permission_required = 'users.view_peran'
    context_object_name = 'peran_list'
    full_template_name = 'users/peran_list.html'
    partial_template_name = 'users/partials/peran_table_body.html'
    success_url_name = 'users:peran_list'
    search_fields = ['nama']
    table_body_id = 'peran-table-body'


class PeranCreateView(BaseCreateView):
    model = Peran
    fields = ['nama']
    success_url_name = 'users:peran_list'
    permission_required = 'users.add_peran'


class PeranUpdateView(BaseUpdateView):
    model = Peran
    fields = ['nama']
    success_url_name = 'users:peran_list'
    permission_required = 'users.change_peran'


class PeranDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Peran
    template_name = 'users/peran_confirm_delete.html'
    success_url = reverse_lazy('users:peran_list')
    permission_required = 'users.delete_peran'

    def get_template_names(self):
        if self.request.htmx:
            return ['users/partials/peran_delete_modal.html']
        return ['users/peran_confirm_delete.html']


class SiswaListView(BaseListView):
    """ListView untuk manajemen data siswa"""
    model = Siswa
    permission_required = ['users.view_siswa']
    full_template_name = 'users/siswa_list.html'
    partial_template_name = 'users/partials/siswa_table_body.html'
    context_object_name = 'siswa_list'
    success_url_name = 'users:siswa_list'
    search_fields = ['first_name', 'last_name', 'nis', 'akun__email']
    table_body_id = 'siswa-table-body'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('akun').order_by('first_name', 'last_name')


class GuruListView(BaseListView):
    """ListView untuk manajemen data guru"""
    model = Guru
    permission_required = ['users.view_guru']
    full_template_name = 'users/guru_list.html'
    partial_template_name = 'users/partials/guru_table_body.html'
    context_object_name = 'guru_list'
    success_url_name = 'users:guru_list'
    search_fields = ['first_name', 'last_name', 'nip', 'jabatan', 'akun__email']
    table_body_id = 'guru-table-body'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('akun').order_by('first_name', 'last_name')

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import AkunChangeForm, AkunCreationForm, AkunPermissionForm
from .models import Akun as AkunType, Peran

Akun: AkunType = get_user_model()


class AkunListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Akun
    template_name = 'users/akun_list.html'
    context_object_name = 'akun_list'
    permission_required = 'users.view_akun'

    def get_queryset(self):
        queryset = Akun.objects.select_related('peran').all()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(email__icontains=query)
        return queryset

    def get_template_names(self):
        return ['users/akun_list.html']


class AkunCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Akun
    form_class = AkunCreationForm
    template_name = 'users/akun_form.html'
    success_url = reverse_lazy('users:akun_list')
    permission_required = 'users.add_akun'

    def form_valid(self, form):
        response = super().form_valid(form) # Call super to save the object
        return response


class AkunDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Akun
    template_name = 'users/akun_detail.html'
    context_object_name = 'akun'
    permission_required = 'users.view_akun'

    def get_queryset(self):
        return Akun.objects.select_related('peran').all()


class AkunUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Akun
    form_class = AkunChangeForm
    template_name = 'users/akun_form.html'
    success_url = reverse_lazy('users:akun_list')
    permission_required = 'users.change_akun'

    def form_valid(self, form):
        response = super().form_valid(form) # Call super to save the object
        return response

    def get_queryset(self):
        return Akun.objects.select_related('peran').all()


class AkunDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Akun
    template_name = 'users/akun_confirm_delete.html'
    success_url = reverse_lazy('users:akun_list')
    permission_required = 'users.delete_akun'

    def get_template_names(self):
        if self.request.htmx:
            return ['users/partials/akun_delete_modal.html']
        return ['users/akun_confirm_delete.html']


class AkunPermissionView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Akun
    form_class = AkunPermissionForm
    template_name = 'users/akun_permissions.html'
    success_url = reverse_lazy('users:akun_list')
    permission_required = 'auth.change_permission'

    def get_queryset(self):
        return (
            Akun.objects.prefetch_related('user_permissions', 'groups')
            .select_related('peran')
            .all()
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

    def form_valid(self, form):
        return super().form_valid(form)

# -- Views peran
class PeranListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Peran
    template_name = 'users/peran_list.html'
    context_object_name = 'peran_list'
    permission_required = 'users.view_peran'

    def get_queryset(self):
        queryset = Peran.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(nama__icontains=query)
        return queryset

    def get_template_names(self):
        if self.request.htmx:
            return ['users/partials/peran_table_body.html']
        return ['users/peran_list.html']

class PeranCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Peran
    fields = ['nama']
    template_name = 'users/peran_form.html'
    success_url = reverse_lazy('users:peran_list')
    permission_required = 'users.add_peran'

    def form_valid(self, form):
        response = super().form_valid(form)
        # django-htmx middleware will automatically convert HttpResponseRedirect to HX-Redirect
        return response

class PeranUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Peran
    fields = ['nama']
    template_name = 'users/peran_form.html'
    success_url = reverse_lazy('users:peran_list')
    permission_required = 'users.change_peran'

    def form_valid(self, form):
        response = super().form_valid(form)
        # django-htmx middleware will automatically convert HttpResponseRedirect to HX-Redirect
        return response

class PeranDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Peran
    template_name = 'users/peran_confirm_delete.html'
    success_url = reverse_lazy('users:peran_list')
    permission_required = 'users.delete_peran'

    def get_template_names(self):
        if self.request.htmx:
            return ['users/partials/peran_delete_modal.html']
        return ['users/peran_confirm_delete.html']

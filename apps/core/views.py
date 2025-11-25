from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q
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

from apps.users.models import Peran
from apps.academics.models import Kelas, Mapel

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

        return context

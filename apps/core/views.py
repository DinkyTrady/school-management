import json
import logging
from datetime import timedelta
from django.shortcuts import render

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.users.models import Peran
from apps.academics.models import Kelas, Mapel

User = get_user_model()
logger = logging.getLogger(__name__)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['is_admin'] = user.is_superuser
        context['is_guru'] = user.is_guru

        # Hanya hitung dan tambahkan data ini jika pengguna adalah admin
        if user.is_superuser:
            # Cukup ambil data untuk kartu ringkasan
            context['total_akun'] = User.objects.count()
            context['total_peran'] = Peran.objects.count()
            context['total_kelas'] = Kelas.objects.count()
            context['total_mapel'] = Mapel.objects.count()

        return context

from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

from apps.users.models import Peran
from apps.academics.models import Kelas, Mapel

User = get_user_model()


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['is_admin'] = user.is_admin
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

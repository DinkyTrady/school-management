# apps/academics/urls.py
from django.urls import path
from . import views

app_name = 'academics'

urlpatterns = [
    # Kelas Management
    path('kelas/', views.KelasListView.as_view(), name='kelas_list'),
    
    # Tahun Ajaran Management
    path('tahun-ajaran/', views.TahunAjaranListView.as_view(), name='tahun_ajaran_list'),
    
    # Jurusan Management  
    path('jurusan/', views.JurusanListView.as_view(), name='jurusan_list'),
    
    # Mata Pelajaran Management
    path('mapel/', views.MapelListView.as_view(), name='mapel_list'),
    
    # Jadwal Management
    path('jadwal/', views.JadwalListView.as_view(), name='jadwal_list'),
    
    # Tambahkan URL CRUD lainnya di sini nanti (Create, Update, Delete)
    # path('kelas/tambah/', views.KelasCreateView.as_view(), name='kelas_create'),
    # path('kelas/<int:pk>/update/', views.KelasUpdateView.as_view(), name='kelas_update'),
]

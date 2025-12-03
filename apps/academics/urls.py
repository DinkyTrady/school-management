# apps/academics/urls.py
from django.urls import path
from . import views

app_name = 'academics'

urlpatterns = [
    # Kelas Management - Full CRUD for Admin
    path('kelas/', views.KelasListView.as_view(), name='kelas_list'),
    path('kelas/add/', views.KelasCreateView.as_view(), name='kelas_add'),
    path('kelas/<int:pk>/edit/', views.KelasUpdateView.as_view(), name='kelas_edit'),
    path('kelas/<int:pk>/delete/', views.KelasDeleteView.as_view(), name='kelas_delete'),
    
    # Tahun Ajaran Management - Full CRUD for Admin
    path('tahun-ajaran/', views.TahunAjaranListView.as_view(), name='tahun_ajaran_list'),
    path('tahun-ajaran/add/', views.TahunAjaranCreateView.as_view(), name='tahun_ajaran_add'),
    path('tahun-ajaran/<int:pk>/', views.TahunAjaranDetailView.as_view(), name='tahun_ajaran_detail'),
    path('tahun-ajaran/<int:pk>/edit/', views.TahunAjaranUpdateView.as_view(), name='tahun_ajaran_edit'),
    path('tahun-ajaran/<int:pk>/delete/', views.TahunAjaranDeleteView.as_view(), name='tahun_ajaran_delete'),
    
    # Jurusan Management - Full CRUD for Admin
    path('jurusan/', views.JurusanListView.as_view(), name='jurusan_list'),
    path('jurusan/add/', views.JurusanCreateView.as_view(), name='jurusan_add'),
    path('jurusan/<int:pk>/', views.JurusanDetailView.as_view(), name='jurusan_detail'),
    path('jurusan/<int:pk>/edit/', views.JurusanUpdateView.as_view(), name='jurusan_edit'),
    path('jurusan/<int:pk>/delete/', views.JurusanDeleteView.as_view(), name='jurusan_delete'),
    
    # Mata Pelajaran Management - Full CRUD for Admin
    path('mapel/', views.MapelListView.as_view(), name='mapel_list'),
    path('mapel/add/', views.MapelCreateView.as_view(), name='mapel_add'),
    path('mapel/<int:pk>/', views.MapelDetailView.as_view(), name='mapel_detail'),
    path('mapel/<int:pk>/edit/', views.MapelUpdateView.as_view(), name='mapel_edit'),
    path('mapel/<int:pk>/delete/', views.MapelDeleteView.as_view(), name='mapel_delete'),
    
    # Jadwal Management - Full CRUD for Admin
    path('jadwal/', views.JadwalListView.as_view(), name='jadwal_list'),
    path('jadwal/add/', views.JadwalCreateView.as_view(), name='jadwal_add'),
    path('jadwal/<int:pk>/edit/', views.JadwalUpdateView.as_view(), name='jadwal_edit'),
    path('jadwal/<int:pk>/delete/', views.JadwalDeleteView.as_view(), name='jadwal_delete'),
]

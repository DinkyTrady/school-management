# apps/grades/urls.py
from django.urls import path
from . import views

app_name = 'grades'

urlpatterns = [
    # Tugas Management - Full CRUD for Guru and Admin
    path('tugas/', views.TugasListView.as_view(), name='tugas_list'),
    path('tugas/<int:pk>/', views.TugasDetailView.as_view(), name='tugas_detail'),
    path('tugas/add/', views.TugasCreateView.as_view(), name='tugas_add'),
    path('tugas/<int:pk>/edit/', views.TugasUpdateView.as_view(), name='tugas_edit'),
    path('tugas/<int:pk>/delete/', views.TugasDeleteView.as_view(), name='tugas_delete'),
    
    # Nilai Management - Full CRUD for Guru and Admin
    path('nilai/', views.NilaiListView.as_view(), name='nilai_list'),
    path('nilai/<int:pk>/', views.NilaiDetailView.as_view(), name='nilai_detail'),
    path('nilai/add/', views.NilaiCreateView.as_view(), name='nilai_add'),
    path('nilai/<int:pk>/edit/', views.NilaiUpdateView.as_view(), name='nilai_edit'),
    path('nilai/<int:pk>/delete/', views.NilaiDeleteView.as_view(), name='nilai_delete'),
    
    # Presensi Management - Full CRUD for Guru and Admin
    path('presensi/', views.PresensiListView.as_view(), name='presensi_list'),
    path('presensi/<int:pk>/', views.PresensiDetailView.as_view(), name='presensi_detail'),
    path('presensi/add/', views.PresensiCreateView.as_view(), name='presensi_add'),
    path('presensi/<int:pk>/edit/', views.PresensiUpdateView.as_view(), name='presensi_edit'),
    path('presensi/<int:pk>/delete/', views.PresensiDeleteView.as_view(), name='presensi_delete'),
    
    # Bulk Absensi from Jadwal
    path('jadwal/<int:jadwal_id>/absensi/', views.JadwalAbsensiView.as_view(), name='jadwal_absensi'),
]
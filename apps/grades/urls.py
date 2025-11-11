# apps/grades/urls.py
from django.urls import path
from . import views

app_name = 'grades'

urlpatterns = [
    # Tugas Management
    path('tugas/', views.TugasListView.as_view(), name='tugas_list'),
    
    # Nilai Management
    path('nilai/', views.NilaiListView.as_view(), name='nilai_list'),
    
    # Presensi Management
    path('presensi/', views.PresensiListView.as_view(), name='presensi_list'),
]
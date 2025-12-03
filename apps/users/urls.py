from django.urls import include, path

from . import views

app_name = 'users'

urlpatterns = [
    # URL untuk otentikasi Django (login, logout, dll.)
    path('auth/', include('django.contrib.auth.urls')),
    # CRUD untuk Akun
    path('akun/', views.AkunListView.as_view(), name='akun_list'),
    path('akun/add/', views.AkunCreateView.as_view(), name='akun_add'),
    path('akun/<int:pk>/', views.AkunDetailView.as_view(), name='akun_detail'),
    path('akun/<int:pk>/edit/', views.AkunUpdateView.as_view(), name='akun_edit'),
    path('akun/<int:pk>/delete/', views.AkunDeleteView.as_view(), name='akun_delete'),
    # CRUD untuk Peran (Roles)
    path('roles/', views.PeranListView.as_view(), name='peran_list'),
    path('roles/add/', views.PeranCreateView.as_view(), name='peran_add'),
    path('roles/<int:pk>/edit/', views.PeranUpdateView.as_view(), name='peran_edit'),
    path('search-permissions/', views.search_permissions, name='search_permissions'),
    path(
        'roles/<int:pk>/delete/', views.PeranDeleteView.as_view(), name='peran_delete'
    ),
    # Siswa Management - Full CRUD for Admin
    path('siswa/', views.SiswaListView.as_view(), name='siswa_list'),
    path('siswa/add/', views.SiswaCreateView.as_view(), name='siswa_add'),
    path('siswa/<int:pk>/', views.SiswaDetailView.as_view(), name='siswa_detail'),
    path('siswa/<int:pk>/edit/', views.SiswaUpdateView.as_view(), name='siswa_edit'),
    path('siswa/<int:pk>/delete/', views.SiswaDeleteView.as_view(), name='siswa_delete'),
    
    # Guru Management - Full CRUD for Admin
    path('guru/', views.GuruListView.as_view(), name='guru_list'),
    path('guru/add/', views.GuruCreateView.as_view(), name='guru_add'),
    path('guru/<int:pk>/', views.GuruDetailView.as_view(), name='guru_detail'),
    path('guru/<int:pk>/edit/', views.GuruUpdateView.as_view(), name='guru_edit'),
    path('guru/<int:pk>/delete/', views.GuruDeleteView.as_view(), name='guru_delete'),
]

htmx_urlpatterns = [
    # path('accounts/check_username/', views.check_email, name='check_username')
]

urlpatterns += htmx_urlpatterns

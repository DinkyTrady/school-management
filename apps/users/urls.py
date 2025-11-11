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
    # Siswa Management
    path('siswa/', views.SiswaListView.as_view(), name='siswa_list'),
    
    # Guru Management
    path('guru/', views.GuruListView.as_view(), name='guru_list'),
]

htmx_urlpatterns = [
    # path('accounts/check_username/', views.check_email, name='check_username')
]

urlpatterns += htmx_urlpatterns

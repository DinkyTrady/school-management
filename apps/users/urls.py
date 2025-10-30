from django.urls import include, path

from . import views

app_name = 'users'

urlpatterns = [
    # URL untuk otentikasi Django (login, logout, dll.)
    path('auth/', include('django.contrib.auth.urls')),
    # CRUD untuk Akun
    path('', views.AkunListView.as_view(), name='akun_list'),
    path('add/', views.AkunCreateView.as_view(), name='akun_add'),
    path('<int:pk>/detail/', views.AkunDetailView.as_view(), name='akun_detail'),
    path('<int:pk>/edit/', views.AkunUpdateView.as_view(), name='akun_edit'),
    path('<int:pk>/delete/', views.AkunDeleteView.as_view(), name='akun_delete'),
    path(
        '<int:pk>/permissions/',
        views.AkunPermissionView.as_view(),
        name='akun_permissions',
    ),
    # CRUD untuk Peran (Roles)
    path('roles/', views.PeranListView.as_view(), name='peran_list'),
    path('roles/add/', views.PeranCreateView.as_view(), name='peran_add'),
    path('roles/<int:pk>/edit/', views.PeranUpdateView.as_view(), name='peran_edit'),
    path(
        'roles/<int:pk>/delete/', views.PeranDeleteView.as_view(), name='peran_delete'
    ),
]

htmx_urlpatterns = [
    # path('accounts/check_username/', views.check_email, name='check_username')
]

urlpatterns += htmx_urlpatterns

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.IntroPageView.as_view(), name='intro'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('permission-test/', views.PermissionTestView.as_view(), name='permission_test'),
]

# apps/academics/urls.py
from django.urls import path
from . import views

app_name = 'academics'

urlpatterns = [
    # URL untuk halaman penuh
    path('kelas/', views.KelasListView.as_view(), name='kelas_list'),
    
    # URL untuk endpoint HTMX
    path('htmx/search-kelas/', views.htmx_search_kelas, name='htmx_search_kelas'),
    
    # Tambahkan URL CRUD lainnya di sini nanti (Create, Update, Delete)
    # path('kelas/tambah/', views.KelasCreateView.as_view(), name='kelas_create'),
    # path('kelas/<int:pk>/update/', views.KelasUpdateView.as_view(), name='kelas_update'),
]

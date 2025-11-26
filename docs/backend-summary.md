# SIGMA - Backend Summary & View Documentation

## 1. URL Configuration Overview

**Root URLconf**: `config/urls.py`

```python
urlpatterns = [
    path('', include('apps.core.urls')),              # /
    path('admin/', admin.site.urls),                  # /admin/
    path('users/', include('apps.users.urls')),       # /users/*
    path('academics/', include('apps.academics.urls')),  # /academics/*
    path('grades/', include('apps.grades.urls')),     # /grades/*
]
```

---

## 2. Core App Views & URLs

**Module**: `apps/core/`

| URL | View | Method(s) | Auth Required | Purpose |
|-----|------|-----------|---------------|---------|
| `/` | `IntroPageView` | GET | No | Landing/intro page; redirects to dashboard if authenticated |
| `/dashboard/` | `DashboardView` | GET | Yes (LoginRequiredMixin) | Admin dashboard showing summary stats (total accounts, roles, classes, subjects) |

### **2.1 IntroPageView**
```python
class IntroPageView(TemplateView):
    template_name = 'core/intro.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:dashboard')
        return super().dispatch(request, *args, **kwargs)
```
- Accessible to anyone
- Redirects authenticated users to dashboard
- Renders `intro.html` with project info

### **2.2 DashboardView**
```python
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'
    
    def get_context_data(self, **kwargs):
        # Adds to context:
        # - is_admin, is_guru (user role checks)
        # - card URLs for akun, peran, kelas lists
        # - total_akun, total_peran, total_kelas, total_mapel (if superuser)
```
- Protected: only authenticated users
- Shows different dashboard based on role
- Admin sees summary cards with counts
- Context variables: `is_admin`, `is_guru`, `card_*_url`, `total_*` counts

---

## 3. Base Mixins (Core App)

**Module**: `apps/core/views.py`

### **3.1 BaseCrudMixin**
Provides foundation for all CRUD views:
- **LoginRequiredMixin**: Enforces authentication
- **PermissionRequiredMixin**: Enforces Django permissions
- **HTMX Detection**: Checks `request.htmx` and returns appropriate template
- **Search Filtering**: Implements `?q=` query parameter searching
- **URL Resolution**: Sets `success_url` and `full/partial_template_name`

**Required Attributes**:
```python
class MyListView(BaseCrudMixin, ListView):
    model = MyModel
    permission_required = 'app.view_model'
    search_fields = ['name', 'description']  # Fields to search on
    full_template_name = 'app/model_list.html'
    partial_template_name = 'app/partials/model_table_body.html'
    success_url_name = 'app:model_list'  # URL name for redirect
    table_body_id = 'model-table-body'  # HTML ID for HTMX swapping
```

**Key Methods**:
- `get_success_url()`: Resolves `success_url_name` to actual URL
- `get_queryset()`: Applies search filtering if `?q=` present
- `get_template_names()`: Returns partial or full template based on `request.htmx`

### **3.2 BaseListView**
Extends `BaseCrudMixin + ListView`:
- Pagination: `paginate_by = 10`
- Renders pagination controls via HTMX
- Inserts pagination HTML out-of-band using `hx-swap-oob="true"`

**Context**:
- `object_list` / `<model>_list`: Paginated queryset
- `page_obj`: Pagination object
- `paginator`: Django paginator
- `table_body_id`: For HTMX swapping
- `pagination`: Out-of-band pagination HTML (if HTMX request)

### **3.3 BaseCreateView / BaseUpdateView / BaseDeleteView**
Generic CRUD views with:
- Form rendering (full page or partial)
- HTMX support
- Success messages

---

## 4. Users App Views

**Module**: `apps/users/views.py`  
**URLs**: `apps/users/urls.py`

### **4.1 Account Management Views**

| View | URL | Methods | Permissions | Description |
|------|-----|---------|-------------|-------------|
| AkunListView | `/users/akun/` | GET | users.view_akun | List accounts with search/pagination |
| AkunCreateView | `/users/akun/add/` | GET, POST | users.add_akun | Create new account with email + password |
| AkunDetailView | `/users/akun/<int:pk>/` | GET | users.view_akun | Read-only account details |
| AkunUpdateView | `/users/akun/<int:pk>/edit/` | GET, POST | users.change_akun | Edit account (role, permissions, staff status) |
| AkunDeleteView | `/users/akun/<int:pk>/delete/` | GET, POST | users.delete_akun | Delete account (with confirmation) |

**AkunListView Details**:
```python
class AkunListView(BaseListView):
    model = Akun
    permission_required = 'users.view_akun'
    search_fields = ['email', 'peran__nama']
    table_body_id = 'akun-table-body'
    
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('peran').all().order_by('id')
```
- Search by email or role name
- Uses `select_related('peran')` to avoid N+1
- Returns table rows or full page based on HTMX

**AkunCreateView Details**:
```python
class AkunCreateView(BaseCreateView):
    model = Akun
    form_class = AkunCreationForm
    permission_required = 'users.add_akun'
```
- Uses `AkunCreationForm`: requires email, password, password confirmation
- Optionally assign groups and specific permissions
- Returns form or form-only HTML (HTMX)

**AkunUpdateView Details**:
```python
class AkunUpdateView(BaseUpdateView):
    model = Akun
    form_class = AkunChangeForm
    permission_required = 'users.change_akun'
    
    def form_valid(self, form):
        self.object = form.save()
        context = self.get_context_data(form=form)
        context['success_message'] = "Akun Berhasil diperbarui."
        return TemplateResponse(self.request, self.get_template_names(), context)
```
- Uses `AkunChangeForm`: edits email, role, is_active, is_staff, is_superuser, permissions
- Shows success message after save
- HTMX-compatible partial rendering

### **4.2 Role Management Views**

| View | URL | Permissions | Description |
|------|-----|-------------|-------------|
| PeranListView | `/users/roles/` | users.view_peran | List roles |
| PeranCreateView | `/users/roles/add/` | users.add_peran | Create role |
| PeranUpdateView | `/users/roles/<int:pk>/edit/` | users.change_peran | Edit role name |
| PeranDeleteView | `/users/roles/<int:pk>/delete/` | users.delete_peran | Delete role |

**PeranListView Details**:
```python
class PeranListView(BaseListView):
    model = Peran
    permission_required = 'users.view_peran'
    search_fields = ['nama']
    table_body_id = 'peran-table-body'
```
- Search by role name
- Simple list without relationships (no select_related needed)

### **4.3 Student & Teacher Views**

| View | URL | Permissions | Description |
|------|-----|-------------|-------------|
| SiswaListView | `/users/siswa/` | users.view_siswa | List students with search |
| GuruListView | `/users/guru/` | users.view_guru | List teachers with search |

**SiswaListView Details**:
```python
class SiswaListView(BaseListView):
    model = Siswa
    permission_required = ['users.view_siswa']
    search_fields = ['first_name', 'last_name', 'nis', 'akun__email']
    
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('akun').order_by('first_name', 'last_name')
```
- Search by name, student ID (NIS), or email
- Uses `select_related('akun')` for user info
- Sorted by first name, last name

### **4.4 Utility Function**

**search_permissions()**:
```python
def search_permissions(request):
    query = request.GET.get('q', '')
    permissions = Permission.objects.filter(name__icontains=query)
    
    # Build form and render permission checkboxes as HTML
    # Used for HTMX autocomplete in account/role edit forms
```
- AJAX endpoint for searching Django permissions
- Returns HTML checkboxes for matching permissions
- Used in account/role edit forms for permission picker

---

## 5. Academics App Views

**Module**: `apps/academics/views.py`  
**URLs**: `apps/academics/urls.py`

| View | URL | Permissions | Description |
|------|-----|-------------|-------------|
| KelasListView | `/academics/kelas/` | academics.view_kelas | List classes (active year only) with student count |
| TahunAjaranListView | `/academics/tahun-ajaran/` | academics.view_tahunajar | List academic years |
| JurusanListView | `/academics/jurusan/` | academics.view_jurusan | List majors |
| MapelListView | `/academics/mapel/` | academics.view_mapel | List subjects |
| JadwalListView | `/academics/jadwal/` | academics.view_jadwal | List schedules (filtered per student role) |

**KelasListView Details**:
```python
class KelasListView(BaseListView):
    model = Kelas
    permission_required = ['academics.view_kelas']
    search_fields = ['nama']
    
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(tahun_ajaran__is_active=True)
        qs = qs.select_related('jurusan', 'wali_kelas', 'tahun_ajaran')
        qs = qs.annotate(jumlah_siswa=Count('kelassiswa'))
        return qs.order_by('nama')
```
- **N+1 Optimization**: Uses `select_related()` for ForeignKeys
- **Aggregation**: Counts students per class using `annotate(jumlah_siswa=Count('kelassiswa'))`
- Filters to active academic year only
- Search by class name

**JadwalListView Details**:
```python
class JadwalListView(BaseListView):
    model = Jadwal
    permission_required = ['academics.view_jadwal']
    search_fields = ['kelas__nama', 'mapel__nama', 'guru__first_name', 'guru__last_name']
    
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('kelas', 'mapel', 'guru', 'kelas__tahun_ajaran')
        qs = qs.filter(kelas__tahun_ajaran__is_active=True)
        
        # If user is student, show only their class schedule
        if user.is_siswa:
            siswa_profile = user.siswa_profile
            kelas_siswa = KelasSiswa.objects.filter(
                siswa=siswa_profile,
                tahun_ajaran__is_active=True
            ).select_related('kelas').first()
            
            if kelas_siswa:
                return qs.filter(kelas=kelas_siswa.kelas).order_by('hari', 'jam_mulai')
            return qs.none()
        
        return qs.order_by('hari', 'jam_mulai')
```
- **Role-Based Filtering**: Students see only their class schedule
- **Query Optimization**: Multiple `select_related()` to avoid N+1
- Search by class name, subject name, or teacher name

---

## 6. Grades App Views

**Module**: `apps/grades/views.py`  
**URLs**: `apps/grades/urls.py`

| View | URL | Permissions | Description |
|------|-----|-------------|-------------|
| TugasListView | `/grades/tugas/` | grades.view_tugas | List assignments (filtered per student) |
| NilaiListView | `/grades/nilai/` | grades.view_nilai | List student grades |
| PresensiListView | `/grades/presensi/` | grades.view_presensi | List attendance records |

**TugasListView Details**:
```python
class TugasListView(BaseListView):
    model = Tugas
    permission_required = ['grades.view_tugas']
    search_fields = ['nama', 'deskripsi', 'jadwal__kelas__nama', 'jadwal__mapel__nama']
    
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('jadwal', 'jadwal__kelas', 'jadwal__mapel', 'jadwal__guru',
                              'jadwal__kelas__tahun_ajaran')
        qs = qs.filter(jadwal__kelas__tahun_ajaran__is_active=True).order_by('-tenggat')
        
        if user.is_siswa:
            # Filter to student's classes only
            ...
        return qs
```
- Search by assignment name or class/subject name
- Deep `select_related()` chain for performance
- Sorted by deadline (most recent first)
- Students see only assignments for their classes

**NilaiListView Details**:
```python
class NilaiListView(BaseListView):
    model = Nilai
    permission_required = ['grades.view_nilai']
    search_fields = ['siswa__first_name', 'siswa__last_name', 'siswa__nis',
                     'jadwal__kelas__nama', 'jadwal__mapel__nama', 'tipe_penilaian']
    
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('siswa', 'siswa__akun', 'jadwal', 'jadwal__kelas',
                               'jadwal__mapel', 'jadwal__guru', 'tugas',
                               'jadwal__kelas__tahun_ajaran')
        return qs.filter(jadwal__kelas__tahun_ajaran__is_active=True)\
                 .order_by('-tanggal_penilaian')
```
- Comprehensive `select_related()` for all related objects
- Search by student name/ID, class, subject, or grade type
- Sorted by assessment date (most recent first)

---

## 7. Forms

**Module**: `apps/users/forms.py`

### **AkunCreationForm**
```python
class AkunCreationForm(ModelForm):
    Fields: email, password, password2, peran, groups, user_permissions
    
    - Validates password strength
    - Confirms password match
    - Allows group + permission assignment
    - DaisyUI styling applied to checkboxes
```

### **AkunChangeForm**
```python
class AkunChangeForm(UserChangeForm):
    Fields: email, peran, is_active, is_staff, is_superuser, groups, user_permissions
    
    - Edit existing account details
    - DaisyUI styling for toggles (is_active, is_staff, is_superuser)
    - DaisyUI styling for checkboxes (groups, permissions)
```

---

## 8. Authentication & Permission Flow

```
Request
  ↓
Django Middleware (includes HtmxMiddleware → sets request.htmx)
  ↓
URL Routing
  ↓
View (BaseCrudMixin)
  ├── LoginRequiredMixin.dispatch()
  │   └─ Redirects unauthenticated to LOGIN_URL (/users/auth/login/)
  ├── PermissionRequiredMixin.check_perms()
  │   └─ Checks user has `permission_required`
  │      If not: raises PermissionDenied → 403 Forbidden
  └─ View.dispatch() → get() / post()
       └─ get_template_names()
           ├─ If request.htmx: return partial_template_name
           └─ Else: return full_template_name
       ↓
Response (HTML or HTMX partial)
```

**Permissions Required** (Django admin-configured):
- `app.view_model`: Can view list/detail
- `app.add_model`: Can create
- `app.change_model`: Can edit
- `app.delete_model`: Can delete

**Custom Checks** (in view logic):
- `user.is_siswa`: Based on role assignment
- `user.is_guru`: Based on role assignment
- Students filtered to own data (class schedule, grades, assignments)

---

## 9. HTMX Integration Details

**How HTMX Works**:
1. User clicks search button or types in search box
2. HTMX sends GET request to `/users/akun/?q=search_term`
3. View detects `request.htmx = True` (set by HtmxMiddleware)
4. `get_template_names()` returns `partial_template_name` (table body only)
5. HTMX swaps only table body, leaving page structure intact

**HTMX Attributes Used**:
```html
<!-- Search input -->
<input hx-get="/users/akun/" hx-trigger="keyup changed delay:500ms" hx-target="#akun-table-body" />

<!-- Pagination link -->
<a hx-get="/users/akun/?page=2" hx-target="#akun-table-body" hx-swap="innerHTML">Next</a>

<!-- Out-of-band swap for pagination -->
<div id="pagination-container" hx-swap-oob="true">...</div>
```

**Partial Templates**:
- `_akun_table_body.html`: Just `<tr>` elements (no surrounding `<table>` tag)
- `_paginate.html`: Pagination controls only
- `_form_content.html`: Form fields only (no `<form>` tag)

---

## 10. Template-View-Model Mapping

| Template | View | Model | Purpose |
|----------|------|-------|---------|
| `akun_list.html` | AkunListView | Akun | Full page: list accounts |
| `akun_detail.html` | AkunDetailView | Akun | Full page: read-only account |
| `akun_permissions.html` | AkunUpdateView | Akun | Full page: manage permissions |
| `peran_list.html` | PeranListView | Peran | Full page: list roles |
| `siswa_list.html` | SiswaListView | Siswa | Full page: list students |
| `guru_list.html` | GuruListView | Guru | Full page: list teachers |
| `kelas_list.html` | KelasListView | Kelas | Full page: list classes with student count |
| `jadwal_list.html` | JadwalListView | Jadwal | Full page: list schedules |
| `tugas_list.html` | TugasListView | Tugas | Full page: list assignments |
| `nilai_list.html` | NilaiListView | Nilai | Full page: list grades |
| `presensi_list.html` | PresensiListView | Presensi | Full page: list attendance |

---

## 11. Query Performance Checklist

| View | Optimization | Status |
|------|---------------|--------|
| AkunListView | `select_related('peran')` | ✅ |
| SiswaListView | `select_related('akun')` | ✅ |
| GuruListView | `select_related('akun')` | ✅ |
| KelasListView | `select_related('jurusan', 'wali_kelas', 'tahun_ajaran')` + `annotate(Count)` | ✅ |
| JadwalListView | Multiple `select_related()` chain | ✅ |
| TugasListView | Multiple `select_related()` chain | ✅ |
| NilaiListView | Multiple `select_related()` chain | ✅ |
| PresensiListView | Multiple `select_related()` chain | ✅ |

---

## 12. Recommended Further Improvements

⚠️ **Missing CRUD for Academic/Grade Models**:
- No CreateView, UpdateView, DeleteView for Kelas, Jadwal, Tugas, Nilai, Presensi
- Currently only ListView available
- Recommendation: Extend with form-based creation/editing views

⚠️ **Missing Bulk Operations**:
- No bulk edit/delete for grades
- No import/export for attendance

⚠️ **No API Endpoints**:
- Only HTML views, no REST API
- Recommendation: Add Django REST Framework if external integrations needed

⚠️ **No Async Tasks**:
- Large grade imports/reports run synchronously
- Recommendation: Add Celery for background processing

---

**End of Backend Summary**

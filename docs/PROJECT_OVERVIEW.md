# SIGMA - Project Overview & Architecture

## 1. Project Description

**SIGMA** (School Information Gateway Management Application) adalah sistem informasi manajemen sekolah yang dirancang untuk mengelola seluruh aspek operasional sekolah secara digital dan terintegrasi. Sistem ini mencakup:

- **User Management**: Manajemen akun pengguna dengan sistem role-based access control (RBAC)
- **Academic Management**: Kelola tahun ajaran, jurusan, kelas, mata pelajaran, dan jadwal pelajaran
- **Grade Management**: Pencatatan tugas, nilai siswa, dan presensi
- **Dashboard**: Ringkasan data untuk admin, guru, dan siswa

Aplikasi menggunakan teknologi modern dengan Django 5.2, Tailwind CSS, dan HTMX untuk memberikan pengalaman pengguna yang responsif dan interaktif tanpa perlu reload halaman.

---

## 2. Technology Stack Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      CLIENT LAYER                            │
│  (Browser: HTML + Tailwind CSS + DaisyUI + HTMX + Alpine)   │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP/HTTPS
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    DJANGO WEB LAYER                          │
│  ┌──────────────────────────────────────────────────────────┤
│  │ MIDDLEWARE STACK                                          │
│  │ - SecurityMiddleware                                      │
│  │ - SessionMiddleware                                       │
│  │ - AuthenticationMiddleware                                │
│  │ - HtmxMiddleware                                          │
│  │ - CsrfViewMiddleware                                      │
│  │ - BrowserReloadMiddleware (dev only)                      │
│  └──────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────────┤
│  │ URL ROUTING (config/urls.py)                             │
│  │ ├── /                       → core.IntroPageView         │
│  │ ├── /dashboard/             → core.DashboardView        │
│  │ ├── /users/                 → users app (auth, CRUD)     │
│  │ ├── /academics/             → academics app (CRUD)       │
│  │ └── /grades/                → grades app (CRUD)          │
│  └──────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────────┤
│  │ VIEW LAYER (Generic Class-Based Views)                   │
│  │ ├── BaseCrudMixin (auth + permission checking)           │
│  │ ├── BaseListView (with HTMX partial support)             │
│  │ ├── BaseCreateView / BaseUpdateView / BaseDeleteView     │
│  │ └── Concrete views (AkunListView, KelasListView, etc.)   │
│  └──────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────────┤
│  │ FORM LAYER (Django Forms + DaisyUI)                      │
│  │ ├── AkunCreationForm / AkunChangeForm                    │
│  │ └── Auto-rendered with DaisyUI classes                   │
│  └──────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────────┤
│  │ TEMPLATE LAYER (Django Templates)                        │
│  │ ├── base.html (Tailwind + HTMX + Alpine.js setup)       │
│  │ ├── app-specific templates (akun_list, jadwal_list, etc.)│
│  │ └── Partials (_form_content, _paginate, _search_input)   │
│  └──────────────────────────────────────────────────────────┤
└────────────────┬─────────────────────────────────────────────┘
                 │ ORM + SQL
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                   MODEL LAYER (ORM)                          │
│  ┌──────────────────────────────────────────────────────────┤
│  │ ABSTRACT MODELS                                           │
│  │ └── Person (first_name, last_name, gender, etc.)         │
│  └──────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────────┤
│  │ AUTH MODELS (apps/users)                                 │
│  │ ├── Akun (Custom AbstractBaseUser, email-based)          │
│  │ ├── Peran (Roles: Admin, Guru, Siswa, etc.)              │
│  │ ├── Siswa (extends Person + OneToOne → Akun)             │
│  │ ├── Guru (extends Person + OneToOne → Akun)              │
│  │ ├── Wali (extends Person, no Akun)                       │
│  │ └── SiswaWali (M2M: Siswa ↔ Wali)                        │
│  └──────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────────┤
│  │ ACADEMIC MODELS (apps/academics)                         │
│  │ ├── TahunAjaran (School year + semester)                 │
│  │ ├── Jurusan (Majors)                                     │
│  │ ├── Kelas (Class: FK Jurusan, Guru, TahunAjaran)        │
│  │ ├── Mapel (Subjects)                                     │
│  │ ├── KelasSiswa (M2M: Siswa ↔ Kelas per year)             │
│  │ └── Jadwal (Schedule: Kelas+Mapel+Guru by day/time)      │
│  └──────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────────┤
│  │ GRADE MODELS (apps/grades)                               │
│  │ ├── Tugas (Assignments: FK Jadwal)                       │
│  │ ├── Nilai (Scores: Siswa+Jadwal+tipe_penilaian)         │
│  │ └── Presensi (Attendance: Siswa+Jadwal+date)             │
│  └──────────────────────────────────────────────────────────┤
└────────────────┬─────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│               DATABASE LAYER                                 │
│  MySQL Database (school_management)                          │
│  - Adapter: PyMySQL 1.1.2                                    │
│  - Configured via DATABASE_URL env variable                  │
│  - Multiple indexes on FK and search fields                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Django Apps Structure

### **3.1 Core App** (`apps/core/`)
**Purpose**: Provide base functionality and landing pages.

| File | Purpose |
|------|---------|
| `models.py` | Abstract `Person` model (base for Siswa, Guru, Wali) |
| `views.py` | `BaseCrudMixin`, `BaseListView`, `IntroPageView`, `DashboardView` |
| `urls.py` | Routes: `''` (intro), `/dashboard/` |
| `admin.py` | Not implemented |
| `templates/` | `intro.html`, `dashboard.html`, `guru_dashboard.html`, partials for CRUD |

**Key Classes**:
- `BaseCrudMixin`: Mixin yang menangani permission checking, HTMX detection, dan URL resolution
- `BaseListView`: ListView yang support search, pagination, dan HTMX partial rendering
- `BaseCreateView/UpdateView/DeleteView`: Generic CRUD views dengan form handling

---

### **3.2 Users App** (`apps/users/`)
**Purpose**: User authentication, role management, and user profile data.

| File | Purpose |
|------|---------|
| `models.py` | Custom `Akun` (User), `Peran` (Roles), `Siswa`, `Guru`, `Wali`, `SiswaWali` |
| `views.py` | `AkunListView`, `AkunCreateView`, `AkunDetailView`, `AkunUpdateView`, `AkunDeleteView`, `PeranListView`, `SiswaListView`, `GuruListView` |
| `urls.py` | Routes for account and role CRUD |
| `forms.py` | `AkunCreationForm`, `AkunChangeForm` |
| `managers.py` | `AkunManager` (custom user manager) |
| `admin.py` | Admin configuration for all user-related models |

**Key Models**:
- `Akun`: Custom user model based on email (not username)
- `Peran`: Roles with names like "Admin", "Guru", "Siswa"
- `Siswa`: Student profile linked OneToOne to Akun
- `Guru`: Teacher profile linked OneToOne to Akun

---

### **3.3 Academics App** (`apps/academics/`)
**Purpose**: Manage school academic structure (classes, subjects, schedules).

| File | Purpose |
|------|---------|
| `models.py` | `TahunAjaran`, `Jurusan`, `Kelas`, `Mapel`, `KelasSiswa`, `Jadwal` |
| `views.py` | `KelasListView`, `TahunAjaranListView`, `JurusanListView`, `MapelListView`, `JadwalListView` |
| `urls.py` | Routes for CRUD views |
| `admin.py` | Admin config for academic models |

**Key Models**:
- `TahunAjaran`: School year (e.g., "2024/2025") + semester (Ganjil/Genap)
- `Jurusan`: Majors (e.g., "IPA", "IPS")
- `Kelas`: Classes linked to Jurusan, teacher, year
- `Jadwal`: Schedule with day, time, class, subject, teacher

---

### **3.4 Grades App** (`apps/grades/`)
**Purpose**: Record student grades, assignments, and attendance.

| File | Purpose |
|------|---------|
| `models.py` | `Tugas`, `Nilai`, `Presensi` |
| `views.py` | `TugasListView`, `NilaiListView`, `PresensiListView` |
| `urls.py` | Routes for grade views |
| `admin.py` | Admin config for grade models |

**Key Models**:
- `Tugas`: Assignments with deadline
- `Nilai`: Student scores (Tugas, Ujian Harian, UTS, UAS)
- `Presensi`: Attendance (Hadir, Sakit, Izin, Alpha)

---

## 4. Authentication & Authorization

- **Auth Backend**: Django's built-in authentication system
- **Custom User Model**: Email-based login (not username)
- **Role-Based Access**: `Peran` model with role names (Admin, Guru, Siswa, etc.)
- **Permission Checks**:
  - `@permission_required` decorator on views
  - `PermissionRequiredMixin` on class-based views
  - Example: `permission_required = 'users.view_akun'`
- **Login/Logout**: Django's built-in views
  - Login URL: `/users/auth/login/`
  - Redirect after login: `/` (dashboard)
  - Logout redirect: `/users/auth/login/`

---

## 5. Frontend Architecture

### **5.1 Static Assets**
- **CSS Framework**: Tailwind CSS v4.1 with DaisyUI v5.0.43
- **Build Process**: PostCSS with nested + simple-vars plugins
- **Source**: `tailwindcss_theme/static_src/src/styles.css`
- **Output**: `tailwindcss_theme/static/css/dist/styles.css`
- **Dev Mode**: `npm run dev` (watches and rebuilds)
- **Prod Mode**: `npm run build:tailwind` (minified)

### **5.2 Interactivity**
- **HTMX v1.26**: For dynamic requests without page reload
  - Search filtering (GET with `?q=`)
  - Pagination updates
  - Form submission and validation
- **Alpine.js**: Likely used for component interactivity (not confirmed in code review)
- **DaisyUI**: Provides Tailwind-based components (buttons, forms, modals, toasts)

### **5.3 Template Structure**
```
templates/
├── base.html                              # Tailwind + DaisyUI setup
├── registration/
│   ├── login.html
│   └── base_auth.html
├── 403.html, 404.html, 500.html          # Error pages
│
tailwindcss_theme/templates/base.html      # Base template with {% tailwind_css %}
│
apps/*/templates/<app>/
├── <model>_list.html                      # Full page list view
├── <model>_detail.html                    # Detail/read-only view
├── <model>_form.html                      # Create/edit form
├── <model>_confirm_delete.html            # Delete confirmation
└── partials/
    ├── _<model>_table_body.html           # Table rows (for HTMX)
    ├── _form_content.html                 # Form fields only (for HTMX)
    ├── _paginate.html                     # Pagination controls
    ├── _search_input.html                 # Search box
    └── ...
```

### **5.4 HTMX Integration**
- **Search**: Input field with `hx-get="/users/akun/?q=..."` triggers partial table body update
- **Pagination**: Pagination links use HTMX to fetch next page without reload
- **Form Submission**: Forms use HTMX for validation feedback without full page reload
- **Middleware Support**: `HtmxMiddleware` adds `request.htmx` boolean flag

---

## 6. Database Design

**Database**: MySQL (configured via `DATABASE_URL` in .env)

**Key Relationships**:
```
Akun (Custom User)
├── 1:1 → Siswa (student profile)
├── 1:1 → Guru (teacher profile)
└── FK → Peran (role)

Siswa
├── FK → Akun
├── M2M → Kelas (via KelasSiswa)
└── M2M → Wali (via SiswaWali)

Guru
├── FK → Akun
└── 1:M → Kelas (wali_kelas)

Kelas
├── FK → Jurusan
├── FK → TahunAjaran
├── FK → Guru (wali_kelas)
├── 1:M → KelasSiswa (students in class)
└── 1:M → Jadwal (schedules)

Jadwal
├── FK → Kelas
├── FK → Mapel (subject)
├── FK → Guru
└── 1:M → Tugas

Nilai (Scores)
├── FK → Siswa
├── FK → Jadwal (context: class+subject+teacher)
└── FK → Tugas (optional, if tipe_penilaian = "Tugas")

Presensi (Attendance)
├── FK → Siswa
├── FK → Jadwal
└── unique_together: (siswa, jadwal, tanggal)
```

---

## 7. Settings & Configuration

**Main File**: `config/settings.py`

**Key Settings**:
```python
DEBUG = env('DEBUG')  # Read from .env (SECURITY: should be False in production)
SECRET_KEY = 'django-insecure-...'  # HARDCODED (SECURITY: move to .env!)
ALLOWED_HOSTS = []  # EMPTY (SECURITY: configure for production)
AUTH_USER_MODEL = 'users.akun'  # Custom user model
LOGIN_URL = '/users/auth/login/'
DATABASE: MySQL via PyMySQL
INSTALLED_APPS: Django built-ins + tailwind + django_htmx + local apps
MIDDLEWARE: Standard Django + HtmxMiddleware
TEMPLATES: DjangoTemplates with APP_DIRS=True
STATIC_URL: /static/ served from disk during development
```

---

## 8. Development Workflow

### **Setup**
```bash
# 1. Clone repository
git clone https://github.com/DinkyTrady/school-management.git
cd school-management

# 2. Create virtual environment (using uv)
uv venv
source .venv/Scripts/activate  # Windows PowerShell

# 3. Install dependencies
uv pip install -e .

# 4. Setup database
python manage.py migrate

# 5. Create superuser
python manage.py createsuperuser

# 6. Create initial data (optional)
python manage.py seed_data
python manage.py seed_akun
```

### **Development Server**
```bash
# Terminal 1: Django dev server
python manage.py runserver

# Terminal 2: Tailwind CSS watcher
cd tailwindcss_theme/static_src && npm run dev

# Access at http://localhost:8000
```

### **Production Deployment**
```bash
# Build static assets
npm run build:tailwind
python manage.py collectstatic

# Set environment variables
export DEBUG=False
export ALLOWED_HOSTS="example.com,www.example.com"
export SECRET_KEY="your-random-secret-key-here"
export DATABASE_URL="mysql://user:pass@host:3306/dbname"

# Run with WSGI server (gunicorn, uWSGI, etc.)
gunicorn config.wsgi:application
```

---

## 9. Key Features Implemented

✅ **User Management**: Create, read, update, delete accounts; role assignment  
✅ **Authentication**: Login/logout with email-based custom user model  
✅ **HTMX Integration**: Dynamic search, pagination, form validation  
✅ **CRUD Mixins**: Reusable class-based views with permission checking  
✅ **Admin Panel**: Comprehensive Django admin interface  
✅ **Database Indexing**: Proper indexes on FK and search fields  
✅ **Role-Based Access**: Permission-based view access control  

---

## 10. Areas for Improvement

⚠️ **Missing Tests**: No unit or integration tests  
⚠️ **No API**: Only HTML views, no REST API endpoints  
⚠️ **No Docker**: No containerization for easy deployment  
⚠️ **No CI/CD**: No GitHub Actions or similar workflows  
⚠️ **Limited Logging**: No structured logging or error tracking  
⚠️ **No Rate Limiting**: No protection against brute force attacks  
⚠️ **No Caching**: Could benefit from Redis caching  

---

## 11. File Inventory & Quick Reference

| Path | Type | Size | Purpose |
|------|------|------|---------|
| manage.py | Python | ~0.5 KB | Django CLI |
| pyproject.toml | TOML | ~0.7 KB | Project metadata + dependencies |
| config/settings.py | Python | ~3.5 KB | Django configuration |
| config/urls.py | Python | ~0.5 KB | Root URL routing |
| config/wsgi.py | Python | ~0.4 KB | WSGI entrypoint |
| config/asgi.py | Python | ~0.4 KB | ASGI entrypoint |
| apps/core/models.py | Python | ~1.2 KB | Person abstract base |
| apps/core/views.py | Python | ~3.5 KB | Base CRUD mixins + dashboard |
| apps/users/models.py | Python | ~2.8 KB | Akun, Peran, Siswa, Guru, Wali |
| apps/users/views.py | Python | ~4.2 KB | User CRUD views |
| apps/users/forms.py | Python | ~3.8 KB | User forms with DaisyUI |
| apps/academics/models.py | Python | ~2.5 KB | Academic models |
| apps/academics/views.py | Python | ~2.8 KB | Academic CRUD views |
| apps/grades/models.py | Python | ~2.2 KB | Grade, task, attendance models |
| apps/grades/views.py | Python | ~2.1 KB | Grade CRUD views |
| tailwindcss_theme/static_src/package.json | JSON | ~0.5 KB | Tailwind build dependencies |
| tailwindcss_theme/static_src/postcss.config.js | JS | ~0.2 KB | PostCSS configuration |
| .env | Dotenv | ~0.1 KB | Environment variables ⚠️ Secrets in repo |

---

## Next Steps

1. **Security**: Fix hardcoded SECRET_KEY and DEBUG setting (see security_audit.md)
2. **Testing**: Write unit tests and integration tests
3. **Deployment**: Configure Docker, CI/CD, and production settings
4. **Scaling**: Consider caching, async tasks, and load balancing
5. **Features**: Add API endpoints, reporting, and advanced filtering

# 📱 SIGMA - Struktur Aplikasi Lengkap & Komprehensif

**Status**: ✅ Dokumentasi Lengkap | **Dibuat**: 2024 | **Bahasa**: Indonesia

---

## 🎯 SIGMA Adalah Apa?

**SIGMA** = **S**ystem **I**nformation & **G**overnment **M**anagement **A**pplication

Aplikasi manajemen akademik sekolah terintegrasi yang mengelola:
- 👤 **Akun Pengguna** (Guru, Siswa, Admin, Wali Murid, Tata Usaha)
- 📚 **Struktur Akademik** (Tahun ajaran, Jurusan, Kelas, Mata pelajaran)
- 📅 **Jadwal Pelajaran** dan distribusi guru per kelas
- 📊 **Input Nilai** siswa (UTS, UAS, Tugas, Ujian Harian)
- ✅ **Tracking Kehadiran** (Presensi siswa)
- 👨‍👩‍👧 **Relasi Siswa-Wali** Murid (Ayah, Ibu, Wali)

**Target User**: Admin, Guru, Siswa, Wali Murid, Tata Usaha

---

## 💻 Tech Stack (Technology Used)

```
┌─────────────────────────────────────────┐
│        SIGMA TECHNOLOGY STACK           │
├─────────────────────────────────────────┤
│ Backend        │ Django 5.2.6           │
│ Language       │ Python 3.14+           │
│ Database       │ MySQL 8.0              │
│ DB Driver      │ PyMySQL 1.1.2          │
│ Frontend       │ Tailwind CSS 4.1       │
│ UI Kit         │ DaisyUI 5.0.43         │
│ Interactivity  │ HTMX 1.26              │
│ Lightweight JS │ Alpine.js              │
│ CSS Processor  │ PostCSS 8.5.6          │
│ Build Tool     │ npm + Tailwind CLI     │
│ Package Mgr    │ pip + uv               │
│ Testing        │ pytest + Factory Boy   │
│ Type Check     │ BasedPyright           │
│ Linter         │ Ruff                   │
│ Auth Model     │ Custom (Email-based)   │
│ RBAC           │ Role-based Permission  │
│ IDE            │ PyCharm / VSCode       │
│ Git            │ GitHub / GitLab        │
│ Deployment     │ Gunicorn + Nginx       │
└─────────────────────────────────────────┘
```

---

## 📁 Struktur Folder & File (Complete Tree View)

```
c:\Users\fatha\sigma\
│
├── 📂 config/                          ← DJANGO CONFIGURATION (ROOT)
│   ├── __init__.py
│   ├── settings.py                     - Main Django settings (3.5 KB)
│   │                                    ├─ Installed apps: core, users, academics, grades
│   │                                    ├─ Database: MySQL connection
│   │                                    ├─ Authentication: Custom Akun model
│   │                                    ├─ Middleware: Security, CSRF, HTMX
│   │                                    ├─ Templates: Template engine config
│   │                                    ├─ Static files: CSS, JS paths
│   │                                    └─ Security: SECRET_KEY, DEBUG settings
│   ├── urls.py                         - Root URL routing (0.5 KB)
│   │                                    ├─ Include apps/*/urls.py
│   │                                    ├─ Static files serving (dev)
│   │                                    └─ Admin panel: /admin/
│   ├── wsgi.py                         - WSGI entry point (production)
│   ├── asgi.py                         - ASGI entry point (async)
│   └── __pycache__/                    - Python cache files
│
├── 📂 apps/                            ← DJANGO APPLICATIONS (CORE)
│   ├── __init__.py                     - Package marker
│   │
│   ├── 📂 core/                        ← BASE INFRASTRUCTURE & DASHBOARD
│   │   ├── __init__.py
│   │   ├── apps.py                     - App configuration
│   │   ├── models.py                   - Base models (1.2 KB)
│   │   │                                ├─ Person (abstract base)
│   │   │                                │  ├─ nama (full name)
│   │   │                                │  ├─ tanggal_lahir (birth date)
│   │   │                                │  ├─ alamat (address)
│   │   │                                │  └─ no_telp (phone)
│   │   │                                └─ Used by: Siswa, Guru, Wali
│   │   ├── views.py                    - Base CRUD views & Dashboard (3.5 KB)
│   │   │                                ├─ BaseCrudMixin (reusable CRUD logic)
│   │   │                                ├─ BaseListView (list with pagination)
│   │   │                                ├─ BaseCreateView (create with validation)
│   │   │                                ├─ BaseUpdateView (update with validation)
│   │   │                                ├─ BaseDeleteView (delete with confirmation)
│   │   │                                ├─ DashboardView (admin dashboard)
│   │   │                                │  ├─ Metrics: Total akun, peran, kelas
│   │   │                                │  ├─ Quick access cards
│   │   │                                │  └─ Recent activities
│   │   │                                └─ Templates auto-generated from model
│   │   ├── urls.py                     - Core app routes
│   │   │                                ├─ path('dashboard/', DashboardView)
│   │   │                                └─ path('intro/', IntroView)
│   │   ├── forms.py                    - Base forms
│   │   ├── admin.py                    - Django admin config
│   │   ├── migrations/                 - Database migrations
│   │   │   ├── 0001_initial.py
│   │   │   └── __init__.py
│   │   ├── templates/core/             - Core templates
│   │   │   ├── base.html               - Main base template (WITH Tailwind + DaisyUI)
│   │   │   │                            ├─ Navbar with logo & user menu
│   │   │   │                            ├─ Sidebar navigation
│   │   │   │                            ├─ Main content block
│   │   │   │                            ├─ Footer
│   │   │   │                            ├─ HTMX script
│   │   │   │                            └─ Alpine.js script
│   │   │   ├── dashboard.html          - Admin dashboard page
│   │   │   │                            ├─ Metrics cards
│   │   │   │                            ├─ Quick access buttons
│   │   │   │                            └─ Activity feed
│   │   │   ├── intro.html              - Project introduction
│   │   │   ├── base_crud_list.html     - Base list view (paginated table)
│   │   │   ├── base_crud_detail.html   - Base detail view
│   │   │   ├── base_crud_form.html     - Base form template
│   │   │   └── partials/               - Reusable template fragments
│   │   │       ├── pagination.html     - Pagination controls
│   │   │       ├── search_bar.html     - Search input
│   │   │       ├── filter_panel.html   - Filter options
│   │   │       └── modal.html          - Modal template
│   │   ├── management/                 - Django management commands
│   │   │   └── commands/
│   │   │       └── seed_data.py        - Command to populate demo data
│   │   ├── templatetags/               - Custom template filters
│   │   │   └── query_params.py         - URL query string helpers
│   │   └── __pycache__/
│   │
│   ├── 📂 users/                       ← AUTHENTICATION & USER MANAGEMENT
│   │   ├── __init__.py
│   │   ├── apps.py                     - App configuration
│   │   ├── models.py                   - User models (2.8 KB)
│   │   │                                ├─ 🔐 Akun (Custom User Model)
│   │   │                                │  ├─ email (unique login credential)
│   │   │                                │  ├─ password (hashed)
│   │   │                                │  ├─ is_active, is_staff, is_superuser
│   │   │                                │  ├─ date_joined, last_login
│   │   │                                │  ├─ FK to Peran (role assignment)
│   │   │                                │  └─ Custom manager: AkunManager
│   │   │                                ├─ 👔 Peran (Role)
│   │   │                                │  ├─ nama: Admin, Guru, Siswa, Wali, Tata Usaha
│   │   │                                │  ├─ permissions (M:M to django.auth.Permission)
│   │   │                                │  └─ is_active
│   │   │                                ├─ 👨 Siswa (Student)
│   │   │                                │  ├─ Extends Person (abstract)
│   │   │                                │  ├─ nis (Student ID, unique)
│   │   │                                │  ├─ OneToOne to Akun
│   │   │                                │  ├─ M:M to Kelas via KelasSiswa
│   │   │                                │  ├─ M:M to Wali via SiswaWali
│   │   │                                │  └─ FK to TahunAjaran (enrollment year)
│   │   │                                ├─ 👨‍🏫 Guru (Teacher)
│   │   │                                │  ├─ Extends Person (abstract)
│   │   │                                │  ├─ nip (Teacher ID, unique)
│   │   │                                │  ├─ jabatan (position: Guru, Kepala Sekolah)
│   │   │                                │  ├─ OneToOne to Akun
│   │   │                                │  └─ M:M to Kelas (classes taught)
│   │   │                                ├─ 👵 Wali (Guardian)
│   │   │                                │  ├─ Extends Person (abstract)
│   │   │                                │  ├─ hubungan (Ayah, Ibu, Wali, Wali Asuh)
│   │   │                                │  └─ M:M to Siswa via SiswaWali
│   │   │                                └─ 📎 SiswaWali (M:N Relationship)
│   │   │                                   ├─ siswa_id, wali_id
│   │   │                                   ├─ hubungan (family relationship)
│   │   │                                   └─ unique_together(siswa, wali)
│   │   ├── views.py                    - User CRUD views (4.2 KB)
│   │   │                                ├─ AkunListView (list all users)
│   │   │                                ├─ AkunCreateView (create new user)
│   │   │                                ├─ AkunDetailView (view user details)
│   │   │                                ├─ AkunUpdateView (edit user)
│   │   │                                ├─ AkunDeleteView (delete user)
│   │   │                                ├─ SiswaListView (list students)
│   │   │                                ├─ GuruListView (list teachers)
│   │   │                                ├─ PeranListView (list roles)
│   │   │                                └─ Permission checks
│   │   ├── urls.py                     - User app routes
│   │   │                                ├─ path('akun/', AkunListView)
│   │   │                                ├─ path('akun/create/', AkunCreateView)
│   │   │                                ├─ path('akun/<id>/', AkunDetailView)
│   │   │                                ├─ path('siswa/', SiswaListView)
│   │   │                                ├─ path('guru/', GuruListView)
│   │   │                                └─ path('peran/', PeranListView)
│   │   ├── forms.py                    - User forms (3.8 KB)
│   │   │                                ├─ AkunCreationForm
│   │   │                                ├─ AkunChangeForm
│   │   │                                ├─ SiswaForm
│   │   │                                ├─ GuruForm
│   │   │                                └─ DaisyUI widget customization
│   │   ├── managers.py                 - Custom AkunManager
│   │   │                                ├─ create_user (with email validation)
│   │   │                                └─ create_superuser
│   │   ├── permissions.py              - Permission system
│   │   │                                ├─ Role-based decorators
│   │   │                                ├─ Permission checks
│   │   │                                └─ Admin-only views
│   │   ├── admin.py                    - Django admin customization
│   │   │                                ├─ AkunAdmin (inline Siswa/Guru)
│   │   │                                ├─ SiswaAdmin (list display, search)
│   │   │                                ├─ GuruAdmin (list display, search)
│   │   │                                └─ PeranAdmin (permissions widget)
│   │   ├── migrations/                 - Database migrations
│   │   │   ├── 0001_initial.py         - Initial schema (Akun, Peran, Siswa, Guru, Wali)
│   │   │   └── __init__.py
│   │   ├── templates/users/            - User templates
│   │   │   ├── akun_list.html          - Account list (table with pagination)
│   │   │   ├── akun_create.html        - Create account form
│   │   │   ├── akun_detail.html        - Account details
│   │   │   ├── akun_update.html        - Edit account form
│   │   │   ├── akun_confirm_delete.html - Delete confirmation
│   │   │   ├── siswa_list.html         - Student list
│   │   │   ├── guru_list.html          - Teacher list
│   │   │   ├── peran_list.html         - Role list
│   │   │   ├── peran_create.html       - Create role form
│   │   │   ├── peran_form.html         - Role form template
│   │   │   ├── peran_confirm_delete.html - Delete role confirmation
│   │   │   └── partials/               - Reusable fragments (HTMX)
│   │   │       ├── user_search.html    - Search form
│   │   │       ├── user_filter.html    - Filter by role
│   │   │       └── user_card.html      - User card component
│   │   ├── management/                 - Django management commands
│   │   │   └── commands/
│   │   │       └── seed_akun.py        - Seed initial users & roles
│   │   └── __pycache__/
│   │
│   ├── 📂 academics/                   ← ACADEMIC STRUCTURE MANAGEMENT
│   │   ├── __init__.py
│   │   ├── apps.py                     - App configuration
│   │   ├── models.py                   - Academic models (2.5 KB)
│   │   │                                ├─ 📆 TahunAjaran (Academic Year)
│   │   │                                │  ├─ tahun (2024/2025)
│   │   │                                │  ├─ semester (Ganjil/Genap)
│   │   │                                │  ├─ tanggal_mulai, tanggal_selesai
│   │   │                                │  ├─ is_active (current academic year)
│   │   │                                │  └─ 1:N to Kelas, Jadwal
│   │   │                                ├─ 🎓 Jurusan (Major)
│   │   │                                │  ├─ nama (IPA, IPS, Bahasa)
│   │   │                                │  ├─ deskripsi
│   │   │                                │  └─ 1:N to Kelas
│   │   │                                ├─ 🏫 Kelas (Class)
│   │   │                                │  ├─ nama (XI-A, XI-B)
│   │   │                                │  ├─ tingkat (grade: 10, 11, 12)
│   │   │                                │  ├─ FK to Jurusan
│   │   │                                │  ├─ FK to Guru (wali_kelas/homeroom teacher)
│   │   │                                │  ├─ FK to TahunAjaran
│   │   │                                │  ├─ M:N to Siswa via KelasSiswa
│   │   │                                │  ├─ 1:N to Jadwal
│   │   │                                │  ├─ unique_together(nama, tahun, jurusan)
│   │   │                                │  └─ 📝 __str__: "XI-A (IPA) - 2024/2025"
│   │   │                                ├─ 📚 Mapel (Subject)
│   │   │                                │  ├─ nama (Matematika, Bahasa Inggris, etc)
│   │   │                                │  ├─ kode (MTK, BIng)
│   │   │                                │  ├─ sks (credit hours)
│   │   │                                │  └─ 1:N to Jadwal
│   │   │                                ├─ 📖 KelasSiswa (Class Registration)
│   │   │                                │  ├─ siswa_id, kelas_id
│   │   │                                │  ├─ tahun_ajaran_id
│   │   │                                │  ├─ tanggal_daftar (registration date)
│   │   │                                │  ├─ status (Aktif, Lulus, Keluar)
│   │   │                                │  └─ unique_together(siswa, kelas, tahun)
│   │   │                                └─ 📅 Jadwal (Schedule)
│   │   │                                   ├─ hari (Senin, Selasa, ..., Jumat)
│   │   │                                   ├─ jam_mulai (08:00)
│   │   │                                   ├─ jam_selesai (09:00)
│   │   │                                   ├─ FK to Kelas, Mapel, Guru
│   │   │                                   ├─ FK to TahunAjaran
│   │   │                                   ├─ ruangan (classroom)
│   │   │                                   ├─ 1:N to Tugas, Nilai, Presensi
│   │   │                                   └─ Constraints:
│   │   │                                      ├─ unique schedule per class
│   │   │                                      └─ unique schedule per teacher
│   │   ├── views.py                    - Academic list views (2.8 KB)
│   │   │                                ├─ TahunAjaranListView
│   │   │                                ├─ JurusanListView
│   │   │                                ├─ KelasListView
│   │   │                                ├─ MapelListView
│   │   │                                ├─ JadwalListView
│   │   │                                └─ Filtering & search
│   │   ├── urls.py                     - Academic routes
│   │   │                                ├─ path('tahun/', TahunAjaranListView)
│   │   │                                ├─ path('jurusan/', JurusanListView)
│   │   │                                ├─ path('kelas/', KelasListView)
│   │   │                                ├─ path('mapel/', MapelListView)
│   │   │                                └─ path('jadwal/', JadwalListView)
│   │   ├── forms.py                    - Academic forms
│   │   ├── admin.py                    - Admin customization
│   │   ├── migrations/                 - Database migrations
│   │   │   ├── 0001_initial.py
│   │   │   ├── 0002_initial.py
│   │   │   └── __init__.py
│   │   ├── templates/academics/        - Academic templates
│   │   │   ├── tahun_list.html         - Academic years
│   │   │   ├── jurusan_list.html       - Majors list
│   │   │   ├── kelas_list.html         - Classes list
│   │   │   ├── mapel_list.html         - Subjects list
│   │   │   ├── jadwal_list.html        - Schedules list
│   │   │   └── partials/               - Reusable fragments
│   │   │       ├── jadwal_search.html  - Schedule search
│   │   │       ├── jadwal_filter.html  - Schedule filter
│   │   │       └── kelas_info.html     - Class info card
│   │   └── __pycache__/
│   │
│   ├── 📂 grades/                      ← ASSESSMENT & ATTENDANCE
│   │   ├── __init__.py
│   │   ├── apps.py                     - App configuration
│   │   ├── models.py                   - Grade models (2.2 KB)
│   │   │                                ├─ 📝 Tugas (Assignment)
│   │   │                                │  ├─ nama (assignment name)
│   │   │                                │  ├─ deskripsi (description)
│   │   │                                │  ├─ mulai (start date)
│   │   │                                │  ├─ tenggat (deadline)
│   │   │                                │  ├─ poin (max points)
│   │   │                                │  ├─ FK to Jadwal
│   │   │                                │  └─ 1:N to Nilai
│   │   │                                ├─ ⭐ Nilai (Grade)
│   │   │                                │  ├─ tipe_penilaian
│   │   │                                │  │  ├─ Tugas
│   │   │                                │  │  ├─ UTS (Mid-term)
│   │   │                                │  │  ├─ UAS (Final exam)
│   │   │                                │  │  └─ Ujian Harian
│   │   │                                │  ├─ nilai (0-100)
│   │   │                                │  ├─ keterangan (notes)
│   │   │                                │  ├─ FK to Siswa, Jadwal, Tugas (optional)
│   │   │                                │  ├─ created_at, updated_at
│   │   │                                │  ├─ Constraints:
│   │   │                                │  │  ├─ unique_together(siswa, jadwal, tipe)
│   │   │                                │  │  └─ Jika tipe=Tugas, tugas harus diisi
│   │   │                                │  └─ Validation: nilai 0-100
│   │   │                                └─ ✅ Presensi (Attendance)
│   │   │                                   ├─ tanggal (attendance date)
│   │   │                                   ├─ status (Hadir, Sakit, Izin, Alpha)
│   │   │                                   ├─ keterangan (notes/reason)
│   │   │                                   ├─ FK to Siswa, Jadwal
│   │   │                                   ├─ created_at, updated_at
│   │   │                                   ├─ Constraints:
│   │   │                                   │  └─ unique_together(siswa, jadwal, tanggal)
│   │   │                                   └─ unique attendance per date/schedule
│   │   ├── views.py                    - Grade list views (2.1 KB)
│   │   │                                ├─ NilaiListView (grades list)
│   │   │                                ├─ PresensiListView (attendance list)
│   │   │                                ├─ TugasListView (assignments list)
│   │   │                                ├─ Filtering & search
│   │   │                                └─ Export to CSV (optional)
│   │   ├── urls.py                     - Grade routes
│   │   │                                ├─ path('nilai/', NilaiListView)
│   │   │                                ├─ path('presensi/', PresensiListView)
│   │   │                                └─ path('tugas/', TugasListView)
│   │   ├── forms.py                    - Grade forms
│   │   ├── admin.py                    - Admin customization
│   │   ├── migrations/                 - Database migrations
│   │   │   ├── 0001_initial.py
│   │   │   ├── 0002_initial.py
│   │   │   └── __init__.py
│   │   ├── templates/grades/           - Grade templates
│   │   │   ├── nilai_list.html         - Grades list (filterable)
│   │   │   ├── nilai_create.html       - Input grade form
│   │   │   ├── presensi_list.html      - Attendance list
│   │   │   ├── presensi_create.html    - Mark attendance form
│   │   │   ├── tugas_list.html         - Assignments list
│   │   │   └── partials/               - Reusable fragments
│   │   │       ├── nilai_filter.html   - Grade filter (by student, type)
│   │   │       ├── presensi_filter.html - Attendance filter
│   │   │       └── nilai_form.html     - Grade input form
│   │   └── __pycache__/
│   │
│   └── __pycache__/
│
├── 📂 templates/                       ← GLOBAL TEMPLATES (HTML)
│   ├── base.html                       - Main base template (Tailwind + DaisyUI)
│   │                                    ├─ DOCTYPE, meta tags, responsive viewport
│   │                                    ├─ Tailwind CSS link
│   │                                    ├─ DaisyUI CSS
│   │                                    ├─ HTMX script
│   │                                    ├─ Alpine.js script
│   │                                    ├─ Navbar with logo & user menu
│   │                                    ├─ Sidebar navigation (collapsible)
│   │                                    ├─ Main content area ({% block content %})
│   │                                    ├─ Footer
│   │                                    └─ Custom JavaScript
│   ├── nav.html                        - Navigation sidebar component
│   │                                    ├─ Logo
│   │                                    ├─ Menu items per role
│   │                                    ├─ Admin: All options
│   │                                    ├─ Guru: Kelas, Jadwal, Nilai, Presensi
│   │                                    ├─ Siswa: My Classes, My Grades
│   │                                    └─ Responsive design
│   ├── 403.html                        - Forbidden (access denied)
│   ├── 404.html                        - Not found
│   ├── 500.html                        - Server error
│   │
│   ├── 📂 admin/                       - Admin-related templates
│   │   ├── dashboard.html              - Admin dashboard
│   │   ├── metrics.html                - Dashboard metrics
│   │   └── quick_access.html           - Quick action buttons
│   │
│   └── 📂 registration/                - Authentication templates
│       ├── login.html                  - Login page ✨ (WhatsApp link added!)
│       │                                ├─ Email input
│       │                                ├─ Password input
│       │                                ├─ Login button
│       │                                ├─ Forgot password link → WhatsApp
│       │                                ├─ Intro link to project info
│       │                                └─ Tailwind + DaisyUI styling
│       ├── base_auth.html              - Auth base template
│       │                                ├─ Different layout (no sidebar)
│       │                                ├─ Centered content
│       │                                └─ Logo display
│       └── intro.html                  - Project introduction page
│
├── 📂 static/                          ← STATIC ASSETS (CSS, JS, Images)
│   └── 📂 css/                         - CSS files
│       ├── dist/                       - Production CSS
│       │   └── styles.css              - Compiled Tailwind (35 KB min, 5 KB gzip)
│       │                                ├─ All Tailwind utilities
│       │                                ├─ DaisyUI components
│       │                                ├─ Custom theme colors
│       │                                └─ Responsive breakpoints
│       └── src/                        - Source CSS
│           └── styles.css              - Tailwind directives input
│                                        ├─ @tailwind base;
│                                        ├─ @tailwind components;
│                                        ├─ @tailwind utilities;
│                                        └─ @layer custom classes;
│
├── 📂 tailwindcss_theme/               ← TAILWIND BUILD SYSTEM
│   ├── __init__.py
│   ├── apps.py                         - Django Tailwind app config
│   │
│   ├── 📂 static/                      - Static files (compiled)
│   │   └── css/
│   │       └── dist/                   - Output CSS files
│   │
│   ├── 📂 static_src/                  - Source files (input)
│   │   ├── package.json                - npm dependencies (2.1 KB)
│   │   │                                ├─ tailwindcss: 4.1.11
│   │   │                                ├─ @tailwindcss/typography
│   │   │                                ├─ daisyui: 5.0.43
│   │   │                                ├─ postcss: 8.5.6
│   │   │                                ├─ autoprefixer
│   │   │                                └─ npm scripts (dev, build)
│   │   ├── postcss.config.js           - PostCSS configuration
│   │   │                                ├─ Tailwind plugin
│   │   │                                ├─ Autoprefixer
│   │   │                                ├─ Nested CSS support
│   │   │                                └─ Simple vars plugin
│   │   ├── tailwind.config.js          - Tailwind customization
│   │   │                                ├─ Content paths (templates, js)
│   │   │                                ├─ Theme colors (extended)
│   │   │                                ├─ Plugins (daisyui, typography)
│   │   │                                └─ DaisyUI config
│   │   ├── src/                        - Source CSS
│   │   │   └── styles.css              - Main Tailwind input
│   │   │                                ├─ @tailwind base;
│   │   │                                ├─ @tailwind components;
│   │   │                                ├─ @tailwind utilities;
│   │   │                                └─ @layer directives
│   │   └── tsconfig.json               - TypeScript config (optional)
│   │
│   └── 📂 templates/                   - Tailwind templates
│       └── base.html                   - Base template with Tailwind setup
│
├── 📂 tests/                           ← TESTING INFRASTRUCTURE (pytest)
│   ├── __init__.py                     - Package marker
│   ├── conftest.py                     - Pytest configuration
│   │                                    ├─ Fixtures for models
│   │                                    ├─ Database setup/teardown
│   │                                    ├─ User/Role fixtures
│   │                                    └─ DJANGO_SETTINGS_MODULE
│   ├── example_tests.py                - 50+ test examples (5.2 KB)
│   │                                    ├─ Model tests (validation, relationships)
│   │                                    ├─ Form tests (field validation)
│   │                                    ├─ View tests (CRUD operations)
│   │                                    ├─ Permission tests (role-based access)
│   │                                    ├─ Integration tests
│   │                                    └─ Happy path + edge cases
│   ├── factories.py                    - Factory Boy factories (3.2 KB)
│   │                                    ├─ PeranFactory
│   │                                    ├─ AkunFactory
│   │                                    ├─ SiswaFactory
│   │                                    ├─ GuruFactory
│   │                                    ├─ TahunAjaranFactory
│   │                                    ├─ KelasFactory
│   │                                    ├─ JadwalFactory
│   │                                    ├─ NilaiFactory
│   │                                    ├─ PresensiFactory
│   │                                    └─ Realistic test data generation
│   └── README.md                       - Testing guide & quick start
│
├── 📂 docs/                            ← COMPREHENSIVE DOCUMENTATION
│   ├── EXECUTIVE_SUMMARY.md            - 1-page project overview
│   ├── PROJECT_OVERVIEW.md             - Complete architecture (10 KB)
│   ├── models_summary.md               - Database schema (8 KB, 15 models)
│   ├── routes.csv                      - All 30+ endpoints mapped
│   ├── backend-summary.md              - Views, forms, URLs (6 KB)
│   ├── frontend_summary.md             - Tailwind, HTMX, templates (5 KB)
│   ├── security_audit.md               - 14 vulnerabilities + fixes
│   ├── quick_fixes.md                  - 8 ready-to-apply patches
│   ├── ERD.txt                         - Entity Relationship Diagram (ASCII)
│   ├── recommendations.md              - 6-12 month roadmap
│   └── test_plan.md                    - Testing strategy & examples
│
├── 📂 extras/                          ← EXTRA FILES
│   ├── school_management.sql           - Database dump (initial schema)
│   └── (other utilities, scripts)
│
├── .env                                ← ENVIRONMENT VARIABLES (⚠️ SECRET!)
│   ├── DEBUG=True
│   ├── DATABASE_URL=mysql://root:@127.0.0.1:3306/school_management
│   ├── SECRET_KEY=django-insecure-...  ⚠️ NOT SECURE!
│   ├── ALLOWED_HOSTS=127.0.0.1,localhost
│   └── LANGUAGE_CODE=id-ID
│
├── .gitignore                          - Git ignore rules
│   ├─ .env (keep secret!)
│   ├─ __pycache__/
│   ├─ *.pyc
│   ├─ .venv/
│   ├─ db.sqlite3 (if used)
│   └─ /staticfiles/
│
├── .idea/                              - PyCharm IDE config
│
├── .venv/                              ← VIRTUAL ENVIRONMENT
│   ├── Scripts/                        - Executables (python.exe, pip.exe)
│   ├── Lib/                            - Installed packages
│   └── (all Python dependencies)
│
├── .git/                               - Git repository (history)
│   ├─ HEAD, refs/, objects/
│   └─ (version control data)
│
├── .nvim.lua                           - Neovim editor config
│
├── manage.py                           - Django CLI (2 KB)
│   ├─ runserver (start dev server)
│   ├─ migrate (apply database migrations)
│   ├─ makemigrations (create migrations)
│   ├─ createsuperuser (create admin user)
│   ├─ collectstatic (collect static files)
│   ├─ shell (Django shell)
│   └─ shell_plus (better shell with auto-imports)
│
├── pyproject.toml                      - PROJECT METADATA & DEPENDENCIES
│   ├─ [project]
│   │  ├─ name = "sigma"
│   │  ├─ version = "0.1.0"
│   │  ├─ description = "School Management System"
│   │  └─ license = "MIT"
│   ├─ [dependencies]
│   │  ├─ Django = "5.2.6"
│   │  ├─ PyMySQL = "1.1.2"
│   │  ├─ django-environ = "*"
│   │  ├─ Tailwind = "*"
│   │  ├─ django-extensions = "*"
│   │  ├─ widget-tweaks = "*"
│   │  ├─ django-htmx = "*"
│   │  ├─ psycopg[binary] = "*"   (PostgreSQL optional)
│   │  └─ requests = "*"
│   └─ [project.optional-dependencies]
│      └─ dev = [pytest, factory-boy, ruff, basedpyright, black, django-debug-toolbar]
│
├── pytest.ini                          - Pytest configuration
│   ├─ [pytest]
│   ├─ DJANGO_SETTINGS_MODULE = config.settings
│   ├─ python_files = tests.py test_*.py *_tests.py
│   ├─ addopts = -v --tb=short
│   └─ testpaths = tests
│
├── conftest.py                         - Pytest fixtures & setup
│   ├─ Django test setup
│   ├─ Database configuration
│   ├─ Shared fixtures
│   └─ Marker definitions
│
├── completion_report.py                - Deliverables verification (1.2 KB)
│   ├─ Checks all documentation files
│   ├─ Verifies testing infrastructure
│   ├─ Validates models & views
│   └─ Generates completion report
│
├── uv.lock                             - Lock file (uv package manager)
│   └─ Exact versions of all dependencies (reproducible builds)
│
├── Procfile.tailwind                   - Tailwind build process (Heroku)
│   ├─ web: gunicorn config.wsgi
│   └─ release: python manage.py migrate
│
├── README.md                           - Project README
│   ├─ Project description
│   ├─ Setup instructions
│   ├─ Running the application
│   ├─ Database setup
│   └─ Contributing guidelines
│
├── DATABASE_DOCUMENTATION.md           - DB schema reference (NEW ✨)
│   ├─ Complete schema with ERD
│   ├─ Table descriptions
│   ├─ Relationships explained
│   └─ SQL examples
│
├── database_demo.py                    - Interactive DB demo (NEW ✨)
│   ├─ 14 demo functions
│   ├─ Shows all tables & relationships
│   ├─ Sample data queries
│   └─ Ready to run: python database_demo.py
│
├── ANALYSIS_SUMMARY.md                 - Analysis overview (NEW ✨)
│
├── INDEX.md                            - Documentation index (NEW ✨)
│
├── FILE_REFERENCE.md                   - File reference guide (NEW ✨)
│
├── START_HERE.txt                      - Quick start guide (NEW ✨)
│
├── VERIFICATION_REPORT.txt             - Verification checklist (NEW ✨)
│
└── COMPLETION_CHECKLIST.txt            - Deliverables checklist (NEW ✨)
```

---

## 🏗️ Penjelasan Tier by Tier

### **Tier 1: Configuration (config/)**
Mengatur Django: database, installed apps, middleware, security, templates.

### **Tier 2: Applications (apps/)**
4 Django apps terpisah dengan MVC pattern:
- **core**: Base infrastructure (mixins, views, dashboard)
- **users**: Authentication & user management (Akun, Peran, Siswa, Guru, Wali)
- **academics**: Academic structure (Kelas, Jadwal, Mapel)
- **grades**: Assessment (Nilai, Tugas, Presensi)

### **Tier 3: Frontend (templates/ + static/)**
- **Templates**: HTML dengan Django template language + Tailwind + DaisyUI
- **Static**: Compiled CSS (Tailwind), JavaScript (HTMX, Alpine.js)

### **Tier 4: Build System (tailwindcss_theme/)**
Kompilasi Tailwind CSS: src → dist

### **Tier 5: Testing (tests/)**
Pytest infrastructure dengan factories untuk test data generation

### **Tier 6: Documentation (docs/)**
11 comprehensive documentation files

---

## 💾 Database Architecture

```
┌──────────────────────────────────────────────────┐
│          SIGMA DATABASE (MySQL)                  │
├──────────────────────────────────────────────────┤
│                                                  │
│  USERS (6 models)                               │
│  ├─ Peran (Admin, Guru, Siswa, Wali, TU)       │
│  ├─ Akun (email-based login)                    │
│  ├─ Siswa (student profile)                     │
│  ├─ Guru (teacher profile)                      │
│  ├─ Wali (guardian profile)                     │
│  └─ SiswaWali (M:N relationship)                │
│                                                  │
│  ACADEMICS (6 models)                           │
│  ├─ TahunAjaran (academic year)                 │
│  ├─ Jurusan (major: IPA, IPS, Bahasa)          │
│  ├─ Kelas (class)                               │
│  ├─ Mapel (subject)                             │
│  ├─ KelasSiswa (class registration)             │
│  └─ Jadwal (schedule)                           │
│                                                  │
│  GRADES (3 models)                              │
│  ├─ Tugas (assignment)                          │
│  ├─ Nilai (grade)                               │
│  └─ Presensi (attendance)                       │
│                                                  │
│  Total: 15 main tables + Django system tables   │
│  Connection: MySQL @ localhost:3306             │
└──────────────────────────────────────────────────┘
```

---

## 🎨 Frontend Architecture

### **Design Stack**
```
HTML (Django templates)
  ↓
Tailwind CSS 4.1 (utility-first styling)
  ↓
DaisyUI 5.0 (pre-built components)
  ↓
HTMX 1.26 (dynamic updates, no reload)
  ↓
Alpine.js (lightweight interactivity)
  ↓
Beautiful, responsive, interactive UI ✨
```

### **Responsive Design**
- **Mobile**: Single column, hamburger menu
- **Tablet**: 2 columns, auto-hide sidebar
- **Desktop**: 3+ columns, permanent sidebar

### **Components Used**
- Buttons, Forms, Cards, Tables, Modals, Alerts, Dropdowns, etc

---

## 🔒 Authentication & Authorization

```
┌─────────────────────────────────────┐
│      AUTHENTICATION FLOW            │
├─────────────────────────────────────┤
│                                     │
│  1. Login (Email + Password)       │
│     ↓                               │
│  2. Akun model (custom user)       │
│     ├─ Email unique                 │
│     ├─ Password hashed              │
│     └─ FK to Peran (role)           │
│     ↓                               │
│  3. Session created                 │
│     ↓                               │
│  4. Access control per view        │
│     ├─ @login_required             │
│     ├─ Role-based permissions      │
│     └─ Object-level permissions    │
│     ↓                               │
│  5. User authorized to resources   │
│                                     │
└─────────────────────────────────────┘
```

### **Roles (Peran)**
- **Admin**: Full access (manage all)
- **Guru** (Teacher): Access Jadwal, Nilai, Presensi
- **Siswa** (Student): View own Jadwal, Nilai, Presensi
- **Wali** (Guardian): View child's Nilai, Presensi
- **Tata Usaha** (Administration): Data management

---

## 🚀 How Request Works (End-to-End)

```
1. User visits: /academics/kelas/

2. Django routing (config/urls.py):
   Include('apps.academics.urls')
   ↓

3. Academic URLs (apps/academics/urls.py):
   path('kelas/', KelasListView.as_view(), name='kelas-list')
   ↓

4. View Processing (apps/academics/views.py):
   - Check user permission (is_staff)
   - Query Kelas.objects.all()
   - Filter & paginate
   - Pass to template
   ↓

5. Template Rendering (templates/academics/kelas_list.html):
   - Load base.html (Tailwind + DaisyUI)
   - Loop through kelas
   - Render table
   - Add HTMX attributes
   ↓

6. Browser:
   - HTML + CSS rendered
   - JavaScript loaded (HTMX, Alpine.js)
   - Interactive elements ready
   ↓

7. User Action (filter, search):
   - HTMX sends request
   - View filters data
   - Returns HTML fragment
   - Update page (no reload)
```

---

## 📊 Model Relationships (ER Diagram)

```
Peran (Role)
  ↑
  │ FK
  │
Akun (User) ←OneToOne→ {Siswa, Guru}
  │
  ├─ Siswa ←M:M→ Kelas (via KelasSiswa)
  │  └─ Siswa ←M:M→ Wali (via SiswaWali)
  │
  └─ Guru ←M:M→ Kelas (wali_kelas)
     └─ Guru ← FK (Jadwal)

TahunAjaran
  ├─ 1:N→ Kelas
  ├─ 1:N→ KelasSiswa
  ├─ 1:N→ Jadwal
  └─ 1:N→ Siswa (optional)

Jurusan
  └─ 1:N→ Kelas

Kelas
  ├─ FK→ Jurusan
  ├─ FK→ Guru (wali_kelas)
  ├─ FK→ TahunAjaran
  ├─ 1:N→ Jadwal
  └─ M:M→ Siswa (via KelasSiswa)

Mapel (Subject)
  └─ 1:N→ Jadwal

Jadwal (Schedule)
  ├─ FK→ Kelas
  ├─ FK→ Guru
  ├─ FK→ Mapel
  ├─ FK→ TahunAjaran
  ├─ 1:N→ Tugas
  ├─ 1:N→ Nilai
  └─ 1:N→ Presensi

Tugas (Assignment)
  ├─ FK→ Jadwal
  └─ 1:N→ Nilai

Nilai (Grade)
  ├─ FK→ Siswa
  ├─ FK→ Jadwal
  └─ FK→ Tugas (optional, if tipe=Tugas)

Presensi (Attendance)
  ├─ FK→ Siswa
  └─ FK→ Jadwal
```

---

## 📱 Key Features

✅ **Email-based Authentication** (not username)  
✅ **Role-Based Access Control** (5 roles)  
✅ **Multi-app Architecture** (core, users, academics, grades)  
✅ **Modern Responsive UI** (Tailwind + DaisyUI)  
✅ **Dynamic Updates** (HTMX, no full page reload)  
✅ **Lightweight Interactivity** (Alpine.js)  
✅ **Database Integrity** (constraints, validations)  
✅ **CRUD Operations** (reusable base views)  
✅ **Admin Dashboard** (metrics, quick access)  
✅ **Testing Infrastructure** (pytest + factories)  
✅ **Comprehensive Documentation** (11+ files)  
✅ **Production-Ready** (WSGI, migrations, security headers)

---

## 🛠️ Development Commands

```powershell
# Activate virtual environment
& .venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
# OR
uv pip install -r requirements.txt

# Create superuser
python manage.py createsuperuser

# Run migrations
python manage.py migrate

# Create initial data
python manage.py seed_data
python manage.py seed_akun

# Run development server
python manage.py runserver

# Run Tailwind build
npm run dev          # Watch mode
npm run build        # Production

# Run tests
pytest tests/ -v
pytest tests/ --cov=apps

# Django shell
python manage.py shell_plus

# Access admin panel
http://127.0.0.1:8000/admin/
```

---

## 📈 Project Statistics

| Metric | Count |
|--------|-------|
| **Django Apps** | 4 |
| **Models** | 15 |
| **Views** | 30+ |
| **Templates** | 40+ |
| **CRUD Endpoints** | 60+ (4 apps × 15 operations) |
| **Test Cases** | 50+ |
| **Documentation Files** | 11+ |
| **Total Lines of Code** | 7,000+ |
| **CSS (minified+gzip)** | 5 KB |
| **Database Tables** | 14 (main) + system tables |

---

## 🎓 Tech Stack Breakdown

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Framework** | Django 5.2.6 | Web framework |
| **Language** | Python 3.14+ | Backend language |
| **Database** | MySQL 8.0 | Data storage |
| **ORM** | Django ORM | Database abstraction |
| **Frontend** | HTML + DjangoTemplate | Template language |
| **Styling** | Tailwind CSS 4.1 | Utility CSS |
| **Components** | DaisyUI 5.0 | Pre-built UI |
| **Interactivity** | HTMX 1.26 | AJAX requests |
| **Lightweight JS** | Alpine.js | DOM manipulation |
| **CSS Build** | PostCSS 8.5 | CSS processing |
| **Testing** | pytest | Test framework |
| **Fixtures** | Factory Boy | Test data |
| **Linting** | Ruff | Code quality |
| **Type Check** | BasedPyright | Static analysis |
| **Admin Panel** | Django Admin | Built-in management |
| **WSGI Server** | Gunicorn | Production server |
| **Reverse Proxy** | Nginx | Web server (optional) |

---

## 🔄 Project Workflow

```
User Interface (Browser)
  ↓ HTTP Request
Django URL Router
  ↓ Pattern Match
Django View
  ↓ Logic + DB Query
Django ORM
  ↓ SQL Query
MySQL Database
  ↓ Data Return
Django Template
  ↓ HTML Render (Tailwind + DaisyUI)
Browser (Display + HTMX/Alpine.js)
  ↓ User sees beautiful responsive UI
```

---

## ✨ WhatsApp Integration (Login Page)

**File**: `templates/registration/login.html` (Line 85)

```html
<!-- Old -->
<button>Hubungi Administrator</button>

<!-- New (WhatsApp Link) ✨ -->
<a href="https://wa.me/6281286443022?text=Halo%20Admin%20SIGMA,%20saya%20butuh%20bantuan%20login%20atau%20lupa%20password." 
   target="_blank" 
   class="btn btn-outline btn-warning w-full gap-2">
  <i class="fa-brands fa-whatsapp"></i>
  Chat WhatsApp
</a>
```

---

## 🎯 Summary

**SIGMA** adalah aplikasi Django modern, terstruktur dengan baik untuk manajemen akademik sekolah. Menggunakan teknologi terkini:
- **Backend**: Django + MySQL
- **Frontend**: Tailwind CSS + HTMX + Alpine.js
- **Architecture**: Multi-app, role-based access
- **Quality**: Testing infrastructure, documentation, security audit
- **Production-ready**: WSGI, migrations, error handling

**Siap untuk operasional sekolah terintegrasi!** 🎓✨

---

**Dibuat dengan ❤️ untuk SIGMA School Management System**

# SIGMA - Models & Database Schema

## 1. Models Summary by App

### **1.1 Core App - Abstract Models**

#### **Person** (Abstract Base Class)
Base class for Siswa, Guru, and Wali.

| Field | Type | Null | Unique | Default | Notes |
|-------|------|------|--------|---------|-------|
| `first_name` | CharField(100) | ❌ | ❌ | - | First name |
| `last_name` | CharField(100) | ❌ | ❌ | - | Last name |
| `alamat` | TextField | ❌ | ❌ | - | Address |
| `tanggal_lahir` | DateTimeField | ❌ | ❌ | - | Date of birth |
| `nomor_handphone` | CharField(20) | ❌ | ❌ | - | Phone number |
| `gender` | CharField(10, choices) | ❌ | ❌ | 'L' | 'L' (Laki-laki) or 'P' (Perempuan) |
| `created_at` | DateTimeField | ❌ | ❌ | auto_now_add | Creation timestamp |
| `updated_at` | DateTimeField | ❌ | ❌ | auto_now | Update timestamp |

**Indexes**: `[first_name, last_name, nomor_handphone]`  
**Methods**:
- `get_full_name()`: Returns "{first_name} {last_name}"
- `get_age()`: Calculates age from `tanggal_lahir`

---

### **1.2 Users App**

#### **Peran** (Roles)
Stores role/permission groups (Admin, Guru, Siswa, etc.).

| Field | Type | Null | Unique | Notes |
|-------|------|------|--------|-------|
| `nama` | CharField(255) | ❌ | ✅ | Unique role name |

**Indexes**: None (small table)

---

#### **Akun** (Custom User Model)
Custom authentication user based on email instead of username.

| Field | Type | Null | Unique | Default | Notes |
|-------|------|------|--------|---------|-------|
| `email` | EmailField | ❌ | ✅ | - | Unique email (USERNAME_FIELD) |
| `peran` | ForeignKey(Peran) | ✅ | ❌ | - | User's role (nullable) |
| `is_active` | BooleanField | ❌ | ❌ | True | Account active status |
| `is_staff` | BooleanField | ❌ | ❌ | False | Django admin access |
| `is_superuser` | BooleanField | ❌ | ❌ | False | Superuser flag |
| `created_at` | DateTimeField | ❌ | ❌ | auto_now | Creation timestamp |
| `password` | CharField | ❌ | ❌ | - | Hashed password |

**Properties** (computed):
- `is_guru`: True if peran.nama == 'Guru'
- `is_siswa`: True if peran.nama == 'Siswa'
- `is_tata_usaha`: True if peran.nama == 'Tata Usaha'
- `is_kepala_sekolah`: True if peran.nama == 'Kepala Sekolah'
- `is_admin`: True if peran.nama == 'Admin'
- `get_user_peran`: Returns peran.nama or empty string

**Manager**: `AkunManager` (custom create_user, create_superuser)

---

#### **Siswa** (Student Profile)
Extends Person, linked OneToOne to Akun.

| Field | Type | Null | Unique | Notes |
|-------|------|------|--------|-------|
| `nis` | CharField(255) | ❌ | ✅ | Student ID number |
| `akun` | OneToOneField(Akun) | ❌ | ✅ | Links to user account (PK) |
| **Inherited from Person**: first_name, last_name, alamat, tanggal_lahir, etc. | | | |

**Related Objects**:
- `KelasSiswa` (reverse FK): Classes student is enrolled in
- `SiswaWali` (reverse FK): Guardians
- `Nilai` (reverse FK): Student's grades
- `Presensi` (reverse FK): Attendance records

---

#### **Guru** (Teacher Profile)
Extends Person, linked OneToOne to Akun.

| Field | Type | Null | Unique | Notes |
|-------|------|------|--------|-------|
| `nip` | CharField(255) | ❌ | ✅ | Teacher ID number |
| `jabatan` | CharField(100) | ❌ | ❌ | Position/title |
| `akun` | OneToOneField(Akun) | ❌ | ✅ | Links to user account (PK) |

**Indexes**: `[jabatan]`  
**Related Objects**:
- `kelas_diampu` (reverse FK): Classes taught (as wali_kelas)
- `Jadwal` (reverse FK): Schedules assigned

---

#### **Wali** (Guardian)
Extends Person, no associated Akun (not a system user).

| Field | Type | Null | Unique | Notes |
|-------|------|------|--------|-------|
| **Inherited from Person**: first_name, last_name, alamat, gender, etc. | | | |

**Related Objects**:
- `SiswaWali` (reverse FK): Students with this guardian

---

#### **SiswaWali** (Student-Guardian Relationship)
M2M relationship between Siswa and Wali.

| Field | Type | Null | Unique | Notes |
|-------|------|------|--------|-------|
| `siswa` | ForeignKey(Siswa) | ❌ | ❌ | Student reference |
| `wali` | ForeignKey(Wali) | ❌ | ❌ | Guardian reference |
| `hubungan` | CharField(10, choices) | ❌ | ❌ | 'Ayah', 'Ibu', 'Wali' |

**Constraints**: `unique_together = (siswa, wali)`  
**Indexes**: `[wali, siswa]`

---

### **1.3 Academics App**

#### **TahunAjaran** (School Year)
Academic year and semester information.

| Field | Type | Null | Unique | Notes |
|-------|------|------|--------|-------|
| `tahun` | CharField(10) | ❌ | ❌ | e.g., "2024/2025" |
| `semester` | CharField(10, choices) | ❌ | ❌ | 'Ganjil' (odd) or 'Genap' (even) |
| `tanggal_mulai` | DateField | ❌ | ❌ | Start date |
| `tanggal_selesai` | DateField | ❌ | ❌ | End date |
| `is_active` | BooleanField | ❌ | ❌ | False | Currently active year |

**Constraints**: `unique_together = (tahun, semester)` → prevents duplicates  
**Related Objects**:
- `Kelas` (reverse FK): Classes in this year
- `KelasSiswa` (reverse FK): Student enrollments

---

#### **Jurusan** (Major/Program)
School major programs (e.g., IPA, IPS, Bisnis).

| Field | Type | Null | Unique | Notes |
|-------|------|------|--------|-------|
| `nama` | CharField(255) | ❌ | ❌ | Major name |
| `deskripsi` | TextField | ✅ | ❌ | Description |

**Indexes**: `nama` (db_index=True)  
**Related Objects**:
- `Kelas` (reverse FK): Classes in this major

---

#### **Kelas** (Class/Form)
Student class/form with assigned teacher and academic year.

| Field | Type | Null | Unique | Notes |
|-------|------|------|--------|-------|
| `nama` | CharField(255) | ❌ | ❌ | e.g., "XI IPA-1" |
| `jurusan` | ForeignKey(Jurusan) | ❌ | ❌ | Major assigned to class |
| `wali_kelas` | ForeignKey(Guru) | ❌ | ❌ | Class teacher (limit_choices_to: peran__nama='Guru') |
| `tahun_ajaran` | ForeignKey(TahunAjaran) | ❌ | ❌ | Academic year |

**Constraints**: `unique_together = (nama, tahun_ajaran)` → class name unique per year  
**Indexes**: `nama`, `jurusan_id`, `wali_kelas_id`, `tahun_ajaran_id`  
**Related Objects**:
- `KelasSiswa` (reverse FK): Students in class
- `Jadwal` (reverse FK): Class schedules

---

#### **Mapel** (Subject/Course)
Subjects taught in school.

| Field | Type | Null | Unique | Notes |
|-------|------|------|--------|-------|
| `nama` | CharField(255) | ❌ | ✅ | Subject name |

**Related Objects**:
- `Jadwal` (reverse FK): Schedules for this subject

---

#### **KelasSiswa** (Class Enrollment)
M2M relationship: tracks which students are in which class for each academic year.

| Field | Type | Null | Unique | Notes |
|-------|------|------|--------|-------|
| `siswa` | ForeignKey(Siswa) | ❌ | ❌ | Student reference |
| `kelas` | ForeignKey(Kelas) | ❌ | ❌ | Class reference |
| `tahun_ajaran` | ForeignKey(TahunAjaran) | ❌ | ❌ | Academic year (denormalized for convenience) |

**Constraints**: `unique_together = (siswa, kelas, tahun_ajaran)` → student in class per year once  
**Indexes**: `[kelas_id, tahun_ajaran_id]` → for filtering students by class/year

---

#### **Jadwal** (Schedule)
Class schedule: which subject is taught by which teacher on which day/time in which class.

| Field | Type | Null | Unique | Notes |
|-------|------|------|--------|-------|
| `hari` | CharField(10, choices) | ❌ | ❌ | Day (Senin-Minggu) |
| `jam_mulai` | TimeField | ❌ | ❌ | Start time (e.g., 07:00) |
| `jam_selesai` | TimeField | ❌ | ❌ | End time (e.g., 08:00) |
| `kelas` | ForeignKey(Kelas) | ❌ | ❌ | Class |
| `mapel` | ForeignKey(Mapel) | ❌ | ❌ | Subject |
| `guru` | ForeignKey(Guru) | ❌ | ❌ | Teacher |

**Constraints**:
- `unique_together = (kelas, hari, jam_mulai)` → no double-booking classes
- `unique_together = (guru, hari, jam_mulai)` → no double-booking teachers

**Indexes**: All FKs indexed  
**Related Objects**:
- `Tugas` (reverse FK): Assignments for this class/subject
- `Nilai` (reverse FK): Student grades
- `Presensi` (reverse FK): Attendance

---

### **1.4 Grades App**

#### **Tugas** (Assignment/Homework)
Assignment given in a class.

| Field | Type | Null | Unique | Notes |
|-------|------|------|--------|-------|
| `nama` | CharField(255) | ❌ | ❌ | Assignment name |
| `deskripsi` | TextField | ❌ | ❌ | Description |
| `mulai` | DateTimeField | ❌ | ❌ | Assignment start time |
| `tenggat` | DateTimeField | ❌ | ❌ | Deadline |
| `jadwal` | ForeignKey(Jadwal) | ❌ | ❌ | Related schedule (class/subject) |

**Indexes**: `nama` (db_index=True), `jadwal_id`  
**Related Objects**:
- `Nilai` (reverse FK): Grades for this assignment

---

#### **Nilai** (Student Score/Grade)
Student grade record. Tipe: Tugas, Ujian Harian (daily test), UTS (mid-term), UAS (final exam).

| Field | Type | Null | Unique | Notes |
|-------|------|------|--------|-------|
| `tipe_penilaian` | CharField(20, choices) | ❌ | ❌ | 'Tugas', 'Ujian Harian', 'UTS', 'UAS' |
| `nilai` | DecimalField(5,2) | ❌ | ❌ | Score (0-100 typically) |
| `tanggal_penilaian` | DateField | ❌ | ❌ | Assessment date |
| `siswa` | ForeignKey(Siswa) | ❌ | ❌ | Student |
| `jadwal` | ForeignKey(Jadwal) | ❌ | ❌ | Context: class+subject+teacher |
| `tugas` | ForeignKey(Tugas) | ✅ | ❌ | Assignment (if tipe='Tugas') |

**Indexes**: All FKs indexed  
**Validation** (in model.clean()):
- Non-'Tugas' grades must be unique per (siswa, jadwal, tipe_penilaian)
- 'Tugas' grades require tugas_id filled
- No duplicate 'Tugas' grades per student

---

#### **Presensi** (Attendance)
Attendance record for student in a class session.

| Field | Type | Null | Unique | Notes |
|-------|------|------|--------|-------|
| `tanggal` | DateField | ❌ | ❌ | Attendance date |
| `status` | CharField(10, choices) | ❌ | ❌ | 'Hadir', 'Sakit', 'Izin', 'Alpha' |
| `keterangan` | TextField | ✅ | ❌ | Notes (if not 'Hadir') |
| `siswa` | ForeignKey(Siswa) | ❌ | ❌ | Student |
| `jadwal` | ForeignKey(Jadwal) | ❌ | ❌ | Schedule (class context) |

**Constraints**: `unique_together = (siswa, jadwal, tanggal)` → one attendance per student per session per day  
**Indexes**: `tanggal` (db_index=True), `[jadwal_id, tanggal]`

---

## 2. Entity Relationship Diagram (Text-based)

```
┌─────────────────────────────────────────────────────────────────┐
│                      AUTHENTICATION                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│    ┌────────────┐                ┌──────────────┐                │
│    │   Akun     │◄───────────────┤   Peran      │                │
│    │ (User)     │  FK: peran     │ (Roles)      │                │
│    └────────────┘                └──────────────┘                │
│      │        │                                                   │
│      │ 1:1    └─────────┬─────────────────┐                      │
│      │                   │                 │                      │
│      ▼                   ▼                 ▼                      │
│   ┌──────────┐     ┌──────────┐      ┌──────────┐               │
│   │  Siswa   │     │   Guru   │      │   Wali   │               │
│   │(Student) │     │(Teacher) │      │(Guardian)│               │
│   └──────────┘     └──────────┘      └──────────┘               │
│        │                │                  │                     │
│        │ M:M            │ 1:M              │ M:M                 │
│        │                │                  │                     │
│        └──────┬─────────┘                  └──────────────────┐  │
│               ▼                                                │  │
│          ┌──────────────┐                      ┌─────────────┴──┤
│          │ KelasSiswa   │                      │  SiswaWali     │
│          │(Enrollment)  │                      │(S-W Rel)       │
│          └──────────────┘                      └────────────────┤
│                                                                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      ACADEMICS                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐      ┌──────────────┐                          │
│  │TahunAjaran  │      │  Jurusan     │                          │
│  │(School Year)│      │  (Major)     │                          │
│  └──────────────┘      └──────────────┘                          │
│        │                       │                                  │
│        │ FK                    │ FK                               │
│        └─────────┬─────────────┘                                │
│                  │                                                │
│                  ▼                                                │
│         ┌──────────────┐                                         │
│         │   Kelas      │◄────────────────┐                       │
│         │  (Class)     │ FK: wali_kelas  │                       │
│         └──────────────┘                 │                       │
│              │                      ┌────────┐                   │
│              │ FK                   │  Guru  │                   │
│              │ (KelasSiswa)         └────────┘                   │
│              │                           │                       │
│              ▼                           │ FK                     │
│        ┌──────────────┐                 │                       │
│        │KelasSiswa   │                 │                       │
│        │(Enrollment) │                 │                       │
│        └──────────────┘         ┌───────────┐                   │
│              │                  │  Jadwal   │◄──────┐           │
│              │ links to         │(Schedule) │       │           │
│              │ Siswa            └───────────┘       │           │
│              │                    │ FK              │           │
│              │                    │ mapel           │           │
│              │                    ▼                 │           │
│              │                ┌────────┐            │           │
│              │                │ Mapel  │            │           │
│              │                │(Subject)│           │           │
│              │                └────────┘            │           │
│              │                                  (Tugas only)     │
│              │                                      │           │
│              └──────────────────────────────────────┘           │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                       GRADES                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│     ┌──────────┐     (from academics)                           │
│     │  Siswa   │                                                 │
│     └──────────┘                                                 │
│          │                                                        │
│          │ FK                                                     │
│          └─────────┬──────────────────┐                         │
│                    │                  │                         │
│                    ▼                  ▼                         │
│            ┌─────────────┐      ┌─────────────┐                │
│            │   Nilai     │      │  Presensi   │                │
│            │   (Score)   │      │(Attendance) │                │
│            └─────────────┘      └─────────────┘                │
│                 │                      │                         │
│                 │ FK: jadwal            │ FK: jadwal             │
│                 └──────────────────┬────┘                       │
│                                    │                             │
│                                    ▼                             │
│                            ┌──────────────┐                     │
│                            │   Jadwal     │                     │
│                            │  (Schedule)  │                     │
│                            └──────────────┘                     │
│                                    │                             │
│                                    │ FK: tugas (optional in Nilai)
│                                    │                             │
│                                    ▼                             │
│                            ┌──────────────┐                     │
│                            │    Tugas     │                     │
│                            │(Assignment)  │                     │
│                            └──────────────┘                     │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Database Indexes

**Designed for Query Optimization**:

| Model | Field(s) | Type | Purpose |
|-------|---------|------|---------|
| Person | (first_name, last_name, nomor_handphone) | Multi-field | Search by name/phone |
| Jurusan | nama | Single | Search by name |
| Kelas | nama, jurusan_id, wali_kelas_id, tahun_ajaran_id | Multi-field | Filter by major, teacher, year |
| Jadwal | All FKs | Single | Join performance |
| Tugas | nama, jadwal_id | Multi-field | Search by name, filter by schedule |
| Nilai | nilai (score), siswa_id, jadwal_id, tugas_id | Multi-field | Filter by score range, student, context |
| Presensi | tanggal, [jadwal_id, tanggal] | Multi-field | Filter by date range, schedule |
| KelasSiswa | [kelas_id, tahun_ajaran_id] | Multi-field | Find students in class/year |
| SiswaWali | [wali_id, siswa_id] | Multi-field | Find students with guardian |

---

## 4. Query Optimization Notes

**Select_related (ForeignKey/OneToOne)**:
- Used in views for reducing N+1 queries
- Examples: `Siswa.objects.select_related('akun')`, `Jadwal.objects.select_related('kelas', 'mapel', 'guru')`

**Prefetch_related (M2M/Reverse FK)**:
- Not heavily used yet but recommended for large datasets
- Example: `Kelas.objects.prefetch_related('kelassiswa_set')`

**Annotate (aggregations)**:
- Used in KelasListView: `annotate(jumlah_siswa=Count('kelassiswa'))`
- Good for counts/sums without additional queries

**N+1 Risk Areas**:
- Looping through Jadwal list and accessing `.kelas.nama` — fix with select_related
- Displaying Nilai list with Jadwal → Mapel → fix with select_related chain
- Count queries on large tables — consider caching

---

## 5. Database Constraints & Unique Together

**Prevent Duplicates**:
- `TahunAjaran`: (tahun, semester) unique
- `Kelas`: (nama, tahun_ajaran) unique
- `Jadwal`: (kelas, hari, jam_mulai) + (guru, hari, jam_mulai) unique
- `KelasSiswa`: (siswa, kelas, tahun_ajaran) unique
- `Presensi`: (siswa, jadwal, tanggal) unique
- `SiswaWali`: (siswa, wali) unique

**Foreign Key Cascades**:
- Most FKs use `on_delete=models.CASCADE` (delete related objects)
- Exceptions: Kelas → Guru/Jurusan/TahunAjaran use `on_delete=models.PROTECT` (prevent deletion if in use)

---

## 6. Default User Roles (Peran)

Suggested role names to seed:
- **Admin**: Full system access
- **Guru**: Teacher (can view/edit grades, attendance, assignments for their classes)
- **Siswa**: Student (can view own grades, attendance, assignments)
- **Tata Usaha (TU)**: Administrative staff
- **Kepala Sekolah**: Principal

See `apps/users/management/commands/seed_akun.py` for seeding script.

---

## 7. Data Model Relationships Quick Reference

```python
# User → Akun → (1:1) → Siswa
siswa = Siswa.objects.get(akun__email='student@school.id')
akun = siswa.akun

# Siswa → Kelas (via KelasSiswa)
classes = siswa.kelassiswa_set.filter(tahun_ajaran__is_active=True)

# Guru → Kelas (1:M via wali_kelas FK)
guru = Guru.objects.get(akun__email='teacher@school.id')
classes_taught = guru.kelas_diampu.all()

# Kelas → Jadwal → Mapel
jadwal = Jadwal.objects.filter(kelas=kelas_obj).select_related('mapel', 'guru')

# Jadwal → Nilai (many grades for one schedule)
grades = Nilai.objects.filter(jadwal=jadwal_obj).select_related('siswa', 'tugas')

# Tugas → Nilai (multiple grades per assignment)
assignment = Tugas.objects.get(id=task_id)
grades = assignment.nilai_set.all()
```

---

## 8. Sample Data Requirements

For testing/demo purposes, seed:

```
TahunAjaran: 2024/2025 (Ganjil, Genap)
Jurusan: IPA, IPS, Bisnis (3 majors)
Mapel: Math, Physics, Chemistry, History, etc. (10+ subjects)
Kelas: XI IPA-1, XI IPA-2, XI IPS-1, etc. (6-10 classes)
Guru: 5-10 teachers with different subjects
Siswa: 20-30 students distributed across classes
```

See `apps/users/management/commands/seed_akun.py` and `apps/core/management/commands/seed_data.py`.

---

**Database Total**: ~15 models, 100+ fields, supporting 3-4 user roles and full academic lifecycle management.

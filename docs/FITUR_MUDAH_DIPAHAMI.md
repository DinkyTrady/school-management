# 📱 SIGMA App - Fitur Mudah Dipahami

## 🎯 Apa itu SIGMA?

**SIGMA** = Sistem manajemen akademik sekolah yang bisa:
- Manage user (siswa, guru, admin)
- Manage kelas & jadwal pelajaran
- Input nilai & presensi siswa
- View laporan akademik

---

## 🎮 Fitur Utama (Yang Paling Penting)

### 1. **Login / Autentikasi** 🔐
```
User bisa login dengan email + password
- Admin, Guru, Siswa, Wali, Tata Usaha
- Jika lupa password → hubungi admin via WhatsApp ✨
```

### 2. **Kelola User (Admin Only)** 👥
```
Admin bisa:
- Buat akun baru (email + password)
- Lihat daftar user
- Edit data user
- Hapus user
- Assign role (Admin, Guru, Siswa, Wali, TU)
```

### 3. **Kelola Siswa (Admin)** 👨
```
Admin bisa:
- Buat profile siswa (nama, NIS, tanggal lahir, alamat)
- Lihat daftar siswa
- Edit data siswa
- Hapus siswa
- Assign ke kelas
```

### 4. **Kelola Guru (Admin)** 👨‍🏫
```
Admin bisa:
- Buat profile guru (nama, NIP, jabatan)
- Lihat daftar guru
- Edit data guru
- Hapus guru
- Assign ke kelas (wali kelas)
```

### 5. **Kelola Kelas** 🏫
```
Admin bisa:
- Buat kelas (nama: XI-A, XI-B, dst)
- Assign jurusan (IPA, IPS, Bahasa)
- Assign wali kelas (guru)
- Lihat jumlah siswa per kelas
- Edit kelas
- Hapus kelas

Guru & Siswa bisa:
- Lihat daftar kelas
```

### 6. **Kelola Jadwal Pelajaran** 📅
```
Admin bisa:
- Buat jadwal (hari, jam, kelas, guru, mapel, ruangan)
- Edit jadwal
- Hapus jadwal
- Prevent: 1 guru tidak bisa teach 2 kelas di jam yg sama
- Prevent: 1 kelas tidak bisa punya 2 jadwal di jam yg sama

Guru bisa:
- Lihat jadwal yang diampu

Siswa bisa:
- Lihat jadwal kelas pribadi (auto-filter)
```

### 7. **Kelola Mata Pelajaran (Mapel)** 📚
```
Admin bisa:
- Buat mapel (Matematika, Bahasa, Seni, dst)
- Edit mapel
- Hapus mapel

Semua bisa:
- Lihat daftar mapel
```

### 8. **Input Nilai Siswa** 📊 (Most Important!)
```
Guru bisa:
- Input nilai siswa (Tugas, UTS, UAS, Ujian Harian)
- Edit nilai
- Hapus nilai
- Nilai scale 0-100

Siswa bisa:
- Lihat nilai pribadi
- Filter by mapel

Wali bisa:
- Lihat nilai anak
```

### 9. **Input Presensi Siswa** ✅
```
Guru bisa:
- Mark kehadiran siswa (Hadir, Sakit, Izin, Alpha)
- Edit presensi
- Hapus presensi

Siswa bisa:
- Lihat kehadiran pribadi

Wali bisa:
- Lihat kehadiran anak
```

### 10. **Kelola Tugas** 📝
```
Guru bisa:
- Buat tugas (nama, deadline, poin)
- Edit tugas
- Hapus tugas

Siswa bisa:
- Lihat tugas kelas (dengan deadline)
```

### 11. **Dashboard** 📈
```
Admin lihat:
- Total akun
- Total kelas
- Total mapel
- Total guru
- Quick access buttons (go to manage pages)

Guru & Siswa:
- Informasi personal
```

### 12. **Search & Filter** 🔍
```
User bisa:
- Search by nama, email, NIS, NIP, kelas
- Filter by role, status, kelas, tahun ajaran
- Real-time search (HTMX - no page reload!)
- See results instantly
```

### 13. **Pagination** 📄
```
List view dengan:
- 10 items per page
- Next/Prev buttons
- Page info (1-10 of 150)
- Go to page (optional)
```

---

## 👥 Role & Permissions

### 🔴 Admin - Full Access
```
✅ Manage users (create, edit, delete)
✅ Manage roles
✅ Manage students, teachers, guardians
✅ Manage academic data (class, subject, schedule)
✅ Input grades & attendance
✅ View dashboard & reports
✅ Access everything
```

### 🔵 Guru (Teacher) - Class Management
```
✅ View students
✅ View class schedule
✅ Input & view grades
✅ Input & view attendance
✅ Create assignments
✅ View report
❌ Manage users
❌ Manage roles
```

### 🟢 Siswa (Student) - Personal Academic
```
✅ View profile
✅ View schedule (auto: hanya schedule kelas pribadi)
✅ View grades (auto: hanya nilai pribadi)
✅ View assignments
✅ View attendance (auto: hanya kehadiran pribadi)
❌ Input grades
❌ Input attendance
❌ Edit anything
```

### 🟡 Wali (Guardian) - Child Monitoring
```
✅ View child profile
✅ View child schedule
✅ View child grades
✅ View child attendance
✅ View child assignments
❌ Edit anything
```

### ⚫ Tata Usaha - Admin Helper
```
✅ View all data (limited)
⚠️ Manage data (depending on config)
❌ Manage users & roles
```

---

## 🎨 UI Features

| Feature | Description |
|---------|-------------|
| **Responsive** | Works on mobile, tablet, desktop |
| **Search** | Real-time search (HTMX) |
| **Filter** | Filter by role, status, kelas, dst |
| **Pagination** | 10 items per page |
| **HTMX** | No full page reload (faster!) |
| **Modal** | Form modal, delete confirmation |
| **Tailwind CSS** | Modern, clean design |
| **DaisyUI** | Pre-built components |
| **Messages** | Success/error notifications |
| **Validation** | Form field validation |

---

## 🔐 Security

- ✅ Password hashing (aman)
- ✅ CSRF protection
- ✅ Session management
- ✅ Permission checking
- ✅ Role-based access control
- ⚠️ HTTPS (recommended but not enforced)

---

## 📊 Database Models

### User Models (6)
- Akun (user account)
- Peran (role: admin, guru, siswa, dst)
- Siswa (student profile)
- Guru (teacher profile)
- Wali (guardian profile)
- SiswaWali (student-guardian relationship)

### Academic Models (6)
- TahunAjaran (2024/2025, semester)
- Jurusan (IPA, IPS, Bahasa)
- Kelas (XI-A, XI-B, dst)
- Mapel (subject)
- KelasSiswa (enrollment)
- Jadwal (schedule)

### Grade Models (3)
- Tugas (assignment)
- Nilai (grade)
- Presensi (attendance)

**Total: 15 Models**

---

## 🚀 Workflow Contoh

### Admin Setup Awal:
```
1. Create Tahun Ajaran (2024/2025 - Ganjil)
2. Create Jurusan (IPA, IPS, Bahasa)
3. Create Guru (5-10 guru)
4. Create Kelas (XI-A, XI-B, XI-C)
5. Create Mapel (8 mapel)
6. Create Jadwal (30-40 jadwal per minggu)
7. Create Siswa (40-100 siswa)
8. Assign Siswa to Kelas
```

### Guru Input Nilai:
```
1. Login sebagai Guru
2. Go to: Grades → Nilai
3. Click: Tambah Nilai
4. Select: Siswa (from kelas yang diampu)
5. Select: Jadwal (auto-fill)
6. Select: Tipe Nilai (UTS, UAS, Tugas, dst)
7. Input: Nilai (0-100)
8. Click: Simpan
→ Siswa bisa lihat nilai di dashboard
```

### Siswa View Nilai:
```
1. Login sebagai Siswa
2. Go to: Grades → Nilai
3. System auto-filter: hanya nilai pribadi
4. View: UTS, UAS, Tugas values
5. Filter: by mapel (Matematika, Bahasa, dst)
```

---

## ✨ Fitur Spesial

### 1. **Auto-Filters untuk Student**
```
Siswa ke halaman Jadwal
→ System auto-filter: hanya jadwal kelas XI-A (siswa's kelas)
→ Tidak perlu manual filter!

Siswa ke halaman Nilai
→ System auto-filter: hanya nilai pribadi
→ Tidak bisa lihat nilai siswa lain!
```

### 2. **Real-Time Search** (HTMX)
```
Admin search: "XI-A"
→ Table instantly filter (no page reload!)
→ Show only "XI-A" classes
```

### 3. **WhatsApp Integration** ✨
```
Siswa lupa password
→ Click: "Chat WhatsApp"
→ Open: WhatsApp chat dengan admin
→ Send template message: "Halo admin..."
```

### 4. **Smart Constraints**
```
Jadwal validation:
- 1 teacher tidak bisa teach 2 classes di jam yg sama
- 1 class tidak bisa punya 2 jadwal di jam yg sama

Nilai validation:
- 1 student tidak bisa punya 2 UTS values di 1 jadwal
- Jika tipe=Tugas, tugas harus diisi

Presensi validation:
- 1 student tidak bisa punya 2 presensi di 1 jadwal di 1 hari
```

### 5. **Query Optimization**
```
App menggunakan:
- select_related() → join queries (reduce DB calls)
- prefetch_related() → optimize M:M (batch queries)
- annotate() → count data di DB level (faster!)

Result: App jalan cepat! ⚡
```

---

## 📊 Fitur Checklist

```
Authentication
  ✅ Login with email
  ✅ Password hashing
  ✅ Session management
  ✅ WhatsApp contact

User Management
  ✅ CRUD Akun
  ✅ CRUD Peran
  ✅ CRUD Siswa
  ✅ CRUD Guru
  ✅ RBAC system

Academic Management
  ✅ CRUD Tahun Ajaran
  ✅ CRUD Jurusan
  ✅ CRUD Kelas
  ✅ CRUD Mapel
  ✅ CRUD Jadwal
  ✅ Search & Filter Jadwal

Grade Management
  ✅ CRUD Tugas
  ✅ CRUD Nilai (4 types)
  ✅ CRUD Presensi
  ✅ Filter by siswa/kelas/mapel

UI/UX
  ✅ Responsive design
  ✅ Real-time search (HTMX)
  ✅ Pagination
  ✅ Modal forms
  ✅ Error messages
  ✅ Toast notifications

Security
  ✅ CSRF protection
  ✅ Password hashing
  ✅ Permission checking
  ✅ Role-based access

Database
  ✅ Query optimization
  ✅ Indexing
  ✅ Constraints
  ✅ Foreign keys

TOTAL: 40+ major features ✅
```

---

## 🎓 Kesimpulan

**SIGMA siap untuk:**
- ✅ Operasional sekolah harian
- ✅ Manage 100+ siswa
- ✅ Track nilai & presensi
- ✅ Generate laporan akademik
- ✅ Multi-user access
- ✅ Secure & reliable

**Perfect untuk presentasi ke dosen/reviewer!** 🚀

---

**File**: FITUR_APLIKASI_QUICK.md

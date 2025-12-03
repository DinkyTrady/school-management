# 📊 SIGMA Database Documentation

## Informasi Koneksi Database

```
Engine: MySQL
Host: 127.0.0.1 (localhost)
Port: 3306
Database: school_management
User: root
Password: (kosong)
```

---

## Entity Relationship Diagram (ERD)

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USERS MANAGEMENT                             │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────────┐
│     PERAN        │
├──────────────────┤
│ id (PK)          │
│ nama (UNIQUE)    │  ← Guru, Siswa, Admin, Tata Usaha, dll
└──────────────────┘
        ▲
        │ 1:N
        │
┌──────────────────┐          ┌─────────────────────┐
│      AKUN        │          │      PERSON         │
├──────────────────┤          ├─────────────────────┤
│ id (PK)          │          │ id (PK)             │
│ email (UNIQUE)   │          │ first_name          │
│ peran_id (FK)    ├──────────▶│ last_name           │
│ is_active        │          │ jenis_kelamin       │
│ is_staff         │          │ tanggal_lahir       │
│ is_superuser     │          │ alamat              │
│ created_at       │          │ no_telepon          │
└──────────────────┘          └─────────────────────┘
   │         │                        ▲  ▲  ▲
   │         │                        │  │  │
   1         │                    ┌───┘  │  └───┐
   │N        │                    │      │      │
   │         │              ┌──────────┐ │  ┌────────┐
   │         │              │  SISWA   │ │  │ GURU   │
   │         │              ├──────────┤ │  ├────────┤
   │         │              │ nis(PK)  │ │  │ nip(PK)│
   │         │              │ akun_id  │ │  │ jabatan│
   │         │              │ (FK→id)  │ │  │ akun_id│
   │         │              └──────────┘ │  └────────┘
   │         │                           │
   │         └───────────────────────────┤
   │                                     │
   │              ┌──────────────┐       │
   │              │    WALI      │       │
   │              ├──────────────┤       │
   │              │ id (PK)      │       │
   │              │ (extends     │       │
   │              │  PERSON)     │       │
   │              └──────────────┘       │
   │                    ▲                │
   │                    │ M:N            │
   │                    │                │
   │              ┌──────────────────┐   │
   │              │  SISWAWALI       │◀──┘
   │              ├──────────────────┤
   │              │ siswa_id (FK)    │
   │              │ wali_id (FK)     │
   │              │ hubungan (Ayah,  │
   │              │           Ibu,   │
   │              │           Wali)  │
   │              └──────────────────┘
   │
   └─ (1:1 Relationship via OneToOneField with CASCADE)


┌─────────────────────────────────────────────────────────────────────┐
│                      ACADEMICS MANAGEMENT                            │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────────────┐
│  TAHUNAJARAN         │
├──────────────────────┤
│ id (PK)              │
│ tahun (VARCHAR)      │  ← "2024/2025"
│ semester             │  ← "Ganjil", "Genap"
│ tanggal_mulai        │
│ tanggal_selesai      │
│ is_active            │
│ UNIQUE(tahun,semester)
└──────────────────────┘
        ▲
        │ 1:N
        │
        │                  ┌──────────────┐
        │                  │  JURUSAN     │
        │                  ├──────────────┤
        │                  │ id (PK)      │
        │                  │ nama (UNIQUE)│  ← IPA, IPS, Bahasa
        │                  │ deskripsi    │
        │                  └──────────────┘
        │                        ▲
        │                        │ 1:N
        │                        │
        │         ┌──────────────────────┐
        └────────▶│      KELAS           │
                  ├──────────────────────┤
                  │ id (PK)              │
                  │ nama                 │ ← "XI-A", "XI-B"
                  │ jurusan_id (FK)      │
                  │ wali_kelas_id (FK)   │ → GURU
                  │ tahun_ajaran_id (FK) │
                  │ UNIQUE(nama,         │
                  │    tahun_ajaran)     │
                  └──────────────────────┘
                           ▲
                    1:N    │    M:N
                           │
            ┌──────────────────────────┐
            │   KELASSISWA             │
            ├──────────────────────────┤
            │ siswa_id (FK)            │
            │ kelas_id (FK)            │
            │ tahun_ajaran_id (FK)     │
            │ UNIQUE(siswa,kelas,      │
            │    tahun_ajaran)         │
            └──────────────────────────┘
                    ▲
                    │ M:1
                    │
            ┌──────────────────────────┐
            │   SISWA (dari users)     │
            └──────────────────────────┘


           ┌──────────────┐
           │    MAPEL     │
           ├──────────────┤
           │ id (PK)      │
           │ nama (UNIQUE)│  ← Matematika, Bahasa Inggris
           └──────────────┘
                  ▲
                  │ 1:N
                  │
           ┌──────────────────────┐
           │     JADWAL           │
           ├──────────────────────┤
           │ id (PK)              │
           │ hari                 │ ← Senin, Selasa, ...
           │ jam_mulai            │
           │ jam_selesai          │
           │ kelas_id (FK)        │
           │ mapel_id (FK)        │
           │ guru_id (FK)         │ → GURU
           │ UNIQUE(kelas,hari,   │
           │    jam_mulai)        │
           │ UNIQUE(guru,hari,    │
           │    jam_mulai)        │
           └──────────────────────┘


┌─────────────────────────────────────────────────────────────────────┐
│                    GRADES & ATTENDANCE MANAGEMENT                    │
└─────────────────────────────────────────────────────────────────────┘

           ┌──────────────┐
           │    TUGAS     │
           ├──────────────┤
           │ id (PK)      │
           │ nama         │
           │ deskripsi    │
           │ mulai        │
           │ tenggat      │
           │ jadwal_id(FK)│ → JADWAL
           └──────────────┘
                  ▲
                  │ 1:N
                  │
           ┌──────────────────────┐
           │      NILAI           │
           ├──────────────────────┤
           │ id (PK)              │
           │ tipe_penilaian       │ ← Tugas, UTS, UAS, Ujian Harian
           │ nilai (DECIMAL)      │
           │ tanggal_penilaian    │
           │ siswa_id (FK)        │ → SISWA
           │ jadwal_id (FK)       │ → JADWAL
           │ tugas_id (FK, NULLABLE)
           │ UNIQUE(siswa,jadwal, │
           │    tipe_penilaian)   │
           └──────────────────────┘
                  ▲
                  │ M:1
                  │
           ┌──────────────┐
           │    SISWA     │
           └──────────────┘


           ┌──────────────────────┐
           │      PRESENSI        │
           ├──────────────────────┤
           │ id (PK)              │
           │ tanggal              │
           │ status               │ ← Hadir, Sakit, Izin, Alpha
           │ keterangan           │
           │ siswa_id (FK)        │ → SISWA
           │ jadwal_id (FK)       │ → JADWAL
           │ UNIQUE(siswa,jadwal, │
           │    tanggal)          │
           └──────────────────────┘
```

---

## Detail Tabel & Kolom

### 1. **PERAN (Roles)**
| Kolom | Tipe | Keterangan |
|-------|------|-----------|
| id | INT (PK) | Primary key |
| nama | VARCHAR(255, UNIQUE) | Nama peran: Admin, Guru, Siswa, Tata Usaha, Kepala Sekolah |

**Constraints:** UNIQUE(nama)

---

### 2. **AKUN (User Accounts)**
| Kolom | Tipe | Keterangan |
|-------|------|-----------|
| id | INT (PK) | Primary key |
| email | VARCHAR(255, UNIQUE) | Email login (username field) |
| peran_id | INT (FK) | Reference ke PERAN |
| password | VARCHAR | Hashed password |
| is_active | BOOLEAN | Status akun aktif/nonaktif |
| is_staff | BOOLEAN | Admin site access |
| is_superuser | BOOLEAN | Super admin flag |
| created_at | DATETIME | Waktu pembuatan akun |

**Indexes:** email (UNIQUE)  
**Foreign Keys:** peran_id → PERAN.id (PROTECT)

**Keterangan:** Extends Django AbstractBaseUser, menjadi user model utama sistem.

---

### 3. **PERSON (Base Class untuk User Profil)**
| Kolom | Tipe | Keterangan |
|-------|------|-----------|
| id | INT (PK) | Primary key |
| first_name | VARCHAR(150) | Nama depan |
| last_name | VARCHAR(150) | Nama belakang |
| jenis_kelamin | CHAR(1) | L atau P |
| tanggal_lahir | DATE | Tanggal lahir |
| alamat | TEXT | Alamat lengkap |
| no_telepon | VARCHAR(15) | Nomor telepon |

**Keterangan:** Abstract base model, digunakan oleh Siswa, Guru, Wali.

---

### 4. **SISWA (Students)**
| Kolom | Tipe | Keterangan |
|-------|------|-----------|
| akun_id | INT (PK, FK) | OneToOne → AKUN.id (CASCADE) |
| nis | VARCHAR(255, UNIQUE) | Nomor Induk Siswa |
| first_name | VARCHAR(150) | Inherited dari PERSON |
| last_name | VARCHAR(150) | Inherited dari PERSON |
| jenis_kelamin | CHAR(1) | Inherited dari PERSON |
| tanggal_lahir | DATE | Inherited dari PERSON |
| alamat | TEXT | Inherited dari PERSON |
| no_telepon | VARCHAR(15) | Inherited dari PERSON |

**Indexes:** nis (UNIQUE)  
**Foreign Keys:** akun_id → AKUN.id (CASCADE)

**Keterangan:** OneToOne relationship dengan AKUN (satu siswa = satu akun).

---

### 5. **GURU (Teachers)**
| Kolom | Tipe | Keterangan |
|-------|------|-----------|
| akun_id | INT (PK, FK) | OneToOne → AKUN.id (CASCADE) |
| nip | VARCHAR(255, UNIQUE) | Nomor Induk Pegawai |
| jabatan | VARCHAR(100) | Posisi: Guru, Kepala Sekolah, dll |
| first_name | VARCHAR(150) | Inherited dari PERSON |
| last_name | VARCHAR(150) | Inherited dari PERSON |
| jenis_kelamin | CHAR(1) | Inherited dari PERSON |
| tanggal_lahir | DATE | Inherited dari PERSON |
| alamat | TEXT | Inherited dari PERSON |
| no_telepon | VARCHAR(15) | Inherited dari PERSON |

**Indexes:** nip (UNIQUE), jabatan (INDEX)  
**Foreign Keys:** akun_id → AKUN.id (CASCADE)

---

### 6. **WALI (Guardians)**
| Kolom | Tipe | Keterangan |
|-------|------|-----------|
| id | INT (PK) | Primary key |
| first_name | VARCHAR(150) | Inherited dari PERSON |
| last_name | VARCHAR(150) | Inherited dari PERSON |
| jenis_kelamin | CHAR(1) | Inherited dari PERSON |
| tanggal_lahir | DATE | Inherited dari PERSON |
| alamat | TEXT | Inherited dari PERSON |
| no_telepon | VARCHAR(15) | Inherited dari PERSON |

**Keterangan:** Profil wali murid (orang tua/wali siswa).

---

### 7. **SISWAWALI (Student-Guardian Relationship)**
| Kolom | Tipe | Keterangan |
|-------|------|-----------|
| id | INT (PK) | Primary key |
| siswa_id | INT (FK) | Reference ke SISWA |
| wali_id | INT (FK) | Reference ke WALI |
| hubungan | VARCHAR(10) | Ayah, Ibu, Wali (pilihan) |

**Constraints:** UNIQUE(siswa_id, wali_id)  
**Indexes:** (wali_id, siswa_id)  
**Foreign Keys:** siswa_id → SISWA.akun_id (CASCADE), wali_id → WALI.id (CASCADE)

**Keterangan:** M:N relationship - satu siswa bisa punya banyak wali, satu wali bisa punya banyak siswa.

---

### 8. **TAHUNAJARAN (Academic Year)**
| Kolom | Tipe | Keterangan |
|-------|------|-----------|
| id | INT (PK) | Primary key |
| tahun | VARCHAR(10) | Format: "2024/2025" |
| semester | VARCHAR(10) | Ganjil atau Genap |
| tanggal_mulai | DATE | Mulai semester |
| tanggal_selesai | DATE | Akhir semester |
| is_active | BOOLEAN | Status tahun aktif (default: False) |

**Constraints:** UNIQUE(tahun, semester)

**Keterangan:** Satu tahun ajaran biasanya terdiri dari 2 semester (Ganjil & Genap).

---

### 9. **JURUSAN (Majors)**
| Kolom | Tipe | Keterangan |
|-------|------|-----------|
| id | INT (PK) | Primary key |
| nama | VARCHAR(255, UNIQUE) | IPA, IPS, Bahasa, dll |
| deskripsi | TEXT | Deskripsi jurusan |

**Indexes:** nama (UNIQUE, INDEX)

---

### 10. **KELAS (Classes)**
| Kolom | Tipe | Keterangan |
|-------|------|-----------|
| id | INT (PK) | Primary key |
| nama | VARCHAR(255) | XI-A, XI-B, XII IPA-1, dll |
| jurusan_id | INT (FK) | Reference ke JURUSAN |
| wali_kelas_id | INT (FK) | Reference ke GURU (wali kelas) |
| tahun_ajaran_id | INT (FK) | Reference ke TAHUNAJARAN |

**Constraints:** UNIQUE(nama, tahun_ajaran_id)  
**Indexes:** nama (INDEX), jurusan_id, wali_kelas_id, tahun_ajaran_id  
**Foreign Keys:**
- jurusan_id → JURUSAN.id (PROTECT)
- wali_kelas_id → GURU.akun_id (PROTECT)
- tahun_ajaran_id → TAHUNAJARAN.id (PROTECT)

**Keterangan:** Satu kelas milik satu jurusan dalam satu tahun ajaran. Dipimpin oleh satu wali kelas (guru).

---

### 11. **MAPEL (Subjects)**
| Kolom | Tipe | Keterangan |
|-------|------|-----------|
| id | INT (PK) | Primary key |
| nama | VARCHAR(255, UNIQUE) | Matematika, Bahasa Inggris, dll |

**Indexes:** nama (UNIQUE)

---

### 12. **KELASSISWA (Class Registration)**
| Kolom | Tipe | Keterangan |
|-------|------|-----------|
| id | INT (PK) | Primary key |
| siswa_id | INT (FK) | Reference ke SISWA |
| kelas_id | INT (FK) | Reference ke KELAS |
| tahun_ajaran_id | INT (FK) | Reference ke TAHUNAJARAN |

**Constraints:** UNIQUE(siswa_id, kelas_id, tahun_ajaran_id)  
**Indexes:** (kelas_id, tahun_ajaran_id)  
**Foreign Keys:**
- siswa_id → SISWA.akun_id (CASCADE)
- kelas_id → KELAS.id (CASCADE)
- tahun_ajaran_id → TAHUNAJARAN.id (CASCADE)

**Keterangan:** M:N relationship - satu siswa bisa terdaftar di satu kelas per tahun ajaran.

---

### 13. **JADWAL (Schedule)**
| Kolom | Tipe | Keterangan |
|-------|------|-----------|
| id | INT (PK) | Primary key |
| hari | VARCHAR(10) | Senin, Selasa, ..., Minggu |
| jam_mulai | TIME | Jam mulai pelajaran |
| jam_selesai | TIME | Jam selesai pelajaran |
| kelas_id | INT (FK) | Reference ke KELAS |
| mapel_id | INT (FK) | Reference ke MAPEL |
| guru_id | INT (FK) | Reference ke GURU (pengajar) |

**Constraints:**
- UNIQUE(kelas_id, hari, jam_mulai) - tidak ada jadwal ganda untuk kelas
- UNIQUE(guru_id, hari, jam_mulai) - guru tidak bisa mengajar 2 jadwal sekaligus

**Indexes:** kelas_id, mapel_id, guru_id  
**Foreign Keys:**
- kelas_id → KELAS.id (CASCADE)
- mapel_id → MAPEL.id (PROTECT)
- guru_id → GURU.akun_id (PROTECT)

**Keterangan:** Jadwal mengajar untuk setiap kelas. Hubungkan dengan siswa via KELASSISWA.

---

### 14. **TUGAS (Assignments)**
| Kolom | Tipe | Keterangan |
|-------|------|-----------|
| id | INT (PK) | Primary key |
| nama | VARCHAR(255) | Judul tugas |
| deskripsi | TEXT | Penjelasan tugas |
| mulai | DATETIME | Waktu tugas dibuka |
| tenggat | DATETIME | Deadline pengumpulan |
| jadwal_id | INT (FK) | Reference ke JADWAL |

**Indexes:** nama (INDEX), jadwal_id  
**Foreign Keys:** jadwal_id → JADWAL.id (CASCADE)

**Keterangan:** Tugas diberikan per jadwal pelajaran. Siswanya ditentukan via KELASSISWA.

---

### 15. **NILAI (Grades)**
| Kolom | Tipe | Keterangan |
|-------|------|-----------|
| id | INT (PK) | Primary key |
| tipe_penilaian | VARCHAR(20) | Tugas, UTS, UAS, Ujian Harian |
| nilai | DECIMAL(5,2) | Nilai angka (0-100) |
| tanggal_penilaian | DATE | Tanggal penilaian |
| siswa_id | INT (FK) | Reference ke SISWA |
| jadwal_id | INT (FK) | Reference ke JADWAL |
| tugas_id | INT (FK, NULL) | Reference ke TUGAS (opsional, jika tipe=Tugas) |

**Constraints:** UNIQUE(siswa_id, jadwal_id, tipe_penilaian) - satu nilai per siswa per jadwal per tipe  
**Indexes:** nilai (INDEX), siswa_id, jadwal_id, tugas_id  
**Foreign Keys:**
- siswa_id → SISWA.akun_id (PROTECT)
- jadwal_id → JADWAL.id (CASCADE)
- tugas_id → TUGAS.id (SET_NULL, nullable)

**Validasi:**
- Jika tipe_penilaian = "Tugas", maka tugas_id harus diisi.
- Jika tipe_penilaian ≠ "Tugas", tidak boleh ada duplikat untuk siswa+jadwal+tipe.

---

### 16. **PRESENSI (Attendance)**
| Kolom | Tipe | Keterangan |
|-------|------|-----------|
| id | INT (PK) | Primary key |
| tanggal | DATE | Tanggal presensi |
| status | VARCHAR(10) | Hadir, Sakit, Izin, Alpha |
| keterangan | TEXT | Alasan (opsional) |
| siswa_id | INT (FK) | Reference ke SISWA |
| jadwal_id | INT (FK) | Reference ke JADWAL |

**Constraints:** UNIQUE(siswa_id, jadwal_id, tanggal) - satu presensi per siswa per jadwal per hari  
**Indexes:** tanggal (INDEX), (jadwal_id, tanggal)  
**Foreign Keys:**
- siswa_id → SISWA.akun_id (CASCADE)
- jadwal_id → JADWAL.id (CASCADE)

---

## Alur Data Utama

### 1. **Pendaftaran & Login**
```
Admin/Guru/Siswa → AKUN (email login) + PERAN
                    ↓
                  GURU/SISWA/WALI (profil)
```

### 2. **Setup Akademik**
```
Admin → TAHUNAJARAN (aktifkan semeseter)
      → JURUSAN (IPA, IPS)
      → KELAS (XI-A, XI-B) + assign GURU (wali)
      → MAPEL (Matematika, dll)
      → JADWAL (kapan+siapa+apa)
```

### 3. **Registrasi Siswa**
```
Admin → SISWA (buat akun)
      → KELASSISWA (daftarkan ke kelas)
```

### 4. **Manajemen Nilai**
```
Guru → TUGAS (buat & publish)
     → JADWAL (tempat tugas)
     → NILAI (input nilai siswa)
```

### 5. **Manajemen Presensi**
```
Guru → JADWAL (kelas apa)
     → PRESENSI (siswa hadir/tidak)
```

---

## SQL Queries Umum

### Cek Jumlah Data
```sql
SELECT 
  (SELECT COUNT(*) FROM apps_users_akun) AS total_akun,
  (SELECT COUNT(*) FROM apps_users_peran) AS total_peran,
  (SELECT COUNT(*) FROM apps_users_siswa) AS total_siswa,
  (SELECT COUNT(*) FROM apps_users_guru) AS total_guru,
  (SELECT COUNT(*) FROM apps_academics_kelas) AS total_kelas,
  (SELECT COUNT(*) FROM apps_academics_mapel) AS total_mapel,
  (SELECT COUNT(*) FROM apps_academics_jadwal) AS total_jadwal,
  (SELECT COUNT(*) FROM apps_grades_nilai) AS total_nilai,
  (SELECT COUNT(*) FROM apps_grades_presensi) AS total_presensi;
```

### Daftar Siswa & Kelasnya
```sql
SELECT s.nis, 
       CONCAT(s.first_name, ' ', s.last_name) AS nama,
       k.nama AS kelas,
       j.nama AS jurusan
FROM apps_users_siswa s
JOIN apps_academics_kelassiswa ks ON s.akun_id = ks.siswa_id
JOIN apps_academics_kelas k ON ks.kelas_id = k.id
JOIN apps_academics_jurusan j ON k.jurusan_id = j.id
WHERE ks.tahun_ajaran_id = (SELECT id FROM apps_academics_tahunajaran WHERE is_active = 1)
ORDER BY k.nama;
```

### Jadwal Pelajaran per Kelas
```sql
SELECT k.nama AS kelas,
       j.hari,
       j.jam_mulai,
       j.jam_selesai,
       m.nama AS mapel,
       CONCAT(g.first_name, ' ', g.last_name) AS guru
FROM apps_academics_jadwal j
JOIN apps_academics_kelas k ON j.kelas_id = k.id
JOIN apps_academics_mapel m ON j.mapel_id = m.id
JOIN apps_users_guru g ON j.guru_id = g.akun_id
WHERE k.id = 1
ORDER BY j.hari, j.jam_mulai;
```

### Nilai Siswa
```sql
SELECT s.nis,
       CONCAT(s.first_name, ' ', s.last_name) AS nama,
       m.nama AS mapel,
       n.tipe_penilaian,
       n.nilai,
       n.tanggal_penilaian
FROM apps_grades_nilai n
JOIN apps_users_siswa s ON n.siswa_id = s.akun_id
JOIN apps_academics_jadwal j ON n.jadwal_id = j.id
JOIN apps_academics_mapel m ON j.mapel_id = m.id
WHERE s.akun_id = 1
ORDER BY n.tanggal_penilaian DESC;
```

### Presensi Siswa
```sql
SELECT s.nis,
       CONCAT(s.first_name, ' ', s.last_name) AS nama,
       p.tanggal,
       p.status,
       p.keterangan
FROM apps_grades_presensi p
JOIN apps_users_siswa s ON p.siswa_id = s.akun_id
WHERE p.siswa_id = 1
ORDER BY p.tanggal DESC;
```

---

## Koneksi Diagram (Visual Simplified)

```
┌─────────────────────────────────────────────────────────────────────┐
│                          SISTEM SIGMA                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  MANAJEMEN PENGGUNA              MANAJEMEN AKADEMIK                 │
│  ├─ Akun                         ├─ Tahun Ajaran                    │
│  ├─ Peran                        ├─ Jurusan                         │
│  ├─ Siswa (OneToOne ← Akun)      ├─ Kelas (FK: Guru, Jurusan)      │
│  ├─ Guru (OneToOne ← Akun)       ├─ Mapel                           │
│  └─ Wali                         ├─ KelasSiswa (M:N Siswa-Kelas)   │
│                                  └─ Jadwal (FK: Guru, Mapel, Kelas)│
│                                                                       │
│  MANAJEMEN NILAI & PRESENSI                                         │
│  ├─ Tugas (FK: Jadwal)                                              │
│  ├─ Nilai (FK: Siswa, Jadwal, Tugas)                               │
│  └─ Presensi (FK: Siswa, Jadwal)                                   │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Kesimpulan

SIGMA menggunakan struktur database relational yang:
- ✅ Mengikuti normalisasi database (3NF)
- ✅ Menggunakan foreign keys untuk relasi integrity
- ✅ Memiliki constraints unique untuk data deduplication
- ✅ Menggunakan indexes untuk performance optimization
- ✅ Mendukung role-based access control (RBAC) via tabel PERAN & AKUN
- ✅ Fleksibel untuk mengelola multiple academic years & semesters
- ✅ Track nilai & presensi per siswa per jadwal

Database siap untuk menunjang operasional sekolah modern! 📚

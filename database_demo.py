#!/usr/bin/env python3
"""
SIGMA Database Demo Script
Jalankan ini untuk menunjukkan database ke dosen secara live!

Penggunaan:
    python database_demo.py

Script ini akan:
1. Menampilkan konfigurasi database
2. Menghitung total data per tabel
3. Menampilkan sample data dari beberapa tabel
4. Menunjukkan relasi antar tabel
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings
from django.db import connection
from apps.users.models import Akun, Peran, Siswa, Guru, Wali, SiswaWali
from apps.academics.models import TahunAjaran, Jurusan, Kelas, Mapel, KelasSiswa, Jadwal
from apps.grades.models import Tugas, Nilai, Presensi


def print_header(title):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def print_subheader(title):
    """Print formatted subheader"""
    print(f"\n▶ {title}")
    print("-"*70)


def show_database_config():
    """Display database configuration"""
    print_header("DATABASE CONFIGURATION")
    
    db_config = settings.DATABASES['default']
    print(f"  Engine:   {db_config.get('ENGINE', 'N/A')}")
    print(f"  Host:     {db_config.get('HOST', 'N/A')}")
    print(f"  Port:     {db_config.get('PORT', 'N/A')}")
    print(f"  Database: {db_config.get('NAME', 'N/A')}")
    print(f"  User:     {db_config.get('USER', 'N/A')}")


def show_table_statistics():
    """Display row count for all main tables"""
    print_header("TABLE STATISTICS (Total Records)")
    
    stats = {
        "PERAN (Roles)": Peran.objects.count(),
        "AKUN (Accounts)": Akun.objects.count(),
        "SISWA (Students)": Siswa.objects.count(),
        "GURU (Teachers)": Guru.objects.count(),
        "WALI (Guardians)": Wali.objects.count(),
        "TAHUN AJARAN (Academic Year)": TahunAjaran.objects.count(),
        "JURUSAN (Major)": Jurusan.objects.count(),
        "KELAS (Class)": Kelas.objects.count(),
        "MAPEL (Subject)": Mapel.objects.count(),
        "KELASSISWA (Class Registration)": KelasSiswa.objects.count(),
        "JADWAL (Schedule)": Jadwal.objects.count(),
        "TUGAS (Assignment)": Tugas.objects.count(),
        "NILAI (Grade)": Nilai.objects.count(),
        "PRESENSI (Attendance)": Presensi.objects.count(),
    }
    
    for table, count in stats.items():
        print(f"  {table:<35} : {count:>5} records")
    
    total = sum(stats.values())
    print(f"\n  {'TOTAL':<35} : {total:>5} records")


def show_peran_list():
    """Display all roles"""
    print_header("DAFTAR PERAN (ROLES)")
    
    perans = Peran.objects.all()
    if not perans.exists():
        print("  (No roles found)")
        return
    
    for i, peran in enumerate(perans, 1):
        akun_count = Akun.objects.filter(peran=peran).count()
        print(f"  {i}. {peran.nama:<20} ({akun_count} akun)")


def show_akun_sample():
    """Display sample accounts"""
    print_header("SAMPLE AKUN (FIRST 5 ACCOUNTS)")
    
    akuns = Akun.objects.select_related('peran').all()[:5]
    if not akuns.exists():
        print("  (No accounts found)")
        return
    
    print(f"  {'No':<3} {'Email':<30} {'Peran':<15} {'Status':<10}")
    print("  " + "-"*60)
    
    for i, akun in enumerate(akuns, 1):
        peran = akun.peran.nama if akun.peran else "N/A"
        status = "Active" if akun.is_active else "Inactive"
        print(f"  {i:<3} {akun.email:<30} {peran:<15} {status:<10}")


def show_siswa_sample():
    """Display sample students with their classes"""
    print_header("SAMPLE SISWA (FIRST 5 STUDENTS)")
    
    siswas = Siswa.objects.select_related('akun').all()[:5]
    if not siswas.exists():
        print("  (No students found)")
        return
    
    print(f"  {'NIS':<10} {'Nama':<25} {'Kelas':<15}")
    print("  " + "-"*52)
    
    for siswa in siswas:
        kelas_list = siswa.kelassiswa_set.select_related('kelas').all()
        kelas_names = ", ".join([ks.kelas.nama for ks in kelas_list]) if kelas_list else "N/A"
        
        nama = siswa.get_full_name()
        print(f"  {siswa.nis:<10} {nama:<25} {kelas_names:<15}")


def show_guru_sample():
    """Display sample teachers"""
    print_header("SAMPLE GURU (FIRST 5 TEACHERS)")
    
    gurus = Guru.objects.select_related('akun').all()[:5]
    if not gurus.exists():
        print("  (No teachers found)")
        return
    
    print(f"  {'NIP':<15} {'Nama':<25} {'Jabatan':<20}")
    print("  " + "-"*62)
    
    for guru in gurus:
        nama = guru.get_full_name()
        print(f"  {guru.nip:<15} {nama:<25} {guru.jabatan:<20}")


def show_kelas_sample():
    """Display sample classes"""
    print_header("SAMPLE KELAS (FIRST 5 CLASSES)")
    
    kelas_list = Kelas.objects.select_related('jurusan', 'wali_kelas', 'tahun_ajaran').all()[:5]
    if not kelas_list.exists():
        print("  (No classes found)")
        return
    
    print(f"  {'Nama':<15} {'Jurusan':<15} {'Wali Kelas':<25} {'Tahun':<10}")
    print("  " + "-"*67)
    
    for kelas in kelas_list:
        wali_nama = kelas.wali_kelas.get_full_name()
        print(f"  {kelas.nama:<15} {kelas.jurusan.nama:<15} {wali_nama:<25} {kelas.tahun_ajaran.tahun:<10}")


def show_jadwal_sample():
    """Display sample schedules"""
    print_header("SAMPLE JADWAL (FIRST 5 SCHEDULES)")
    
    jadwals = Jadwal.objects.select_related('kelas', 'mapel', 'guru').all()[:5]
    if not jadwals.exists():
        print("  (No schedules found)")
        return
    
    print(f"  {'Kelas':<12} {'Mapel':<20} {'Hari':<10} {'Jam':<12} {'Guru':<20}")
    print("  " + "-"*75)
    
    for jadwal in jadwals:
        jam = f"{jadwal.jam_mulai.strftime('%H:%M')}-{jadwal.jam_selesai.strftime('%H:%M')}"
        guru_nama = jadwal.guru.get_full_name()
        print(f"  {jadwal.kelas.nama:<12} {jadwal.mapel.nama:<20} {jadwal.hari:<10} {jam:<12} {guru_nama:<20}")


def show_nilai_sample():
    """Display sample grades"""
    print_header("SAMPLE NILAI (FIRST 5 GRADES)")
    
    nilais = Nilai.objects.select_related('siswa', 'jadwal__mapel').all()[:5]
    if not nilais.exists():
        print("  (No grades found)")
        return
    
    print(f"  {'Siswa':<25} {'Mapel':<20} {'Tipe':<15} {'Nilai':<8}")
    print("  " + "-"*70)
    
    for nilai in nilais:
        siswa_nama = nilai.siswa.get_full_name()
        mapel = nilai.jadwal.mapel.nama if nilai.jadwal.mapel else "N/A"
        print(f"  {siswa_nama:<25} {mapel:<20} {nilai.tipe_penilaian:<15} {nilai.nilai:<8}")


def show_presensi_sample():
    """Display sample attendance"""
    print_header("SAMPLE PRESENSI (FIRST 5 ATTENDANCE)")
    
    presnesis = Presensi.objects.select_related('siswa', 'jadwal__mapel').all()[:5]
    if not presnesis.exists():
        print("  (No attendance found)")
        return
    
    print(f"  {'Siswa':<25} {'Mapel':<20} {'Tanggal':<15} {'Status':<10}")
    print("  " + "-"*72)
    
    for presensi in presnesis:
        siswa_nama = presensi.siswa.get_full_name()
        mapel = presensi.jadwal.mapel.nama if presensi.jadwal.mapel else "N/A"
        print(f"  {siswa_nama:<25} {mapel:<20} {presensi.tanggal:<15} {presensi.status:<10}")


def show_relasi_example():
    """Show data relationship example"""
    print_header("CONTOH RELASI DATA")
    
    print_subheader("1. Akun → Peran (Relationship)")
    akun = Akun.objects.select_related('peran').filter(peran__isnull=False).first()
    if akun:
        print(f"  Akun: {akun.email}")
        print(f"  └─ Peran: {akun.peran.nama}")
    
    print_subheader("2. Siswa → Akun → Peran (OneToOne + FK)")
    siswa = Siswa.objects.select_related('akun__peran').first()
    if siswa:
        print(f"  Siswa: {siswa.get_full_name()} (NIS: {siswa.nis})")
        print(f"  └─ Akun: {siswa.akun.email}")
        print(f"     └─ Peran: {siswa.akun.peran.nama if siswa.akun.peran else 'N/A'}")
    
    print_subheader("3. Siswa → Kelas (via KelasSiswa)")
    siswa = Siswa.objects.prefetch_related('kelassiswa_set__kelas').first()
    if siswa:
        print(f"  Siswa: {siswa.get_full_name()}")
        kelas_list = siswa.kelassiswa_set.all()
        if kelas_list.exists():
            for ks in kelas_list[:3]:
                print(f"  └─ Kelas: {ks.kelas.nama} (Tahun: {ks.tahun_ajaran.tahun})")
        else:
            print(f"  └─ (Belum terdaftar di kelas manapun)")
    
    print_subheader("4. Kelas → Jadwal → Mapel & Guru")
    kelas = Kelas.objects.prefetch_related('jadwal_set__mapel', 'jadwal_set__guru').first()
    if kelas:
        print(f"  Kelas: {kelas.nama}")
        jadwals = kelas.jadwal_set.all()
        if jadwals.exists():
            for jadwal in jadwals[:2]:
                print(f"  ├─ {jadwal.hari} {jadwal.jam_mulai}: {jadwal.mapel.nama} (Guru: {jadwal.guru.get_full_name()})")
        else:
            print(f"  └─ (Belum ada jadwal)")
    
    print_subheader("5. Siswa → Nilai (per Mapel)")
    siswa = Siswa.objects.prefetch_related('nilai_set__jadwal__mapel').first()
    if siswa:
        print(f"  Siswa: {siswa.get_full_name()}")
        nilais = siswa.nilai_set.all()
        if nilais.exists():
            for nilai in nilais[:3]:
                print(f"  ├─ {nilai.jadwal.mapel.nama}: {nilai.nilai} ({nilai.tipe_penilaian})")
        else:
            print(f"  └─ (Belum ada nilai)")


def show_database_stats_advanced():
    """Show advanced statistics"""
    print_header("ADVANCED STATISTICS")
    
    # Active academic year
    print_subheader("Tahun Ajaran Aktif")
    active_year = TahunAjaran.objects.filter(is_active=True).first()
    if active_year:
        print(f"  Tahun: {active_year.tahun}")
        print(f"  Semester: {active_year.semester}")
        print(f"  Periode: {active_year.tanggal_mulai} s/d {active_year.tanggal_selesai}")
        
        kelas_count = Kelas.objects.filter(tahun_ajaran=active_year).count()
        siswa_count = KelasSiswa.objects.filter(tahun_ajaran=active_year).count()
        print(f"  Jumlah Kelas: {kelas_count}")
        print(f"  Jumlah Siswa (registered): {siswa_count}")
    else:
        print("  (Tidak ada tahun ajaran aktif)")
    
    # Nilai statistics
    print_subheader("Statistik Nilai")
    if Nilai.objects.exists():
        avg_nilai = Nilai.objects.extra(select={'avg': 'AVG(nilai)'}).values('avg').first()['avg']
        max_nilai = Nilai.objects.order_by('-nilai').first()
        print(f"  Rata-rata nilai: {avg_nilai:.2f}")
        print(f"  Nilai tertinggi: {max_nilai.nilai} ({max_nilai.siswa.get_full_name()})")
    else:
        print("  (Belum ada data nilai)")
    
    # Presensi statistics
    print_subheader("Statistik Presensi")
    if Presensi.objects.exists():
        hadir_count = Presensi.objects.filter(status='Hadir').count()
        sakit_count = Presensi.objects.filter(status='Sakit').count()
        izin_count = Presensi.objects.filter(status='Izin').count()
        alpha_count = Presensi.objects.filter(status='Alpha').count()
        total_presensi = Presensi.objects.count()
        
        print(f"  Total Presensi: {total_presensi}")
        print(f"  ├─ Hadir: {hadir_count} ({hadir_count/total_presensi*100:.1f}%)")
        print(f"  ├─ Sakit: {sakit_count} ({sakit_count/total_presensi*100:.1f}%)")
        print(f"  ├─ Izin: {izin_count} ({izin_count/total_presensi*100:.1f}%)")
        print(f"  └─ Alpha: {alpha_count} ({alpha_count/total_presensi*100:.1f}%)")
    else:
        print("  (Belum ada data presensi)")


def main():
    """Main function"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "SIGMA DATABASE DEMO - LIVE PRESENTATION" + " "*14 + "║")
    print("║" + " "*20 + "untuk presentasi ke dosen/reviewer" + " "*15 + "║")
    print("╚" + "="*68 + "╝")
    
    # Run all demo functions
    show_database_config()
    show_table_statistics()
    show_peran_list()
    show_akun_sample()
    show_siswa_sample()
    show_guru_sample()
    show_kelas_sample()
    show_jadwal_sample()
    show_nilai_sample()
    show_presensi_sample()
    show_relasi_example()
    show_database_stats_advanced()
    
    # Summary
    print_header("KESIMPULAN PRESENTASI")
    print("""
  ✓ Database MySQL "school_management" berisi data akademik lengkap
  ✓ 14 tabel utama dengan relasi yang terstruktur (normalisasi 3NF)
  ✓ Mendukung multi-user dengan role-based access control (RBAC)
  ✓ Fitur lengkap: Akun, Siswa, Guru, Kelas, Jadwal, Nilai, Presensi
  ✓ Constraints & indexes untuk data integrity & performance
  ✓ Siap untuk operasional sekolah modern dengan sistem terintegrasi
    """)
    
    print("="*70)
    print(f"  Demo selesai! Database siap untuk presentasi ke dosen.")
    print("="*70 + "\n")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

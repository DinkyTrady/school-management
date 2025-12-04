import datetime

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.academics.models import Jurusan, Kelas, Mapel, TahunAjaran, Jadwal, KelasSiswa
from apps.grades.models import Nilai, Presensi, Tugas
from apps.users.models import Akun, Guru, Peran, Siswa, SiswaWali, Wali


class Command(BaseCommand):
    help = "Seed the database with initial and dummy data"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting database seeding..."))

        peran_map = self._seed_peran()
        self._seed_superuser(peran_map)

        jurusan_map = self._seed_jurusan()
        tahun_ajaran_map = self._seed_tahun_ajaran()
        mapel_map = self._seed_mapel()

        guru_map = self._seed_guru(peran_map)
        siswa_map, wali_map = self._seed_siswa_dan_wali(peran_map)

        kelas_map = self._seed_kelas(jurusan_map, guru_map, tahun_ajaran_map)
        self._seed_kelas_siswa(siswa_map, kelas_map, tahun_ajaran_map)

        jadwal_map = self._seed_jadwal(kelas_map, mapel_map, guru_map)

        tugas_map = self._seed_tugas(jadwal_map)
        self._seed_nilai(siswa_map, jadwal_map, tugas_map)
        self._seed_presensi(siswa_map, jadwal_map)

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))

    def _seed_peran(self):
        self.stdout.write("Seeding Peran...")
        peran_data = ["Admin", "Guru", "Siswa", "Tata Usaha", "Kepala Sekolah"]
        peran_map = {}
        for nama_peran in peran_data:
            peran, created = Peran.objects.get_or_create(nama=nama_peran)
            peran_map[nama_peran] = peran
            self._log_creation(created, "Peran", nama_peran)
        return peran_map

    def _seed_superuser(self, peran_map):
        self.stdout.write("Seeding Superuser...")
        if not Akun.objects.filter(email="admin@sekolah.com").exists():
            Akun.objects.create_superuser(
                email="admin@sekolah.com",
                password="admin123",
                peran=peran_map["Admin"],
            )
            self.stdout.write(self.style.SUCCESS("  Created Superuser: admin@sekolah.com"))
        else:
            self.stdout.write("  Superuser already exists: admin@sekolah.com")

    def _seed_jurusan(self):
        self.stdout.write("Seeding Jurusan...")
        jurusan_data = ["Ilmu Pengetahuan Alam", "Ilmu Pengetahuan Sosial", "Bahasa"]
        jurusan_map = {}
        for nama_jurusan in jurusan_data:
            jurusan, created = Jurusan.objects.get_or_create(nama=nama_jurusan)
            jurusan_map[nama_jurusan] = jurusan
            self._log_creation(created, "Jurusan", nama_jurusan)
        return jurusan_map

    def _seed_tahun_ajaran(self):
        self.stdout.write("Seeding Tahun Ajaran...")
        tahun_ajaran_data = [("2024/2025", "Ganjil"), ("2024/2025", "Genap")]
        tahun_ajaran_map = {}
        for tahun, semester in tahun_ajaran_data:
            is_active = (tahun == "2024/2025" and semester == "Ganjil")
            ta, created = TahunAjaran.objects.get_or_create(
                tahun=tahun,
                semester=semester,
                defaults={
                    "tanggal_mulai": datetime.date(2024, 7, 1) if semester == "Ganjil" else datetime.date(2025, 1, 1),
                    "tanggal_selesai": datetime.date(2024, 12, 31) if semester == "Ganjil" else datetime.date(2025, 6, 30),
                    "is_active": is_active,
                },
            )
            # Ensure active status is correct if object already exists
            if not created and is_active and not ta.is_active:
                # Deactivate others if we are activating this one
                TahunAjaran.objects.filter(is_active=True).update(is_active=False)
                ta.is_active = True
                ta.save()
                
            key = f"{tahun}-{semester}"
            tahun_ajaran_map[key] = ta
            self._log_creation(created, "Tahun Ajaran", key)
        return tahun_ajaran_map

    def _seed_mapel(self):
        self.stdout.write("Seeding Mapel...")
        mapel_data = ["Matematika", "Bahasa Indonesia", "Fisika", "Kimia", "Biologi"]
        mapel_map = {}
        for nama_mapel in mapel_data:
            mapel, created = Mapel.objects.get_or_create(nama=nama_mapel)
            mapel_map[nama_mapel] = mapel
            self._log_creation(created, "Mapel", nama_mapel)
        return mapel_map

    def _seed_guru(self, peran_map):
        self.stdout.write("Seeding Guru...")
        guru_map = {}
        guru_data = [
            {
                "email": "budi.guru@sekolah.com",
                "first_name": "Budi",
                "last_name": "Prasetyo",
                "nip": "198001012005011001",
                "jabatan": "Guru Matematika",
            },
            {
                "email": "siti.guru@sekolah.com",
                "first_name": "Siti",
                "last_name": "Rahayu",
                "nip": "198505052010012002",
                "jabatan": "Guru Bahasa Indonesia",
            },
        ]
        for data in guru_data:
            akun, created = Akun.objects.get_or_create(
                email=data["email"], defaults={"peran": peran_map["Guru"]}
            )
            if created:
                akun.set_password("guru123")
                akun.save()

            guru, guru_created = Guru.objects.get_or_create(
                akun=akun,
                defaults={
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                    "nip": data["nip"],
                    "jabatan": data["jabatan"],
                    "gender": "L" if data["first_name"] == "Budi" else "P",
                    "alamat": f"Jl. Guru No. {len(guru_map) + 1}",
                    "tanggal_lahir": datetime.datetime(1980, 1, 1, 0, 0, 0),
                    "nomor_handphone": f"08121111000{len(guru_map) + 1}",
                },
            )
            guru_map[data["email"]] = guru
            self._log_creation(guru_created, "Guru", data["email"])
        return guru_map

    def _seed_siswa_dan_wali(self, peran_map):
        self.stdout.write("Seeding Siswa, Wali, and Hubungan...")
        siswa_map = {}
        wali_map = {}
        siswa_data = [
            {
                "email": "andi.siswa@sekolah.com",
                "first_name": "Andi",
                "last_name": "Setiawan",
                "nis": "NIS001",
                "wali_nama": "Bambang Setiawan",
            },
            {
                "email": "bunga.siswa@sekolah.com",
                "first_name": "Bunga",
                "last_name": "Lestari",
                "nis": "NIS002",
                "wali_nama": "Siti Aminah",
            },
        ]
        for data in siswa_data:
            akun, created = Akun.objects.get_or_create(
                email=data["email"], defaults={"peran": peran_map["Siswa"]}
            )
            if created:
                akun.set_password("siswa123")
                akun.save()

            siswa, siswa_created = Siswa.objects.get_or_create(
                akun=akun,
                defaults={
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                    "nis": data["nis"],
                    "gender": "L" if data["first_name"] == "Andi" else "P",
                    "alamat": f"Jl. Siswa No. {len(siswa_map) + 1}",
                    "tanggal_lahir": datetime.datetime(2008, 3, 15, 0, 0, 0),
                    "nomor_handphone": f"08132222000{len(siswa_map) + 1}",
                },
            )
            siswa_map[data["email"]] = siswa
            self._log_creation(siswa_created, "Siswa", data["email"])

            wali_nama_parts = data["wali_nama"].split(" ", 1)
            wali, wali_created = Wali.objects.get_or_create(
                first_name=wali_nama_parts[0],
                last_name=wali_nama_parts[1] if len(wali_nama_parts) > 1 else "",
                defaults={
                    "nomor_handphone": f"08563333000{len(wali_map) + 1}",
                    "alamat": siswa.alamat,
                    "tanggal_lahir": datetime.datetime(1975, 5, 10, 0, 0, 0),
                    "gender": "L",
                },
            )
            wali_map[data["wali_nama"]] = wali
            self._log_creation(wali_created, "Wali", data["wali_nama"])

            _, hub_created = SiswaWali.objects.get_or_create(
                siswa=siswa, wali=wali, defaults={"hubungan": "Ayah"}
            )
            self._log_creation(hub_created, "Hubungan", f"{siswa.first_name} -> {wali.first_name}")
        return siswa_map, wali_map

    def _seed_kelas(self, jurusan_map, guru_map, tahun_ajaran_map):
        self.stdout.write("Seeding Kelas...")
        kelas_map = {}
        kelas_data = [
            {
                "nama": "X IPA 1",
                "jurusan": "Ilmu Pengetahuan Alam",
                "wali_kelas_email": "budi.guru@sekolah.com",
                "tahun_ajaran": "2024/2025-Ganjil",
            }
        ]
        for data in kelas_data:
            kelas, created = Kelas.objects.get_or_create(
                nama=data["nama"],
                tahun_ajaran=tahun_ajaran_map[data["tahun_ajaran"]],
                defaults={
                    "jurusan": jurusan_map[data["jurusan"]],
                    "wali_kelas": guru_map[data["wali_kelas_email"]],
                },
            )
            kelas_map[data["nama"]] = kelas
            self._log_creation(created, "Kelas", data["nama"])
        return kelas_map

    def _seed_kelas_siswa(self, siswa_map, kelas_map, tahun_ajaran_map):
        self.stdout.write("Seeding KelasSiswa...")
        
        # Ambil kelas pertama yang tersedia untuk diisi siswa
        target_kelas = list(kelas_map.values())[0]
        # Gunakan tahun ajaran dari kelas tersebut
        target_ta = target_kelas.tahun_ajaran

        for siswa in siswa_map.values():
            _, created = KelasSiswa.objects.get_or_create(  # Langsung create objek KelasSiswa
                siswa=siswa,
                kelas=target_kelas,
                tahun_ajaran=target_ta,
            )
            self._log_creation(created, "KelasSiswa", f"{siswa.first_name} -> {target_kelas.nama}")


    def _seed_jadwal(self, kelas_map, mapel_map, guru_map):
        self.stdout.write("Seeding Jadwal...")
        jadwal_map = {}
        jadwal_data = [
            {
                "hari": "Senin",
                "jam_mulai": "07:00",
                "jam_selesai": "08:30",
                "kelas": "X IPA 1",
                "mapel": "Matematika",
                "guru_email": "budi.guru@sekolah.com",
            },
            {
                "hari": "Senin",
                "jam_mulai": "08:30",
                "jam_selesai": "10:00",
                "kelas": "X IPA 1",
                "mapel": "Bahasa Indonesia",
                "guru_email": "siti.guru@sekolah.com",
            },
        ]
        for data in jadwal_data:
            jadwal, created = Jadwal.objects.get_or_create(
                hari=data["hari"],
                jam_mulai=data["jam_mulai"],
                kelas=kelas_map[data["kelas"]],
                defaults={
                    "jam_selesai": data["jam_selesai"],
                    "mapel": mapel_map[data["mapel"]],
                    "guru": guru_map[data["guru_email"]],
                },
            )
            key = f"{data['kelas']}-{data['hari']}-{data['jam_mulai']}"
            jadwal_map[key] = jadwal
            self._log_creation(created, "Jadwal", key)
        return jadwal_map

    def _seed_tugas(self, jadwal_map):
        self.stdout.write("Seeding Tugas...")
        tugas_map = {}
        jadwal_matematika = list(jadwal_map.values())[0]
        tugas, created = Tugas.objects.get_or_create(
            nama="Tugas Aljabar Bab 1",
            jadwal=jadwal_matematika,
            defaults={
                "deskripsi": "Kerjakan soal latihan 1.1 di buku paket halaman 10.",
                "mulai": datetime.datetime.now(),
                "tenggat": datetime.datetime.now() + datetime.timedelta(days=7),
            },
        )
        tugas_map["Tugas Aljabar Bab 1"] = tugas
        self._log_creation(created, "Tugas", tugas.nama)
        return tugas_map

    def _seed_nilai(self, siswa_map, jadwal_map, tugas_map):
        self.stdout.write("Seeding Nilai...")
        siswa_andi = list(siswa_map.values())[0]
        jadwal_matematika = list(jadwal_map.values())[0]
        tugas_aljabar = list(tugas_map.values())[0]

        _, created = Nilai.objects.get_or_create(
            siswa=siswa_andi,
            jadwal=jadwal_matematika,
            tipe_penilaian="Tugas",
            tugas=tugas_aljabar,
            defaults={"nilai": 85.50, "tanggal_penilaian": datetime.date.today()},
        )
        self._log_creation(created, "Nilai", f"{siswa_andi.first_name} - Matematika")

    def _seed_presensi(self, siswa_map, jadwal_map):
        self.stdout.write("Seeding Presensi...")
        siswa_andi = list(siswa_map.values())[0]
        jadwal_matematika = list(jadwal_map.values())[0]
        _, created = Presensi.objects.get_or_create(
            siswa=siswa_andi,
            jadwal=jadwal_matematika,
            tanggal=datetime.date.today(),
            defaults={"status": "Hadir"},
        )
        self._log_creation(created, "Presensi", f"{siswa_andi.first_name} - Matematika")

    def _log_creation(self, created, model_name, instance_name):
        if created:
            self.stdout.write(self.style.SUCCESS(f"  Created {model_name}: {instance_name}"))
        else:
            self.stdout.write(f"  {model_name} already exists: {instance_name}")

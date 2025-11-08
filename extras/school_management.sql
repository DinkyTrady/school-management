/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-12.0.2-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: school_management
-- ------------------------------------------------------
-- Server version	12.0.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Current Database: `school_management`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `school_management` /*!40100 DEFAULT CHARACTER SET utf8mb3 COLLATE utf8mb3_uca1400_ai_ci */;

USE `school_management`;

--
-- Table structure for table `academics_jadwal`
--

DROP TABLE IF EXISTS `academics_jadwal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `academics_jadwal` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `hari` varchar(10) NOT NULL,
  `jam_mulai` time(6) NOT NULL,
  `jam_selesai` time(6) NOT NULL,
  `guru_id` bigint(20) NOT NULL,
  `kelas_id` bigint(20) NOT NULL,
  `mapel_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_class_schedule_time` (`kelas_id`,`hari`,`jam_mulai`),
  UNIQUE KEY `unique_teacher_schedule_time` (`guru_id`,`hari`,`jam_mulai`),
  KEY `academics_jadwal_mapel_id_4d02ad93_fk_academics_mapel_id` (`mapel_id`),
  CONSTRAINT `academics_jadwal_guru_id_b1129535_fk_users_guru_akun_id` FOREIGN KEY (`guru_id`) REFERENCES `users_guru` (`akun_id`),
  CONSTRAINT `academics_jadwal_kelas_id_a5bb18bb_fk_academics_kelas_id` FOREIGN KEY (`kelas_id`) REFERENCES `academics_kelas` (`id`),
  CONSTRAINT `academics_jadwal_mapel_id_4d02ad93_fk_academics_mapel_id` FOREIGN KEY (`mapel_id`) REFERENCES `academics_mapel` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `academics_jadwal`
--

LOCK TABLES `academics_jadwal` WRITE;
/*!40000 ALTER TABLE `academics_jadwal` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `academics_jadwal` VALUES
(1,'Senin','07:00:00.000000','08:30:00.000000',2,1,1),
(2,'Senin','08:30:00.000000','10:00:00.000000',3,1,2);
/*!40000 ALTER TABLE `academics_jadwal` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `academics_jurusan`
--

DROP TABLE IF EXISTS `academics_jurusan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `academics_jurusan` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nama` varchar(255) NOT NULL,
  `deskripsi` longtext DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `academics_jurusan_nama_7a770b6d` (`nama`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `academics_jurusan`
--

LOCK TABLES `academics_jurusan` WRITE;
/*!40000 ALTER TABLE `academics_jurusan` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `academics_jurusan` VALUES
(1,'Ilmu Pengetahuan Alam',NULL),
(2,'Ilmu Pengetahuan Sosial',NULL),
(3,'Bahasa',NULL);
/*!40000 ALTER TABLE `academics_jurusan` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `academics_kelas`
--

DROP TABLE IF EXISTS `academics_kelas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `academics_kelas` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nama` varchar(255) NOT NULL,
  `jurusan_id` bigint(20) NOT NULL,
  `wali_kelas_id` bigint(20) NOT NULL,
  `tahun_ajaran_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_class_period` (`nama`,`tahun_ajaran_id`),
  KEY `academics_kelas_nama_87b0007f` (`nama`),
  KEY `academics_kelas_jurusan_id_e670e432_fk_academics_jurusan_id` (`jurusan_id`),
  KEY `academics_kelas_wali_kelas_id_1555b3e3_fk_users_guru_akun_id` (`wali_kelas_id`),
  KEY `academics_kelas_tahun_ajaran_id_71fa26ca_fk_academics` (`tahun_ajaran_id`),
  CONSTRAINT `academics_kelas_jurusan_id_e670e432_fk_academics_jurusan_id` FOREIGN KEY (`jurusan_id`) REFERENCES `academics_jurusan` (`id`),
  CONSTRAINT `academics_kelas_tahun_ajaran_id_71fa26ca_fk_academics` FOREIGN KEY (`tahun_ajaran_id`) REFERENCES `academics_tahunajaran` (`id`),
  CONSTRAINT `academics_kelas_wali_kelas_id_1555b3e3_fk_users_guru_akun_id` FOREIGN KEY (`wali_kelas_id`) REFERENCES `users_guru` (`akun_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `academics_kelas`
--

LOCK TABLES `academics_kelas` WRITE;
/*!40000 ALTER TABLE `academics_kelas` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `academics_kelas` VALUES
(1,'X IPA 1',1,2,1);
/*!40000 ALTER TABLE `academics_kelas` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `academics_kelassiswa`
--

DROP TABLE IF EXISTS `academics_kelassiswa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `academics_kelassiswa` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `kelas_id` bigint(20) NOT NULL,
  `siswa_id` bigint(20) NOT NULL,
  `tahun_ajaran_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `academics_kelassiswa_siswa_id_kelas_id_tahun__dbdba28f_uniq` (`siswa_id`,`kelas_id`,`tahun_ajaran_id`),
  KEY `academics_kelassiswa_tahun_ajaran_id_8236c924_fk_academics` (`tahun_ajaran_id`),
  KEY `academics_k_kelas_i_6272db_idx` (`kelas_id`,`tahun_ajaran_id`),
  CONSTRAINT `academics_kelassiswa_kelas_id_3c262a4d_fk_academics_kelas_id` FOREIGN KEY (`kelas_id`) REFERENCES `academics_kelas` (`id`),
  CONSTRAINT `academics_kelassiswa_siswa_id_71ed679a_fk_users_siswa_akun_id` FOREIGN KEY (`siswa_id`) REFERENCES `users_siswa` (`akun_id`),
  CONSTRAINT `academics_kelassiswa_tahun_ajaran_id_8236c924_fk_academics` FOREIGN KEY (`tahun_ajaran_id`) REFERENCES `academics_tahunajaran` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `academics_kelassiswa`
--

LOCK TABLES `academics_kelassiswa` WRITE;
/*!40000 ALTER TABLE `academics_kelassiswa` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `academics_kelassiswa` VALUES
(1,1,4,1),
(2,1,5,1);
/*!40000 ALTER TABLE `academics_kelassiswa` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `academics_mapel`
--

DROP TABLE IF EXISTS `academics_mapel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `academics_mapel` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nama` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `academics_mapel_nama_5f945f91` (`nama`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `academics_mapel`
--

LOCK TABLES `academics_mapel` WRITE;
/*!40000 ALTER TABLE `academics_mapel` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `academics_mapel` VALUES
(2,'Bahasa Indonesia'),
(5,'Biologi'),
(3,'Fisika'),
(4,'Kimia'),
(1,'Matematika');
/*!40000 ALTER TABLE `academics_mapel` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `academics_tahunajaran`
--

DROP TABLE IF EXISTS `academics_tahunajaran`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `academics_tahunajaran` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `tahun` varchar(10) NOT NULL,
  `semester` varchar(10) NOT NULL,
  `tanggal_mulai` date NOT NULL,
  `tanggal_selesai` date NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_academic_period` (`tahun`,`semester`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `academics_tahunajaran`
--

LOCK TABLES `academics_tahunajaran` WRITE;
/*!40000 ALTER TABLE `academics_tahunajaran` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `academics_tahunajaran` VALUES
(1,'2024/2025','Ganjil','2024-07-01','2024-12-31',0),
(2,'2024/2025','Genap','2025-01-01','2025-06-30',0);
/*!40000 ALTER TABLE `academics_tahunajaran` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `auth_permission` VALUES
(1,'Can add log entry',1,'add_logentry'),
(2,'Can change log entry',1,'change_logentry'),
(3,'Can delete log entry',1,'delete_logentry'),
(4,'Can view log entry',1,'view_logentry'),
(5,'Can add permission',2,'add_permission'),
(6,'Can change permission',2,'change_permission'),
(7,'Can delete permission',2,'delete_permission'),
(8,'Can view permission',2,'view_permission'),
(9,'Can add group',3,'add_group'),
(10,'Can change group',3,'change_group'),
(11,'Can delete group',3,'delete_group'),
(12,'Can view group',3,'view_group'),
(13,'Can add content type',4,'add_contenttype'),
(14,'Can change content type',4,'change_contenttype'),
(15,'Can delete content type',4,'delete_contenttype'),
(16,'Can view content type',4,'view_contenttype'),
(17,'Can add session',5,'add_session'),
(18,'Can change session',5,'change_session'),
(19,'Can delete session',5,'delete_session'),
(20,'Can view session',5,'view_session'),
(21,'Can add akun',6,'add_akun'),
(22,'Can change akun',6,'change_akun'),
(23,'Can delete akun',6,'delete_akun'),
(24,'Can view akun',6,'view_akun'),
(25,'Can add peran',7,'add_peran'),
(26,'Can change peran',7,'change_peran'),
(27,'Can delete peran',7,'delete_peran'),
(28,'Can view peran',7,'view_peran'),
(29,'Can add wali',8,'add_wali'),
(30,'Can change wali',8,'change_wali'),
(31,'Can delete wali',8,'delete_wali'),
(32,'Can view wali',8,'view_wali'),
(33,'Can add siswa',9,'add_siswa'),
(34,'Can change siswa',9,'change_siswa'),
(35,'Can delete siswa',9,'delete_siswa'),
(36,'Can view siswa',9,'view_siswa'),
(37,'Can add guru',10,'add_guru'),
(38,'Can change guru',10,'change_guru'),
(39,'Can delete guru',10,'delete_guru'),
(40,'Can view guru',10,'view_guru'),
(41,'Can add siswa wali',11,'add_siswawali'),
(42,'Can change siswa wali',11,'change_siswawali'),
(43,'Can delete siswa wali',11,'delete_siswawali'),
(44,'Can view siswa wali',11,'view_siswawali'),
(45,'Can add jadwal',12,'add_jadwal'),
(46,'Can change jadwal',12,'change_jadwal'),
(47,'Can delete jadwal',12,'delete_jadwal'),
(48,'Can view jadwal',12,'view_jadwal'),
(49,'Can add jurusan',13,'add_jurusan'),
(50,'Can change jurusan',13,'change_jurusan'),
(51,'Can delete jurusan',13,'delete_jurusan'),
(52,'Can view jurusan',13,'view_jurusan'),
(53,'Can add kelas',14,'add_kelas'),
(54,'Can change kelas',14,'change_kelas'),
(55,'Can delete kelas',14,'delete_kelas'),
(56,'Can view kelas',14,'view_kelas'),
(57,'Can add kelas siswa',15,'add_kelassiswa'),
(58,'Can change kelas siswa',15,'change_kelassiswa'),
(59,'Can delete kelas siswa',15,'delete_kelassiswa'),
(60,'Can view kelas siswa',15,'view_kelassiswa'),
(61,'Can add mapel',16,'add_mapel'),
(62,'Can change mapel',16,'change_mapel'),
(63,'Can delete mapel',16,'delete_mapel'),
(64,'Can view mapel',16,'view_mapel'),
(65,'Can add tahun ajaran',17,'add_tahunajaran'),
(66,'Can change tahun ajaran',17,'change_tahunajaran'),
(67,'Can delete tahun ajaran',17,'delete_tahunajaran'),
(68,'Can view tahun ajaran',17,'view_tahunajaran'),
(69,'Can add presensi',18,'add_presensi'),
(70,'Can change presensi',18,'change_presensi'),
(71,'Can delete presensi',18,'delete_presensi'),
(72,'Can view presensi',18,'view_presensi'),
(73,'Can add tugas',19,'add_tugas'),
(74,'Can change tugas',19,'change_tugas'),
(75,'Can delete tugas',19,'delete_tugas'),
(76,'Can view tugas',19,'view_tugas'),
(77,'Can add nilai',20,'add_nilai'),
(78,'Can change nilai',20,'change_nilai'),
(79,'Can delete nilai',20,'delete_nilai'),
(80,'Can view nilai',20,'view_nilai');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_users_akun_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_users_akun_id` FOREIGN KEY (`user_id`) REFERENCES `users_akun` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `django_content_type` VALUES
(12,'academics','jadwal'),
(13,'academics','jurusan'),
(14,'academics','kelas'),
(15,'academics','kelassiswa'),
(16,'academics','mapel'),
(17,'academics','tahunajaran'),
(1,'admin','logentry'),
(3,'auth','group'),
(2,'auth','permission'),
(4,'contenttypes','contenttype'),
(20,'grades','nilai'),
(18,'grades','presensi'),
(19,'grades','tugas'),
(5,'sessions','session'),
(6,'users','akun'),
(10,'users','guru'),
(7,'users','peran'),
(9,'users','siswa'),
(11,'users','siswawali'),
(8,'users','wali');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `django_migrations` VALUES
(1,'contenttypes','0001_initial','2025-10-30 12:31:24.592059'),
(2,'contenttypes','0002_remove_content_type_name','2025-10-30 12:31:24.619629'),
(3,'auth','0001_initial','2025-10-30 12:31:24.700162'),
(4,'auth','0002_alter_permission_name_max_length','2025-10-30 12:31:24.715296'),
(5,'auth','0003_alter_user_email_max_length','2025-10-30 12:31:24.718618'),
(6,'auth','0004_alter_user_username_opts','2025-10-30 12:31:24.721552'),
(7,'auth','0005_alter_user_last_login_null','2025-10-30 12:31:24.724316'),
(8,'auth','0006_require_contenttypes_0002','2025-10-30 12:31:24.725273'),
(9,'auth','0007_alter_validators_add_error_messages','2025-10-30 12:31:24.728300'),
(10,'auth','0008_alter_user_username_max_length','2025-10-30 12:31:24.731191'),
(11,'auth','0009_alter_user_last_name_max_length','2025-10-30 12:31:24.734465'),
(12,'auth','0010_alter_group_name_max_length','2025-10-30 12:31:24.751477'),
(13,'auth','0011_update_proxy_permissions','2025-10-30 12:31:24.754539'),
(14,'auth','0012_alter_user_first_name_max_length','2025-10-30 12:31:24.757247'),
(15,'users','0001_initial','2025-10-30 12:31:24.998101'),
(16,'academics','0001_initial','2025-10-30 12:31:25.074786'),
(17,'academics','0002_initial','2025-10-30 12:31:25.344947'),
(18,'admin','0001_initial','2025-10-30 12:31:25.383210'),
(19,'admin','0002_logentry_remove_auto_add','2025-10-30 12:31:25.388822'),
(20,'admin','0003_logentry_add_action_flag_choices','2025-10-30 12:31:25.394353'),
(21,'grades','0001_initial','2025-10-30 12:31:25.470351'),
(22,'grades','0002_initial','2025-10-30 12:31:25.617528'),
(23,'sessions','0001_initial','2025-10-30 12:31:25.636939');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `grades_nilai`
--

DROP TABLE IF EXISTS `grades_nilai`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `grades_nilai` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `tipe_penilaian` varchar(20) NOT NULL,
  `nilai` decimal(5,2) NOT NULL,
  `tanggal_penilaian` date NOT NULL,
  `jadwal_id` bigint(20) NOT NULL,
  `siswa_id` bigint(20) NOT NULL,
  `tugas_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `grades_nilai_jadwal_id_86960d8a_fk_academics_jadwal_id` (`jadwal_id`),
  KEY `grades_nilai_nilai_1a443d6f` (`nilai`),
  KEY `grades_nilai_siswa_id_c6dcd6e0_fk_users_siswa_akun_id` (`siswa_id`),
  KEY `grades_nilai_tugas_id_8af9ab12_fk_grades_tugas_id` (`tugas_id`),
  CONSTRAINT `grades_nilai_jadwal_id_86960d8a_fk_academics_jadwal_id` FOREIGN KEY (`jadwal_id`) REFERENCES `academics_jadwal` (`id`),
  CONSTRAINT `grades_nilai_siswa_id_c6dcd6e0_fk_users_siswa_akun_id` FOREIGN KEY (`siswa_id`) REFERENCES `users_siswa` (`akun_id`),
  CONSTRAINT `grades_nilai_tugas_id_8af9ab12_fk_grades_tugas_id` FOREIGN KEY (`tugas_id`) REFERENCES `grades_tugas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grades_nilai`
--

LOCK TABLES `grades_nilai` WRITE;
/*!40000 ALTER TABLE `grades_nilai` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `grades_nilai` VALUES
(1,'Tugas',85.50,'2025-10-30',1,4,1);
/*!40000 ALTER TABLE `grades_nilai` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `grades_presensi`
--

DROP TABLE IF EXISTS `grades_presensi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `grades_presensi` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `tanggal` date NOT NULL,
  `status` varchar(10) NOT NULL,
  `keterangan` longtext DEFAULT NULL,
  `jadwal_id` bigint(20) NOT NULL,
  `siswa_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `grades_presensi_siswa_id_jadwal_id_tanggal_11db5c23_uniq` (`siswa_id`,`jadwal_id`,`tanggal`),
  KEY `grades_presensi_tanggal_8e35f094` (`tanggal`),
  KEY `grades_pres_jadwal__fd7a20_idx` (`jadwal_id`,`tanggal`),
  CONSTRAINT `grades_presensi_jadwal_id_0012a206_fk_academics_jadwal_id` FOREIGN KEY (`jadwal_id`) REFERENCES `academics_jadwal` (`id`),
  CONSTRAINT `grades_presensi_siswa_id_42d08c6c_fk_users_siswa_akun_id` FOREIGN KEY (`siswa_id`) REFERENCES `users_siswa` (`akun_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grades_presensi`
--

LOCK TABLES `grades_presensi` WRITE;
/*!40000 ALTER TABLE `grades_presensi` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `grades_presensi` VALUES
(1,'2025-10-30','Hadir',NULL,1,4);
/*!40000 ALTER TABLE `grades_presensi` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `grades_tugas`
--

DROP TABLE IF EXISTS `grades_tugas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `grades_tugas` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nama` varchar(255) NOT NULL,
  `deskripsi` longtext NOT NULL,
  `mulai` datetime(6) NOT NULL,
  `tenggat` datetime(6) NOT NULL,
  `jadwal_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `grades_tugas_nama_08cacf49` (`nama`),
  KEY `grades_tugas_jadwal_id_e6ecdb8d_fk_academics_jadwal_id` (`jadwal_id`),
  CONSTRAINT `grades_tugas_jadwal_id_e6ecdb8d_fk_academics_jadwal_id` FOREIGN KEY (`jadwal_id`) REFERENCES `academics_jadwal` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grades_tugas`
--

LOCK TABLES `grades_tugas` WRITE;
/*!40000 ALTER TABLE `grades_tugas` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `grades_tugas` VALUES
(1,'Tugas Aljabar Bab 1','Kerjakan soal latihan 1.1 di buku paket halaman 10.','2025-10-30 12:31:29.649030','2025-11-06 12:31:29.649033',1);
/*!40000 ALTER TABLE `grades_tugas` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `users_akun`
--

DROP TABLE IF EXISTS `users_akun`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_akun` (
  `created_at` datetime(6) NOT NULL,
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `peran_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `users_akun_peran_id_b1a93af0_fk_users_peran_id` (`peran_id`),
  CONSTRAINT `users_akun_peran_id_b1a93af0_fk_users_peran_id` FOREIGN KEY (`peran_id`) REFERENCES `users_peran` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_akun`
--

LOCK TABLES `users_akun` WRITE;
/*!40000 ALTER TABLE `users_akun` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `users_akun` VALUES
('2025-10-30 12:31:29.168519',1,'pbkdf2_sha256$1000000$zzMebFC4pXExop2Yy5yuSk$F0e5Vpkwy7Yzw4xlqln+D5732YZqDhH78W1J5Xu5deg=','2025-10-30 12:31:45.481845',1,'admin@sekolah.com',1,1,1),
('2025-10-30 12:31:29.303075',2,'pbkdf2_sha256$1000000$KlOi4RWvsiQg8k8BqCRuTG$Y4e4YAPScUp4GVjMlruA4Y7O13ruKFMVghfWLYbmrsY=',NULL,0,'budi.guru@sekolah.com',1,0,2),
('2025-10-30 12:31:29.415352',3,'pbkdf2_sha256$1000000$s3TPOCljmwSzw6RCIdcFsO$28r7JONs3fvAYEt7wWRB3eQETI2m4ro1rjXJpiBuk0o=',NULL,0,'siti.guru@sekolah.com',1,0,2),
('2025-10-30 12:31:29.528489',4,'pbkdf2_sha256$1000000$LQjiDp1E5fW7HbPrH9t5KX$pwH4WQ5wBYrCArlsQeTtND27mFeYs8YIpmH/QPDspEs=',NULL,0,'andi.siswa@sekolah.com',1,0,3),
('2025-10-30 12:31:29.642056',5,'pbkdf2_sha256$1000000$uhu2qqbJ3eVeWqCaw9ZFAh$6WeS6v0hmVWzKRTMLG8K31794eHUpUAP2jT7PDCob9I=',NULL,0,'bunga.siswa@sekolah.com',1,0,3);
/*!40000 ALTER TABLE `users_akun` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `users_akun_groups`
--

DROP TABLE IF EXISTS `users_akun_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_akun_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `akun_id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_akun_groups_akun_id_group_id_e5dca79c_uniq` (`akun_id`,`group_id`),
  KEY `users_akun_groups_group_id_b2d22304_fk_auth_group_id` (`group_id`),
  CONSTRAINT `users_akun_groups_akun_id_9b807634_fk_users_akun_id` FOREIGN KEY (`akun_id`) REFERENCES `users_akun` (`id`),
  CONSTRAINT `users_akun_groups_group_id_b2d22304_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_akun_groups`
--

LOCK TABLES `users_akun_groups` WRITE;
/*!40000 ALTER TABLE `users_akun_groups` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `users_akun_groups` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `users_akun_user_permissions`
--

DROP TABLE IF EXISTS `users_akun_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_akun_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `akun_id` bigint(20) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_akun_user_permissions_akun_id_permission_id_a7631c5c_uniq` (`akun_id`,`permission_id`),
  KEY `users_akun_user_perm_permission_id_a556a5a1_fk_auth_perm` (`permission_id`),
  CONSTRAINT `users_akun_user_perm_permission_id_a556a5a1_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `users_akun_user_permissions_akun_id_2a92ab56_fk_users_akun_id` FOREIGN KEY (`akun_id`) REFERENCES `users_akun` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_akun_user_permissions`
--

LOCK TABLES `users_akun_user_permissions` WRITE;
/*!40000 ALTER TABLE `users_akun_user_permissions` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `users_akun_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `users_guru`
--

DROP TABLE IF EXISTS `users_guru`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_guru` (
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `alamat` longtext NOT NULL,
  `tanggal_lahir` datetime(6) NOT NULL,
  `nomor_handphone` varchar(20) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `nip` varchar(255) NOT NULL,
  `jabatan` varchar(100) NOT NULL,
  `akun_id` bigint(20) NOT NULL,
  PRIMARY KEY (`akun_id`),
  UNIQUE KEY `nip` (`nip`),
  KEY `users_guru_jabatan_44c913_idx` (`jabatan`),
  CONSTRAINT `users_guru_akun_id_bd93227c_fk_users_akun_id` FOREIGN KEY (`akun_id`) REFERENCES `users_akun` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_guru`
--

LOCK TABLES `users_guru` WRITE;
/*!40000 ALTER TABLE `users_guru` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `users_guru` VALUES
('Budi','Prasetyo','Jl. Guru No. 1','1979-12-31 17:00:00.000000','081211110001','L','2025-10-30 12:31:29.305201','2025-10-30 12:31:29.305209','198001012005011001','Guru Matematika',2),
('Siti','Rahayu','Jl. Guru No. 2','1979-12-31 17:00:00.000000','081211110002','P','2025-10-30 12:31:29.417098','2025-10-30 12:31:29.417104','198505052010012002','Guru Bahasa Indonesia',3);
/*!40000 ALTER TABLE `users_guru` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `users_peran`
--

DROP TABLE IF EXISTS `users_peran`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_peran` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nama` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nama` (`nama`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_peran`
--

LOCK TABLES `users_peran` WRITE;
/*!40000 ALTER TABLE `users_peran` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `users_peran` VALUES
(1,'Admin'),
(2,'Guru'),
(5,'Kepala Sekolah'),
(3,'Siswa'),
(4,'Tata Usaha');
/*!40000 ALTER TABLE `users_peran` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `users_siswa`
--

DROP TABLE IF EXISTS `users_siswa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_siswa` (
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `alamat` longtext NOT NULL,
  `tanggal_lahir` datetime(6) NOT NULL,
  `nomor_handphone` varchar(20) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `nis` varchar(255) NOT NULL,
  `akun_id` bigint(20) NOT NULL,
  PRIMARY KEY (`akun_id`),
  UNIQUE KEY `nis` (`nis`),
  CONSTRAINT `users_siswa_akun_id_b05ffb96_fk_users_akun_id` FOREIGN KEY (`akun_id`) REFERENCES `users_akun` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_siswa`
--

LOCK TABLES `users_siswa` WRITE;
/*!40000 ALTER TABLE `users_siswa` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `users_siswa` VALUES
('Andi','Setiawan','Jl. Siswa No. 1','2008-03-14 17:00:00.000000','081322220001','L','2025-10-30 12:31:29.530223','2025-10-30 12:31:29.530229','NIS001',4),
('Bunga','Lestari','Jl. Siswa No. 2','2008-03-14 17:00:00.000000','081322220002','P','2025-10-30 12:31:29.643445','2025-10-30 12:31:29.643452','NIS002',5);
/*!40000 ALTER TABLE `users_siswa` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `users_siswawali`
--

DROP TABLE IF EXISTS `users_siswawali`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_siswawali` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `hubungan` varchar(10) NOT NULL,
  `wali_id` bigint(20) NOT NULL,
  `siswa_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_siswawali_siswa_id_wali_id_8f570a62_uniq` (`siswa_id`,`wali_id`),
  KEY `users_siswa_wali_id_3840d5_idx` (`wali_id`,`siswa_id`),
  CONSTRAINT `users_siswawali_siswa_id_4145bee1_fk_users_siswa_akun_id` FOREIGN KEY (`siswa_id`) REFERENCES `users_siswa` (`akun_id`),
  CONSTRAINT `users_siswawali_wali_id_6bf3a6b8_fk_users_wali_id` FOREIGN KEY (`wali_id`) REFERENCES `users_wali` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_siswawali`
--

LOCK TABLES `users_siswawali` WRITE;
/*!40000 ALTER TABLE `users_siswawali` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `users_siswawali` VALUES
(1,'Ayah',1,4),
(2,'Ayah',2,5);
/*!40000 ALTER TABLE `users_siswawali` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `users_wali`
--

DROP TABLE IF EXISTS `users_wali`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_wali` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `alamat` longtext NOT NULL,
  `tanggal_lahir` datetime(6) NOT NULL,
  `nomor_handphone` varchar(20) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_wali`
--

LOCK TABLES `users_wali` WRITE;
/*!40000 ALTER TABLE `users_wali` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `users_wali` VALUES
(1,'Bambang','Setiawan','Jl. Siswa No. 1','1975-05-09 17:00:00.000000','085633330001','L','2025-10-30 12:31:29.531255','2025-10-30 12:31:29.531261'),
(2,'Siti','Aminah','Jl. Siswa No. 2','1975-05-09 17:00:00.000000','085633330002','L','2025-10-30 12:31:29.644639','2025-10-30 12:31:29.644645');
/*!40000 ALTER TABLE `users_wali` ENABLE KEYS */;
UNLOCK TABLES;
commit;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2025-10-31 20:28:09

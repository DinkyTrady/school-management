from typing import override

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from apps.core.models import Person

from .managers import AkunManager


class Peran(models.Model):
    nama = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name_plural = 'Peran Akun'


class Akun(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    peran = models.ForeignKey(Peran, on_delete=models.PROTECT, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True, auto_created=True, editable=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AkunManager()

    @override
    def __str__(self):
        return self.email

    @property
    def get_user_peran(self):
        if not self.peran:
            return ''
        return self.peran.nama

    def has_peran(self, role_name):
        if not self.peran:
            return False
        return self.peran.nama.lower() == role_name.lower()

    @property
    def is_guru(self):
        return self.has_peran('Guru')

    @property
    def is_siswa(self):
        return self.has_peran('Siswa')

    @property
    def is_tata_usaha(self):
        return self.has_peran('Tata Usaha')

    @property
    def is_kepala_sekolah(self):
        return self.has_peran('Kepala Sekolah')

    @property
    def is_admin(self):
        return self.has_peran('Admin')

    def sync_permissions(self):
        """Sync user group assignment based on their role"""
        from .permissions import RoleBasedPermissions
        RoleBasedPermissions.assign_user_to_group(self)
    
    def save(self, *args, **kwargs):
        """Override save to auto-sync permissions when role changes"""
        is_new = self.pk is None
        old_peran = None
        
        if not is_new:
            try:
                old_instance = Akun.objects.get(pk=self.pk)
                old_peran = old_instance.peran
            except Akun.DoesNotExist:
                pass
        
        super().save(*args, **kwargs)
        
        # Sync group membership if role changed or new user
        if is_new or old_peran != self.peran:
            self.sync_permissions()

    def can_access_model(self, model_name, action='view'):
        """Check if user can access specific model based on role"""
        from .permissions import RoleBasedPermissions
        return RoleBasedPermissions.user_can_access_data(self, model_name, action)
    
    def can_edit_delete_model(self, model_name):
        """Check if user can edit/delete specific model"""
        from .permissions import RoleBasedPermissions
        return RoleBasedPermissions.user_can_edit_delete(self, model_name)
    
    def get_accessible_actions(self, model_name):
        """Get list of accessible actions for a model"""
        from .permissions import RoleBasedPermissions
        return RoleBasedPermissions.get_user_accessible_actions(self, model_name)

    # Permission methods based on intro.html role descriptions
    
    # Administrator permissions: "Mengelola seluruh sistem dan data akademik sekolah dengan kontrol penuh"
    def can_manage_users(self):
        """Administrator: Manajemen akun pengguna"""
        return self.is_admin

    def can_manage_roles_access(self):
        """Administrator: Pengaturan peran & hak akses"""
        return self.is_admin

    def can_manage_academic_data(self):
        """Administrator: Manajemen data akademik"""
        return self.is_admin

    def can_view_reports_analytics(self):
        """Administrator: Laporan dan analitik sistem"""
        return self.is_admin

    # Guru permissions: "Mengelola kelas, nilai, tugas, dan interaksi dengan siswa mereka"
    def can_manage_class_students(self):
        """Guru: Kelola data kelas dan siswa"""
        return self.is_guru or self.is_admin

    def can_input_grades_assignments(self):
        """Guru: Input nilai dan tugas"""
        return self.is_guru or self.is_admin

    def can_monitor_student_attendance(self):
        """Guru: Pantau kehadiran siswa"""
        return self.is_guru or self.is_admin

    def can_view_schedule_curriculum(self):
        """Guru: Lihat jadwal dan kurikulum"""
        return self.is_guru or self.is_admin

    # Siswa permissions: "Melihat informasi akademik dan data pembelajaran mereka dengan mudah"
    def can_view_profile_biodata(self):
        """Siswa: Lihat profil dan biodata"""
        return True  # All authenticated users

    def can_access_class_schedule(self):
        """Siswa: Akses jadwal pelajaran"""
        return self.is_siswa or self.is_guru or self.is_admin

    def can_view_grades_assignments(self):
        """Siswa: Lihat nilai dan tugas"""
        return self.is_siswa or self.is_guru or self.is_admin

    def can_monitor_own_attendance(self):
        """Siswa: Pantau kehadiran pribadi"""
        return self.is_siswa or self.is_guru or self.is_admin
        
    # Helper methods for template usage
    def has_edit_permission(self, model_name):
        """Template helper: Check if user can edit model"""
        return self.can_edit_delete_model(model_name)
    
    def has_delete_permission(self, model_name):
        """Template helper: Check if user can delete model"""
        return self.can_edit_delete_model(model_name)
    
    def has_add_permission(self, model_name):
        """Template helper: Check if user can add new records"""
        actions = self.get_accessible_actions(model_name)
        return 'add' in actions

    class Meta:
        verbose_name_plural = 'Akun'


class Siswa(Person):
    nis = models.CharField(max_length=255, unique=True)
    akun = models.OneToOneField(
        Akun, on_delete=models.CASCADE, primary_key=True, related_name='siswa_profile'
    )

    @override
    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name_plural = 'Siswa'


class Guru(Person):
    nip = models.CharField(max_length=255, unique=True)
    jabatan = models.CharField(max_length=100)
    akun = models.OneToOneField(
        Akun, on_delete=models.CASCADE, primary_key=True, related_name='guru_profile'
    )

    @override
    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name_plural = 'Guru'
        indexes = [models.Index(fields=['jabatan'])]


class Wali(Person):
    @override
    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name_plural = 'Wali Murid'


class SiswaWali(models.Model):
    HUBUNGAN_CHOICES = [
        ('Ayah', 'Ayah'),
        ('Ibu', 'Ibu'),
        ('Wali', 'Wali'),
    ]
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    wali = models.ForeignKey(Wali, on_delete=models.CASCADE)
    hubungan = models.CharField(max_length=10, choices=HUBUNGAN_CHOICES)

    class Meta:
        unique_together = ('siswa', 'wali')
        indexes = [models.Index(fields=['wali', 'siswa'])]
        verbose_name_plural = 'Hubungan Siswa-Wali'

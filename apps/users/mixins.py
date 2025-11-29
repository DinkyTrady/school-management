from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import Akun, Siswa, Guru


class RoleBasedAccessMixin(LoginRequiredMixin):
    """
    Mixin untuk mengontrol akses berdasarkan peran sesuai deskripsi intro.html
    """
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        # Check role-based access
        if not self.check_role_access(request.user):
            raise PermissionDenied("Anda tidak memiliki akses untuk halaman ini.")
            
        return super().dispatch(request, *args, **kwargs)
    
    def check_role_access(self, user):
        """Override this method to implement specific role checks"""
        return True


class AdminOnlyMixin(RoleBasedAccessMixin):
    """
    Administrator: Mengelola seluruh sistem dan data akademik sekolah dengan kontrol penuh
    """
    
    def check_role_access(self, user):
        return user.is_admin


class GuruAccessMixin(RoleBasedAccessMixin):
    """
    Guru: Mengelola kelas, nilai, tugas, dan interaksi dengan siswa mereka
    """
    
    def check_role_access(self, user):
        return user.is_guru or user.is_admin


class SiswaAccessMixin(RoleBasedAccessMixin):
    """
    Siswa: Melihat informasi akademik dan data pembelajaran mereka dengan mudah
    """
    
    def check_role_access(self, user):
        return user.is_siswa or user.is_guru or user.is_admin


class OwnDataOnlyMixin(RoleBasedAccessMixin):
    """
    Siswa hanya dapat mengakses data mereka sendiri
    """
    
    def check_role_access(self, user):
        if user.is_admin or user.is_guru:
            return True
        
        if user.is_siswa:
            # Check if accessing own data
            return self.is_accessing_own_data(user)
            
        return False
    
    def is_accessing_own_data(self, user):
        """Override this to implement specific own-data checks"""
        return True


class SiswaDataFilterMixin:
    """
    Mixin untuk filter data siswa berdasarkan peran:
    - Admin/Guru: Lihat semua data
    - Siswa: Hanya data sendiri
    """
    
    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        
        if user.is_admin or user.is_guru:
            return qs
        
        if user.is_siswa:
            # Filter to own data only
            if hasattr(user, 'siswa_profile'):
                return qs.filter(siswa=user.siswa_profile)
            else:
                return qs.none()
        
        return qs.none()


class GuruDataFilterMixin:
    """
    Mixin untuk filter data yang terkait dengan guru:
    - Admin: Lihat semua data
    - Guru: Hanya data kelas/mapel yang diajar
    - Siswa: Tidak bisa akses
    """
    
    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        
        if user.is_admin:
            return qs
        
        if user.is_guru and hasattr(user, 'guru_profile'):
            # Filter to classes/subjects taught by this teacher
            guru_profile = user.guru_profile
            
            # This would need to be customized based on the specific model
            # For example, for Jadwal model:
            if self.model.__name__ == 'Jadwal':
                return qs.filter(guru=guru_profile)
            # For Nilai/Presensi models:
            elif self.model.__name__ in ['Nilai', 'Presensi']:
                return qs.filter(jadwal__guru=guru_profile)
            
        return qs.none()


class ProfileAccessMixin(OwnDataOnlyMixin):
    """
    Kontrol akses untuk profile data:
    - Admin: Akses semua profile
    - Guru: Akses profile siswa di kelasnya + profile sendiri
    - Siswa: Hanya profile sendiri
    """
    
    def is_accessing_own_data(self, user):
        # Get the profile being accessed
        if 'pk' in self.kwargs:
            profile_pk = self.kwargs['pk']
            
            # Check if it's their own profile
            if user.is_siswa and hasattr(user, 'siswa_profile'):
                return str(user.siswa_profile.pk) == str(profile_pk)
            elif user.is_guru and hasattr(user, 'guru_profile'):
                return str(user.guru_profile.pk) == str(profile_pk)
        
        return False
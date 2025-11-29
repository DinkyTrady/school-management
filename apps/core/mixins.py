from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy


class RoleBasedPermissionMixin(LoginRequiredMixin):
    """
    Mixin to enforce role-based permissions based on intro.html role descriptions
    """
    required_permission = None  # e.g., 'view', 'add', 'change', 'delete'
    model_name = None  # e.g., 'tugas', 'nilai', 'presensi'
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            if self.required_permission in ['add', 'change', 'delete']:
                messages.error(
                    request,
                    f"Anda tidak memiliki izin untuk {self.get_permission_message()}. "
                    f"Peran '{request.user.get_user_peran}' hanya dapat melihat data."
                )
                return redirect(self.get_permission_denied_url())
            else:
                raise PermissionDenied(
                    f"Anda tidak memiliki izin untuk mengakses {self.model_name or 'data ini'}."
                )
        return super().dispatch(request, *args, **kwargs)
    
    def has_permission(self):
        """Check if user has required permission for the model"""
        if not self.request.user.is_authenticated:
            return False
            
        if not self.model_name or not self.required_permission:
            return True  # No specific permission required
            
        return self.request.user.can_access_model(
            self.model_name, 
            self.required_permission
        )
    
    def get_permission_message(self):
        """Get user-friendly permission message"""
        messages = {
            'add': 'menambah data',
            'change': 'mengubah data', 
            'delete': 'menghapus data',
            'view': 'melihat data'
        }
        return messages.get(self.required_permission, 'mengakses data')
    
    def get_permission_denied_url(self):
        """URL to redirect to when permission denied"""
        # Try to get the list view for the same model
        if hasattr(self, 'success_url') and self.success_url:
            return self.success_url
        return reverse_lazy('core:dashboard')


class ViewOnlyMixin(RoleBasedPermissionMixin):
    """Mixin for view-only access"""
    required_permission = 'view'


class FullAccessMixin(RoleBasedPermissionMixin):
    """Mixin for full CRUD access (Admin only)"""
    def has_permission(self):
        return (
            self.request.user.is_authenticated and 
            self.request.user.is_admin
        )


class GuruEditMixin(RoleBasedPermissionMixin):
    """Mixin for Guru edit access (grades only)"""
    def has_permission(self):
        if not self.request.user.is_authenticated:
            return False
            
        # Admin always has access
        if self.request.user.is_admin:
            return True
            
        # Guru can only edit grades data
        if self.request.user.is_guru:
            return (
                self.model_name and 
                self.model_name.lower() in ['tugas', 'nilai', 'presensi']
            )
        
        return False


class SiswaViewOnlyMixin(RoleBasedPermissionMixin):
    """Mixin specifically for Siswa view-only access"""
    required_permission = 'view'
    
    def has_permission(self):
        return (
            self.request.user.is_authenticated and
            self.request.user.can_access_model(self.model_name or '', 'view')
        )


# Mixins for specific models based on intro.html roles

class TugasPermissionMixin(RoleBasedPermissionMixin):
    """Permission mixin for Tugas model - Guru can CRUD, others view only"""
    model_name = 'tugas'


class NilaiPermissionMixin(RoleBasedPermissionMixin):
    """Permission mixin for Nilai model - Guru can CRUD, others view only"""
    model_name = 'nilai'


class PresensiPermissionMixin(RoleBasedPermissionMixin):
    """Permission mixin for Presensi model - Guru can CRUD, others view only"""
    model_name = 'presensi'


class AcademicViewOnlyMixin(ViewOnlyMixin):
    """Mixin for academic data (Kelas, Jadwal, etc.) - All roles view only except Admin"""
    def has_permission(self):
        if not self.request.user.is_authenticated:
            return False
        
        # Admin has full access
        if self.request.user.is_admin:
            return True
            
        # Others can only view
        return self.required_permission == 'view'


class UserManagementMixin(FullAccessMixin):
    """Mixin for user management - Admin only"""
    def has_permission(self):
        return (
            self.request.user.is_authenticated and 
            self.request.user.can_manage_users()
        )
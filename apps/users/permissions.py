from django.contrib.auth.models import Permission as DjangoPermission, Group
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q


class RoleBasedPermissions:
    """
    Permission system berdasarkan peran sesuai dengan deskripsi di intro.html
    Implements role-based access control with Groups and Permissions
    """
    
    # Role definitions from intro.html
    ADMIN_ROLE = 'Administrator'
    GURU_ROLE = 'Guru'
    SISWA_ROLE = 'Siswa'
    
    @classmethod
    def setup_groups_and_permissions(cls):
        """Create groups and assign permissions based on intro.html role descriptions"""
        # Create groups if they don't exist
        admin_group, _ = Group.objects.get_or_create(name=cls.ADMIN_ROLE)
        guru_group, _ = Group.objects.get_or_create(name=cls.GURU_ROLE)
        siswa_group, _ = Group.objects.get_or_create(name=cls.SISWA_ROLE)
        
        # Clear existing permissions
        admin_group.permissions.clear()
        guru_group.permissions.clear() 
        siswa_group.permissions.clear()
        
        # Assign permissions to groups
        admin_group.permissions.set(cls.get_admin_permissions())
        guru_group.permissions.set(cls.get_guru_permissions())
        siswa_group.permissions.set(cls.get_siswa_permissions())
        
        return admin_group, guru_group, siswa_group
    
    @staticmethod
    def get_admin_permissions():
        """
        Administrator: Mengelola seluruh sistem dan data akademik sekolah dengan kontrol penuh
        - Manajemen akun pengguna
        - Pengaturan peran & hak akses  
        - Manajemen data akademik
        - Laporan dan analitik sistem
        """
        # Administrator has ALL permissions (full control)
        return DjangoPermission.objects.all()
    
    @staticmethod
    def get_guru_permissions():
        """
        Guru: Mengelola kelas, nilai, tugas, dan interaksi dengan siswa mereka
        - Kelola data kelas dan siswa
        - Input nilai dan tugas
        - Pantau kehadiran siswa
        - Lihat jadwal dan kurikulum
        """
        permissions = []
        
        # View permissions for user data
        permissions.extend(DjangoPermission.objects.filter(
            Q(codename='view_siswa') | 
            Q(codename='view_guru') | 
            Q(codename='view_akun')
        ))
        
        # Full access to academics (view only for reference data)
        permissions.extend(DjangoPermission.objects.filter(
            content_type__app_label='academics',
            codename__in=[
                'view_kelas', 'view_jadwal', 'view_mapel', 
                'view_jurusan', 'view_tahunajar', 'view_kelassiswa'
            ]
        ))
        
        # Full CRUD access to grades (nilai, tugas, presensi)
        permissions.extend(DjangoPermission.objects.filter(
            content_type__app_label='grades'
        ))
        
        return permissions
    
    @staticmethod 
    def get_siswa_permissions():
        """
        Siswa: Melihat informasi akademik dan data pembelajaran mereka dengan mudah
        - Lihat profil dan biodata
        - Akses jadwal pelajaran
        - Lihat nilai dan tugas  
        - Pantau kehadiran pribadi
        """
        # Siswa only gets VIEW permissions (read-only access)
        return DjangoPermission.objects.filter(
            Q(codename__startswith='view_') |
            Q(codename='view_siswa') |
            Q(content_type__app_label='academics', codename__startswith='view_') |
            Q(content_type__app_label='grades', codename__startswith='view_')
        )
    
    @classmethod
    def assign_user_to_group(cls, user):
        """Assign user to appropriate group based on their role (peran)"""
        if not user.peran:
            return
            
        # Remove user from all groups first
        user.groups.clear()
        
        # Ensure groups exist
        cls.setup_groups_and_permissions()
        
        role_name = user.peran.nama
        
        try:
            if role_name in ['Admin', 'Administrator']:
                group = Group.objects.get(name=cls.ADMIN_ROLE)
                user.groups.add(group)
            elif role_name == 'Guru':
                group = Group.objects.get(name=cls.GURU_ROLE)
                user.groups.add(group)
            elif role_name == 'Siswa':
                group = Group.objects.get(name=cls.SISWA_ROLE)
                user.groups.add(group)
            else:
                # For other roles like 'Tata Usaha', 'Kepala Sekolah'
                # Default to view-only access (same as siswa)
                group = Group.objects.get(name=cls.SISWA_ROLE)
                user.groups.add(group)
        except Group.DoesNotExist:
            pass
    
    @staticmethod
    def user_can_access_data(user, model_name, action='view'):
        """
        Check if user can access specific model data based on their role
        Returns True/False for permission check
        """
        if not user.is_authenticated or not user.peran:
            return False
            
        role = user.peran.nama
        
        # Admin can access everything
        if role in ['Admin', 'Administrator']:
            return True
            
        # Guru permissions from intro.html
        if role == 'Guru':
            # Can manage grades data (tugas, nilai, presensi)
            if model_name.lower() in ['tugas', 'nilai', 'presensi']:
                return True
            # Can view academic and student data
            if model_name.lower() in ['kelas', 'jadwal', 'mapel', 'jurusan', 'tahunajar', 'kelassiswa', 'siswa']:
                return action == 'view'
            # Default: view only
            return action == 'view'
            
        # Siswa permissions from intro.html - read-only access only
        if role == 'Siswa':
            return action == 'view'
            
        # Other roles (Tata Usaha, Kepala Sekolah) get read-only access
        return action == 'view'
    
    @staticmethod
    def get_user_accessible_actions(user, model_name):
        """
        Get list of actions (view, add, change, delete) user can perform on model
        """
        if not user.is_authenticated or not user.peran:
            return []
            
        role = user.peran.nama
        actions = []
        
        # Admin gets all actions
        if role in ['Admin', 'Administrator']:
            return ['view', 'add', 'change', 'delete']
        
        # Guru gets different access levels based on model
        elif role == 'Guru':
            if model_name.lower() in ['tugas', 'nilai', 'presensi']:
                # Full CRUD for grades
                return ['view', 'add', 'change', 'delete']
            elif model_name.lower() in ['kelas', 'jadwal', 'mapel', 'jurusan', 'tahunajar', 'kelassiswa', 'siswa']:
                # View only for reference data
                return ['view']
            else:
                return ['view']
        
        # Siswa and others get view-only
        else:
            return ['view']
    
    @staticmethod 
    def user_can_edit_delete(user, model_name):
        """
        Check if user can edit/delete specific model based on intro.html roles
        """
        if not user.is_authenticated or not user.peran:
            return False
            
        role = user.peran.nama
        
        # Admin can edit/delete everything
        if role in ['Admin', 'Administrator']:
            return True
        
        # Guru can only edit/delete grades data 
        elif role == 'Guru':
            return model_name.lower() in ['tugas', 'nilai', 'presensi']
        
        # Siswa cannot edit/delete anything
        else:
            return False

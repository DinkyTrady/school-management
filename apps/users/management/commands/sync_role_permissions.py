from django.core.management.base import BaseCommand
from django.db import transaction
from apps.users.models import Akun
from apps.users.permissions import RoleBasedPermissions


class Command(BaseCommand):
    help = 'Sync permissions for all users based on their roles according to intro.html'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Syncing role-based permissions..."))
        
        users = Akun.objects.all()
        
        for user in users:
            if user.peran:
                old_perm_count = user.user_permissions.count()
                RoleBasedPermissions.assign_permissions_to_user(user)
                new_perm_count = user.user_permissions.count()
                
                self.stdout.write(
                    f"✓ {user.email} ({user.peran.nama}): {old_perm_count} -> {new_perm_count} permissions"
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"⚠ {user.email}: No role assigned, skipping")
                )
        
        self.stdout.write(self.style.SUCCESS("Role-based permissions sync completed!"))
        
        # Show summary
        self._show_permission_summary()

    def _show_permission_summary(self):
        """Show permission summary for each role"""
        self.stdout.write("\nPermission Summary:")
        self.stdout.write("=" * 50)
        
        admin_perms = RoleBasedPermissions.get_admin_permissions()
        guru_perms = RoleBasedPermissions.get_guru_permissions()
        siswa_perms = RoleBasedPermissions.get_siswa_permissions()
        
        self.stdout.write(f"📋 Administrator: {admin_perms.count()} permissions (full access)")
        self.stdout.write(f"👨‍🏫 Guru: {len(guru_perms)} permissions (manage classes, grades)")
        self.stdout.write(f"👨‍🎓 Siswa: {len(siswa_perms)} permissions (view own data)")
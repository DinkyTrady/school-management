from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from apps.users.permissions import RoleBasedPermissions
from apps.users.models import Akun


class Command(BaseCommand):
    help = 'Setup role-based permissions and groups according to intro.html descriptions'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset', 
            action='store_true',
            help='Reset all groups and permissions before setup'
        )
        parser.add_argument(
            '--sync-users',
            action='store_true', 
            help='Sync existing users to appropriate groups'
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 Setting up SIGMA role-based permissions...\n')
        )

        # Reset groups if requested
        if options['reset']:
            self.stdout.write('🔄 Resetting existing groups...')
            Group.objects.filter(
                name__in=[
                    RoleBasedPermissions.ADMIN_ROLE,
                    RoleBasedPermissions.GURU_ROLE, 
                    RoleBasedPermissions.SISWA_ROLE
                ]
            ).delete()
            self.stdout.write(self.style.SUCCESS('✅ Groups reset\n'))

        # Create groups and assign permissions
        self.stdout.write('📋 Creating groups and assigning permissions...')
        admin_group, guru_group, siswa_group = RoleBasedPermissions.setup_groups_and_permissions()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Groups created:\n'
                f'   • {admin_group.name}: {admin_group.permissions.count()} permissions\n'
                f'   • {guru_group.name}: {guru_group.permissions.count()} permissions\n'
                f'   • {siswa_group.name}: {siswa_group.permissions.count()} permissions\n'
            )
        )

        # Sync existing users if requested
        if options['sync_users']:
            self.stdout.write('👥 Syncing existing users to groups...')
            users_synced = 0
            
            for user in Akun.objects.exclude(peran__isnull=True):
                old_groups_count = user.groups.count()
                user.sync_permissions()
                new_groups_count = user.groups.count()
                users_synced += 1
                
                self.stdout.write(
                    f'   • {user.email} ({user.peran.nama}): '
                    f'{old_groups_count} → {new_groups_count} groups'
                )
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ {users_synced} users synced to groups\n')
            )

        # Display role descriptions from intro.html
        self.stdout.write(
            self.style.SUCCESS(
                '📖 Role Descriptions (from intro.html):\n\n'
                '🔧 Administrator:\n'
                '   • Mengelola seluruh sistem dan data akademik sekolah dengan kontrol penuh\n'
                '   • Manajemen akun pengguna\n'
                '   • Pengaturan peran & hak akses\n'
                '   • Manajemen data akademik\n'
                '   • Laporan dan analitik sistem\n\n'
                
                '👨‍🏫 Guru:\n'
                '   • Mengelola kelas, nilai, tugas, dan interaksi dengan siswa mereka\n'
                '   • Kelola data kelas dan siswa (VIEW only)\n'
                '   • Input nilai dan tugas (FULL access)\n'
                '   • Pantau kehadiran siswa (FULL access)\n'
                '   • Lihat jadwal dan kurikulum (VIEW only)\n\n'
                
                '👨‍🎓 Siswa:\n'
                '   • Melihat informasi akademik dan data pembelajaran mereka dengan mudah\n'
                '   • Lihat profil dan biodata (VIEW only)\n'
                '   • Akses jadwal pelajaran (VIEW only)\n'
                '   • Lihat nilai dan tugas (VIEW only)\n'
                '   • Pantau kehadiran pribadi (VIEW only)\n\n'
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                '🎉 Permission setup complete!\n\n'
                'Next steps:\n'
                '1. Test permissions with different user roles\n'
                '2. Update templates to hide edit/delete buttons for view-only users\n'
                '3. Add permission checks in views\n'
            )
        )
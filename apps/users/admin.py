from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe

from .forms import AkunChangeForm, AkunCreationForm
from .models import Akun, Guru, Peran, Siswa, SiswaWali, Wali

# Customize Admin Site
admin.site.site_header = "SIGMA Admin Panel"
admin.site.site_title = "SIGMA Admin"
admin.site.index_title = "Sistem Informasi Manajemen Akademik"


@admin.register(Peran)
class PeranAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama', 'get_user_count')
    search_fields = ('nama',)
    list_per_page = 20
    
    def get_user_count(self, obj):
        count = obj.akun_set.count()
        url = reverse('admin:users_akun_changelist') + f'?peran__id__exact={obj.id}'
        return format_html('<a href="{}">{} users</a>', url, count)
    get_user_count.short_description = 'Total Users'


@admin.register(Akun)
class AkunAdmin(UserAdmin):
    add_form = AkunCreationForm
    form = AkunChangeForm
    list_display = (
        'email',
        'get_peran_badge',
        'get_profile_link',
        'created_at',
        'last_login',
        'is_staff',
        'is_active',
    )
    list_filter = (
        'peran',
        'is_staff',
        'is_active',
        'created_at',
        'last_login',
    )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            'Personal Info',
            {'fields': ('first_name', 'last_name')},
        ),
        (
            'Permissions & Role',
            {'fields': ('peran', 'is_staff', 'is_active', 'is_superuser')},
        ),
        (
            'Important dates',
            {'fields': ('last_login', 'created_at')},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'password1',
                    'password2',
                    'peran',
                    'is_staff',
                    'is_active',
                ),
            },
        ),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'last_login')
    list_per_page = 25

    def get_peran_badge(self, obj):
        if obj.peran:
            colors = {
                'Administrator': 'red',
                'Guru': 'orange', 
                'Siswa': 'blue'
            }
            color = colors.get(obj.peran.nama, 'gray')
            return format_html(
                '<span style="background: {}; color: white; padding: 2px 6px; border-radius: 3px; font-size: 12px;">{}</span>',
                color, obj.peran.nama
            )
        return format_html('<span style="color: gray;">No Role</span>')
    get_peran_badge.short_description = 'Role'
    get_peran_badge.admin_order_field = 'peran'

    def get_profile_link(self, obj):
        if obj.peran:
            if obj.peran.nama == 'Siswa':
                try:
                    siswa = obj.siswa_profile
                    url = reverse('admin:users_siswa_change', args=[siswa.pk])
                    return format_html('<a href="{}">👨‍🎓 View Profile</a>', url)
                except:
                    pass
            elif obj.peran.nama == 'Guru':
                try:
                    guru = obj.guru_profile
                    url = reverse('admin:users_guru_change', args=[guru.pk])
                    return format_html('<a href="{}">👨‍🏫 View Profile</a>', url)
                except:
                    pass
        return '-'
    get_profile_link.short_description = 'Profile'


@admin.register(Siswa)
class SiswaAdmin(admin.ModelAdmin):
    list_display = (
        'nis',
        'get_full_name_with_avatar',
        'get_gender_icon',
        'get_current_class',
        'get_akun_status',
        'nomor_handphone',
    )
    list_filter = ('gender', 'akun__is_active', 'akun__created_at')
    search_fields = ('nis', 'first_name', 'last_name', 'akun__email')
    autocomplete_fields = ('akun',)
    list_per_page = 30
    
    fieldsets = (
        (None, {
            'fields': ('akun', 'nis')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'gender', 'nomor_handphone', 'alamat', 'tanggal_lahir')
        }),
    )

    @admin.display(description='Nama Lengkap', ordering='first_name')
    def get_full_name_with_avatar(self, obj):
        avatar = '👨‍🎓' if obj.gender == 'L' else '👩‍🎓'
        return format_html('{} {}', avatar, obj.get_full_name())
    
    @admin.display(description='Gender', ordering='gender')
    def get_gender_icon(self, obj):
        if obj.gender == 'L':
            return format_html('<span style="color: blue;">♂ Laki-laki</span>')
        return format_html('<span style="color: pink;">♀ Perempuan</span>')
    
    @admin.display(description='Kelas Saat Ini')
    def get_current_class(self, obj):
        from apps.academics.models import KelasSiswa
        try:
            kelas_siswa = KelasSiswa.objects.filter(
                siswa=obj, 
                tahun_ajaran__is_active=True
            ).select_related('kelas').first()
            if kelas_siswa:
                return kelas_siswa.kelas.nama
            return '-'
        except:
            return '-'
    
    @admin.display(description='Status Akun')
    def get_akun_status(self, obj):
        if obj.akun.is_active:
            return format_html('<span style="color: green;">✓ Aktif</span>')
        return format_html('<span style="color: red;">✗ Tidak Aktif</span>')


@admin.register(Guru)
class GuruAdmin(admin.ModelAdmin):
    list_display = (
        'nip',
        'get_full_name_with_avatar',
        'jabatan',
        'get_gender_icon',
        'get_total_kelas',
        'get_akun_status',
        'nomor_handphone',
    )
    list_filter = ('gender', 'jabatan', 'akun__is_active', 'akun__created_at')
    search_fields = ('nip', 'first_name', 'last_name', 'akun__email', 'jabatan')
    autocomplete_fields = ('akun',)
    list_per_page = 25
    
    fieldsets = (
        (None, {
            'fields': ('akun', 'nip', 'jabatan')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'gender', 'nomor_handphone', 'alamat', 'tanggal_lahir')
        }),
    )

    @admin.display(description='Nama Lengkap', ordering='first_name')
    def get_full_name_with_avatar(self, obj):
        avatar = '👨‍🏫' if obj.gender == 'L' else '👩‍🏫'
        return format_html('{} {}', avatar, obj.get_full_name())
    
    @admin.display(description='Gender', ordering='gender')
    def get_gender_icon(self, obj):
        if obj.gender == 'L':
            return format_html('<span style="color: blue;">♂ Laki-laki</span>')
        return format_html('<span style="color: pink;">♀ Perempuan</span>')
    
    @admin.display(description='Jumlah Kelas')
    def get_total_kelas(self, obj):
        from apps.academics.models import Kelas
        count = Kelas.objects.filter(wali_kelas=obj).count()
        if count > 0:
            return format_html('<strong>{}</strong> kelas', count)
        return '0 kelas'
    
    @admin.display(description='Status Akun')
    def get_akun_status(self, obj):
        if obj.akun.is_active:
            return format_html('<span style="color: green;">✓ Aktif</span>')
        return format_html('<span style="color: red;">✗ Tidak Aktif</span>')


@admin.register(Wali)
class WaliAdmin(admin.ModelAdmin):
    list_display = (
        'get_full_name',
        'gender',
        'nomor_handphone',
        'alamat',
    )
    search_fields = ('first_name', 'last_name', 'nomor_handphone')

    @admin.display(description='Nama Lengkap', ordering='first_name')
    def get_full_name(self, obj):
        return obj.get_full_name()


@admin.register(SiswaWali)
class SiswaWaliAdmin(admin.ModelAdmin):
    list_display = ('siswa', 'wali', 'hubungan')
    list_filter = ('hubungan',)
    search_fields = (
        'siswa__first_name',
        'siswa__last_name',
        'wali__first_name',
        'wali__last_name',
    )
    autocomplete_fields = ('siswa', 'wali')

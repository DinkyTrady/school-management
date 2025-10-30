from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import AkunChangeForm, AkunCreationForm
from .models import Akun, Guru, Peran, Siswa, SiswaWali, Wali


@admin.register(Peran)
class PeranAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama')
    search_fields = ('nama',)


@admin.register(Akun)
class AkunAdmin(UserAdmin):
    add_form = AkunCreationForm
    form = AkunChangeForm
    list_display = (
        'email',
        'is_staff',
        'is_active',
    )
    list_filter = (
        'email',
        'is_staff',
        'is_active',
    )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            'Permissions',
            {'fields': ('is_staff', 'is_active', 'peran')},
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
    search_fields = ('email',)
    ordering = ('email',)


@admin.register(Siswa)
class SiswaAdmin(admin.ModelAdmin):
    list_display = (
        'nis',
        'get_full_name',
        'gender',
        'akun',
        'nomor_handphone',
    )
    list_filter = ('gender', 'akun__is_active')
    search_fields = ('nis', 'first_name', 'last_name', 'akun__email')
    autocomplete_fields = ('akun',)

    @admin.display(description='Nama Lengkap', ordering='first_name')
    def get_full_name(self, obj):
        return obj.get_full_name()


@admin.register(Guru)
class GuruAdmin(admin.ModelAdmin):
    list_display = (
        'nip',
        'get_full_name',
        'jabatan',
        'gender',
        'akun',
        'nomor_handphone',
    )
    list_filter = ('gender', 'jabatan', 'akun__is_active')
    search_fields = ('nip', 'first_name', 'last_name', 'akun__email', 'jabatan')
    autocomplete_fields = ('akun',)

    @admin.display(description='Nama Lengkap', ordering='first_name')
    def get_full_name(self, obj):
        return obj.get_full_name()


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

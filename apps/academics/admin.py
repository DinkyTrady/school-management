from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count

from .models import Jadwal, Jurusan, Kelas, KelasSiswa, Mapel, TahunAjaran


@admin.register(TahunAjaran)
class TahunAjaranAdmin(admin.ModelAdmin):
    list_display = (
        'get_tahun_info',
        'get_semester_badge',
        'get_status',
        'get_period',
        'get_kelas_count',
        'is_active',
    )
    search_fields = ('tahun',)
    list_filter = ('is_active', 'semester', 'tahun')
    list_editable = ('is_active',)
    list_per_page = 20
    
    fieldsets = (
        (None, {
            'fields': ('tahun', 'semester', 'is_active')
        }),
        ('Periode', {
            'fields': ('tanggal_mulai', 'tanggal_selesai')
        }),
    )

    @admin.display(description='Tahun Ajaran', ordering='tahun')
    def get_tahun_info(self, obj):
        return format_html('<strong>{}</strong>', obj.tahun)
    
    @admin.display(description='Semester', ordering='semester')
    def get_semester_badge(self, obj):
        color = '#3b82f6' if obj.semester == 'Ganjil' else '#10b981'
        return format_html(
            '<span style="background: {}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            color, obj.semester
        )
    
    @admin.display(description='Status', ordering='is_active')
    def get_status(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green; font-weight: bold;">🟢 Aktif</span>')
        return format_html('<span style="color: gray;">⚪ Tidak Aktif</span>')
    
    @admin.display(description='Periode')
    def get_period(self, obj):
        return format_html(
            '<small>{} s/d {}</small>',
            obj.tanggal_mulai.strftime('%d %b %Y'),
            obj.tanggal_selesai.strftime('%d %b %Y')
        )
    
    @admin.display(description='Jumlah Kelas')
    def get_kelas_count(self, obj):
        count = obj.kelas_set.count()
        return format_html('<strong>{}</strong> kelas', count)


@admin.register(Jurusan)
class JurusanAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama', 'deskripsi')
    search_fields = ('nama',)


# Kelas will be registered later with inlines


@admin.register(Mapel)
class MapelAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama')
    search_fields = ('nama',)


# Inline Admin
class KelasSiswaInline(admin.TabularInline):
    model = KelasSiswa
    extra = 0
    autocomplete_fields = ('siswa',)
    verbose_name = "Siswa di Kelas"
    verbose_name_plural = "Daftar Siswa di Kelas"

class JadwalInline(admin.TabularInline):
    model = Jadwal
    extra = 0
    autocomplete_fields = ('mapel', 'guru')
    verbose_name = "Jadwal Pelajaran"
    verbose_name_plural = "Jadwal Pelajaran Kelas"

# KelasAdmin with inlines

@admin.register(Kelas)
class KelasAdmin(admin.ModelAdmin):
    list_display = ('get_kelas_info', 'get_jurusan_badge', 'get_wali_kelas_info', 'get_tahun_ajaran', 'get_siswa_count')
    list_filter = ('jurusan', 'tahun_ajaran__is_active', 'tahun_ajaran')
    search_fields = ('nama', 'jurusan__nama', 'wali_kelas__first_name', 'wali_kelas__last_name', 'tahun_ajaran__tahun')
    autocomplete_fields = ('jurusan', 'wali_kelas', 'tahun_ajaran')
    list_select_related = ('jurusan', 'wali_kelas', 'tahun_ajaran')
    list_per_page = 25
    inlines = [KelasSiswaInline, JadwalInline]
    
    fieldsets = (
        (None, {
            'fields': ('nama', 'jurusan', 'tahun_ajaran')
        }),
        ('Wali Kelas', {
            'fields': ('wali_kelas',)
        }),
    )

    @admin.display(description='Kelas', ordering='nama')
    def get_kelas_info(self, obj):
        return format_html('🏫 <strong>{}</strong>', obj.nama)
    
    @admin.display(description='Jurusan', ordering='jurusan__nama')
    def get_jurusan_badge(self, obj):
        colors = {
            'IPA': '#ef4444',      # Red
            'IPS': '#3b82f6',      # Blue
            'Bahasa': '#10b981',   # Green
        }
        # Get color based on jurusan name or default
        color = '#6b7280'  # Default gray
        for key, value in colors.items():
            if key.lower() in obj.jurusan.nama.lower():
                color = value
                break
                
        return format_html(
            '<span style="background: {}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            color, obj.jurusan.nama
        )
    
    @admin.display(description='Wali Kelas', ordering='wali_kelas__first_name')
    def get_wali_kelas_info(self, obj):
        avatar = '👨‍🏫' if obj.wali_kelas.gender == 'L' else '👩‍🏫'
        return format_html(
            '{} {}<br><small>NIP: {}</small>',
            avatar, obj.wali_kelas.get_full_name(), obj.wali_kelas.nip
        )
    
    @admin.display(description='Tahun Ajaran', ordering='tahun_ajaran__tahun')
    def get_tahun_ajaran(self, obj):
        status = '🟢' if obj.tahun_ajaran.is_active else '⚪'
        return format_html(
            '{} {}<br><small>{}</small>',
            status, obj.tahun_ajaran.tahun, obj.tahun_ajaran.semester
        )
    
    @admin.display(description='Jumlah Siswa')
    def get_siswa_count(self, obj):
        count = obj.kelassiswa_set.count()
        return format_html('<strong>{}</strong> siswa', count)
    
    actions = ['export_kelas_data']
    
    @admin.action(description='Export data kelas terpilih')
    def export_kelas_data(self, request, queryset):
        from django.http import HttpResponse
        import csv
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="kelas_data.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Nama Kelas', 'Jurusan', 'Wali Kelas', 'Tahun Ajaran', 'Jumlah Siswa'])
        
        for kelas in queryset:
            writer.writerow([
                kelas.nama,
                kelas.jurusan.nama,
                kelas.wali_kelas.get_full_name(),
                f"{kelas.tahun_ajaran.tahun} {kelas.tahun_ajaran.semester}",
                kelas.kelassiswa_set.count()
            ])
        
        return response


@admin.register(KelasSiswa)
class KelasSiswaAdmin(admin.ModelAdmin):
    list_display = ('get_nama_siswa', 'get_nama_kelas', 'tahun_ajaran')
    list_filter = ('tahun_ajaran__is_active', 'kelas__jurusan', 'tahun_ajaran')
    search_fields = ('siswa__first_name', 'siswa__last_name', 'kelas__nama', 'tahun_ajaran__tahun')
    autocomplete_fields = ('siswa', 'kelas', 'tahun_ajaran')
    list_select_related = ('siswa', 'kelas', 'tahun_ajaran')

    @admin.display(description='Siswa', ordering='siswa__first_name')
    def get_nama_siswa(self, obj):
        return obj.siswa.get_full_name()

    @admin.display(description='Kelas', ordering='kelas__nama')
    def get_nama_kelas(self, obj):
        return obj.kelas.nama


@admin.register(Jadwal)
class JadwalAdmin(admin.ModelAdmin):
    list_display = (
        'get_nama_kelas',
        'mapel',
        'get_nama_guru',
        'hari',
        'jam_mulai',
        'jam_selesai',
    )
    list_filter = ('hari', 'kelas__jurusan', 'mapel', 'guru', 'kelas__tahun_ajaran__is_active')
    search_fields = ('kelas__nama', 'mapel__nama', 'guru__first_name', 'guru__last_name')
    autocomplete_fields = ('kelas', 'mapel', 'guru')
    list_select_related = ('kelas', 'mapel', 'guru')

    @admin.display(description='Guru', ordering='guru__first_name')
    def get_nama_guru(self, obj):
        return obj.guru.get_full_name()

    @admin.display(description='Kelas', ordering='kelas__nama')
    def get_nama_kelas(self, obj):
        return obj.kelas.nama

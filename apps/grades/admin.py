from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Avg, Count
from .models import Tugas, Nilai, Presensi


@admin.register(Tugas)
class TugasAdmin(admin.ModelAdmin):
    list_display = ('nama', 'get_jadwal_info', 'get_period', 'get_status', 'get_submission_count')
    list_filter = ('jadwal__kelas__jurusan', 'jadwal__mapel', 'mulai', 'tenggat')
    search_fields = ('nama', 'deskripsi', 'jadwal__kelas__nama', 'jadwal__mapel__nama')
    autocomplete_fields = ('jadwal',)
    list_select_related = ('jadwal__kelas', 'jadwal__mapel', 'jadwal__guru')
    list_per_page = 25
    date_hierarchy = 'tenggat'
    
    fieldsets = (
        (None, {
            'fields': ('nama', 'jadwal', 'deskripsi')
        }),
        ('Waktu', {
            'fields': ('mulai', 'tenggat'),
            'classes': ('collapse',)
        }),
    )

    @admin.display(description='Jadwal', ordering='jadwal__kelas__nama')
    def get_jadwal_info(self, obj):
        return format_html(
            '<strong>{}</strong><br><small>📚 {} - 👨‍🏫 {}</small>',
            obj.jadwal.kelas.nama,
            obj.jadwal.mapel.nama,
            obj.jadwal.guru.get_full_name()
        )
    
    @admin.display(description='Period', ordering='mulai')
    def get_period(self, obj):
        return format_html(
            '<small>📅 {} → {}</small>',
            obj.mulai.strftime('%d/%m %H:%M'),
            obj.tenggat.strftime('%d/%m %H:%M')
        )
    
    @admin.display(description='Status')
    def get_status(self, obj):
        from django.utils import timezone
        now = timezone.now()
        if now < obj.mulai:
            return format_html('<span style="color: blue;">🔜 Belum Dimulai</span>')
        elif now > obj.tenggat:
            return format_html('<span style="color: red;">⏰ Terlambat</span>')
        else:
            return format_html('<span style="color: green;">⏳ Berlangsung</span>')
    
    @admin.display(description='Submissions')
    def get_submission_count(self, obj):
        count = obj.nilai_set.count()
        return format_html('<strong>{}</strong> siswa', count)


@admin.register(Nilai)
class NilaiAdmin(admin.ModelAdmin):
    list_display = (
        'get_siswa_info',
        'get_mapel_kelas',
        'get_tipe_badge',
        'get_nilai_grade',
        'tanggal_penilaian',
        'get_tugas_link',
    )
    list_filter = ('tipe_penilaian', 'tanggal_penilaian', 'jadwal__kelas__jurusan', 'jadwal__mapel', 'jadwal__kelas')
    search_fields = ('siswa__first_name', 'siswa__last_name', 'jadwal__mapel__nama', 'tugas__nama', 'siswa__nis')
    autocomplete_fields = ('siswa', 'jadwal', 'tugas')
    list_select_related = ('siswa', 'jadwal__mapel', 'jadwal__kelas', 'tugas')
    list_per_page = 30
    date_hierarchy = 'tanggal_penilaian'
    
    fieldsets = (
        (None, {
            'fields': ('siswa', 'jadwal', 'tipe_penilaian')
        }),
        ('Penilaian', {
            'fields': ('nilai', 'tanggal_penilaian', 'tugas')
        }),
    )

    @admin.display(description='Siswa', ordering='siswa__first_name')
    def get_siswa_info(self, obj):
        avatar = '👨‍🎓' if obj.siswa.gender == 'L' else '👩‍🎓'
        return format_html(
            '{} <strong>{}</strong><br><small>NIS: {}</small>',
            avatar, obj.siswa.get_full_name(), obj.siswa.nis
        )
    
    @admin.display(description='Mata Pelajaran & Kelas', ordering='jadwal__mapel__nama')
    def get_mapel_kelas(self, obj):
        if obj.jadwal:
            return format_html(
                '<strong>{}</strong><br><small>📚 {}</small>',
                obj.jadwal.mapel.nama,
                obj.jadwal.kelas.nama
            )
        return "-"
    
    @admin.display(description='Tipe', ordering='tipe_penilaian')
    def get_tipe_badge(self, obj):
        colors = {
            'Tugas': '#3b82f6',      # Blue
            'Ujian Harian': '#f59e0b', # Amber  
            'UTS': '#ef4444',        # Red
            'UAS': '#dc2626',        # Dark red
        }
        color = colors.get(obj.tipe_penilaian, '#6b7280')
        return format_html(
            '<span style="background: {}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            color, obj.tipe_penilaian
        )
    
    @admin.display(description='Nilai', ordering='nilai')
    def get_nilai_grade(self, obj):
        nilai = float(obj.nilai)
        if nilai >= 85:
            color, grade = '#22c55e', 'A'  # Green
        elif nilai >= 70:
            color, grade = '#3b82f6', 'B'  # Blue
        elif nilai >= 55:
            color, grade = '#f59e0b', 'C'  # Amber
        elif nilai >= 40:
            color, grade = '#ef4444', 'D'  # Red
        else:
            color, grade = '#dc2626', 'E'  # Dark red
            
        return format_html(
            '<span style="color: {}; font-weight: bold; font-size: 16px;">{}</span><br><small>Grade: {}</small>',
            color, nilai, grade
        )
    
    @admin.display(description='Tugas')
    def get_tugas_link(self, obj):
        if obj.tugas:
            return format_html(
                '<a href="/admin/grades/tugas/{}/change/" style="text-decoration: none;">📝 {}</a>',
                obj.tugas.pk, obj.tugas.nama
            )
        return '-'


@admin.register(Presensi)
class PresensiAdmin(admin.ModelAdmin):
    list_display = (
        'get_siswa_info',
        'get_mapel_kelas',
        'tanggal',
        'get_status_badge',
        'get_keterangan_short',
    )
    list_filter = ('status', 'tanggal', 'jadwal__kelas__jurusan', 'jadwal__mapel', 'jadwal__kelas')
    search_fields = ('siswa__first_name', 'siswa__last_name', 'keterangan', 'siswa__nis')
    autocomplete_fields = ('siswa', 'jadwal')
    list_select_related = ('siswa', 'jadwal__mapel', 'jadwal__kelas')
    list_per_page = 40
    date_hierarchy = 'tanggal'
    
    fieldsets = (
        (None, {
            'fields': ('siswa', 'jadwal', 'tanggal')
        }),
        ('Kehadiran', {
            'fields': ('status', 'keterangan')
        }),
    )

    @admin.display(description='Siswa', ordering='siswa__first_name')
    def get_siswa_info(self, obj):
        avatar = '👨‍🎓' if obj.siswa.gender == 'L' else '👩‍🎓'
        return format_html(
            '{} <strong>{}</strong><br><small>NIS: {}</small>',
            avatar, obj.siswa.get_full_name(), obj.siswa.nis
        )

    @admin.display(description='Mata Pelajaran & Kelas', ordering='jadwal__mapel__nama')
    def get_mapel_kelas(self, obj):
        if obj.jadwal:
            return format_html(
                '<strong>{}</strong><br><small>📚 {}</small>',
                obj.jadwal.mapel.nama,
                obj.jadwal.kelas.nama
            )
        return "-"
    
    @admin.display(description='Status', ordering='status')
    def get_status_badge(self, obj):
        status_config = {
            'Hadir': ('✅', '#22c55e', 'white'),
            'Sakit': ('🤒', '#f59e0b', 'white'),  
            'Izin': ('📄', '#3b82f6', 'white'),
            'Alpha': ('❌', '#ef4444', 'white'),
        }
        
        icon, bg_color, text_color = status_config.get(obj.status, ('❓', '#6b7280', 'white'))
        
        return format_html(
            '<span style="background: {}; color: {}; padding: 4px 8px; border-radius: 15px; font-size: 12px; font-weight: bold;">{} {}</span>',
            bg_color, text_color, icon, obj.status
        )
    
    @admin.display(description='Keterangan')
    def get_keterangan_short(self, obj):
        if obj.keterangan:
            if len(obj.keterangan) > 30:
                return format_html(
                    '<span title="{}">{}</span>',
                    obj.keterangan, obj.keterangan[:30] + '...'
                )
            return obj.keterangan
        return '-'

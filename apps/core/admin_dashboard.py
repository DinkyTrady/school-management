from django.contrib.admin import AdminSite
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.urls import path
from django.db.models import Count, Avg
from django.utils.html import format_html

class SIGMAAdminSite(AdminSite):
    site_header = "SIGMA Administration"
    site_title = "SIGMA Admin"
    index_title = "Sistem Informasi Manajemen Akademik"
    
    def index(self, request, extra_context=None):
        """
        Display custom admin dashboard with statistics
        """
        extra_context = extra_context or {}
        
        # Get statistics
        try:
            from apps.users.models import Akun, Siswa, Guru
            from apps.academics.models import Kelas, TahunAjaran
            from apps.grades.models import Tugas, Nilai, Presensi
            
            # User statistics
            total_users = Akun.objects.count()
            total_siswa = Siswa.objects.count()
            total_guru = Guru.objects.count()
            active_users = Akun.objects.filter(is_active=True).count()
            
            # Academic statistics  
            total_kelas = Kelas.objects.count()
            active_tahun_ajaran = TahunAjaran.objects.filter(is_active=True).count()
            
            # Grades statistics
            total_tugas = Tugas.objects.count()
            total_nilai = Nilai.objects.count()
            total_presensi = Presensi.objects.count()
            
            # Average grade
            avg_nilai = Nilai.objects.aggregate(avg=Avg('nilai'))['avg'] or 0
            
            # Recent activities (last 10)
            recent_tugas = Tugas.objects.select_related('jadwal__kelas', 'jadwal__mapel').order_by('-id')[:5]
            recent_nilai = Nilai.objects.select_related('siswa', 'jadwal__mapel').order_by('-id')[:5]
            
            extra_context.update({
                'statistics': {
                    'users': {
                        'total': total_users,
                        'siswa': total_siswa,
                        'guru': total_guru,
                        'active': active_users,
                    },
                    'academic': {
                        'kelas': total_kelas,
                        'tahun_ajaran': active_tahun_ajaran,
                    },
                    'grades': {
                        'tugas': total_tugas,
                        'nilai': total_nilai,
                        'presensi': total_presensi,
                        'avg_nilai': round(avg_nilai, 2),
                    }
                },
                'recent_activities': {
                    'tugas': recent_tugas,
                    'nilai': recent_nilai,
                }
            })
            
        except Exception as e:
            # If there's an error getting statistics, just pass
            pass
        
        return super().index(request, extra_context)
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('statistics/', self.admin_view(self.statistics_view), name='statistics'),
            path('export-data/', self.admin_view(self.export_data_view), name='export_data'),
        ]
        return custom_urls + urls
    
    def statistics_view(self, request):
        """
        Custom statistics view
        """
        context = {
            'title': 'SIGMA Statistics',
            'site_header': self.site_header,
        }
        
        # Add more detailed statistics here
        try:
            from apps.users.models import Akun, Siswa, Guru
            from apps.grades.models import Nilai
            from django.db.models import Count, Q
            
            # Grade distribution
            grade_distribution = Nilai.objects.aggregate(
                grade_a=Count('id', filter=Q(nilai__gte=85)),
                grade_b=Count('id', filter=Q(nilai__gte=70, nilai__lt=85)),
                grade_c=Count('id', filter=Q(nilai__gte=55, nilai__lt=70)),
                grade_d=Count('id', filter=Q(nilai__gte=40, nilai__lt=55)),
                grade_e=Count('id', filter=Q(nilai__lt=40)),
            )
            
            # Attendance statistics
            from apps.grades.models import Presensi
            attendance_stats = Presensi.objects.aggregate(
                hadir=Count('id', filter=Q(status='Hadir')),
                sakit=Count('id', filter=Q(status='Sakit')),
                izin=Count('id', filter=Q(status='Izin')),
                alpha=Count('id', filter=Q(status='Alpha')),
            )
            
            context.update({
                'grade_distribution': grade_distribution,
                'attendance_stats': attendance_stats,
            })
            
        except Exception as e:
            context['error'] = str(e)
        
        return TemplateResponse(request, 'admin/statistics.html', context)
    
    def export_data_view(self, request):
        """
        Export system data
        """
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sigma_data.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['SIGMA System Data Export'])
        writer.writerow(['Generated on:', timezone.now().strftime('%Y-%m-%d %H:%M:%S')])
        writer.writerow([])  # Empty row
        
        # Add more export logic here
        
        return response

# Create custom admin site instance
sigma_admin_site = SIGMAAdminSite(name='sigma_admin')
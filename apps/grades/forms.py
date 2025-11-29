from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Tugas, Nilai, Presensi


class TugasForm(forms.ModelForm):
    """Form untuk create dan update Tugas"""
    
    class Meta:
        model = Tugas
        fields = ['nama', 'deskripsi', 'jadwal', 'mulai', 'tenggat']
        widgets = {
            'nama': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Masukkan nama tugas'
            }),
            'deskripsi': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full',
                'placeholder': 'Deskripsi tugas...',
                'rows': 4
            }),
            'jadwal': forms.Select(attrs={
                'class': 'select select-bordered w-full'
            }),
            'mulai': forms.DateTimeInput(attrs={
                'class': 'input input-bordered w-full',
                'type': 'datetime-local'
            }),
            'tenggat': forms.DateTimeInput(attrs={
                'class': 'input input-bordered w-full',
                'type': 'datetime-local'
            }),
        }
        labels = {
            'nama': 'Nama Tugas',
            'deskripsi': 'Deskripsi',
            'jadwal': 'Jadwal (Kelas & Mata Pelajaran)',
            'mulai': 'Waktu Mulai',
            'tenggat': 'Tenggat Waktu'
        }
    
    def clean(self):
        cleaned_data = super().clean()
        mulai = cleaned_data.get('mulai')
        tenggat = cleaned_data.get('tenggat')
        
        if mulai and tenggat:
            if mulai >= tenggat:
                raise ValidationError({
                    'tenggat': 'Tenggat waktu harus setelah waktu mulai.'
                })
            
            # Check if tenggat is in the past
            if tenggat < timezone.now():
                raise ValidationError({
                    'tenggat': 'Tenggat waktu tidak boleh di masa lalu.'
                })
        
        return cleaned_data


class NilaiForm(forms.ModelForm):
    """Form untuk create dan update Nilai"""
    
    class Meta:
        model = Nilai
        fields = ['siswa', 'jadwal', 'tugas', 'tipe_penilaian', 'nilai', 'tanggal_penilaian']
        widgets = {
            'siswa': forms.Select(attrs={
                'class': 'select select-bordered w-full'
            }),
            'jadwal': forms.Select(attrs={
                'class': 'select select-bordered w-full'
            }),
            'tugas': forms.Select(attrs={
                'class': 'select select-bordered w-full'
            }),
            'tipe_penilaian': forms.Select(attrs={
                'class': 'select select-bordered w-full'
            }),
            'nilai': forms.NumberInput(attrs={
                'class': 'input input-bordered w-full',
                'min': '0',
                'max': '100',
                'step': '0.1',
                'placeholder': 'Masukkan nilai (0-100)'
            }),
            'tanggal_penilaian': forms.DateInput(attrs={
                'class': 'input input-bordered w-full',
                'type': 'date'
            }),
        }
        labels = {
            'siswa': 'Siswa',
            'jadwal': 'Jadwal (Kelas & Mata Pelajaran)',
            'tugas': 'Tugas (Opsional)',
            'tipe_penilaian': 'Tipe Penilaian',
            'nilai': 'Nilai',
            'tanggal_penilaian': 'Tanggal Penilaian'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make tugas field optional by default
        self.fields['tugas'].required = False
        
        # Filter tugas based on jadwal when editing
        if 'jadwal' in self.data:
            try:
                jadwal_id = int(self.data.get('jadwal'))
                self.fields['tugas'].queryset = Tugas.objects.filter(jadwal_id=jadwal_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.jadwal:
            self.fields['tugas'].queryset = Tugas.objects.filter(jadwal=self.instance.jadwal)
    
    def clean_nilai(self):
        nilai = self.cleaned_data.get('nilai')
        if nilai is not None:
            if nilai < 0 or nilai > 100:
                raise ValidationError('Nilai harus antara 0 dan 100.')
        return nilai
    
    def clean(self):
        cleaned_data = super().clean()
        tipe_penilaian = cleaned_data.get('tipe_penilaian')
        tugas = cleaned_data.get('tugas')
        
        # Validate tugas field for 'Tugas' type
        if tipe_penilaian == 'Tugas' and not tugas:
            raise ValidationError({
                'tugas': 'Tugas harus dipilih untuk tipe penilaian "Tugas".'
            })
        
        return cleaned_data


class PresensiForm(forms.ModelForm):
    """Form untuk create dan update Presensi"""
    
    class Meta:
        model = Presensi
        fields = ['siswa', 'jadwal', 'tanggal', 'status', 'keterangan']
        widgets = {
            'siswa': forms.Select(attrs={
                'class': 'select select-bordered w-full'
            }),
            'jadwal': forms.Select(attrs={
                'class': 'select select-bordered w-full'
            }),
            'tanggal': forms.DateInput(attrs={
                'class': 'input input-bordered w-full',
                'type': 'date'
            }),
            'status': forms.Select(attrs={
                'class': 'select select-bordered w-full'
            }),
            'keterangan': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full',
                'placeholder': 'Keterangan tambahan (opsional)...',
                'rows': 3
            }),
        }
        labels = {
            'siswa': 'Siswa',
            'jadwal': 'Jadwal (Kelas & Mata Pelajaran)',
            'tanggal': 'Tanggal',
            'status': 'Status Kehadiran',
            'keterangan': 'Keterangan'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make keterangan optional
        self.fields['keterangan'].required = False
    
    def clean_tanggal(self):
        tanggal = self.cleaned_data.get('tanggal')
        if tanggal:
            # Don't allow future dates
            if tanggal > timezone.now().date():
                raise ValidationError('Tanggal presensi tidak boleh di masa depan.')
        return tanggal
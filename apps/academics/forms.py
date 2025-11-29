from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Kelas, TahunAjaran, Jurusan, Mapel, Jadwal, KelasSiswa


class KelasForm(forms.ModelForm):
    """Form untuk create dan update Kelas"""
    
    class Meta:
        model = Kelas
        fields = ['nama', 'jurusan', 'wali_kelas', 'tahun_ajaran']
        widgets = {
            'nama': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Contoh: X IPA 1, XI IPS 2, XII TKJ A'
            }),
            'jurusan': forms.Select(attrs={
                'class': 'select select-bordered w-full'
            }),
            'wali_kelas': forms.Select(attrs={
                'class': 'select select-bordered w-full'
            }),
            'tahun_ajaran': forms.Select(attrs={
                'class': 'select select-bordered w-full'
            }),
        }
        labels = {
            'nama': 'Nama Kelas',
            'jurusan': 'Jurusan',
            'wali_kelas': 'Wali Kelas',
            'tahun_ajaran': 'Tahun Ajaran'
        }


class TahunAjaranForm(forms.ModelForm):
    """Form untuk create dan update Tahun Ajaran"""
    
    class Meta:
        model = TahunAjaran
        fields = ['tahun', 'semester', 'tanggal_mulai', 'tanggal_selesai', 'is_active']
        widgets = {
            'tahun': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': '2024/2025'
            }),
            'semester': forms.Select(attrs={
                'class': 'select select-bordered w-full'
            }),
            'tanggal_mulai': forms.DateInput(attrs={
                'class': 'input input-bordered w-full',
                'type': 'date'
            }),
            'tanggal_selesai': forms.DateInput(attrs={
                'class': 'input input-bordered w-full',
                'type': 'date'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'checkbox checkbox-primary'
            }),
        }
        labels = {
            'tahun': 'Tahun Ajaran',
            'semester': 'Semester',
            'tanggal_mulai': 'Tanggal Mulai',
            'tanggal_selesai': 'Tanggal Selesai',
            'is_active': 'Aktif'
        }
    
    def clean(self):
        cleaned_data = super().clean()
        tanggal_mulai = cleaned_data.get('tanggal_mulai')
        tanggal_selesai = cleaned_data.get('tanggal_selesai')
        
        if tanggal_mulai and tanggal_selesai:
            if tanggal_mulai >= tanggal_selesai:
                raise ValidationError({
                    'tanggal_selesai': 'Tanggal selesai harus setelah tanggal mulai.'
                })
        
        return cleaned_data


class JurusanForm(forms.ModelForm):
    """Form untuk create dan update Jurusan"""
    
    class Meta:
        model = Jurusan
        fields = ['nama', 'deskripsi']
        widgets = {
            'nama': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Contoh: IPA, IPS, Teknik Komputer Jaringan'
            }),
            'deskripsi': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full',
                'placeholder': 'Deskripsi jurusan...',
                'rows': 4
            }),
        }
        labels = {
            'nama': 'Nama Jurusan',
            'deskripsi': 'Deskripsi'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make deskripsi optional
        self.fields['deskripsi'].required = False


class MapelForm(forms.ModelForm):
    """Form untuk create dan update Mata Pelajaran"""
    
    class Meta:
        model = Mapel
        fields = ['nama']
        widgets = {
            'nama': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Contoh: Matematika, Bahasa Indonesia, Fisika'
            }),
        }
        labels = {
            'nama': 'Nama Mata Pelajaran'
        }


class JadwalForm(forms.ModelForm):
    """Form untuk create dan update Jadwal"""
    
    class Meta:
        model = Jadwal
        fields = ['hari', 'jam_mulai', 'jam_selesai', 'kelas', 'mapel', 'guru']
        widgets = {
            'hari': forms.Select(attrs={
                'class': 'select select-bordered w-full'
            }),
            'jam_mulai': forms.TimeInput(attrs={
                'class': 'input input-bordered w-full',
                'type': 'time'
            }),
            'jam_selesai': forms.TimeInput(attrs={
                'class': 'input input-bordered w-full',
                'type': 'time'
            }),
            'kelas': forms.Select(attrs={
                'class': 'select select-bordered w-full'
            }),
            'mapel': forms.Select(attrs={
                'class': 'select select-bordered w-full'
            }),
            'guru': forms.Select(attrs={
                'class': 'select select-bordered w-full'
            }),
        }
        labels = {
            'hari': 'Hari',
            'jam_mulai': 'Jam Mulai',
            'jam_selesai': 'Jam Selesai',
            'kelas': 'Kelas',
            'mapel': 'Mata Pelajaran',
            'guru': 'Guru Pengajar'
        }
    
    def clean(self):
        cleaned_data = super().clean()
        jam_mulai = cleaned_data.get('jam_mulai')
        jam_selesai = cleaned_data.get('jam_selesai')
        
        if jam_mulai and jam_selesai:
            if jam_mulai >= jam_selesai:
                raise ValidationError({
                    'jam_selesai': 'Jam selesai harus setelah jam mulai.'
                })
        
        return cleaned_data
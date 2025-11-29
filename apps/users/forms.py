from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import Group, Permission
from django.forms import (
    CharField,
    CheckboxSelectMultiple,
    ModelForm,
    ModelMultipleChoiceField,
    PasswordInput,
    ValidationError,
)
from django import forms
from django.db import models

from .models import Akun, Peran, Siswa, Guru


class AkunCreationForm(ModelForm):
    password = CharField(
        label='Password',
        widget=PasswordInput,
        help_text='<ul><li>Your password can’t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can’t be a commonly used password.</li><li>Your password can’t be entirely numeric.</li></ul>',
    )
    password2 = CharField(
        label='Password confirmation',
        widget=PasswordInput,
        help_text='Enter the same password as before, for verification.',
    )
    groups = ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=CheckboxSelectMultiple,
        required=False,
        label='Group',
    )
    user_permissions = ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=CheckboxSelectMultiple,
        required=False,
        label='Izin Spesifik',
    )

    class Meta:
        model = Akun
        fields = ('email', 'peran')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.order_fields(
            [
                'email',
                'password',
                'password2',
                'peran',
                'groups',
                'user_permissions',
            ]
        )
        # Tambahkan class DaisyUI untuk checkbox
        for field_name in ['groups', 'user_permissions']:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update({'class': 'checkbox'})

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise ValidationError('The two password fields must match.')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            if 'groups' in self.cleaned_data:
                user.groups.set(self.cleaned_data['groups'])
            if 'user_permissions' in self.cleaned_data:
                user.user_permissions.set(self.cleaned_data['user_permissions'])
        return user


class AkunChangeForm(UserChangeForm):
    groups = ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=CheckboxSelectMultiple,
        required=False,
        label='Group',
    )
    user_permissions = ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=CheckboxSelectMultiple,
        required=False,
        label='Izin Spesifik',
    )

    class Meta(UserChangeForm.Meta):
        model = Akun
        fields = (
            'email',
            'peran',
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'password' in self.fields:
            del self.fields['password']
        # Tambahkan class DaisyUI untuk checkbox
        for field_name in ['groups', 'user_permissions']:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update({'class': 'checkbox'})

        # Tambahkan class DaisyUI untuk field boolean
        self.fields['is_active'].widget.attrs.update({'class': 'toggle toggle-primary'})
        self.fields['is_staff'].widget.attrs.update({'class': 'toggle toggle-primary'})
        self.fields['is_superuser'].widget.attrs.update(
            {'class': 'toggle toggle-primary'}
        )

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

            self.save_m2m()
        return instance


class SiswaForm(ModelForm):
    """Form untuk create dan update Siswa"""
    
    class Meta:
        model = Siswa
        fields = ['akun', 'nis', 'first_name', 'last_name', 'gender', 'nomor_handphone', 'alamat', 'tanggal_lahir']
        widgets = {
            'akun': forms.Select(attrs={
                'class': 'select select-bordered w-full'
            }),
            'nis': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Nomor Induk Siswa'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Nama depan'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Nama belakang'
            }),
            'gender': forms.Select(attrs={
                'class': 'select select-bordered w-full'
            }),
            'nomor_handphone': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': '08xxxxxxxxxx'
            }),
            'alamat': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full',
                'rows': 3,
                'placeholder': 'Alamat lengkap siswa'
            }),
            'tanggal_lahir': forms.DateInput(attrs={
                'class': 'input input-bordered w-full',
                'type': 'date'
            }),
        }
        labels = {
            'akun': 'Akun Pengguna',
            'nis': 'NIS',
            'first_name': 'Nama Depan',
            'last_name': 'Nama Belakang',
            'gender': 'Jenis Kelamin',
            'nomor_handphone': 'Nomor Handphone',
            'alamat': 'Alamat',
            'tanggal_lahir': 'Tanggal Lahir'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter akun to only show Siswa role accounts or accounts without profiles
        from django.db import models as django_models
        siswa_akuns = Akun.objects.filter(
            django_models.Q(peran__nama='Siswa') & 
            django_models.Q(siswa_profile__isnull=True)
        )
        if self.instance.pk:  # If editing, include current akun
            siswa_akuns = siswa_akuns | Akun.objects.filter(pk=self.instance.akun_id)
        
        self.fields['akun'].queryset = siswa_akuns
        self.fields['alamat'].required = False


class GuruForm(ModelForm):
    """Form untuk create dan update Guru"""
    
    class Meta:
        model = Guru
        fields = ['akun', 'nip', 'first_name', 'last_name', 'gender', 'jabatan', 'nomor_handphone', 'alamat', 'tanggal_lahir']
        widgets = {
            'akun': forms.Select(attrs={
                'class': 'select select-bordered w-full'
            }),
            'nip': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Nomor Induk Pegawai'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Nama depan'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Nama belakang'
            }),
            'gender': forms.Select(attrs={
                'class': 'select select-bordered w-full'
            }),
            'jabatan': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Contoh: Guru Matematika, Wakil Kepala Sekolah'
            }),
            'nomor_handphone': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': '08xxxxxxxxxx'
            }),
            'alamat': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full',
                'rows': 3,
                'placeholder': 'Alamat lengkap guru'
            }),
            'tanggal_lahir': forms.DateInput(attrs={
                'class': 'input input-bordered w-full',
                'type': 'date'
            }),
        }
        labels = {
            'akun': 'Akun Pengguna',
            'nip': 'NIP',
            'first_name': 'Nama Depan',
            'last_name': 'Nama Belakang',
            'gender': 'Jenis Kelamin',
            'jabatan': 'Jabatan',
            'nomor_handphone': 'Nomor Handphone',
            'alamat': 'Alamat',
            'tanggal_lahir': 'Tanggal Lahir'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter akun to only show Guru role accounts or accounts without profiles
        from django.db import models as django_models
        guru_akuns = Akun.objects.filter(
            django_models.Q(peran__nama='Guru') & 
            django_models.Q(guru_profile__isnull=True)
        )
        if self.instance.pk:  # If editing, include current akun
            guru_akuns = guru_akuns | Akun.objects.filter(pk=self.instance.akun_id)
            
        self.fields['akun'].queryset = guru_akuns
        self.fields['alamat'].required = False

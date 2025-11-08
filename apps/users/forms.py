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

from .models import Akun, Peran


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

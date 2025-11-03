from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group, Permission
from django.forms import (
    CheckboxSelectMultiple,
    ModelForm,
    ModelMultipleChoiceField,
    Select,
)
from .models import Akun, Peran


class AkunCreationForm(UserCreationForm):
    groups = ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=CheckboxSelectMultiple,
        required = False,
        label='Group'
    )
    user_permissions = ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=CheckboxSelectMultiple,
        required=False,
        label='Izin Spesifik'
    )

    class Meta(UserCreationForm.Meta):
        model = Akun
        fields = (
            'email',
            'password',
            'password2',
            'peran',
            'groups',
            'user_permissions',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Tambahkan class DaisyUI untuk checkbox
        for field_name in ['groups', 'user_permissions']:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update({'class': 'checkbox'})

    def save(self, commit=True):
        user = super().save(commit=False)
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
        label='Group'
    )
    user_permissions = ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=CheckboxSelectMultiple,
        required=False,
        label='Izin Spesifik'
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

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
    class Meta(UserCreationForm.Meta):
        model = Akun
        fields = ("email", "peran")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['peran'].queryset = Peran.objects.all()
        self.fields['peran'].widget = Select(
            attrs={'class': 'select select-bordered w-full'}
        )


class AkunChangeForm(UserChangeForm):
    class Meta:
        model = Akun
        fields = ('email', 'peran', 'is_active', 'is_staff', 'is_superuser')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'password' in self.fields:
            del self.fields['password']
        self.fields['peran'].queryset = Peran.objects.all()
        self.fields['peran'].widget = Select(
            attrs={'class': 'select select-bordered w-full'}
        )

class AkunPermissionForm(ModelForm):
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

    class Meta:
        model = Akun
        fields = ['is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        user = super().save(commit=False)

        if commit:
            user.save()

            user.groups.set(self.cleaned_data['groups'])
            user.user_permissions.set(self.cleaned_data['user_permissions'])
        return user

from django import template
from django.contrib.auth.models import Permission

register = template.Library()


@register.filter
def can_edit(user, app_model):
    """
    Check if user can edit/change objects for given app.model
    Usage: {% if user|can_edit:"users.akun" %}
    """
    if not user.is_authenticated:
        return False
    
    # Parse app_model format like "users.akun"
    if '.' in app_model:
        app_label, model_name = app_model.split('.', 1)
        permission_name = f"{app_label}.change_{model_name}"
    else:
        permission_name = f"change_{app_model}"
    
    return user.has_perm(permission_name)


@register.filter 
def can_delete(user, app_model):
    """
    Check if user can delete objects for given app.model
    Usage: {% if user|can_delete:"users.akun" %}
    """
    if not user.is_authenticated:
        return False
    
    # Parse app_model format like "users.akun"
    if '.' in app_model:
        app_label, model_name = app_model.split('.', 1)
        permission_name = f"{app_label}.delete_{model_name}"
    else:
        permission_name = f"delete_{app_model}"
    
    return user.has_perm(permission_name)


@register.filter
def can_add(user, app_model):
    """
    Check if user can add/create objects for given app.model
    Usage: {% if user|can_add:"users.akun" %}
    """
    if not user.is_authenticated:
        return False
    
    # Parse app_model format like "users.akun"
    if '.' in app_model:
        app_label, model_name = app_model.split('.', 1)
        permission_name = f"{app_label}.add_{model_name}"
    else:
        permission_name = f"add_{app_model}"
    
    return user.has_perm(permission_name)


@register.simple_tag
def user_role_name(user):
    """
    Get user role name
    Usage: {% user_role_name user %}
    """
    if hasattr(user, 'peran') and user.peran:
        return user.peran.nama
    return 'Tidak Ada Peran'


@register.simple_tag
def can_manage_data(user, data_type):
    """
    Check if user can manage specific data types based on role
    Usage: {% can_manage_data user "academic" %}
    """
    if not user.is_authenticated:
        return False
        
    if user.is_admin:
        return True
    
    if data_type == 'academic' and user.is_guru:
        return True
    
    if data_type == 'users' and user.is_admin:
        return True
        
    return False

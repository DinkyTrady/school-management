from django import template
from django.contrib.auth.models import AnonymousUser
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def can_edit_model(user, model_name):
    """
    Template filter to check if user can edit a specific model
    Usage: {% if user|can_edit_model:"tugas" %}
    """
    if isinstance(user, AnonymousUser) or not hasattr(user, 'can_edit_delete_model'):
        return False
    return user.can_edit_delete_model(model_name)


@register.filter  
def can_delete_model(user, model_name):
    """
    Template filter to check if user can delete a specific model
    Usage: {% if user|can_delete_model:"tugas" %}
    """
    if isinstance(user, AnonymousUser) or not hasattr(user, 'can_edit_delete_model'):
        return False
    return user.can_edit_delete_model(model_name)


@register.filter
def can_add_model(user, model_name):
    """
    Template filter to check if user can add new records for a model
    Usage: {% if user|can_add_model:"tugas" %}
    """
    if isinstance(user, AnonymousUser) or not hasattr(user, 'get_accessible_actions'):
        return False
    actions = user.get_accessible_actions(model_name)
    return 'add' in actions


@register.filter
def can_view_model(user, model_name):
    """
    Template filter to check if user can view a specific model
    Usage: {% if user|can_view_model:"tugas" %}
    """
    if isinstance(user, AnonymousUser) or not hasattr(user, 'can_access_model'):
        return False
    return user.can_access_model(model_name, 'view')


@register.filter
def user_accessible_actions(user, model_name):
    """
    Template filter to get list of accessible actions for user on model
    Usage: {% for action in user|user_accessible_actions:"tugas" %}
    """
    if isinstance(user, AnonymousUser) or not hasattr(user, 'get_accessible_actions'):
        return []
    return user.get_accessible_actions(model_name)


@register.simple_tag
def user_role_display(user):
    """
    Template tag to display user role
    Usage: {% user_role_display user %}
    """
    if isinstance(user, AnonymousUser):
        return "Guest"
    return getattr(user, 'get_user_peran', 'No Role')


@register.inclusion_tag('core/partials/action_buttons.html')
def show_action_buttons(user, model_name, object_id=None, list_url=None):
    """
    Inclusion tag to show appropriate action buttons based on user permissions
    Usage: {% show_action_buttons user "tugas" object.id %}
    """
    if isinstance(user, AnonymousUser):
        return {'buttons': []}
    
    actions = user.get_accessible_actions(model_name) if hasattr(user, 'get_accessible_actions') else []
    
    buttons = []
    
    if 'view' in actions and object_id:
        buttons.append({
            'action': 'view',
            'label': 'Lihat',
            'icon': 'fas fa-eye',
            'class': 'btn-info',
            'url': f'#{model_name}-view-{object_id}'  # You'll need to customize this
        })
    
    if 'change' in actions and object_id:
        buttons.append({
            'action': 'edit', 
            'label': 'Edit',
            'icon': 'fas fa-edit',
            'class': 'btn-warning',
            'url': f'#{model_name}-edit-{object_id}'  # You'll need to customize this
        })
    
    if 'delete' in actions and object_id:
        buttons.append({
            'action': 'delete',
            'label': 'Hapus', 
            'icon': 'fas fa-trash',
            'class': 'btn-error',
            'url': f'#{model_name}-delete-{object_id}'  # You'll need to customize this
        })
    
    if 'add' in actions:
        buttons.append({
            'action': 'add',
            'label': 'Tambah',
            'icon': 'fas fa-plus',
            'class': 'btn-success',
            'url': f'#{model_name}-add'  # You'll need to customize this
        })
    
    return {
        'buttons': buttons,
        'user_role': user.get_user_peran if hasattr(user, 'get_user_peran') else 'No Role',
        'model_name': model_name
    }


@register.simple_tag
def permission_check(user, permission_type, model_name):
    """
    Generic permission check tag
    Usage: {% permission_check user "edit" "tugas" as can_edit %}
    """
    if isinstance(user, AnonymousUser):
        return False
        
    if permission_type == 'edit' or permission_type == 'change':
        return user.can_edit_delete_model(model_name) if hasattr(user, 'can_edit_delete_model') else False
    elif permission_type == 'delete':
        return user.can_edit_delete_model(model_name) if hasattr(user, 'can_edit_delete_model') else False
    elif permission_type == 'add':
        actions = user.get_accessible_actions(model_name) if hasattr(user, 'get_accessible_actions') else []
        return 'add' in actions
    elif permission_type == 'view':
        return user.can_access_model(model_name, 'view') if hasattr(user, 'can_access_model') else False
    
    return False


@register.simple_tag
def role_badge(user):
    """
    Template tag to display role badge
    Usage: {% role_badge user %}
    """
    if isinstance(user, AnonymousUser):
        return mark_safe('<span class="badge badge-ghost">Guest</span>')
    
    role = getattr(user, 'get_user_peran', 'No Role')
    
    badge_classes = {
        'Administrator': 'badge-error',  # Red for admin
        'Admin': 'badge-error',
        'Guru': 'badge-warning',         # Orange for guru
        'Siswa': 'badge-info',           # Blue for siswa
    }
    
    badge_class = badge_classes.get(role, 'badge-ghost')
    
    return mark_safe(f'<span class="badge {badge_class}">{role}</span>')
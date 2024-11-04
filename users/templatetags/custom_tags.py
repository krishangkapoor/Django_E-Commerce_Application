from django import template

register = template.Library()

@register.filter(name='in_roles')
def in_roles(user, roles_string):
    roles_list = roles_string.split(',')
    return user.role in roles_list if hasattr(user, 'role') else False

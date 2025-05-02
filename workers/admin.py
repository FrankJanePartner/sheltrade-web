"""
Admin Configuration for the Workers App.

This module registers the `Workers` model with the Django admin site.
By registering the model, administrators can manage Workers Activities via the Django admin panel.

Features:
- Displays Workers Activities in the Django admin interface.
- Allows admin users to view, edit, and delete activities.

To access the Django admin panel, log in as a superuser and navigate to `/admin/`.

Usage:
- The `Workers` model is automatically available in the Django admin dashboard after registration.
"""
from django.contrib import admin
from .models import WorkersActivity

# Register the Workers model in the Django admin panel
admin.site.register(WorkersActivity)




# class CustomUserAdmin(UserAdmin):
#     def get_form(self, request, obj=None, **kwargs):
#         form = super().get_form(request, obj, **kwargs)
#         is_superuser = request.user.is_superuser

#         if not is_superuser:
#             form.base_fields['username'].disabled = True
#             form.base_fields['is_superuser'].disabled = True
#             form.base_fields['user_permissions'].disabled = True
#             form.base_fields['groups'].disabled = True
#         return form


# from django.contrib import admin
# from .models import Product
# from guardian.admin import GuardedModelAdmin
# from guardian.shortcuts import get_objects_for_user

# @admin.register(Product)
# class ProductAdmin(GuardedModelAdmin):
#     list_display = ('name',)

#     def has_module_permission(self, request):
#         if super().has_module_permission(request):
#             return True
#         return self.get_model_objects(request).exists()

#     def get_queryset(self, request):
#         if request.user.is_superuser:
#             return super().get_queryset(request)
#         data = self.get_model_objects(request)
#         return data

#     def get_model_objects(self, request, action=None, klass=None):
#         opts = self.opts
#         actions = [action] if action else ['view','edit','delete']
#         klass = klass if klass else opts.model
#         model_name = klass._meta.model_name
#         return get_objects_for_user(user=request.user, perms=[f'{perm}_{model_name}' for perm in actions], klass=klass, any_perm=True)

#     def has_permission(self, request, obj, action):
#         opts = self.opts
#         code_name = f'{action}_{opts.model_name}'
#         if obj:
#             return request.user.has_perm(f'{opts.app_label}.{code_name}', obj)
#         else:
#             return self.get_model_objects(request).exists()

#     def has_view_permission(self, request, obj=None):
#         return self.has_permission(request, obj, 'view')

#     def has_change_permission(self, request, obj=None):
#         return self.has_permission(request, obj, 'change')

#     def has_delete_permission(self, request, obj=None):
#         return self.has_permission(request, obj, 'delete')
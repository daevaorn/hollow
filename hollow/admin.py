# -*- coding: utf-8 -*-
from django.contrib import admin

from hollow import query, utils


utils.patch_log_entry_model()


class AdminSite(admin.AdminSite):
    def has_permission(self, request):
        return request.user.is_authenticated() and request.user.is_staff

    def index(self, request, extra_context=None):
        # FIXME: нужен свой user
        request.user.has_module_perms = lambda app_label: True

        return super(AdminSite, self).index(request, extra_context)

    def app_index(self, request, app_label, extra_context=None):
        request.user.has_module_perms = lambda app_label: True

        return super(AdminSite, self).app_index(request, app_label, extra_context)

    def check_dependencies(self):
        pass


class ModelAdmin(admin.ModelAdmin):
    def queryset(self, request):
        return query.QuerySet(self.model)

    def get_model_perms(self, request):
        return {
            'add':    self.has_add_permission(request),
            'change': self.has_change_permission(request, None),
            'delete': self.has_delete_permission(request, None),
        }

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def log_addition(self, request, object):
        pass

    def log_change(self, request, object, message):
        pass

    def log_deletion(self, request, object, object_repr):
        pass

    def message_user(self, request, message):
        pass

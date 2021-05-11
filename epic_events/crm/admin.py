from django.utils.translation import gettext, gettext_lazy as _
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import Client, Contract, CustomUser, Event, EventStatus, UserFunction


class EventAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser or request.user.groups.filter(name='management').exists():
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == "support_contact":
            kwargs["queryset"] = CustomUser.objects.filter(function__function='support')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_change_permission(self, request, obj=None):
        if request.user.groups.filter(name='support').exists():
            return obj is None or request.user == obj.support_contact
        if request.user.groups.filter(name='sale').exists():
            return obj is None or request.user == obj.contract_set.all()[0].sales_contact
        return super().has_change_permission(request,obj)



class ContractAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser or request.user.groups.filter(name='management').exists():
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == "client":
            kwargs["queryset"] = Client.objects.filter(sales_contact=request.user)
        if db_field.name == "sales_contact":
            kwargs["queryset"] = CustomUser.objects.filter(email=request.user.email)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_change_permission(self, request, obj=None):
        if request.user.groups.filter(name='sale').exists():
            return obj is None or request.user == obj.sales_contact
        return super().has_change_permission(request,obj)

class ClientAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        if request.user.groups.filter(name='sale').exists():
            return obj is None or request.user == obj.sales_contact
        return super().has_change_permission(request,obj)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser or request.user.groups.filter(name='management').exists():
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == "sales_contact":
            kwargs["queryset"] = CustomUser.objects.filter(email=request.user.email)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': ('function', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)






admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserFunction)
admin.site.register(EventStatus)
admin.site.register(Event, EventAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Contract, ContractAdmin)



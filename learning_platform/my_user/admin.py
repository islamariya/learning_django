from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from .models import MyUser

@admin.register(MyUser)
class MyUserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name','email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_student','is_teacher',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2'),
        }),
    )
    list_display = ('phone_number', 'first_name', 'last_name', 'is_staff', 'is_student','is_teacher')
    list_filter = ['is_student', 'is_teacher', 'is_staff', 'is_superuser']
    search_fields = ('phone_number', 'first_name', 'last_name', 'is_student', 'is_teacher')
    ordering = ('phone_number',)
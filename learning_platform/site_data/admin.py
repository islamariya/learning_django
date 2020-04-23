from django.contrib import admin

from .models import UserCorrespondence


@admin.register(UserCorrespondence)
class UserCorrespondenceAdmin(admin.ModelAdmin):
    list_display = ['date_of_receiving', 'subject', 'status']

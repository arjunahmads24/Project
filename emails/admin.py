from django.contrib import admin
from .models import Email

class EmailDisplayAdmin(admin.ModelAdmin):
    model = Email
    list_display = ['email', 'active', 'datetime_added']
    readonly_fields = ['datetime_added']

admin.site.register(Email, EmailDisplayAdmin)

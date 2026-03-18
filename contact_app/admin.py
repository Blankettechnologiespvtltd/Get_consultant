from django.contrib import admin
from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile', 'region', 'created_at')
    search_fields = ('name', 'email', 'mobile')
    list_filter = ('region', 'created_at')
    ordering = ('-created_at',)
    list_per_page = 10

admin.site.register(Contact, ContactAdmin)

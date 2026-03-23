from django.contrib import admin
from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile', 'subject', 'message', 'created_at')
    search_fields = ('name', 'email', 'mobile')
    list_filter = ('subject', 'created_at')
    ordering = ('-created_at',)
    list_per_page = 10

admin.site.register(Contact, ContactAdmin)

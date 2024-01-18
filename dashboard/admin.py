from django.contrib import admin

# Register your models here.
from .models import Contacts, Crushesdb, OTPAttempts

class ContactsAdmin(admin.ModelAdmin):
    list_display = ['email']


class CrushesdbAdmin(admin.ModelAdmin):
    list_display = ['submitter_email','crush_email']

admin.site.register(Contacts, ContactsAdmin)
admin.site.register(Crushesdb, CrushesdbAdmin)
admin.site.register(OTPAttempts)

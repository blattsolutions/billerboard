from django.contrib import admin
from .models import ListenImport, Liste, Entry, EntryRate, ListAssignment, DataEntryProfile
# Register your models here.

admin.site.register(ListenImport)
admin.site.register(Liste)
admin.site.register(Entry)
admin.site.register(EntryRate)
admin.site.register(ListAssignment)
admin.site.register(DataEntryProfile)


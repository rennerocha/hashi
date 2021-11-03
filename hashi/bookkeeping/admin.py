from bookkeeping.models import Account, Entry, Tag
from django.contrib import admin

admin.site.register(Account)
admin.site.register(Tag)


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ("date", "value", "type", "description", "account")
    list_filter = ("type", "account")

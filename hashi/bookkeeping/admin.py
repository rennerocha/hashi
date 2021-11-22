from bookkeeping.models import Account, Entry, Tag
from django.contrib import admin

admin.site.register(Account)
admin.site.register(Tag)


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ("date", "value", "type", "description", "account", "entry_tags")
    list_filter = ("type", "account")

    def entry_tags(self, obj):
        return " | ".join([a.name for a in obj.tags.all().order_by("name")])

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related("tags")

from bookkeeping.models import Entry
from django.shortcuts import render


def entry_list(request):
    context = {"entries": Entry.objects.all()}
    return render(request, "bookkeeping/entry_list.html", context=context)

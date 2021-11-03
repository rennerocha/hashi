from bookkeeping.models import Entry, EntryType
from django.db.models import Sum
from django.shortcuts import render


def entry_list(request):
    entries = Entry.objects.all()

    total_expense, total_income = 0, 0
    for entry in entries.values("type").annotate(total_value=Sum("value")):
        if entry["type"] == EntryType.INCOME.value:
            total_income = entry["total_value"]
        elif entry["type"] == EntryType.EXPENSE.value:
            total_expense = entry["total_value"]

    context = {
        "entries": Entry.objects.all(),
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": total_income - total_expense,
    }
    return render(request, "bookkeeping/entry_list.html", context=context)

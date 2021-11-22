import datetime
from urllib.parse import urlencode

from bookkeeping.models import EntryType
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from model_bakery import baker


class EntryList(TestCase):
    def test_access_entry_list(self):
        response = self.client.get(reverse("bookkeeping:entry-list"))
        self.assertEqual(response.status_code, 200)

    def test_access_entry_list_with_correct_template(self):
        response = self.client.get(reverse("bookkeeping:entry-list"))
        self.assertTemplateUsed(response, "bookkeeping/entry_list.html")

    def test_entry_list_with_no_entries(self):
        response = self.client.get(reverse("bookkeeping:entry-list"))

        self.assertQuerysetEqual(response.context["entries"], [])

    def test_entry_list_with_entries(self):
        entry_1 = baker.make("bookkeeping.Entry")
        entry_2 = baker.make("bookkeeping.Entry")

        response = self.client.get(reverse("bookkeeping:entry-list"))

        self.assertQuerysetEqual(
            response.context["entries"], [entry_1, entry_2], ordered=False
        )

    def test_entry_list_with_entries_of_current_month_by_default(self):
        this_month_date = timezone.now().date().replace(day=1)
        last_month_date = this_month_date - datetime.timedelta(days=1)
        next_month_date = (this_month_date + datetime.timedelta(days=32)).replace(day=1)

        entry_1 = baker.make("bookkeeping.Entry", date=last_month_date)
        entry_2 = baker.make("bookkeeping.Entry", date=this_month_date)
        entry_3 = baker.make("bookkeeping.Entry", date=next_month_date)

        response = self.client.get(reverse("bookkeeping:entry-list"))

        self.assertFalse(entry_1 in response.context["entries"])
        self.assertTrue(entry_2 in response.context["entries"])
        self.assertFalse(entry_3 in response.context["entries"])

    def test_entry_list_with_total_income(self):
        baker.make("bookkeeping.Entry", value=500, type=EntryType.INCOME)
        baker.make("bookkeeping.Entry", value=400, type=EntryType.INCOME)

        response = self.client.get(reverse("bookkeeping:entry-list"))

        self.assertEqual(response.context["total_income"], 900)

    def test_entry_list_with_total_expense(self):
        baker.make("bookkeeping.Entry", value=500, type=EntryType.EXPENSE)
        baker.make("bookkeeping.Entry", value=400, type=EntryType.EXPENSE)

        response = self.client.get(reverse("bookkeeping:entry-list"))

        self.assertEqual(response.context["total_expense"], 900)

    def test_entry_list_with_balance_context(self):
        baker.make("bookkeeping.Entry", value=100, type=EntryType.EXPENSE)
        baker.make("bookkeeping.Entry", value=100, type=EntryType.EXPENSE)
        baker.make("bookkeeping.Entry", value=500, type=EntryType.INCOME)
        baker.make("bookkeeping.Entry", value=500, type=EntryType.INCOME)

        response = self.client.get(reverse("bookkeeping:entry-list"))

        self.assertEqual(response.context["total_expense"], 200)
        self.assertEqual(response.context["total_income"], 1000)
        self.assertEqual(response.context["balance"], 800)

    def test_entry_list_filter_by_year_and_month(self):
        this_month_date = timezone.now().date().replace(day=1)
        last_month_date = this_month_date - datetime.timedelta(days=1)
        next_month_date = (this_month_date + datetime.timedelta(days=32)).replace(day=1)

        entry_1 = baker.make("bookkeeping.Entry", date=last_month_date)
        entry_2 = baker.make("bookkeeping.Entry", date=this_month_date)
        entry_3 = baker.make("bookkeeping.Entry", date=next_month_date)

        url_params = {"month": last_month_date.month, "year": last_month_date.year}
        entry_list_url = f'{reverse("bookkeeping:entry-list")}?{urlencode(url_params)}'

        response = self.client.get(entry_list_url)

        self.assertTrue(entry_1 in response.context["entries"])
        self.assertFalse(entry_2 in response.context["entries"])
        self.assertFalse(entry_3 in response.context["entries"])

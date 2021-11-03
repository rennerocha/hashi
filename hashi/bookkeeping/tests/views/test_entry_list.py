from django.test import TestCase
from django.urls import reverse
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

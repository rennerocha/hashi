import datetime

from bookkeeping.models import Account, Entry, EntryType, Tag, new_entry
from django.test import TestCase


class NewEntry(TestCase):
    def setUp(self):
        self.account = Account.objects.create(name="My Bank")
        self.entry_params = {
            "date": datetime.date.today(),
            "value": 123.45,
            "type": EntryType.INCOME,
            "description": "Test Entry",
        }

    def test_create_new_entry_for_existing_account(self):
        entry = new_entry(
            **self.entry_params,
            account_name=self.account.name,
        )
        expected_entry = Entry(**self.entry_params, account=self.account)

        self.assertEqual(entry.date, expected_entry.date)
        self.assertEqual(entry.value, expected_entry.value)
        self.assertEqual(entry.type, expected_entry.type)
        self.assertEqual(entry.description, expected_entry.description)
        self.assertEqual(entry.account, expected_entry.account)

    def test_raise_error_if_account_does_not_exist(self):
        with self.assertRaises(ValueError):
            new_entry(
                **self.entry_params,
                account_name="Not My Bank",
            )

    def test_create_new_entry_with_existing_tag(self):
        tag = Tag.objects.create(name="rent")
        entry = new_entry(
            **self.entry_params,
            account_name=self.account.name,
            tags=[
                "rent",
            ],
        )
        self.assertQuerysetEqual(
            entry.tags.all(),
            [
                tag,
            ],
        )

    def test_create_new_entry_with_multiple_existing_tags(self):
        tag_1 = Tag.objects.create(name="rent")
        tag_2 = Tag.objects.create(name="regular")

        entry = new_entry(
            **self.entry_params,
            account_name=self.account.name,
            tags=["regular", "rent"],
        )

        self.assertQuerysetEqual(
            entry.tags.all(),
            [
                tag_1,
                tag_2,
            ],
            ordered=False,
        )

    def test_create_new_entry_with_new_tag(self):
        entry = new_entry(
            **self.entry_params, account_name=self.account.name, tags=["electricity"]
        )

        electricity_tag = Tag.objects.filter(name="electricity")
        self.assertTrue(electricity_tag.exists())
        self.assertQuerysetEqual(
            entry.tags.all(),
            [
                electricity_tag.first(),
            ],
            ordered=False,
        )

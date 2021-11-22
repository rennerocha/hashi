# This is a temporary solution to load entries that are stored in
# the existing version of LHC finances. We can remove it as
# soon we deprecate the old system and start using this new app
# to manage LHC finances
import sqlite3

from bookkeeping.models import Account, EntryType, new_entry
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Load entries of existing database"

    def add_arguments(self, parser):
        parser.add_argument("--db")
        parser.add_argument("--start_date", required=False)

    def handle(self, *args, **options):
        db = options["db"]
        self.stdout.write(f"Loading entries from: {db}")

        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        query = "SELECT * FROM entry"

        start_date = options.get("start_date")
        if start_date is not None:
            self.stdout.write(f"Start date: {start_date}")
            query += f" WHERE entry_date >= '{start_date}'"

        counter = 0
        for entry in cursor.execute(query):
            _, date, value, account_name, tags, description = entry

            Account.objects.get_or_create(name=account_name)

            if value >= 0:
                type_ = EntryType.INCOME
            else:
                type_ = EntryType.EXPENSE
                value = -1 * value

            tags = tags.split(",")

            new_entry(date, value, type_, description, account_name, tags=tags)

            counter += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully loaded {counter} entries."))

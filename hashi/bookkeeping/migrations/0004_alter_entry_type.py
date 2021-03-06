# Generated by Django 3.2.9 on 2021-12-01 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bookkeeping", "0003_alter_entry_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="entry",
            name="type",
            field=models.PositiveSmallIntegerField(
                choices=[(1, "INCOME"), (2, "EXPENSE"), (3, "TRANSFER")]
            ),
        ),
    ]

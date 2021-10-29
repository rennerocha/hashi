from django.db import models


class EntryType(models.IntegerChoices):
    INCOME = 1, "INCOME"
    EXPENSE = 2, "EXPENSE"


class Account(models.Model):
    name = models.CharField(max_length=12, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=12, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Entry(models.Model):
    date = models.DateField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.PositiveSmallIntegerField(choices=EntryType.choices)
    account = models.ForeignKey(Account, null=True, on_delete=models.SET_NULL)
    description = models.CharField(max_length=128)
    tags = models.ManyToManyField(Tag)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "entries"


def new_entry(date, value, type, description, account_name, tags=None):
    account = Account.objects.filter(name=account_name).first()
    if account is None:
        raise ValueError(f"Unable to find an Account with name '{account_name}'")

    entry = Entry.objects.create(
        date=date,
        value=value,
        type=type,
        description=description,
        account=account,
    )
    if tags is not None:
        for tag_name in tags:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            entry.tags.add(tag)

    return entry

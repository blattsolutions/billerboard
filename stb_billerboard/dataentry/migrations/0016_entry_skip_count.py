# Generated by Django 4.2.7 on 2023-12-21 19:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dataentry", "0015_entry_is_paid"),
    ]

    operations = [
        migrations.AddField(
            model_name="entry",
            name="skip_count",
            field=models.IntegerField(default=0),
        ),
    ]

# Generated by Django 4.2.7 on 2023-12-04 06:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("billerboard", "0009_alter_unternehmen_options_and_more"),
        ("dataentry", "0005_entry_on_hold_entry_started_at"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="liste",
            name="unternehmen",
        ),
        migrations.AddField(
            model_name="liste",
            name="kontekte",
            field=models.ManyToManyField(blank=True, to="billerboard.kontakt"),
        ),
    ]

# Generated by Django 4.2.7 on 2023-12-13 05:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("billerboard", "0010_remove_unternehmen_kontakt_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="kontakt",
            name="anrede",
            field=models.CharField(
                blank=True,
                choices=[("HERR", "Herr"), ("FRAU", "Frau")],
                max_length=200,
                null=True,
            ),
        ),
    ]

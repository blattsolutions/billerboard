# Generated by Django 4.2.7 on 2024-01-22 11:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("billerboard", "0013_dealdaten_datei_dealdaten_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="deal",
            name="deal_closed_at",
            field=models.DateField(blank=True, null=True),
        ),
    ]

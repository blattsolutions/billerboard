# Generated by Django 4.2.7 on 2023-12-04 06:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("dataentry", "0007_rename_kontekte_liste_kontakte"),
    ]

    operations = [
        migrations.AlterField(
            model_name="liste",
            name="import_liste",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="import_liste",
                to="dataentry.listenimport",
            ),
        ),
    ]

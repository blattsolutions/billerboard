# Generated by Django 4.2.7 on 2023-11-23 08:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        (
            "billerboard",
            "0005_kontakt_anrede_kontakt_doer_kontakt_eingetragen_von_and_more",
        ),
        ("dataentry", "0002_entryrate_entry_rate"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listenimport",
            name="liste",
            field=models.FileField(max_length=500, upload_to="uploads/listen/"),
        ),
        migrations.CreateModel(
            name="UserRate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "rate",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="dataentry.entryrate",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ListAssignment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "kontakt",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="kontakt",
                        to="billerboard.kontakt",
                    ),
                ),
                (
                    "liste",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="liste",
                        to="dataentry.liste",
                    ),
                ),
                (
                    "unternehmen",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="unternehmen",
                        to="billerboard.unternehmen",
                    ),
                ),
            ],
        ),
    ]

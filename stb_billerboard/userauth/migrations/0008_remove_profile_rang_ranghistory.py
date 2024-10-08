# Generated by Django 4.2.7 on 2024-01-31 14:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("userauth", "0007_profile_last_rang_update_alter_profile_rang"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="rang",
        ),
        migrations.CreateModel(
            name="RangHistory",
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
                ("rang_updated_at", models.DateTimeField(auto_now_add=True)),
                (
                    "rang",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="userauth.rang"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rang_history",
                        to="userauth.profile",
                    ),
                ),
            ],
        ),
    ]

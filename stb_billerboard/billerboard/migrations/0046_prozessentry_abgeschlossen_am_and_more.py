# Generated by Django 4.2.9 on 2024-05-03 02:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('billerboard', '0045_alter_share_share_added_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='prozessentry',
            name='abgeschlossen_am',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='prozessentry',
            name='prozess_von_zwei',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prozess_von_zwei', to=settings.AUTH_USER_MODEL),
        ),
    ]

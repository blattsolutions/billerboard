# Generated by Django 4.2.9 on 2024-02-27 04:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('billerboard', '0028_alter_interviewboardentry_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProzessEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prozess_added_at', models.DateTimeField(auto_now_add=True)),
                ('stelle', models.CharField(max_length=200)),
                ('kunde', models.CharField(blank=True, max_length=200, null=True)),
                ('revenue', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('eingetragen_von', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='eingetragen_von_prozess', to=settings.AUTH_USER_MODEL)),
                ('prozess_von', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prozess_von', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

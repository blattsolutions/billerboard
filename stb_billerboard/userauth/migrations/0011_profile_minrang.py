# Generated by Django 4.2.9 on 2024-04-03 07:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0010_profile_ist_aktiv_profile_toolabrechnungszyklus_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='minrang',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='userauth.rang'),
        ),
    ]

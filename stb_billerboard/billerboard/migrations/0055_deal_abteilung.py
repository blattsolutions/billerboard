# Generated by Django 4.2.9 on 2024-06-25 08:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0011_profile_minrang'),
        ('billerboard', '0054_deal_bonding_mail'),
    ]

    operations = [
        migrations.AddField(
            model_name='deal',
            name='abteilung',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='userauth.abteilung'),
        ),
    ]

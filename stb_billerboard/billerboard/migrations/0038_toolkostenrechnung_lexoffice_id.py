# Generated by Django 4.2.9 on 2024-03-11 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billerboard', '0037_tool_toolkostenrechnung'),
    ]

    operations = [
        migrations.AddField(
            model_name='toolkostenrechnung',
            name='lexoffice_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]

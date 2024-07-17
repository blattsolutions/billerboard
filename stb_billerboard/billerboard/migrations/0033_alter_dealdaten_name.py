# Generated by Django 4.2.9 on 2024-02-27 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billerboard', '0032_deal_genehmigt_von'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dealdaten',
            name='name',
            field=models.CharField(choices=[('AGB', 'AGB vom Kunden'), ('DSGVO', 'DSGVO vom Kandidaten'), ('VERTRAG', 'Vertrag unterschrieben von beiden Parteien'), ('SERVICEABRECHNUNG', 'Serviceabrechnung'), ('SONSTIGES', 'Sonstiges')], max_length=200),
        ),
    ]

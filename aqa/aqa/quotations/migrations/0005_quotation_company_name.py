# Generated by Django 3.0.9 on 2020-09-19 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotations', '0004_auto_20200919_1002'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotation',
            name='company_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]

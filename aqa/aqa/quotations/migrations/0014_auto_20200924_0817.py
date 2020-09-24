# Generated by Django 3.0.9 on 2020-09-24 08:17

import aqa.quotations.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('quotations', '0013_auto_20200924_0803'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotation',
            name='created_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AddField(
            model_name='quotation',
            name='expiry_date',
            field=models.DateField(blank=True, default=aqa.quotations.models.quote_duration, null=True),
        ),
    ]

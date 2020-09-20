# Generated by Django 3.0.9 on 2020-09-20 09:47

import aqa.quotations.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('quotations', '0008_auto_20200920_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotation',
            name='created_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='quotation',
            name='expiry_date',
            field=models.DateField(blank=True, default=aqa.quotations.models.quote_duration, null=True),
        ),
    ]

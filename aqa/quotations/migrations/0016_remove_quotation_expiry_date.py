# Generated by Django 3.0.9 on 2020-09-24 08:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotations', '0015_auto_20200924_0833'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quotation',
            name='expiry_date',
        ),
    ]

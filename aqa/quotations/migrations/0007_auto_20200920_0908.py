# Generated by Django 3.0.9 on 2020-09-20 09:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotations', '0006_auto_20200920_0851'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quotation',
            old_name='created',
            new_name='created_date',
        ),
    ]

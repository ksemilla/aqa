# Generated by Django 3.0.9 on 2020-10-08 10:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotations', '0018_auto_20201008_0948'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quotationitem',
            name='line_number',
        ),
    ]
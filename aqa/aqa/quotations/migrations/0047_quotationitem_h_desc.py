# Generated by Django 3.0.9 on 2020-11-08 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotations', '0046_auto_20201030_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotationitem',
            name='h_desc',
            field=models.PositiveIntegerField(default=1),
        ),
    ]

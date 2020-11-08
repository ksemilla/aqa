# Generated by Django 3.0.9 on 2020-11-08 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotations', '0047_quotationitem_h_desc'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quotation',
            old_name='discount',
            new_name='discount_rate',
        ),
        migrations.AddField(
            model_name='quotation',
            name='discount_amount',
            field=models.IntegerField(default=0),
        ),
    ]

# Generated by Django 3.0.9 on 2020-10-15 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_auto_20201014_0841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sell_price',
            field=models.IntegerField(default=0),
        ),
    ]

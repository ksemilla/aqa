# Generated by Django 3.0.9 on 2020-09-20 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20200920_0905'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='cost_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='sell_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='stock_qty',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='model_name',
            field=models.CharField(max_length=30, null=True),
        ),
    ]

# Generated by Django 3.0.9 on 2020-09-20 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20200919_1058'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='model_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]

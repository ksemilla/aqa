# Generated by Django 3.0.9 on 2020-09-20 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20200920_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(max_length=200, null=True),
        ),
    ]

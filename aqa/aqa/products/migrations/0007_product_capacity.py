# Generated by Django 3.0.9 on 2020-09-20 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20200920_0937'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='capacity',
            field=models.CharField(max_length=20, null=True),
        ),
    ]

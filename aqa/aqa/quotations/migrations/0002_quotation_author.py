# Generated by Django 3.0.9 on 2020-08-31 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotation',
            name='author',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]

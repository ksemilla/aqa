# Generated by Django 3.0.9 on 2020-10-10 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotations', '0020_auto_20201008_1357'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotationitem',
            name='line_number',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]

# Generated by Django 3.0.9 on 2020-10-13 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20201010_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='scope',
            field=models.CharField(choices=[('user', 'user'), ('admin', 'admin'), ('ae', 'ae'), ('se', 'se'), ('sl', 'sl'), ('bh', 'bh'), ('scm', 'scm')], default='user', max_length=16),
        ),
    ]

# Generated by Django 3.0.9 on 2020-09-19 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='scope',
            field=models.CharField(choices=[('user', 'user'), ('admin', 'admin'), ('ae', 'ae'), ('se', 'se'), ('sl', 'sl')], default='user', max_length=16),
        ),
    ]

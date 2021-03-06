# Generated by Django 3.0.9 on 2020-10-13 15:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quotations', '0025_auto_20201013_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotation',
            name='application_engr',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quotations_as_ae', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='quotation',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quotations_as_author', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='quotation',
            name='sales_engr',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quotations_as_se', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='quotation',
            name='sales_lead',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quotations_as_sl', to=settings.AUTH_USER_MODEL),
        ),
    ]

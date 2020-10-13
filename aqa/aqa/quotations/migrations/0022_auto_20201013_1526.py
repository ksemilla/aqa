# Generated by Django 3.0.9 on 2020-10-13 15:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quotations', '0021_quotationitem_line_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotation',
            name='application_engr',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='application_engr', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='quotation',
            name='sales_engr',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sales_engr', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='quotation',
            name='sales_lead',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sales_lead', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='quotation',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL),
        ),
    ]
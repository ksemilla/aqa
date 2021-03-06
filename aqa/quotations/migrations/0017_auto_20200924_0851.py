# Generated by Django 3.0.9 on 2020-09-24 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quotations', '0016_remove_quotation_expiry_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quotationitem',
            name='cost_price',
        ),
        migrations.RemoveField(
            model_name='quotationitem',
            name='sell_price',
        ),
        migrations.AlterField(
            model_name='quotationitem',
            name='quotation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quotations.Quotation'),
        ),
    ]

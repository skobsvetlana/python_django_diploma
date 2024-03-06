# Generated by Django 5.0.1 on 2024-03-06 11:29

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_deliverycost'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliverycost',
            name='dateFrom',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deliverycost',
            name='dateTo',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='deliverycost',
            name='minCostForFreeDelivery',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='deliverycost',
            name='express',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='deliverycost',
            name='standart',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]

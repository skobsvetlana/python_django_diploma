# Generated by Django 5.0.1 on 2024-02-16 14:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_remove_category_category_id_category_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, db_column='parent', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='children', to='catalog.category'),
        ),
    ]

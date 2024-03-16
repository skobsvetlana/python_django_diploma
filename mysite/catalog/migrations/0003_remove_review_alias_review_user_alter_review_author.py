# Generated by Django 5.0.1 on 2024-03-10 17:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_review_alias'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='alias',
        ),
        migrations.AddField(
            model_name='review',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='review',
            name='author',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
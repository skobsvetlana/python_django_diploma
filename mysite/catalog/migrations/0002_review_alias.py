# Generated by Django 5.0.1 on 2024-03-10 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='alias',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
# Generated by Django 5.1.5 on 2025-01-28 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='time',
            field=models.TimeField(auto_now_add=True),
        ),
    ]

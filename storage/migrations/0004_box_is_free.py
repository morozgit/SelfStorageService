# Generated by Django 4.0 on 2023-11-17 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0003_storage_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='box',
            name='is_occupied',
            field=models.BooleanField(default=False, verbose_name='Занят'),
        ),
    ]

# Generated by Django 3.2.15 on 2023-12-05 11:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('announcements', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcements',
            name='author',
            field=models.CharField(max_length=100),
        ),
    ]

# Generated by Django 3.2.23 on 2024-02-09 20:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("software", "0002_auto_20240208_0245"),
    ]

    operations = [
        migrations.AddField(
            model_name="software",
            name="file_size",
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="software",
            name="tags",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]

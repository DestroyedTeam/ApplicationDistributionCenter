# Generated by Django 3.2.15 on 2024-01-30 19:42

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="FrontEndUser",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("username", models.CharField(max_length=200, unique=True)),
                ("password", models.CharField(max_length=200)),
                ("email", models.EmailField(max_length=200, unique=True)),
            ],
            options={
                "verbose_name": "前台用户管理",
                "verbose_name_plural": "前台用户管理",
                "db_table": "front_end_user",
            },
        ),
    ]

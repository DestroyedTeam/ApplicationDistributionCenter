# Generated by Django 3.2.23 on 2024-03-06 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontenduser', '0010_alter_frontenduser_django_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='frontenduser',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
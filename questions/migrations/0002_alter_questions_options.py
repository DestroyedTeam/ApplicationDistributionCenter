# Generated by Django 3.2.15 on 2024-01-13 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='questions',
            options={'ordering': ['-date'], 'verbose_name': '反馈中心', 'verbose_name_plural': '反馈中心'},
        ),
    ]
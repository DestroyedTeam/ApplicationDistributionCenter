# Generated by Django 3.2.23 on 2024-03-05 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontenduser', '0007_frontenduser_nickname'),
    ]

    operations = [
        migrations.AddField(
            model_name='frontenduser',
            name='state',
            field=models.IntegerField(choices=[(1, '正常'), (2, '封禁')], default=1),
        ),
    ]
# Generated by Django 3.2.23 on 2024-03-15 06:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('frontenduser', '0012_alter_frontenduser_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='frontenduser',
            name='django_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
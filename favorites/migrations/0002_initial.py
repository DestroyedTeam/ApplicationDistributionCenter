# Generated by Django 3.2.15 on 2024-01-30 19:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('software', '0001_initial'),
        ('favorites', '0001_initial'),
        ('front', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='favorites',
            name='correlation_software',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='software.software'),
        ),
        migrations.AddField(
            model_name='favorites',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='frontenduser.frontenduser'),
        ),
        migrations.AlterUniqueTogether(
            name='favorites',
            unique_together={('user', 'correlation_article'), ('user', 'correlation_software')},
        ),
    ]
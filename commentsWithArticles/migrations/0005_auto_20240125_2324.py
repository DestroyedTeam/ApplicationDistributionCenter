# Generated by Django 3.2.15 on 2024-01-25 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('software', '0004_auto_20240125_2324'),
        ('commentsWithArticles', '0004_comment_correlation_model'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-updated_time'], 'verbose_name': '文章管理', 'verbose_name_plural': '文章管理'},
        ),
        migrations.AlterUniqueTogether(
            name='article',
            unique_together={('title', 'correlation_software')},
        ),
        migrations.AlterUniqueTogether(
            name='comment',
            unique_together={('correlation_article', 'correlation_software')},
        ),
        migrations.RemoveField(
            model_name='comment',
            name='correlation_model',
        ),
    ]

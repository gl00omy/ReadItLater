# Generated by Django 4.2.3 on 2023-07-20 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paperCapsule', '0014_remove_article_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='is_archived',
            field=models.BooleanField(default=False),
        ),
    ]

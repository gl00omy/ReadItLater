# Generated by Django 4.2.3 on 2023-07-18 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paperCapsule', '0010_article_archived'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='highlights',
            field=models.TextField(blank=True, null=True),
        ),
    ]

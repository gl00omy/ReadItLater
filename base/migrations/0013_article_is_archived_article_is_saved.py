# Generated by Django 4.2 on 2023-05-08 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_favoritearticle'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='is_archived',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='article',
            name='is_saved',
            field=models.BooleanField(default=False),
        ),
    ]

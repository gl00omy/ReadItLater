# Generated by Django 4.2 on 2023-05-06 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_rename_archiveddarticle_archivedarticle'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='favorites',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
# Generated by Django 4.2.3 on 2023-07-17 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paperCapsule', '0003_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(blank=True, to='paperCapsule.tag'),
        ),
    ]

# Generated by Django 4.2.3 on 2023-07-18 13:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('paperCapsule', '0008_article_favorites'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='saves',
            field=models.ManyToManyField(blank=True, related_name='save_article', to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 4.2.3 on 2023-07-29 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_eventviews'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]

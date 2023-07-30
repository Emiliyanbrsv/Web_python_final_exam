# Generated by Django 4.2.3 on 2023-07-29 16:56

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0005_event_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='get_slug', unique=True),
        ),
    ]

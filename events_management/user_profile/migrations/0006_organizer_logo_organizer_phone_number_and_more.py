# Generated by Django 4.2.3 on 2023-07-12 13:00

import django.core.validators
from django.db import migrations, models
import events_management.user_profile.validators


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0005_organizer'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizer',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='profile_photos/', validators=[events_management.user_profile.validators.validate_file_less_than_5mb]),
        ),
        migrations.AddField(
            model_name='organizer',
            name='phone_number',
            field=models.CharField(default=1, max_length=20, validators=[django.core.validators.MinLengthValidator(4)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='organizer',
            name='website',
            field=models.URLField(default=1),
            preserve_default=False,
        ),
    ]

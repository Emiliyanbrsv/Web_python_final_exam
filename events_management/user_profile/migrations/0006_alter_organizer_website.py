# Generated by Django 4.2.3 on 2023-08-11 15:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0005_alter_organizer_website'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizer',
            name='website',
            field=models.URLField(blank=True, max_length=254, null=True, validators=[django.core.validators.MinLengthValidator(2)]),
        ),
    ]

# Generated by Django 4.2.3 on 2023-08-08 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0009_eventregistration_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventregistration',
            name='phone_number',
            field=models.CharField(max_length=11),
        ),
    ]

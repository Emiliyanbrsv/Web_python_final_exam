# Generated by Django 4.2.3 on 2023-07-12 03:08

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import events_management.event.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_name', models.CharField(max_length=30, validators=[django.core.validators.MinLengthValidator(2)])),
                ('country', models.CharField(max_length=30, validators=[django.core.validators.MinLengthValidator(2)])),
                ('description', models.TextField(max_length=300, validators=[django.core.validators.MinLengthValidator(10)])),
                ('image', models.ImageField(upload_to='locations/', validators=[events_management.event.validators.validate_file_less_than_5mb])),
            ],
            options={
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, validators=[django.core.validators.MinLengthValidator(2)])),
                ('start_date_time', models.DateTimeField(validators=[events_management.event.validators.check_if_date_is_past])),
                ('end_date_time', models.DateTimeField(validators=[events_management.event.validators.check_if_date_is_past])),
                ('description', models.TextField(max_length=300, validators=[django.core.validators.MinLengthValidator(10)])),
                ('image', models.ImageField(upload_to='events/', validators=[events_management.event.validators.validate_file_less_than_5mb])),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.location')),
            ],
            options={
                'ordering': ('pk',),
            },
        ),
    ]

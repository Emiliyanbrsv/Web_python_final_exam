# Generated by Django 4.2.3 on 2023-07-11 22:13

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import events_management.user_profile.models
import events_management.user_profile.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('first_name', models.CharField(max_length=30, validators=[django.core.validators.MinLengthValidator(2)])),
                ('last_name', models.CharField(max_length=30, validators=[django.core.validators.MinLengthValidator(2)])),
                ('date_of_birth', models.DateField(blank=True, null=True, validators=[events_management.user_profile.validators.check_if_date_is_future])),
                ('gender', models.CharField(choices=[('male', 'MALE'), ('female', 'FEMALE'), ('do not show', 'DO_NOT_SHOW')], default=events_management.user_profile.models.Gender['DO_NOT_SHOW'], max_length=11)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profile_photos/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

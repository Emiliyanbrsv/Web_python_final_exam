from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from events_management.user_profile.validators import check_if_date_is_future
from events_management.utils.utils import Gender
from events_management.user_profile.validators import validate_name_start_with_capital_letter, \
    validate_name_is_only_letters, \
    validate_phone_number, validate_file_less_than_5mb

# user_profile

UserModel = get_user_model()


class Profile(models.Model):
    __MAX_LEN_NAME = 30
    __MIN_LEN_NAME = 2

    first_name = models.CharField(
        max_length=__MAX_LEN_NAME,
        validators=(
            MinLengthValidator(__MIN_LEN_NAME),
            validate_name_start_with_capital_letter,
            validate_name_is_only_letters,
        ),
        null=False,
        blank=False,
    )

    last_name = models.CharField(
        max_length=__MAX_LEN_NAME,
        validators=(
            MinLengthValidator(__MIN_LEN_NAME),
            validate_name_start_with_capital_letter,
            validate_name_is_only_letters,
        ),
        null=False,
        blank=False,
    )

    date_of_birth = models.DateField(
        validators=(
            check_if_date_is_future,
        ),
        null=True,
        blank=True,
    )

    phone_number = models.CharField(
        max_length=13,
        validators=(
            MinLengthValidator(5),
            validate_phone_number,
        ),
        null=True,
        blank=True,
    )

    gender = models.CharField(
        choices=Gender.choices(),
        max_length=Gender.max_length(),
    )

    profile_image = models.ImageField(
        upload_to='profile_photos/',
        validators=(
            validate_file_less_than_5mb,
        ),
        null=True,
        blank=True,
    )

    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )


class Organizer(models.Model):
    __MAX_LEN_NAME = 30
    __MIN_LEN_NAME = 2
    __MAX_LEN_DESCRIPTION = 300
    __MIN_LEN_DESCRIPTION = 10
    __MAX_LEN_WEBSITE = 254
    __MIN_LEN_WEBSITE = 2

    name = models.CharField(
        max_length=__MAX_LEN_NAME,
        validators=(
            MinLengthValidator(__MIN_LEN_NAME),
        ),
        null=False,
        blank=False,
    )

    description = models.TextField(
        max_length=__MAX_LEN_DESCRIPTION,
        validators=(
            MinLengthValidator(__MIN_LEN_DESCRIPTION),
        ),
        null=False,
        blank=False,
    )

    website = models.URLField(
        max_length=__MAX_LEN_WEBSITE,
        validators=(
            MinLengthValidator(__MIN_LEN_WEBSITE),
        ),
        null=True,
        blank=True,
    )

    phone_number = models.CharField(
        max_length=13,
        validators=(
            MinLengthValidator(5),
            validate_phone_number,
        ),
        null=False,
        blank=False,
    )

    logo = models.ImageField(
        upload_to='profile_photos/',
        validators=(
            validate_file_less_than_5mb,
        ),
        null=True,
        blank=True,
    )

    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )


@receiver(post_save, sender=UserModel)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.profile_type == 'organizer':
            Organizer.objects.create(user=instance)
        else:
            Profile.objects.create(user=instance)

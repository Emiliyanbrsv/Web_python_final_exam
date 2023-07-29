from enum import Enum

from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from events_management.user_profile.validators import check_if_date_is_future, validate_file_less_than_5mb

# user_profile

UserModel = get_user_model()


class ChoicesMixin:
    @classmethod
    def choices(cls):
        return [(choice.value, choice.name) for choice in cls]


class ChoicesStringsMixin(ChoicesMixin):
    @classmethod
    def max_length(cls):
        return max(len(x.value) for x in cls)


class Gender(ChoicesStringsMixin, Enum):
    MALE = 'Male'
    FEMALE = 'Female'
    DO_NOT_SHOW = 'Do not show'


class Profile(models.Model):
    __MAX_LEN_NAME = 30
    __MIN_LEN_NAME = 2

    first_name = models.CharField(
        max_length=__MAX_LEN_NAME,
        validators=(
            MinLengthValidator(__MIN_LEN_NAME),
        ),
        null=False,
        blank=False,
    )

    last_name = models.CharField(
        max_length=__MAX_LEN_NAME,
        validators=(
            MinLengthValidator(__MIN_LEN_NAME),
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
    name = models.CharField(
        max_length=300
    )

    description = models.TextField(
        max_length=300
    )

    website = models.URLField(
        max_length=200

    )
    phone_number = models.CharField(
        max_length=20,
        validators=(
            MinLengthValidator(4),
        ),
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

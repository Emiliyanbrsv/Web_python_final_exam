from autoslug.utils import slugify
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models

from events_management.common.models import Location
from events_management.event.validators import check_if_date_is_past
from events_management.user_profile.models import Organizer
from events_management.event.validators import validate_file_less_than_5mb, validate_name_start_with_capital_letter, \
    validate_name_is_only_letters, validate_phone_number

UserModel = get_user_model()


class Event(models.Model):
    __MAX_LEN_NAME = 30
    __MIN_LEN_NAME = 2
    __MAX_LEN_DESCRIPTION = 300
    __MIN_LEN_DESCRIPTION = 10

    name = models.CharField(
        max_length=__MAX_LEN_NAME,
        validators=(
            MinLengthValidator(__MIN_LEN_NAME),
        ),
        null=False,
        blank=False,
    )

    start_date_time = models.DateTimeField(
        validators=(
            check_if_date_is_past,
        ),
        null=False,
        blank=False,
    )

    end_date_time = models.DateTimeField(
        validators=(
            check_if_date_is_past,
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

    image = models.ImageField(
        upload_to='events/',
        validators=(
            validate_file_less_than_5mb,
        ),
        null=True,
        blank=True,
    )

    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
    )

    organizer = models.ForeignKey(
        Organizer,
        on_delete=models.CASCADE,
    )

    slug = models.SlugField(
        unique=True,
        editable=False,
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.slug:
            self.slug = slugify(f'{self.name}-{self.pk}')
        return super().save(*args, **kwargs)

    def is_registered(self, user):
        return self.eventregistration_set.filter(user=user).exists()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ('pk',)


class EventViews(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE
    )

    views_count = models.PositiveIntegerField(
        default=0
    )

    date_and_time_of_view = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} viewed {self.event.name} ({self.views_count} views)"


class EventRegistration(models.Model):
    __MAX_LEN_NAME = 30
    __MIN_LEN_NAME = 2
    __DEFAULT_ATTENDEES = 1

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

    attendees = models.PositiveIntegerField(
        default=__DEFAULT_ATTENDEES,
        null=False,
        blank=False,
    )

    phone_number = models.CharField(
        max_length=12,
        validators=(
            MinLengthValidator(5),
            validate_phone_number,
        ),
        null=False,
        blank=False,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE
    )

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
    )

    registration_date = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ('pk',)

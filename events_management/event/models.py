from autoslug import AutoSlugField
from django.core.validators import MinLengthValidator
from django.db import models

from events_management.event.validators import check_if_date_is_past
from events_management.event.validators import validate_file_less_than_5mb
from events_management.user_profile.models import Organizer


# event model
class Location(models.Model):
    __NAME_MAX_LEN = 30
    __NAME_MIN_LEN = 2
    __MAX_LEN_DESCRIPTION = 300
    __MIN_LEN_DESCRIPTION = 10

    city_name = models.CharField(
        max_length=__NAME_MAX_LEN,
        validators=(
            MinLengthValidator(__NAME_MIN_LEN),
        ),
        null=False,
        blank=False,
    )

    country = models.CharField(
        max_length=__NAME_MAX_LEN,
        validators=(
            MinLengthValidator(__NAME_MIN_LEN),
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
        upload_to='locations/',
        validators=(
            validate_file_less_than_5mb,
        ),
        null=False,
        blank=False,
    )

    class Meta:
        ordering = ('pk',)

    def __str__(self):
        return f'{self.city_name}, {self.country}'


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

    #
    # slug = AutoSlugField(
    #     populate_from=lambda instance: f'{instance.location.city_name}-{instance.pk}',
    #     unique=True,
    #     editable=False,
    # )

    class Meta:
        ordering = ('pk',)

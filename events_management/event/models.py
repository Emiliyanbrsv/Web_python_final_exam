from autoslug import AutoSlugField
from autoslug.utils import slugify
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models

from events_management.event.validators import check_if_date_is_past
from events_management.event.validators import validate_file_less_than_5mb
from events_management.user_profile.models import Organizer

UserModel = get_user_model()


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

    slug = models.SlugField(
        unique=True,
        editable=False,
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.slug:
            self.slug = slugify(f'{self.name}-{self.pk}')
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ('pk',)


class EventViews(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        # related_name='eventviews',
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE
    )

    views_count = models.PositiveIntegerField(
        default=0
    )

    # date_and_time_of_view = models.DateTimeField(
    #     auto_now_add=True,
    # )

    def __str__(self):
        return f"{self.user.username} viewed {self.event.name} ({self.views_count} views)"


class EventRegistration(models.Model):

    first_name = models.CharField(
        max_length=30,
        null=False,
        blank=False,
    )

    last_name = models.CharField(
        max_length=30,
        null=False,
        blank=False,
    )

    attendees = models.PositiveIntegerField(
        default=1,
        null=False,
        blank=False,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE
    )

    phone_number = models.IntegerField(
        null=False,
        blank=False,
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

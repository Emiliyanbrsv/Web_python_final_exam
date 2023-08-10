from django.core.validators import MinLengthValidator
from django.db import models

from events_management.common.validators import validate_file_less_than_5mb, validate_name_start_with_capital_letter, \
    validate_name_is_only_letters


# common model
class Location(models.Model):
    __NAME_MAX_LEN = 30
    __NAME_MIN_LEN = 2
    __MAX_LEN_DESCRIPTION = 300
    __MIN_LEN_DESCRIPTION = 10

    city_name = models.CharField(
        max_length=__NAME_MAX_LEN,
        validators=(
            MinLengthValidator(__NAME_MIN_LEN),
            validate_name_start_with_capital_letter,
            validate_name_is_only_letters,
        ),
        null=False,
        blank=False,
    )

    country = models.CharField(
        max_length=__NAME_MAX_LEN,
        validators=(
            MinLengthValidator(__NAME_MIN_LEN),
            validate_name_start_with_capital_letter,
            validate_name_is_only_letters,
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

    def __str__(self):
        return f'{self.city_name}, {self.country}'

    class Meta:
        ordering = ('pk',)

from django.core.exceptions import ValidationError
from django.utils import timezone

from events_management.utils.utils import megabytes_to_bytes


def check_if_date_is_past(value):
    today = timezone.now()
    if value < today:
        raise ValidationError('Event start date cannot be in the past.')


def validate_file_less_than_5mb(fileobj):
    filesize = fileobj.file.size
    megabyte_limit = 5.0
    if filesize > megabytes_to_bytes(megabyte_limit):
        raise ValidationError(f'Max file size is {megabyte_limit}MB')

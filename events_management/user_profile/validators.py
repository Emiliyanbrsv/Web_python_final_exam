from datetime import date

from django.core.exceptions import ValidationError

from events_management.utils.utils import megabytes_to_bytes


def check_if_date_is_future(value):
    today = date.today()
    if value > today:
        raise ValidationError('Date of birth cannot be in the future.')


def validate_file_less_than_5mb(fileobj):
    filesize = fileobj.file.size
    megabyte_limit = 5.0
    if filesize > megabytes_to_bytes(megabyte_limit):
        raise ValidationError(f'Max file size is {megabyte_limit}MB')

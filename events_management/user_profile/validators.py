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


def validate_name_start_with_capital_letter(value: str):
    if not value[0].isupper():
        raise ValidationError("Name should start with a capital letter.")


def validate_name_is_only_letters(value: str):
    if not value.isalpha():
        raise ValidationError("Name should contain only letters.")


def validate_phone_number(value):
    if not value.isdigit():
        raise ValidationError("Phone number should contain only digits.")

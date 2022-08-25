from django.core.exceptions import ValidationError
from datetime import datetime


def validate_date_not_in_past(date):
    if date < datetime.now().date():
        raise ValidationError('Date cannot be in the past!')


def validate_date_time_not_in_past(date_time):
    if date_time.replace(tzinfo=None) < datetime.now():
        raise ValidationError('Date cannot be in the past!')

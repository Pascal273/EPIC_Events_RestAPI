from django.core.exceptions import ValidationError
from datetime import datetime


def validate_date_not_in_past(date):
    if date < datetime.now().date():
        raise ValidationError('Date cannot be in the past!')

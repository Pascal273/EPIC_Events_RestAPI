from .validators import validate_date_not_in_past

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Client(models.Model):
    """ The Model for Clients"""
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=30, unique=True)
    phone = models.CharField(max_length=30, null=True)
    mobile = models.CharField(max_length=30, null=True)
    company_name = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    sales_contact = models.ForeignKey(
        to=User, on_delete=models.SET_NULL, null=True)
    existing = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Contract(models.Model):
    """The model for Contracts"""
    STATUS_OPTIONS = (
        ('SIGNED', 'SIGNED'),
        ('APPROVED', 'APPROVED'),
        ('CLOSED', 'CLOSED'),
        ('CANCELLED', 'CANCELLED'),
        ('EXPIRED', 'EXPIRED')
    )

    client = models.ForeignKey(
        to=Client, on_delete=models.CASCADE, related_name='client')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_OPTIONS)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_due = models.DateField(validators=[validate_date_not_in_past])

    def __str__(self):
        datetime_obj = self.date_created
        datetime_str = datetime_obj.strftime("%m.%d.%Y, %H:%M")
        return f'{self.client} - contract from {datetime_str}'


class Event(models.Model):
    """The model for Events"""
    STATUS_OPTIONS = (
        ('PROCESSING', 'PROCESSING'),
        ('UPCOMING', 'UPCOMING'),
        ('ONGOING', 'ONGOING'),
        ('COMPLETED', 'COMPLETED'),
        ('CANCELLED', 'CANCELLED')
    )

    event_name = models.CharField(max_length=50, null=True)
    contract = models.OneToOneField(to=Contract,  # only one event per contract
                                    on_delete=models.CASCADE,
                                    related_name='contract')
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    support_contact = models.ForeignKey(
        to=User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=10, choices=STATUS_OPTIONS)
    attendees = models.IntegerField()
    event_date_time = models.DateTimeField(null=True)
    notes = models.CharField(max_length=255, null=True)

    def __str__(self):
        date = self.event_date_time.strftime("%m-%d-&Y, %H:%M")
        return f'{self.event_name} - {date}'

    def save(self, *args, **kwargs):
        contract = self.contract
        self.client = contract.client
        super(Event, self).save(*args, **kwargs)

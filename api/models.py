from .validators import validate_date_not_in_past

from django.db import models
from django.db.models import Q
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
        ('OPEN', 'OPEN'),
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

    def save(self, *args, **kwargs):
        """
        Modified save method to convert the related client as
        'existing' or 'potential' clients depending on the contract's status.
        """
        not_active = ['OPEN', 'CLOSED', 'CANCELLED', 'EXPIRED']
        active = ['SIGNED', 'APPROVED']
        client = self.client
        # contract active -> client 'existing'
        if self.status not in not_active:
            client.existing = True
            client.save()

        # contract not active -> client not 'existing'
        active_contracts = Contract.objects.filter(
            Q(client=client) & Q(status__in=active)
        ).exists()
        if self.status in not_active and not active_contracts:
            client.existing = False
            client.save()

        super(Contract, self).save(*args, **kwargs)

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
        """
        custom method to:
        - add client from related contract automatically
        - change contract status to approved if an event is created
        """

        contract = self.contract
        self.client = contract.client
        if contract.status == 'SIGNED':
            contract.status = 'APPROVED'
            contract.save()
        super(Event, self).save(*args, **kwargs)

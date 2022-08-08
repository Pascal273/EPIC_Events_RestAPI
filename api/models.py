from django.db import models
from django.contrib.auth import get_user_model


class Client(models.Model):
    """ The Model for Clients"""
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    phone = models.CharField(max_length=30, null=True)
    mobile = models.CharField(max_length=30, null=True)
    company_name = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    sales_contact = models.ForeignKey(
        to=get_user_model(), on_delete=models.SET_NULL, null=True)
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
    payment_due = models.DateTimeField()

    def __str__(self):
        return f'{self.client} - contract from {self.date_created}'


class Event(models.Model):
    """The model for Events"""
    STATUS_OPTIONS = (
        ('PROCESSING', 'PROCESSING'),
        ('UPCOMING', 'UPCOMING'),
        ('ONGOING', 'ONGOING'),
        ('COMPLETED', 'COMPLETED'),
        ('CANCELLED', 'CANCELLED')
    )

    name = models.CharField(max_length=50, null=True)
    contract = models.ForeignKey(to=Contract, on_delete=models.CASCADE)
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    support_contact = models.ForeignKey(
        to=get_user_model(), on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=10, choices=STATUS_OPTIONS)
    attendees = models.IntegerField()
    event_date = models.DateTimeField(null=True)
    notes = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    """The model for Team"""

    name = models.CharField(max_length=50)
    permissions = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class TeamMembers(models.Model):
    """Through table to establish the team membership of an employee"""
    employee = models.ForeignKey(to=get_user_model(),
                                 on_delete=models.CASCADE,
                                 related_name='employee')

    team = models.ForeignKey(to=Team,
                             on_delete=models.SET_NULL,
                             related_name='team',
                             null=True)

    class Meta:
        unique_together = ('employee', 'team')

    def __str__(self):
        return f'{self.employee}_{self.team}'

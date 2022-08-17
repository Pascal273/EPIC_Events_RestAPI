from django.contrib.auth.models import \
    AbstractUser, BaseUserManager, Group, Permission
from django.utils.translation import gettext_lazy as _

from django.db import models


class UserManager(BaseUserManager):
    """Model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    The User-Model - uses unique email only, instead of username.
    """
    email = models.EmailField(unique=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email


class Employee(models.Model):
    user = models.OneToOneField(to=User,
                                on_delete=models.CASCADE,
                                related_name='user',
                                null=False)
    phone = models.CharField(max_length=30, null=True)
    mobile = models.CharField(max_length=30, null=True)
    hire_date = models.DateField(null=True)
    birth_date = models.DateField(null=True)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


class Team(Group):

    class Meta:
        proxy = True
        app_label = 'authentication'
        verbose_name = _('Team')

    def __str__(self):
        return self.name


class TeamMembership(models.Model):
    """Through table to establish the team membership of an employee"""
    employee = models.OneToOneField(to=User,
                                    on_delete=models.CASCADE,
                                    related_name='employee')

    team = models.ForeignKey(to=Team,
                             on_delete=models.SET_NULL,
                             related_name='team',
                             null=True
                             )

    class Meta:
        unique_together = ['employee', 'team']
        verbose_name_plural = _('Team Memberships')

    def __str__(self):
        return f'{self.team.name} | ' \
               f'{self.employee.first_name} {self.employee.last_name}'

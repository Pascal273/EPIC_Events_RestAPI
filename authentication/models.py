from django.contrib.auth.models import \
    AbstractBaseUser, BaseUserManager, Group, Permission, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

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
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    The Custom-User-Model - uses unique email only, instead of username.
    """
    email = models.EmailField(unique=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'birth_date']

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=30, null=True)
    mobile = models.CharField(max_length=30, null=True)
    hire_date = models.DateField(null=True)
    birth_date = models.DateField(null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    def __str__(self):
        return self.email


class Team(Group):

    class Meta:
        proxy = True
        app_label = 'authentication'
        verbose_name = _('Team')

    def __str__(self):
        return self.name


# TODO save changes on team permissions on user permissions!
# @receiver(post_save, sender=Team)
# def post_save_permissions(sender, instance, created, **kwargs):
#     if not created:
#         print(instance.permissions.all())
#         print(kwargs)


class TeamMembership(models.Model):
    """Through table to establish the team membership of an employee"""
    user = models.OneToOneField(to=User,
                                on_delete=models.CASCADE,
                                related_name='user')

    team = models.ForeignKey(to=Team,
                             on_delete=models.SET_NULL,
                             related_name='team',
                             null=True
                             )

    class Meta:
        unique_together = ['user', 'team']
        verbose_name_plural = _('Team Memberships')

    def __str__(self):
        return f'{self.team.name} | ' \
               f'{self.user.first_name} {self.user.last_name}'

    def save(self, *args, **kwargs):
        """
        Custom Save-Method to update User_groups, staff status,
        superuser status and user_permissions automatically.
        """
        user = self.user
        team = self.team
        # set group
        user.groups.set([team])
        # user is active when added to a team.
        user.is_active = True
        # set team permissions to the user permissions.
        team_permissions = team.permissions.all()
        user.user_permissions.set(team_permissions)
        # management team members are staff and superusers.
        if user.groups.first().name == 'Management':
            user.is_staff = True
            user.is_superuser = True
        # members of other teams are not staff nor superusers.
        if user.groups.first().name != 'Management':
            user.is_staff = False
            user.is_superuser = False
        user.save()
        super(TeamMembership, self).save(*args, **kwargs)

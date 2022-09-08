from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Team, TeamMembership


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    team = serializers.SerializerMethodField()  # -> get_team

    def get_team(self, user):
        team_membership = user.groups.first().name
        if team_membership:
            return team_membership
        return None

    class Meta:
        model = User
        fields = ['email', 'url', 'first_name', 'last_name', 'password',
                  'phone', 'mobile', 'birth_date', 'last_login', 'hire_date',
                  'joined', 'is_active', 'team']
        read_only_fields = ['is_staff', 'is_superuser']


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class TeamMembershipSerializer(serializers.ModelSerializer):

    team = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Team.objects.all(),
    )
    user = serializers.SlugRelatedField(
        slug_field='email',
        # only show users that aren't members of any team already
        queryset=User.objects.all().exclude(
            user__in=TeamMembership.objects.all().values_list(
                'user', flat=True
            )
        ),
    )

    class Meta:
        model = TeamMembership
        fields = ['id', 'team', 'user']


class NestedUserSerializer(UserSerializer):
    """Serializer for Employees in Nested views"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'mobile']

from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Team, TeamMembership


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    team = serializers.SerializerMethodField()  # -> get_team

    def get_team(self, user):
        team_membership = TeamMembership.objects.filter(user=user).first()
        if team_membership:
            return TeamSerializer(
                team_membership.team, many=False, required=False
            ).data['name']
        return None

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'phone',
                  'mobile', 'birth_date', 'last_login', 'hire_date',
                  'joined', 'is_active', 'team']
        read_only_fields = ['is_staff', 'is_superuser', 'team']


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
            user__in=[
                member for member in TeamMembership.objects.all()
            ]
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

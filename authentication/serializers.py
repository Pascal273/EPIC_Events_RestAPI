from rest_framework import serializers

from .models import User, Employee, TeamMembership, Team


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class TeamMembershipSerializer(serializers.ModelSerializer):

    team = serializers.CharField()
    employee = serializers.EmailField()

    class Meta:
        model = TeamMembership
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer for the Full Employee-View"""
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    team = serializers.SerializerMethodField()

    def get_team(self, employee):
        """Gets representation from TeamMembershipSerializer to display the
        name of the Team the employee is a member of."""
        team_member_obj = TeamMembership.objects.get(employee=employee.user.id)
        return TeamMembershipSerializer(
            team_member_obj, many=False).data['team']

    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ['user', ]


class NestedEmployeeSerializer(EmployeeSerializer):
    """Serializer for Employees in Nested views"""
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'phone', 'mobile']

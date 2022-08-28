from django.shortcuts import render, redirect

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .serializers import *
from .permissions import IsNotAuthenticated, IsManagement
from .forms import SignUpForm


class UserViewSet(viewsets.ModelViewSet):
    """API endpoint that allows Users to be viewed."""

    queryset = User.objects.all().order_by('-hire_date')
    serializer_class = UserSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions,
        IsManagement
    ]


class TeamMembershipViewSet(viewsets.ModelViewSet):
    """API endpoint that allows Team Memberships to be viewed."""

    queryset = TeamMembership.objects.all().order_by('team')
    serializer_class = TeamMembershipSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions,
        IsManagement
    ]


class TeamViewSet(viewsets.ModelViewSet):
    """API endpoint that allows Team Memberships to be viewed."""

    queryset = Team.objects.all().order_by('name')
    serializer_class = TeamSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions,
        IsManagement
    ]


class UserSignUpView(GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [permissions.AllowAny, IsNotAuthenticated]
    write_only = True

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            try:
                user = get_user_model()
                validate_password(serializer.data['password'], user)
            except ValidationError as error:
                return Response(str(error), status=status.HTTP_400_BAD_REQUEST)

            serializer.create(serializer.data)
            return Response({'Account created': serializer.data['email']},
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def signup(request):
    """The view for the sign-up page."""
    # allow only unauthenticated user to visit the signup page
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = SignUpForm()
        return render(request, 'signup/signup.html', {'form': form})

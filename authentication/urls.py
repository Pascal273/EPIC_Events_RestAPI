from django.urls import path, include
from rest_framework.routers import DefaultRouter

from authentication import views

router = DefaultRouter()

router.register(r'users', views.UserViewSet, basename='user')
router.register(
    r'team_members', views.TeamMembershipViewSet, basename='team_member')
router.register(r'teams', views.TeamViewSet, basename='team')

urlpatterns = [
    path('', include(router.urls)),
]

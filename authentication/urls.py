from django.urls import path, include
from rest_framework.routers import DefaultRouter

from authentication import views

router = DefaultRouter()

router.register(r'employees', views.EmployeeViewSet, basename='employees')
router.register(
    r'team_members', views.TeamMembershipViewSet, basename='team_members')
router.register(r'teams', views.TeamViewSet, basename='teams')

urlpatterns = [
    path('', include(router.urls))
]
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from authentication import views

router = DefaultRouter()

router.register(r'users', views.UserViewSet, basename='users')
router.register(
    r'team_members', views.TeamMembershipViewSet, basename='team_members')
router.register(r'teams', views.TeamViewSet, basename='teams')

urlpatterns = [
    path('', include(router.urls)),
    path('request_signup/', views.UserSignUpView.as_view(),
         name='request_signup'),
]

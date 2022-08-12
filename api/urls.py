from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()

router.register(r'clients', views.ClientViewSet)
router.register(r'contracts', views.ContractViewSet)
router.register(r'events', views.EventViewSet)

urlpatterns = [
    path('', include(router.urls))
]

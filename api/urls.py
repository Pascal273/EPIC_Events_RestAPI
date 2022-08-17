from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()

router.register(
    r'potential_clients',
    views.PotentialClientViewSet,
    basename='potential_clients'
)
router.register(
    r'existing_clients',
    views.ExistingClientViewSet,
    basename='existing_clients'
)
router.register(
    r'contracts',
    views.ContractViewSet,
    basename='contracts'
)
router.register(
    r'events',
    views.EventViewSet,
    basename='events'
)

urlpatterns = [
    path('', include(router.urls))
]

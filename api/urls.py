from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()

router.register(
    r'clients',
    views.ClientViewSet,
    basename='client'
)
router.register(
    r'potential_clients',
    views.PotentialClientViewSet,
    basename='potential_client'
)
router.register(
    r'existing_clients',
    views.ExistingClientViewSet,
    basename='existing_client'
)
router.register(
    r'contracts',
    views.ContractViewSet,
    basename='contract'
)
router.register(
    r'events',
    views.EventViewSet,
    basename='event'
)

urlpatterns = [
    path('', include(router.urls))
]

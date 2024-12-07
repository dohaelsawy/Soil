from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import BookingsViewSet

router = DefaultRouter()
router.register(r'',BookingsViewSet, basename="bookings")



urlpatterns = [] + router.urls
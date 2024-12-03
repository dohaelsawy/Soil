from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import SpaceViewSet
from . import views

router = DefaultRouter()
router.register(r'', SpaceViewSet,basename="spaces")

urlpatterns = [

] + router.urls
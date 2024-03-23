from django.urls import path
from rest_framework import routers

from airport import views

app_name = "airport"

router = routers.DefaultRouter()
router.register("airports", views.AirportViewSet)
router.register("cities", views.CityViewSet)
router.register("countries", views.CountryViewSet)

urlpatterns = router.urls

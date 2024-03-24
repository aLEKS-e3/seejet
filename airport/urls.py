from django.urls import path
from rest_framework import routers

from airport import views

app_name = "airport"

router = routers.DefaultRouter()
router.register("airports", views.AirportViewSet)
router.register("cities", views.CityViewSet)
router.register("countries", views.CountryViewSet)
router.register("routes", views.RouteViewSet)
router.register("airplane-types", views.AirplaneTypeViewSet)
router.register("airplanes", views.AirplaneViewSet)
router.register("crew", views.CrewViewSet)
router.register("flights", views.FlightViewSet)

urlpatterns = router.urls

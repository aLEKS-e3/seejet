from django.urls import path
from rest_framework import routers

from airport import views

app_name = "airport"

router = routers.DefaultRouter()
router.register("airports", views.AirportViewSet)

urlpatterns = router.urls

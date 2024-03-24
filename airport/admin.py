from django.contrib import admin

from airport import models

admin.site.register(models.Airport)
admin.site.register(models.Country)
admin.site.register(models.City)
admin.site.register(models.AirplaneType)
admin.site.register(models.Crew)
admin.site.register(models.Airplane)
admin.site.register(models.Route)
admin.site.register(models.Flight)

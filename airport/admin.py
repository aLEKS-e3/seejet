from django.contrib import admin

from airport import models

admin.site.register(models.Airport)
admin.site.register(models.Country)
admin.site.register(models.City)

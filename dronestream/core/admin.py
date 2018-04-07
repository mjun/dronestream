from django.contrib import admin

from .models import Country, Province, Town, Strike

admin.site.register(Country)
admin.site.register(Province)
admin.site.register(Town)
admin.site.register(Strike)

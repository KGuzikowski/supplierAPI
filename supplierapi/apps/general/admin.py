from django.contrib import admin

from .models import Country, DialingCode, Industry

admin.site.register(Country)
admin.site.register(Industry)
admin.site.register(DialingCode)

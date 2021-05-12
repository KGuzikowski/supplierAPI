from django.contrib import admin

from .models import Address, Company, Employee, PhoneNumber, Role

admin.site.register(Company)
admin.site.register(Employee)
admin.site.register(Role)
admin.site.register(Address)
admin.site.register(PhoneNumber)

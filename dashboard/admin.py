from django.contrib import admin

# Register your models here.
from  beautyapp.models import Appointment
from dashboard.models import Guest, Expenses
admin.site.register(Appointment)
admin.site.register(Guest)
admin.site.register(Expenses)


# admin.site.register(User)

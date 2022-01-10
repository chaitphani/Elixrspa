from django.contrib import admin
from django.db.models.fields import DurationField

from .models import *
from dashboard.models import *


class GiftAdmin(admin.ModelAdmin):
    list_display=('name','email','mobile','address','message','price')


admin.site.register(Gift, GiftAdmin)
admin.site.register(Citys)
admin.site.register(User)
admin.site.register(Carriers)
admin.site.register(Services)
admin.site.register(Appointment)
admin.site.register(Guest)
admin.site.register(Expenses)
admin.site.register(Addstaff)
admin.site.register(Franchisee)
admin.site.register(Addduration)
admin.site.register(Paymentmod)
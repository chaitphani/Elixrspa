from django.contrib import admin

from dashboard.models import *
from beautyapp.models import User

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
admin.site.register(Franchisee)
admin.site.register(Addduration)
admin.site.register(Paymentmod)

admin.site.register(BranchMaster)
admin.site.register(GroupMaster)
admin.site.register(AccountMaster)
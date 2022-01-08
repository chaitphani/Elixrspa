from django.urls import path
from spadashboard import views
from django.contrib import admin

from django.conf import settings
admin.site.header = 'Elixir Beauty Spa'

urlpatterns = [
    path('',views.home,name='homek'),
    path('attendancelist',views.attendancelist,name='attendancelist'),
    path('citylist',views.citylist,name='citylist'),
    path('clientlist',views.clientlist,name='clientlist'),
    path('expensedetails',views.expensedetails,name='expensedetails'),
    path('franchiseelist',views.franchiseelist,name='franchiseelist'),
    path('managerlist',views.managerlist,name='managerlist'),
    path('servicelist',views.servicelist,name='servicelist'),
    path('stafflist',views.stafflist,name='stafflist'),
    path('useractivity',views.useractivity,name='useractivity'),
]    
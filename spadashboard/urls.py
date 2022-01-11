from django.urls import path
from spadashboard import views


urlpatterns = (

    path('',views.home,name='homek'),
    path('attendancelist',views.attendancelist,name='attendancelist'),

    path('gift',views.gift,name='gift'),
    path('carriers',views.carriers,name='carriers'),
    path('appointment',views.appointment,name='appointment'),
    path('payment_mode',views.payment_mode,name='payment_mode'),
    path('add-duration',views.add_duration,name='add_duration'),
    path('daily-report',views.daily_report,name='daily_report'),
    
    path('city',views.citylist,name='citylist'),
    path('city/<int:id>/update', views.city_edit, name='update_city'),

    path('service',views.servicelist,name='servicelist'),
    path('service/<int:id>/update', views.service_edit, name='update_service'),
    path('service/<int:id>/delete', views.service_delete, name='delete_service'),

    path('expense',views.expense_list,name='expense_list'),
    path('expense/<int:id>/update', views.expense_edit, name='update_expense'),
    path('expense/<int:id>/delete', views.delete_expense, name='delete_expense'),

    path('client',views.clientlist,name='clientlist'),
    path('client/<int:id>/update', views.client_edit, name='edit_client'),
    path('client/<int:id>/delete', views.client_delete, name='delete_client'),

    path('franchisee',views.franchiseelist,name='franchiseelist'),
    path('franchisee/<int:id>/delete', views.franchise_delete, name='delete_franchise'),

    path('manager',views.managerlist,name='managerlist'),
    path('manager/<int:id>/update', views.manager_edit, name='update_manager'),
    path('manager/<int:id>/delete', views.manager_delete, name='delete_manager'),

    path('staff',views.stafflist,name='stafflist'),
    path('staff/<int:id>/update', views.staff_edit, name='update_staff'),
    path('staff/<int:id>/delete', views.staff_delete, name="delete_staff"),
    
    path('useractivity',views.useractivity,name='useractivity'),
)
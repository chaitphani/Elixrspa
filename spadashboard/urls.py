from os import name
from django.urls import path
from spadashboard import views


urlpatterns = (

    path('',views.dashboard,name='dashboard'),
    path('attendancelist',views.attendancelist,name='attendancelist'),

    path('appointment/list',views.appointment,name='list_appointment'),
    path('daily-report',views.daily_report,name='daily_report'),

    path('account-master',views.account_master,name='account_master'),
    path('account-master/<int:id>/update', views.account_master_edit, name='update_account_master'),
    path('account-master/<int:id>/delete', views.account_master_delete, name='delete_account_master'),

    path('group-master',views.group_master,name='group_master'),
    path('group-master/<int:id>/update', views.group_master_edit, name='update_group_master'),
    path('group-master/<int:id>/delete', views.group_master_delete, name='delete_group_master'),

    path('branch-master',views.branch_master,name='branch_master'),
    path('branch-master/<int:id>/update', views.branch_master_edit, name='update_branch_master'),
    path('branch-master/<int:id>/delete', views.branch_master_delete, name='delete_branch_master'),

    path('payment-mode',views.payment_mode,name='payment_mode'),
    path('payment-mode/<int:id>/delete', views.payment_mode_delete, name='delete_payment_mode'),

    path('duration',views.duration,name='duration'),
    path('duration/<int:id>/delete', views.duration_delete, name='delete_duration'),

    path('careers',views.careers,name='careers'),
    path('career/<int:id>/delete', views.careere_delete, name="delete_career"),

    path('gift',views.gift,name='gift'),
    path('gift/<int:id>/delete', views.gift_delete, name='delete_gift'),

    path('city',views.citylist,name='citylist'),
    path('city/<int:id>/update', views.city_edit, name='update_city'),
    path('city/<int:id>/delete', views.city_delete, name='delete_city'),

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

    path('attendace/in', views.in_attendace, name='attendance_in'),
    path('attendace/out', views.out_attendace, name='attendance_out'),
    

    path('item-master',views.item_master,name='item_master'),
    path('add-commission',views.add_commission,name='add_commission'),
    path('membership-plan',views.membership_plan,name='membership_plan'),
    path('membership-list',views.membership_list,name='membership_list'),
)
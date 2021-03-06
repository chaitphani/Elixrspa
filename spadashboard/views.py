from django.shortcuts import render, redirect
from beautyapp.models import *
from dashboard.models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import auth

import datetime


def dashboard(request):
    return render(request,'spadashboard/home.html')


def attendancelist(request):  
    data = {
        'attendance':Attendence.objects.all(),
        'staffs':AccountMaster.objects.filter(group_master__name='staff'),
    }
    return render(request,'spadashboard/attendancelist.html', data)


def in_attendace(request):

    today = datetime.date.today()
    staff_obj = AccountMaster.objects.get(id=request.POST.get('account_master'))
    exist_staff_today = Attendence.objects.filter(date__day=today.day, date__month=today.month, date__year=today.year)

    if not len(exist_staff_today) > 0:
        if request.method == 'POST':
            attendace = Attendence.objects.create(time_in=request.POST.get('time_in'), account_master=staff_obj)
            attendace.save()
            messages.success(request, 'Check-in success @' + attendace.time_in)
            return redirect('attendancelist')
    else:
        messages.error(request, 'Today"s check-in found for this staff...')
    return redirect('attendancelist')


def out_attendace(request):

    today = datetime.date.today()
    staff_obj = AccountMaster.objects.get(id=request.POST.get('account_master'))
    attendace_obj_today = Attendence.objects.filter(account_master=staff_obj, date__day=today.day, date__month=today.month, date__year=today.year)
    
    if request.method == 'POST':
        if len(attendace_obj_today) > 0:
            attendace_obj = attendace_obj_today.first()
            if not attendace_obj.time_out:
                attendace_obj.time_out = request.POST.get('time_out')
                attendace_obj.save()
                messages.success(request, 'Check-out success @' + attendace_obj.time_out)
                return redirect('attendancelist')
            else:
                messages.info(request, 'Today"s check-out found for this staff...')            
        else:
            messages.info(request, 'Today"s check-in not found for this staff...')            
    return redirect('attendancelist')


def citylist(request):

    if request.method == 'POST':
        city = Citys.objects.create(name=request.POST['name'])
        city.save()
        return redirect('citylist')

    data = {
        'cities':Citys.objects.all(),
    }
    return render(request,'spadashboard/citylist.html', data)


def city_edit(request, id):
    city = Citys.objects.get(id=id)
    city.name = request.POST['name']
    city.save()
    return redirect('citylist')


def city_delete(request, id):
    city_obj = Citys.objects.get(id=id)
    city_obj.delete()
    return redirect('citylist')


@login_required(login_url='/beautyapp/login/')
def clientlist(request):

    if request.method == 'POST':

        service_obj = Services.objects.get(id=request.POST['service'])
        duration_obj = Addduration.objects.get(id=request.POST.get('duration'))
        pay_mode_obj = Paymentmod.objects.get(id=request.POST['paym'])
        client_member = AccountMaster.objects.get(id=request.POST['client_member'], group_master__name='client')
        therapist = AccountMaster.objects.get(id=request.POST['therapist'], group_master__name='staff')

        date = request.POST.get('date')
        in_time = request.POST.get('timein')
        out_time = request.POST.get('timeout')
        price = request.POST.get('price')

        new_guest = Guest.objects.create(date=date, time_in=in_time, time_out=out_time, price=price, services=service_obj, duration=duration_obj, payment=pay_mode_obj, client_member=client_member, therapist=therapist)
        
        new_guest.save()
        return redirect('clientlist')

        # repeated_client = Guest.objects.filter(mobile=mobile)
        # if repeated_client:

        #     old_guest = Guest.objects.create(date=date, gname=name, mobile='Repeat', city=city_obj, services=service_obj, treatment_by=staff_obj, duration=duration_obj,time_in=in_time, time_out=out_time, price=price, payment=pay_mode_obj, user_existence='Old', account_master=account_master)
        #     old_guest.save()

        #     data_1 = {'repeated':'repeated', 'rep_guests':repeated_client}
        #     return render(request,'spadashboard/clientlist.html', data_1)
        # else:

    # if request.user.is_superuser:
    # staff_members = Addstaff.objects.all()
    # else:
    #     staff_members = Addstaff.objects.filter(city=request.user.city)

    # if request.user.is_superuser:
    # guests = Guest.objects.all()
    # else:
        # guests = Guest.objects.filter(city=request.user.city)

    data = {
        'payment_modes':Paymentmod.objects.all(),
        'durations':Addduration.objects.all(),
        'services':Services.objects.all(),
        'duration':Addduration.objects.all(),
        "paym": Paymentmod.objects.all(),
        'clients':AccountMaster.objects.filter(group_master__name='client'),
        'staffs':AccountMaster.objects.filter(group_master__name='staff'),
        'guests':Guest.objects.all(),
    }
    return render(request,'spadashboard/clientlist.html', data)


def client_edit(request, id):
    
    client_obj  = Guest.objects.get(id=id)
    client_obj.comments = request.POST.get('cmt')
    client_obj.save()
    return redirect('clientlist')


def client_delete(request, id):
    client_obj = Guest.objects.get(id=id)
    client_obj.delete()
    return redirect('clientlist')
    

def expense_list(request):

    if request.method == 'POST':
        group_master = GroupMaster.objects.get(id=request.POST['group_master'])

        expense_obj = Expenses(date=request.POST['date'], particular=request.POST['particular'], bill_no=request.POST['bill_no'], amount=request.POST['amount'], reciept=request.FILES.get('rc'), group_master=group_master)

        expense_obj.save()
        return redirect('expense_list')

    data = {
        'expenses':Expenses.objects.all(),
        'city': GroupMaster.objects.filter(name='expense')
    }
    return render(request,'spadashboard/expensedetails.html', data)


def expense_edit(request, id):

    eexpense_obj = Expenses.objects.get(id=id)
    eexpense_obj.date = request.POST['date']
    eexpense_obj.particular = request.POST['particular']
    eexpense_obj.bill_no = request.POST['bill_no']
    eexpense_obj.amount = request.POST['amount']
    # eexpense_obj.group_master = request.POST['amount']
    eexpense_obj.save()
    return redirect('expense_list')


def delete_expense(request, id):
    expense_obj = Expenses.objects.get(id=id)
    expense_obj.delete()
    return redirect('expense_list')


def franchiseelist(request):

    if request.method == 'POST':
        franchise = Franchisee.objects.create(name=request.POST['name'], email=request.POST['email'], mobileno=request.POST['mobileno'], location=request.POST['location'], subject=request.POST['subject'])
        franchise.save()
        return redirect('franchiseelist')

    data = {
        'franchises':Franchisee.objects.all()
    }        
    return render(request,'spadashboard/franchiseelist.html', data)


def franchise_delete(request, id):
    franchise_obj = Franchisee.objects.get(id=id)
    franchise_obj.delete()
    return redirect('franchiseelist')


def managerlist(request):
    
    if request.method == 'POST':
        email = request.POST['email']
        group_master = GroupMaster.objects.get(id=request.POST['group_master'])
        username=request.POST['username']

        if User.objects.filter(username=username).exists():
            messages.info(request,'username taken')
            return redirect('managerlist')
        elif User.objects.filter(email=email).exists():
            messages.info(request,'mobile number is taken')
            return redirect('managerlist')
        else:
            user=User.objects.create_user(username=username, email=email, password=request.POST['password'], group_master=group_master, is_staff=True)
            user.save()
            return redirect('managerlist')

    data = {
        'managers':User.objects.filter(is_superuser=False),
        'city':GroupMaster.objects.filter(name='manager'),
    }                
    return render(request,'spadashboard/managerlist.html', data)


def manager_edit(request, id):

    manager_obj = User.objects.get(id=id)
    group_member = GroupMaster.objects.get(id=request.POST.get('group_member'))

    # manager_obj.first_name = request.POST['name']
    manager_obj.email = request.POST['email']

    manager_obj.group_member = group_member
    manager_obj.username = request.POST['username']
    manager_obj.set_password(str(request.POST['password']))
    manager_obj.save()
    return redirect('managerlist')    


def manager_delete(request, id):
    manager = User.objects.get(id=id, group_master__name='manager')
    manager.delete()
    return redirect('managerlist')


def servicelist(request):

    if request.method == 'POST':
        name = request.POST['name']
        service = Services(name=name)
        service.save()
        return redirect('servicelist')

    data = {
        'service':Services.objects.all()
    }
    return render(request,'spadashboard/servicelist.html', data)


def service_edit(request, id):

    service = Services.objects.get(id=id)
    service.name = request.POST['name']
    service.save()
    return redirect('servicelist')


def service_delete(request, id):
    service = Services.objects.get(id=id)
    service.delete()
    return redirect('servicelist') 


@login_required(login_url='/beautyapp/login/')
def stafflist(request):

    if request.method == 'POST':

        city = Citys.objects.get(id=request.POST['city'])
        staff=Addstaff(name=request.POST['name'], mobileno=request.POST['mobileno'], city=city)
        staff.save()
        return redirect('stafflist')

    if request.user.is_superuser:
        staff = Addstaff.objects.all()
    else:
        staff = Addstaff.objects.filter(city=request.user.city)  

    data = {
        'staff':Addstaff.objects.all(),
        'city':Citys.objects.all(),
    }
    return render(request,'spadashboard/stafflist.html', data)


def staff_edit(request, id):

    staff = Addstaff.objects.get(id=id)
    staff.name = request.POST['name']
    staff.mobileno = request.POST['mobileno']
    city_obj = Citys.objects.get(id=request.POST['city'])
    staff.city = city_obj
    staff.save()
    return redirect('stafflist')


def staff_delete(request, id):
    
    staff = Addstaff.objects.get(id=id)
    staff.delete()
    return redirect("stafflist")


def useractivity(request):
    return render(request,'spadashboard/useractivity.html')


def careers(request):
    data = {
        'careers':Carriers.objects.all()
    }
    return render(request,'spadashboard/carriers.html', data)


def careere_delete(request, id):
    career_obj = Carriers.objects.get(id=id)
    career_obj.delete()
    return redirect('careers')


# @login_required(login_url='/beautyapp/login/')
# def durationlist(request):
#     if request.method == 'POST':
#         name= request.POST['name']
#         dn = Addduration(duration=name)
#         dn.save()
#         return redirect(adduration)
#     # else:
#     context_data = {
#         'dn': Addduration.objects.all()
#     }


def gift(request):
    data = {
        'gifts':Gift.objects.all()
    }
    return render(request,'spadashboard/gift.html', data)


def gift_delete(request, id):
    g=Gift.objects.get(id=id)
    g.delete()
    return redirect('gift')    


def duration(request):

    if request.method == 'POST':
        new_duration = Addduration.objects.create(duration = request.POST.get('duration'))
        new_duration.save()
        return redirect('duration')

    data = {
        'durations':Addduration.objects.all()
    }
    return render(request,'spadashboard/add_duration.html', data)


def duration_delete(request, id):

    duration_obj = Addduration.objects.get(id=id)
    duration_obj.delete()
    return redirect('duration')


def payment_mode(request):

    if request.method == 'POST':

        group_master = GroupMaster.objects.get(id=request.POST.get('group_master'))
        new_payment_mode = Paymentmod.objects.create(name=request.POST.get('name'), group_master=group_master)
        new_payment_mode.save()
        return redirect('payment_mode')

    data = {
        'payment_modes':Paymentmod.objects.all(),
        'group_master':GroupMaster.objects.all(),
    }
    return render(request,'spadashboard/payment_mode.html', data)


def payment_mode_delete(request, id):

    payment_mode_obj = Paymentmod.objects.get(id=id)
    payment_mode_obj.delete()
    return redirect('payment_mode')

    
def appointment(request):
    return render(request,'spadashboard/appointment.html')


def daily_report(request):
    data = {
        'guests':Guest.objects.filter(client_member__name='client')
    }
    return render(request,'spadashboard/daily_report.html', data)


def branch_master(request):

    if request.method == 'POST':
        new_branch_master = BranchMaster.objects.create(name=request.POST.get('name'))
        new_branch_master.code = '10000-'+str(new_branch_master.id)
        new_branch_master.save()
        return redirect('branch_master')

    data = {
        'branch_master':BranchMaster.objects.all()
    }
    return render(request,'spadashboard/branch_master.html', data)


def branch_master_edit(request, id):
    
    branch_master_obj = BranchMaster.objects.get(id=id)
    branch_master_obj.name = request.POST.get('name')
    branch_master_obj.save()
    return redirect('branch_master')


def branch_master_delete(request, id):

    branch_master_obj = BranchMaster.objects.get(id=id)
    branch_master_obj.delete()
    return redirect('branch_master')


def group_master(request):

    if request.method == 'POST':
        city = Citys.objects.get(id=request.POST.get('city'))

        new_group_master = GroupMaster.objects.create(name=request.POST.get('name'), city=city)
        new_group_master.code = '20000-'+str(new_group_master.id)
        new_group_master.save()
            
        return redirect('group_master')

    data = {
        'city':Citys.objects.all(),
        'group_master':GroupMaster.objects.all()
    }
    return render(request,'spadashboard/group_master.html', data)


def group_master_edit(request, id):

    group_master_obj = GroupMaster.objects.get(id=id)
    city_obj = Citys.objects.get(id=request.POST.get('city'))

    group_master_obj.name = request.POST.get('name')
    group_master_obj.city = city_obj
    group_master_obj.save()
    return redirect('group_master')


def group_master_delete(request, id):

    group_master_obj = GroupMaster.objects.get(id=id)
    group_master_obj.delete()
    return redirect('group_master')    



def account_master(request):
    if request.method == 'POST':

        name = request.POST.get('name')
        mobile_number = request.POST.get('mobile_number')
        address_1 = request.POST.get('address_1')
        address_2 = request.POST.get('address_2')
        address_3 = request.POST.get('address_3')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')

        branch_master_obj = BranchMaster.objects.get(id=request.POST.get('branch_master'))
        group_master_obj = GroupMaster.objects.get(id=request.POST.get('group_master'))

        if AccountMaster.objects.filter(mobile_number=mobile_number, group_master__name='client').exists():
            new_account_master = AccountMaster.objects.create(name=name, address_1=address_1, address_2=address_2, address_3=address_3, state=state, pincode=pincode, mobile_number='Repeat', branch_master=branch_master_obj, group_master=group_master_obj, user_existence='old')
        else:
            new_account_master = AccountMaster.objects.create(name=name, address_1=address_1, address_2=address_2, address_3=address_3, state=state, pincode=pincode, mobile_number=mobile_number, branch_master=branch_master_obj, group_master=group_master_obj, user_existence='New')

        new_account_master.code = '30000-'+str(new_account_master.id)
        new_account_master.save()
        return redirect('account_master')

    data = {
        'branch_master':BranchMaster.objects.all(),
        'group_master':GroupMaster.objects.all(),
        'cities':Citys.objects.all(),
        'account_master':AccountMaster.objects.all(),
    }
    return render(request,'spadashboard/account_master.html', data)


def account_master_edit(request, id):   

    account_master_obj = AccountMaster.objects.get(id=id)
    branch_master_obj = BranchMaster.objects.get(id=request.POST.get('branch_master'))
    group_master_obj = GroupMaster.objects.get(id=request.POST.get('group_master'))

    account_master_obj.name = request.POST.get('name')
    account_master_obj.address_1 = request.POST.get('address_1')
    account_master_obj.address_2 = request.POST.get('address_2')
    account_master_obj.address_3 = request.POST.get('address_3')
    account_master_obj.state = request.POST.get('state')
    account_master_obj.pincode = request.POST.get('pincode')
    account_master_obj.mobile_number = request.POST.get('mobile_number')
    account_master_obj.branch_master = branch_master_obj
    account_master_obj.group_master = group_master_obj
    account_master_obj.save()
    return redirect('account_master')


def account_master_delete(request, id):

    account_master_obj = AccountMaster.objects.get(id=id)
    account_master_obj.delete()
    return redirect('account_master')
    

def item_master(request):
    return render(request,'spadashboard/item_master.html')
def add_commission(request):
    return render(request,'spadashboard/add_commission.html')
def membership_plan(request):
    return render(request,'spadashboard/membership_plan.html')
def membership_list(request):
    return render(request,'spadashboard/membership_list.html')
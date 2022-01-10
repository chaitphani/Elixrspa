from django.shortcuts import render, redirect
from beautyapp.models import *
from dashboard.models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def home(request):
    return render(request,'spadashboard/home.html')

def attendancelist(request):
    return render(request,'spadashboard/attendancelist.html')


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


@login_required(login_url='/beautyapp/login/')
def clientlist(request):

    if request.method == 'POST':
        service_obj = Services.objects.get(pk=request.POST['service'])
        staff_obj = Addstaff.objects.get(pk=request.POST['serviceby'])
        pay_mode_obj = Paymentmod.objects.get(pk=request.POST['paym'])
        duration_obj = Addduration.objects.get(duration=request.POST.get('duration'))
        city_obj = Citys.objects.get(id=request.POST['city'])

        new_guest = Guest.objects.create(date=request.POST.get('date'), gname=request.POST.get('name'), mobile=request.POST.get('mobileno'), city=city_obj, services=service_obj, treatment_by=staff_obj, duration=duration_obj,time_in=request.POST.get('timein'), time_out=request.POST.get('timeout'), price=request.POST.get('price'), payment=pay_mode_obj)
        new_guest.save()
        
        repeated_client = Guest.objects.filter(mobile=request.POST.get('mobileno'))
        if repeated_client:
            data_1 = {'repeated':'repeated', 'rep_guests':repeated_client}
            return render(request,'spadashboard/clientlist.html', data_1)
        # else:
        return redirect('clientlist')

    # if request.user.is_superuser:
    # staff_members = Addstaff.objects.all()
    # else:
    #     staff_members = Addstaff.objects.filter(city=request.user.city)

    # if request.user.is_superuser:
    # guests = Guest.objects.all()
    # else:
        # guests = Guest.objects.filter(city=request.user.city)

    data = {
        'cities':Citys.objects.all(),
        'payment_modes':Paymentmod.objects.all(),
        'durations':Addduration.objects.all(),
        'services':Services.objects.all(),
        'staffs':Addstaff.objects.all(),
        'duration':Addduration.objects.all(),
        "paym": Paymentmod.objects.all(),
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
        city = Citys.objects.get(id=request.POST['city'])
        expense_obj = Expenses(date=request.POST['date'], particular=request.POST['particular'], bill_no=request.POST['bill_no'], amount=request.POST['amount'], reciept=request.FILES.get('rc'), city=city)
        expense_obj.save()
        return redirect('expense_list')

    data = {
        'expenses':Expenses.objects.all(),
        'city': Citys.objects.all()
    }
    return render(request,'spadashboard/expensedetails.html', data)


def expense_edit(request, id):

    eexpense_obj = Expenses.objects.get(id=id)
    eexpense_obj.date = request.POST['date']
    eexpense_obj.particular = request.POST['particular']
    eexpense_obj.bill_no = request.POST['bill_no']
    eexpense_obj.amount = request.POST['amount']
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
        city = Citys.objects.get(id=request.POST['city'])
        username=request.POST['username']

        if User.objects.filter(username=username).exists():
            messages.info(request,'username taken')
            return redirect('managerlist')
        elif User.objects.filter(email=email).exists():
            messages.info(request,'mobile number is taken')
            return redirect('managerlist')
        else:
            user=User.objects.create_user(username=username, email=email, password=request.POST['password'], city=city, is_staff=True)
            user.save()
            return redirect('managerlist')

    data = {
        'managers':User.objects.filter(is_superuser=False),
        'city':Citys.objects.all(),
    }                
    return render(request,'spadashboard/managerlist.html', data)


def manager_edit(request, id):

    manager_obj = User.objects.get(id=id)
    city=Citys.objects.get(id=request.POST.get('city'))

    # manager_obj.first_name = request.POST['name']
    manager_obj.email = request.POST['email']

    manager_obj.city = city
    manager_obj.username = request.POST['username']
    manager_obj.set_password(str(request.POST['password']))
    manager_obj.save()
    return redirect('managerlist')    


def manager_delete(request, id):
    manager = User.objects.get(id=id)
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


def useractivity(request):
    return render(request,'spadashboard/useractivity.html')


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
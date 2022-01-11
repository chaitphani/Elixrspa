from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import auth
from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import *
from .msg91 import msg91
from beautyapp.models import *

import datetime


def admin_login(request):

    if request.method=='POST':
        register=auth.authenticate(username=request.POST['username'],password=request.POST['password'])
        if register is not None:
            auth.login(request,register)
            return redirect(dashboard)
        else:
            messages.info(request,'invalid credentials')
            return redirect(admin_login)
    else:
        return render(request,'dashboard/admin_login.html')



@login_required(login_url='admin_login')
def dashboard(request):

    if request.method == 'POST':
        to_date = request.POST['to_date']
        f_date = request.POST['from_date']

        if request.user.is_superuser:
            guests = Guest.objects.filter(date__range=(to_date,f_date))
        else:
            city = request.user.city
            guests = Guest.objects.filter(city=city,date__range=(to_date,f_date))

    else:
        # if request.user.is_superuser:
        guests = Guest.objects.all()
        # else:
        #     city = request.user.city
        #     guests = Guest.objects.filter(city=city)
    return render(request,'dashboard/guest_list.html', {'guests':guests})


def guest(request):

    if request.method == 'POST':
        date = request.POST['date']
        name = request.POST['name']
        mobileno = request.POST['mobileno']
        timein = request.POST['timein']
        timeout = request.POST['timeout']
        price = request.POST['price']

        rep_guest = Guest.objects.filter(mobile=mobileno)
        if rep_guest:
            return render(request,'dashboard/guest.html', {'repeated':"repeated",'rep_guests':rep_guest } )

        s = Services.objects.get(pk=request.POST['service'])
        a = Addstaff.objects.get(pk=request.POST['serviceby'])
        p = Paymentmod.objects.get(pk=request.POST['paym'])
        d = Addduration.objects.get(duration=request.POST.get('duration'))
        city = Citys.objects.get(id=request.POST['city'])

        new_guest = Guest.objects.create(date=date, gname=name, mobile=mobileno, city=city, services=s, treatment_by=a, duration=d,time_in=timein, time_out=timeout, price=price, payment=p)

        new_guest.save()
        return redirect('guest')
    
    services = Services.objects.all()
    # if request.user.is_superuser:
    staffs = Addstaff.objects.all()
    # else:
    #     staff_city = request.user.city
    #     staffs = Addstaff.objects.filter(city=staff_city)

    city = Citys.objects.all()
    paym = Paymentmod.objects.all()
    duration = Addduration.objects.all()
    user_city = request.user.city

    return render(request,'dashboard/guest.html',{'services':services,'staffs':staffs,'city':city,'paym':paym,'duration':duration,'user_city':user_city})


# def guest_list(request):
#     guests = Guest.objects.all()
#     return render(request,'dashboard/guest_list.html',{'guests':guests})


def gdel(request,id):

    dc=Guest.objects.get(id=id)
    dc.delete()
    return redirect('clientlist')

def carriers(request):
    careers=Carriers.objects.all()
    return render(request,'dashboard/carriers.html', {'careers':careers})


def gifts(request):
    gifts = Gift.objects.all()
    return render(request,'dashboard/gifts.html',{'gifts':gifts})


def appointment(request):

    if request.user.is_superuser:
        appointment = Appointment.objects.all()
    else:
        city = request.user.city
        if city is None:
            return redirect(dashboard)
        appointment = Appointment.objects.filter(city=city).order_by('-date')

    paginator = Paginator(appointment, 5)  # 10 appointments in each page
    page = request.GET.get('page')
    try:
        appointment_list = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer deliver the first page
        appointment_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        appointment_list = paginator.page(paginator.num_pages)
    return render(request,'dashboard/appointment.html',{'appointment':appointment_list,'page': page} )


# def edit(request, id):
#     city = Citys.objects.get(id=id)
#     context = {'city': city}
#     return render(request, 'crud/edit.html', context)


def confirm_appointment(request,id):

    appointment = Appointment.objects.get(id=id)
    if request.method == 'POST':
        comments = request.POST['comments']
        mobileno = appointment.mobileno
        print(msg91(mobileno,comments))
        appointment.status = "MSG Sent"
        appointment.save()
    return redirect("adminappointment")


def update(request, id):

    city = Citys.objects.get(id=id)
    city.name = request.POST['name']
    city.save()
    return redirect('citylist')


def clientupdate(request, id):

    if request.method == 'POST':
        
        g  = Guest.objects.get(id=id)
        g.time_in = request.POST['time_in']
        g.time_out= request.POST['time_out']
        g.duration=request.POST['duration']
        g.total_time = request.POST['total_time']
        g.comments = request.POST['comments']
        g.save()
        return redirect(dashboard)
    return redirect(dashboard)


def update_guest(request, id):

    if request.method == 'POST':
        g  = Guest.objects.get(id=id)
        g.comments = request.POST.get('cmt')
        g.save()
        return redirect(dashboard)


def modify(request, id):
    
    service = Services.objects.get(id=id)
    service.name = request.POST['name']
    service.save()
    return redirect('servicelist')


def deletes(request,id):
    service = Services.objects.get(id=id)
    service.delete()
    return redirect('servicelist')


def jobdelete(request,id):
    ca=Carriers.objects.get(id=id)
    ca.delete()
    return redirect(carriers)


def deletgift(request,id):
    g=Gift.objects.get(id=id)
    g.delete()
    return redirect(gifts)


def deleted(request,id):
    appointments=Appointment.objects.get(id=id)
    appointments.delete()
    return redirect(appointment)


def delete(request,id):
    city = Citys.objects.get(id=id)
    city.delete()
    return redirect( addcity)


def addservice(request):

    if request.method == 'POST':
        name = request.POST['name']
        service = Services(name=name)
        service.save()
        return redirect('servicelist')
    else:
        context_data = {
            'service':Services.objects.all()
        }
    return render(request,'dashboard/addservices.html',context_data)


# def price(request):
#     if request.method == 'POST':
#         price = request.POST['price']
#         p = Price(price=price)
#         p.save()
#         return redirect(price)
#     else:
#         context_data = {
#         'p':Addprice.objects.all()
#         }
#     return render(request,'dashboard/price.html',context_data)


def addstaff(request):

    if request.method == 'POST':
        name = request.POST['name']
        mobileno = request.POST['mobileno']
        city = request.POST['city']

        city = Citys.objects.get(id=city)
        staff=Addstaff(name=name,mobileno=mobileno,city=city)
        staff.save()
        return redirect('stafflist')
        
    if request.user.is_superuser:
        staff = Addstaff.objects.all()
    else:
        staff_city = request.user.city
        staff = Addstaff.objects.filter(city=staff_city)

    context_data = {
        'staff':staff,
        'city':Citys.objects.all()
    }
    return render(request,'dashboard/addstaff.html', context_data)


def delete_staff(request,id):
    staff = Addstaff.objects.get(id=id)
    staff.delete()
    return redirect("stafflist")


def update_staff(request, id):

    staff = Addstaff.objects.get(id=id)
    staff.name = request.POST['name']
    staff.mobileno = request.POST['mobileno']
    city_obj = Citys.objects.get(id=request.POST['city'])
    staff.city = city_obj
    staff.save()
    return redirect('stafflist')


def addcity(request):

    if request.method == 'POST':
        name = request.POST['name']
        city = Citys(name=name)
        city.save()
        return redirect('citylist')
    else:
        context_data = {
          'city':Citys.objects.all()
        }
    return render(request,'dashboard/addcity.html',context_data)


def addprice(request):

    if request.method == 'POST':
        name = request.POST['name']
        price =Addprice(name=name)
        price.save()
        return redirect(addprice)
    else:
        context_data = {
          'price':Addprice.objects.all()
        }
    return render(request,'dashboard/addcity.html',context_data)


def admin_login(request):
    
    if request.method=='POST':
        register=auth.authenticate(username=request.POST['username'],password=request.POST['password'])
    
        if register is not None:
            auth.login(request,register)
            return redirect('dashboard')
        else:
            messages.info(request,'invalid credentials')
            return redirect('admin_login')
    else:
        return render(request,'dashboard/admin_login.html')


def franch(request):
    f=Franchisee.objects.all()
    return render(request,'dashboard/franch.html', {'f': f})


def deletefranch(request, id):
    f = Franchisee.objects.get(id=id)
    f.delete()
    return redirect(franch)


def report(request):
    guests = Guest.objects.all()
    return render(request,'dashboard/report.html', {'guests': guests})


def admin_logout(request):
    auth.logout(request)
    return redirect('home')


def addmanager(request):

    if request.method == 'POST':
        name = request.POST['name']
        mobileno = request.POST['mobileno']
        city=request.POST['city']
        city = Citys.objects.get(id=city)
        username=request.POST['username']
        password=request.POST['password']

        if User.objects.filter(username=username).exists():
                messages.info(request,'username taken')
                return redirect(addmanager)
        elif User.objects.filter(email=mobileno).exists():
                messages.info(request,'mobile number is taken')
                return redirect(addmanager)
        else:
                user=User.objects.create_user(first_name=name,username=username,email=mobileno,password=password,city=city)
                user.is_staff = True
                user.save()
                return redirect(addmanager)
    else:
        manager = User.objects.filter(is_superuser=False)
        context_data = {
            'manager':manager,
            'city':Citys.objects.all()
        }
    return render(request,'dashboard/addmanager.html',context_data)


def update_manager(request, id):

    if request.method == 'POST':
        m = User.objects.get(id=id)
        m.first_name = request.POST['name']
        m.email = request.POST['mobileno']
        c=request.POST.get('city')
        city=Citys.objects.get(id=c)
        city.save()

        m.city = city
        m.username = request.POST['username']
        m.set_password(str(request.POST['password']))
        m.save()
        return redirect(addmanager)
    return redirect(addmanager)


def delete_manager(request,id):
    manager = User.objects.get(id=id)
    manager.delete()
    return redirect(addmanager)


def attendence(request):
    atten = Attendence.objects.all()
    return render(request,'dashboard/attendence.html',{'atten':atten})


def timein(request):

    if request.method == 'POST':
        name = request.POST['name']
        time_in=request.POST['timein']
        remarks = request.POST['remarks']
        a = Addstaff.objects.get(pk=name)
        # if Attendence.objects.filter(name=a,date__startswith = datetime.datetime.today().strftime('%Y-%m-%d')).exists():
        #     messages.info(request,a.name+' already entered attendance for the day.')
        #     return redirect(timein)
        c = 0
        for i in Attendence.objects.filter(name=a,date__startswith = datetime.datetime.today().strftime('%Y-%m-%d')):
            c = c+1

        if c >= 1:
            messages.info(request,a.name+' already entered attendance for the day.')
            return redirect(timein)
        else:
            if time_in in " ":
                at = Attendence(name=a,remarks=remarks)
            else:
                at = Attendence(name=a,time_in=time_in,remarks=remarks)
            at.save()
            return redirect(attendence)
    else:
        staf=Addstaff.objects.all()
    return render(request,'dashboard/timein.html',{'staf':staf})


def timeout(request):

    if request.method == 'POST':
        name = request.POST['name']
        time_out = request.POST['timeout']
        b = Addstaff.objects.get(id=name)
        a = get_object_or_404( Attendence,Q(name=b) & Q(date__startswith = datetime.datetime.today().strftime('%Y-%m-%d') ))
        # a = Attendence.objects.get( name=b)
        a.time_out = time_out
        a.save()
        return redirect(timeout)
    else:
        staff = Addstaff.objects.all()
    return render(request,'dashboard/timeout.html',{'staff':staff})


def delete_atten(request,id):
    t = Attendence.objects.get(id=id)
    t.delete()
    return redirect(attendence)


def expenses(request):

    if request.method == 'POST':
        date = request.POST['date']
        particular = request.POST['particular']
        bill_no = request.POST['bill_no']
        amount = request.POST['amount']
        reciept = request.FILES.get('rc')
        city = request.POST['city']
        city = Citys.objects.get(id=city)
        ex = Expenses(date=date,particular=particular,bill_no=bill_no,amount=amount,reciept=reciept,city=city)
        ex.save()
        return redirect(expenses)
    else:
        city = Citys.objects.all()
    return render(request,'dashboard/expenses.html',{'city':city})


def update_expense(request, id):

    if request.method == 'POST':
        e = Expenses.objects.get(id=id)
        e.date = request.POST['date']
        e.particular = request.POST['particular']
        e.bill_no = request.POST['bill_no']
        e.amount = request.POST['amount']
        e.save()
        return redirect(expenses)
    return redirect(expenses)


def delete_expense(request,id):
    exp = Expenses.objects.get(id=id)
    exp.delete()
    return redirect(exdetail)


def exdetail(request):

    if request.method == 'POST':
        to_date = request.POST.get('to_date')
        f_date = request.POST.get('from_date')

        if request.user.is_superuser:
            ex = Expenses.objects.filter(date__range=(to_date,f_date))
        else:
            city = request.user.city
            ex = Expenses.objects.filter(city=city,date__range=(to_date,f_date))
    else:
        if request.user.is_superuser:
            ex = Expenses.objects.all()
        else:
            city = request.user.city
            ex = Expenses.objects.filter(city=city)
    return render(request,'dashboard/expensedetails.html', {'ex':ex})


def paymentmod(request):

    if request.method == 'POST':
        name = request.POST['name']
        pay = Paymentmod(name=name)
        pay.save()
        return redirect(paymentmod)
    else:
        context_data = {
          'pay': Paymentmod.objects.all()
        }
    return render(request,'dashboard/paymentmod.html',context_data)


def paymentmod(request):

    if request.method == 'POST':
        name = request.POST['name']
        pay = Paymentmod(name=name)
        pay.save()
        return redirect(paymentmod)
    else:
        context_data = {
          'pay': Paymentmod.objects.all()
        }
    return render(request,'dashboard/paymentmod.html',context_data)


def paymentmodchange(request, id):
    p = Paymentmod.objects.get(id=id)
    p.name = request.POST['name']
    p.save()
    return redirect(paymentmod)


def deletepaymentmod(request,id):
    p = Paymentmod.objects.get(id=id)
    p.delete()
    return redirect(paymentmod)


def adduration(request):

    if request.method == 'POST':
        name= request.POST['name']
        dn = Addduration(duration=name)
        dn.save()
        return redirect(adduration)
    else:
        context_data = {
          'dn': Addduration.objects.all()
        }
    return render(request,'dashboard/adduration.html',context_data)


def durationchange(request, id):
    a = Addduration.objects.get(id=id)
    a.name = request.POST['name']
    a.save()
    return redirect(adduration)


def deleteduration(request,id):
    a = Addduration.objects.get(id=id)
    a.delete()
    return redirect(adduration)


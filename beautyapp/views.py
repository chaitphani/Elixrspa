from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# from django.core.mail import EmailMessage
# from django.conf import settings

from .models import *
from dashboard.models import *


def table(request):

    data = { 'FOOT REFLEXOLOGY':[0,'30/60','599/999',[]], 'FULL LEG MASSAGE':[0,'30/60','599/999',[]] , 'HEAD SHOULDER & NECK':[0,'30/60','599/999',[]], 'FULL BODY MASSAGE': [1,'60/90','',[ ['AROMA THERAPY','1200 / 1900'],['SWEDISH MASSAGE','1500 / 2200'],\
        ['BALINESE MASSAGE','1500 / 2200'],['DEEP TISSUE MASSAGE','1800 / 2500'],['AYURVEDIC BODY MASSAGE','1500 / 2200'],['POTLI MASSAGE','2000 / 2700'],['ABHAYANGAM MASSAGE','1800 / 2500'],['LOMI LOMI MASSAGE','1800 / 2500'],['THAI MASSAGE','1800 / 2500'],['COUPLE MASSAGE','2600 / 3600'],]],\
        'BLEACHING':[1,'-','',[ ['FACE & NECK','350'],['D TAN','450'] ]], 'WAXING (ONLY FOR LADIES)':[1,'-','',[['FULL ARMS','300'], ]] \
        }

    context = {'data':data}
    return render(request,'table.html',context)


def home(request):
    return render(request,'beautyapp/hom1.html')

def memberplan(request):
    return render(request,'beautyapp/memberplan.html')

def eservice(request):
    service=Services.objects.all()
    return render(request,'beautyapp/eservice.html',{'service':service})

def about(request):
    return render(request,'beautyapp/about1.html')

def footrefl(request):
    return render(request,'beautyapp/footrefl.html')

def services(request):
    return render(request,'beautyapp/service.html')

def gallery(request):
    return render(request,'beautyapp/gallery1.html')

def espackage(request):
    return render(request,'beautyapp/espackage.html')

def mens(request):
    return render(request,'beautyapp/mens.html')

def contact(request):
    return render(request,'beautyapp/contact1.html')

def careers(request):

    if request.method == 'POST':

        name = request.POST['name']
        address = request.POST['address']
        email = request.POST['email']
        mobileno = request.POST['mobileno']
        totalexp = request.POST['totalexp']
        lastsalary = request.POST['lastsalary']
        fileupload = request.FILES['fileupload']
        profile_pic = request.FILES['pc']

        careers=Carriers.objects.create(name=name, address=address, email=email, mobileno=mobileno, totalexp=totalexp,lastsalary=lastsalary, fileupload=fileupload, profile_pic=profile_pic)
        careers.save()

        return redirect(home)
    return render(request,'beautyapp/careers.html')


@login_required(login_url='/beautyapp/login')
def appointment(request):

    if request.method == 'POST':
        # account_sid = 'AC9e59c0f3c67ba050e8de9220fabef012'
        # auth_token = '8296009e858fd9c21ba0c5462a95b2d0'
        # client = Client(account_sid, auth_token)
        # message = client.messages.create(
        #               from_='+14242383634',
        #               body ='hello sandy',
        #               to ="+918356016968",
        #                )
        service_obj = Services.objects.get(id=request.POST['services'])
        city_obj = Citys.objects.get(id=request.POST['city'])
        appointment=Appointment(name=request.POST['name'], mobileno=request.POST['mobileno'], email=request.POST['email'], city=city_obj,date=request.POST['pdate'], time=request.POST['ptime'], services=service_obj)

        appointment.save()
        return redirect(home)

    else:
        context_data = {
            'appointment':'appointment',
            'services':Services.objects.all(),
            'city':Citys.objects.all()
        }
        return render(request,'beautyapp/appointment.html', context_data)


def logout(request):
    auth.logout(request)
    return redirect('home')


@login_required(login_url='/beautyapp/login')
def buygift(request):

    if request.method == 'POST':
        gift=Gift(name=request.POST['name'], email=request.POST['email'], mobile=request.POST['mobile'], address=request.POST['address'],price=request.POST['price'], message=request.POST['message'])

        gift.save()
        return redirect('home')
    else:
        return render(request,'beautyapp/gift.html')


def login(request):

    if request.method=='POST':
        register = auth.authenticate(username=request.POST['username'],password=request.POST['password'])
        if register is not None:
            auth.login(request, register)
            return redirect('dashboard')
        else:
            messages.info(request,'invalid credentials')
            return redirect('login')
    else:
        return render(request,'beautyapp/login.html')


def register(request):

    if request.method == 'POST':

        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']

        if User.objects.filter(username=username).exists():
            messages.info(request,'username taken')
            return redirect('register')

        if Register.objects.filter(email=email).exists():
            messages.info(request,'email is taken')
            return redirect('register')

        if password1 == password2 :
            user=User.objects.create_user(first_name=request.POST['first_name'], last_name=request.POST['last_name'], username=username,password=password1, email=email)
            user.save()
            return redirect('login')
        else:
            messages.info(request,'password do not match')
            return redirect('register')
    return render(request,'beautyapp/register.html')


def franchisee(request):

    if request.method == 'POST':
        name=request.POST['name']
        email=request.POST['email']
        mobileno=request.POST['mobileno']
        location=request.POST['location']
        subject=request.POST['subject']
        french=Franchisee(name=name,email=email,mobileno=mobileno,location=location,subject=subject)
        french.save()
        return redirect(home)
    else:
        return render(request,'beautyapp/franchisee.html')


# def show_genres(request):
#     return render(request, "beautyapp/test.html", {'genres': Genre.objects.all()})

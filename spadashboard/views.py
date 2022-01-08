from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'spadashboard/home.html')
def attendancelist(request):
    return render(request,'spadashboard/attendancelist.html')
def citylist(request):
    return render(request,'spadashboard/citylist.html')
def clientlist(request):
    return render(request,'spadashboard/clientlist.html')
def expensedetails(request):
    return render(request,'spadashboard/expensedetails.html')
def franchiseelist(request):
    return render(request,'spadashboard/franchiseelist.html')
def managerlist(request):
    return render(request,'spadashboard/managerlist.html')
def servicelist(request):
    return render(request,'spadashboard/servicelist.html')
def stafflist(request):
    return render(request,'spadashboard/stafflist.html')
def useractivity(request):
    return render(request,'spadashboard/useractivity.html')
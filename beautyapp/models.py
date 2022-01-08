from django.db import models
from django.contrib.auth.models import AbstractUser


class Register(models.Model):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password1=models.CharField(max_length=100)
    password2=models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.firstame)


class Citys(models.Model):
    name=models.CharField(max_length=50,default="delhi")

    def __str__(self):
        return '{}'.format(self.name)


class User(AbstractUser):
    city = models.ForeignKey(Citys, on_delete=models.SET_NULL,null=True,blank=True)


class Services(models.Model):

    name=models.CharField(max_length=500,default="Services")
    # duration = models.ForeignKey(Addduration, on_delete=models.CASCADE,null=True)
    # price  = models.ForeignKey(Addprice, on_delete=CASCADE,null=True)

    def __str__(self):
        return '{}'.format(self.name)


class Gift(models.Model):

    name=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    mobile=models.IntegerField()
    address=models.CharField(max_length=200)
    message=models.CharField(max_length=500)
    price=models.IntegerField()

    def __str__(self):
        return '{}'.format(self.name)


class Appointment(models.Model):

    name=models.CharField(max_length=50)
    mobileno = models.IntegerField()
    email=models.CharField(max_length=50, default="null")
    date=models.DateField()
    time=models.TimeField()

    city = models.ForeignKey(Citys, on_delete=models.SET_NULL,null=True)
    services = models.ForeignKey(Services, on_delete=models.SET_NULL, null=True)

    status = models.CharField(max_length=250, null=True)

    def __str__(self):
        return '{}'.format(self.name)

class Carriers(models.Model):

    name=models.CharField(max_length=100)
    address=models.CharField(max_length=200)
    date=models.DateField()
    email=models.CharField(max_length=100)
    mobileno = models.IntegerField()
    totalexp=models.CharField(max_length=100)
    lastsalary=models.IntegerField()
    fileupload=models.FileField(upload_to='resume/pdfs/')
    profile_pic=models.ImageField(upload_to='Images/img/')

    def __str__(self):
        return '{}'.format(self.name)


class Franchisee(models.Model):

    name = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    mobileno = models.CharField(max_length=15)
    location=models.CharField(max_length=100)
    subject = models.CharField(max_length=500)

    def __str__(self):
        return '{}'.format(self.name)


# class Genre(MPTTModel):
#     name = models.CharField(max_length=50, unique=True)
#     parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

#     class MPTTMeta:
#         order_insertion_by = ['name']

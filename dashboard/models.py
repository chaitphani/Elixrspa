from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import related


class Addduration(models.Model):
    duration = models.CharField(max_length=250)
    def __str__(self):
        return '{}'.format(self.duration)

    class Meta: 
        verbose_name = "Duration"
        verbose_name_plural = "Duration"


class Paymentmod(models.Model):

    name = models.CharField(max_length=250)
    group_master = models.ForeignKey('GroupMaster', on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta: 
        verbose_name = "PaymentMode"
        verbose_name_plural = "PaymentModes"


class Attendence(models.Model):

    date = models.DateTimeField(auto_now_add=True)
    time_in = models.TimeField(null=True, blank=True)
    time_out = models.TimeField(null=True, blank=True)
    remarks = models.CharField(max_length=250, default="present")

    account_master = models.ForeignKey('AccountMaster', on_delete=models.CASCADE)
    
    def __str__(self):
        return '{}'.format(self.name)

    class Meta: 
        verbose_name = "Attendence"
        verbose_name_plural = "Attendence"


class Expenses(models.Model):

    date=models.DateTimeField(auto_now_add=True)
    particular = models.CharField(max_length=250)
    bill_no = models.CharField(max_length=400, default="none")
    amount = models.CharField(max_length=50)
    remarks = models.CharField(max_length=250)
    reciept=models.ImageField(upload_to='Images/expenses/', blank=True, null=True)

    group_master = models.ForeignKey('GroupMaster', on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.bill_no)

    class Meta: 
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"


class BranchMaster(models.Model):

    code = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.name)

    
class GroupMaster(models.Model):

    code = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=30)
    date = models.DateTimeField(auto_now_add=True)
    
    city = models.ForeignKey('Citys', on_delete=models.CASCADE)
    
    def __str__(self):
        return '{}'.format(self.name)


class AccountMaster(models.Model):

    code = models.CharField(max_length=10, null=True,blank=True)
    name = models.CharField(max_length=20)
    address_1 = models.CharField(max_length=120, null=True, blank=True)
    address_2 = models.CharField(max_length=120, null=True, blank=True)
    address_3 = models.CharField(max_length=120, null=True, blank=True)
    state = models.CharField(max_length=30, null=True, blank=True)
    pincode = models.CharField(max_length=6, null=True, blank=True)
    mobile_number = models.CharField(max_length=13)

    user_existence = models.BooleanField(default=False)  # old, new

    branch_master = models.ForeignKey(BranchMaster, on_delete=models.CASCADE)
    group_master = models.ForeignKey(GroupMaster, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.name)


class Guest(models.Model):

    date = models.DateTimeField()
    time_in = models.TimeField()
    time_out = models.TimeField()
    price = models.CharField(max_length=50)
    # out = models.BooleanField(default=True)

    services = models.ForeignKey('Services', on_delete=models.CASCADE)
    duration = models.ForeignKey(Addduration, on_delete=models.CASCADE)
    payment  =models.ForeignKey(Paymentmod, on_delete=models.CASCADE)
    client_member = models.ForeignKey(AccountMaster, on_delete=models.CASCADE, related_name='client_account_master')
    therapist = models.ForeignKey(AccountMaster, on_delete=models.CASCADE, related_name='staff_account_master')

    comments = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.account_master.name)


class Register(models.Model):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password1 = models.CharField(max_length=100)
    password2 = models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.firstame)

    class Meta: 
        verbose_name = "Attendance"
        verbose_name_plural = "Attendance"


class Citys(models.Model):
    name = models.CharField(max_length=50,default="delhi")

    def __str__(self):
        return '{}'.format(self.name)

    class Meta: 
        verbose_name = "City"
        verbose_name_plural = "Cities"


class Services(models.Model):

    name = models.CharField(max_length=500,default="Services")
    group_master = models.ForeignKey('GroupMaster', on_delete=models.CASCADE)

    # duration = models.ForeignKey(Addduration, on_delete=models.CASCADE,null=True)
    # price  = models.ForeignKey(Addprice, on_delete=CASCADE,null=True)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta: 
        verbose_name = "Service"
        verbose_name_plural = "Services"


class Gift(models.Model):

    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    mobile = models.CharField(max_length=13)
    address = models.CharField(max_length=200)
    message = models.TextField()
    price = models.FloatField()

    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '{}'.format(self.name)


class Appointment(models.Model):

    name = models.CharField(max_length=50)
    mobileno = models.IntegerField()
    email = models.CharField(max_length=50, default="null")
    date = models.DateField()
    time = models.TimeField()

    city = models.ForeignKey(Citys, on_delete=models.CASCADE)
    services = models.ForeignKey(Services, on_delete=models.CASCADE)

    status = models.CharField(max_length=250, null=True)

    def __str__(self):
        return '{}'.format(self.name)


class Carriers(models.Model):

    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(unique=True)
    mobileno = models.CharField(max_length=13)
    totalexp = models.FloatField()
    lastsalary = models.FloatField(null=True, blank=True)
    fileupload = models.FileField(upload_to='media/careers/resume')
    profile_pic = models.ImageField(upload_to='media/careers/profile_pics')

    def __str__(self):
        return '{}'.format(self.name)

    class Meta: 
        verbose_name = "Career"
        verbose_name_plural = "Career"


class Franchisee(models.Model):

    name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    mobileno = models.CharField(max_length=13)
    location = models.CharField(max_length=100)
    subject = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '{}'.format(self.name)

    class Meta: 
        verbose_name = "Franchise"
        verbose_name_plural = "Franchises"


class Item(models.Model):

    code = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=20)
    quantity = models.FloatField()
    description = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.name)


# class Genre(MPTTModel):
#     name = models.CharField(max_length=50, unique=True)
#     parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

#     class MPTTMeta:
#         order_insertion_by = ['name']


# class Addprice(models.Model):
#     price = models.FloatField()

#     def __str__(self):
#         return '{}'.format(self.price)

#     class Meta: 
#         verbose_name = "Price"
#         verbose_name_plural = "Prices"



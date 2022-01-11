from django.db import models
from beautyapp.models import Citys, Services


class Addstaff(models.Model):

    name = models.CharField(max_length=250)
    mobileno = models.CharField(max_length=12)
    city = models.ForeignKey(Citys, on_delete=models.SET_NULL, null=True)
    # services = models.ForeignKey(Services, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta: 
        verbose_name = "Staff"
        verbose_name_plural = "Staff"

class Addprice(models.Model):
    price = models.FloatField()

    def __str__(self):
        return '{}'.format(self.price)

    class Meta: 
        verbose_name = "Price"
        verbose_name_plural = "Prices"

class Addduration(models.Model):
    duration = models.CharField(max_length=250)

    def __str__(self):
        return '{}'.format(self.duration)

    class Meta: 
        verbose_name = "Duration"
        verbose_name_plural = "Duration"

class Paymentmod(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta: 
        verbose_name = "PaymentMode"
        verbose_name_plural = "PaymentModes"

class Guest(models.Model):

    # PAY_CHOICES = (("ONLINE","online"),("CASH","cash"))

    gname = models.CharField(max_length=50)
    mobile = models.CharField(max_length=100)
    time_in = models.TimeField()
    time_out = models.TimeField()
    price = models.CharField(max_length=50)
    out = models.BooleanField(default=True)
    date=models.DateTimeField(auto_now_add=True)

    city = models.ForeignKey(Citys, on_delete=models.SET_NULL,null=True)
    services = models.ForeignKey(Services, on_delete=models.SET_NULL, null=True)
    treatment_by = models.ForeignKey(Addstaff, on_delete=models.SET_NULL, null=True)
    duration = models.ForeignKey(Addduration, on_delete=models.SET_NULL,null=True)
    payment  =models.ForeignKey(Paymentmod, on_delete=models.SET_NULL, null=True)

    comments = models.CharField(max_length=500, default="NA", null=True, blank=True)
    # total_time = models.CharField(max_length=50)

    def __str__(self):
        return '{}'.format(self.gname)


class Attendence(models.Model):

    date = models.DateTimeField(auto_now_add=True)
    name = models.ForeignKey(Addstaff, on_delete=models.SET_NULL, null=True)
    time_in = models.TimeField(null=True, blank=True)
    time_out = models.TimeField(null=True, blank=True)
    remarks = models.CharField(max_length=250, default="present")

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
    city = models.ForeignKey(Citys, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return '{}'.format(self.bill_no)

    class Meta: 
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"
from django.db import models
from django.contrib.auth.models import AbstractUser
from dashboard.models import GroupMaster


class User(AbstractUser):
    group_master = models.ForeignKey(GroupMaster, on_delete=models.SET_NULL, null=True)

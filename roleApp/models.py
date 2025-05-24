from django.contrib.auth.models import AbstractUser , Group , Permission
from django.db import models
from . manager import *
from django.utils import timezone

class Profile(AbstractUser):
    ROLE_CHOICES = (
        ('SUPERADMIN', 'SuperAdmin'),
        ('ADMIN', 'Admin'),
        ('MANAGER', 'Manager'),
        ('MEMBER', 'Member'),
    )

    username = None
    email = models.EmailField(unique=True,null=True,blank=True)
    is_email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='SUPERADMIN')
    address=models.CharField(max_length=50,null=True,blank=True)
    otp = models.IntegerField(null=True, blank=True)
   
    USERNAME_FIELD = 'email'
 
    REQUIRED_FIELDS = []
    groups = models.ManyToManyField(Group, related_name="company_groups")  # ✅ Fix
    user_permissions = models.ManyToManyField(Permission, related_name="company_permissions")
 
    objects = UserManager()
   
    def __str__(self):
        return f"{self.email}"



class SuperAdmin(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='superadmin_profile')
    department = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"SuperAdmin: {self.user.email}"



class Admin(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='admin_profile')
    department = models.CharField(max_length=100, null=True, blank=True)
    can_create_managers = models.BooleanField(default=False)

    def __str__(self):
        return f"Admin: {self.user.email}"


class Manager(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='manager_profile')
    team_name = models.CharField(max_length=100, null=True, blank=True)
    number_of_members = models.IntegerField(default=0)

    def __str__(self):
        return f"Manager: {self.user.email}"



class Member(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='member_profile')
    date_joined_team = models.DateField(auto_now_add=True,null=True, blank=True)
    assigned_project = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Member: {self.user.email}"

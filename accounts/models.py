from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.db import models
from django.utils import timezone
from complaints.models import *
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Permission



class CustomUserManager(BaseUserManager):
    use_in_migrations = True
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if password is None:
            raise TypeError('Superusers must have a password.')

        return self.create_user(email, password, **extra_fields)
    
    # def has_module_perms(self, user_obj, app_label):
    #     # Return True if the user has any permissions in the given app_label.
    #     return  user_obj.is_superuser 

class CustomUser(AbstractBaseUser,  PermissionsMixin):
    # ...
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="customuser_groups",
        related_query_name="user",
    )
    # ...

    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='customuser_permissions' # specify a unique related name
    )


    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150,unique=True)
    email = models.EmailField(max_length=254,null=False,blank=False,unique=True)
    Phone_Number = models.IntegerField(null=False,blank=False)
    first_name = models.CharField(max_length=150,null=False,blank=False)
    last_name = models.CharField(max_length=150,null=False,blank=False)
    password = models.CharField(max_length=128,null=False,blank=False)
    gender = models.CharField(max_length=7,null=False,blank=False)
    state = models.ForeignKey(state_master,to_field='state_name',null=False,blank=False,on_delete=models.PROTECT,related_name="state+")
    district = models.ForeignKey(district_master,to_field='district_name',null=False,blank=False,on_delete=models.PROTECT,related_name="complaint_in_district+")
    aadhaarno = models.IntegerField(null=False, blank=False)

    address = models.CharField(max_length=500,null=False,blank=False)
    pincode = models.IntegerField(null=False,blank=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_user = models.BooleanField(default=True)

    state_id_no = models.IntegerField(null=True,blank=True)
    district_id_no = models.IntegerField(null=True,blank=True)


    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True,)

    profile_image = models.ImageField(null=True, blank=True, upload_to="Profile images/",default="Profile images/default.png")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','Phone_Number','first_name','last_name','password','gender','aadhaarno','state','district','address','pincode']


    objects = CustomUserManager()

    def __str__(self):
        return self.email

class rank_master(models.Model):
    rank_id = models.AutoField(primary_key=True,unique=True)
    rank_name = models.CharField(max_length=150,unique=True,null=False,blank=False)
    def __str__(self):
        return self.rank_name

class police_incharge(AbstractBaseUser,  PermissionsMixin):
    # ...
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="police_incharge_groups",
        related_query_name="police_incharge",
    )
    # ...
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='policeincharge_permissions' # specify a unique related name
    )
    status_id_choices = (
        ('active', 'active'),
        ('inactive', 'inactive'),
        ('deleted', 'deleted'),
        ('suspended', 'suspended'),
    )

    incharge_id = models.AutoField(primary_key=True,unique=True)
    username = models.CharField(max_length=150,unique=True)
    email = models.EmailField(max_length=254,null=False,unique=True)
    Phone_Number = models.IntegerField(null=False,blank=False)
    first_name = models.CharField(max_length=150,null=False,blank=False)
    last_name = models.CharField(max_length=150,null=False,blank=False)
    password = models.CharField(max_length=128,null=False,blank=False)
    gender = models.CharField(max_length=7,null=False,blank=False)
    state = models.ForeignKey(state_master,to_field='state_name',null=False,blank=False,on_delete=models.PROTECT,related_name="state+")
    district = models.ForeignKey(district_master,to_field='district_name',null=False,blank=False,on_delete=models.PROTECT,related_name="complaint_in_district+")
    aadhaarno = models.IntegerField(null=False, blank=False)

    rank_name = models.ForeignKey(rank_master,to_field='rank_name',null=False,blank=False,on_delete=models.PROTECT)

    state_id_no = models.IntegerField(null=True,blank=True)
    district_id_no = models.IntegerField(null=True,blank=True)
    rank_id = models.IntegerField(null=True,blank=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to="Profile images/",default="Profile images/default.png")

    address = models.CharField(max_length=500,null=False,blank=False)
    pincode = models.IntegerField(null=False,blank=False)
    
    status_id = models.CharField(max_length=10,null=False, blank=False,choices=status_id_choices)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    station_name = models.OneToOneField(police_station_master,null=False, blank=False,on_delete=models.PROTECT)
    station_id = models.IntegerField(null=True,blank=True)

    USERNAME_FIELD = 'email'


    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_user = models.BooleanField(default=True)
    
class police_officer(AbstractBaseUser,  PermissionsMixin):
    # ...
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="police",
        related_query_name="police",
    )
    # ...
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='police_permissions' # specify a unique related name
    )
    status_id_choices = (
        ('active', 'active'),
        ('inactive', 'inactive'),
        ('deleted', 'deleted'),
        ('suspended', 'suspended'),
    )
    police_id = models.AutoField(primary_key=True,unique=True)
    username = models.CharField(max_length=150,unique=True)
    email = models.EmailField(max_length=254,null=False,unique=True)
    Phone_Number = models.IntegerField(null=False,blank=False)
    first_name = models.CharField(max_length=150,null=False,blank=False)
    last_name = models.CharField(max_length=150,null=False,blank=False)
    password = models.CharField(max_length=128,null=False,blank=False)
    gender = models.CharField(max_length=7,null=False,blank=False)
    state = models.ForeignKey(state_master,to_field='state_name',null=False,blank=False,on_delete=models.PROTECT,related_name="state+")
    state_id_no = models.IntegerField(null=True,blank=True)
    district = models.ForeignKey(district_master,to_field='district_name',null=False,blank=False,on_delete=models.PROTECT,related_name="complaint_in_district+")
    district_id_no = models.IntegerField(null=True,blank=True)
    station_name = models.ForeignKey(police_station_master,null=True, blank=True,on_delete=models.PROTECT)
    aadhaarno = models.IntegerField(null=False, blank=False)

    rank_name = models.ForeignKey(rank_master,to_field='rank_name',null=False,blank=False,on_delete=models.PROTECT)
    rank_id = models.IntegerField(null=True,blank=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to="Profile images/",default="Profile images/default.png")

    address = models.CharField(max_length=500,null=False,blank=False)
    pincode = models.IntegerField(null=False,blank=False)

    state_id_no = models.IntegerField(null=True,blank=True)
    district_id_no = models.IntegerField(null=True,blank=True)
    status_id = models.CharField(max_length=10,null=False, blank=False,choices=status_id_choices)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'


    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_user = models.BooleanField(default=True)
    

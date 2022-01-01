from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager

from django.utils import timezone

# Create your models here.
class AccountManager(BaseUserManager):
    def create_user(self,email,phone,name,password = None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email,phone=phone,name=name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email,name , password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email,name , password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField()
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField(null=True)
    picture = models.ImageField(blank=True, null=True,upload_to = "media")
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_owner = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default= timezone.now)
    last_login = models.DateTimeField(null=True)
    
   
    objects = AccountManager()
    
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
   
    

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.name)
        return full_name.strip()


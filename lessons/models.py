from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager,BaseUserManager
import uuid

#Custom UserManager
class CustomUserManager(BaseUserManager):
      def _create_user(self, email, first_name,last_name, id, password=None, **extra_fields):
                if not email:
                    raise ValueError("The given email must be set")
                email = self.normalize_email(email)
                user=self.model(email=email,first_name=first_name,last_name=last_name,id=id,**extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
      def create_user(self, email, first_name, last_name, id, password=None, **extra_fields):
          extra_fields.setdefault('is_staff',False)
          extra_fields.setdefault('is_superuser',False)
          return self._create_user(email,first_name,last_name,id,password,**extra_fields)
      
      def create_superuser(self, email, first_name=None, last_name=None, id=None, password=None, **extra_fields):
          extra_fields.setdefault('is_staff', True)
          extra_fields.setdefault('is_superuser', True)

          if extra_fields.get('is_staff') is not True:
                raise ValueError('Superuser must have is_staff=True.')
          if extra_fields.get('is_superuser') is not True:
                raise ValueError('Superuser must have is_superuser=True.')

          return self._create_user(email, first_name, last_name, id, password, **extra_fields)


#Student model
class Student(AbstractUser):
   
    username=''
    first_name=models.CharField(max_length=50,blank=False)
    last_name=models.CharField(max_length=50,blank=False)
    email=models.EmailField(unique=True, blank=False)
    id=models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    USERNAME_FIELD='email'
    REQUIRED_FIELDS = [] 
    objects =  CustomUserManager()


    
    
    
    




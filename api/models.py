from django.db import models
from django.contrib.auth.models import BaseUserManager , AbstractBaseUser , PermissionsMixin
from datetime import date

# Create your models here.

class UserManager(BaseUserManager):

    """Custom User Manager to Mangage the User Model
    """

    def create_user(self, email , password , **other_fields):
        if not email :
            raise ValueError("Email must be provided")
        user_email = self.normalize_email(email)
        user = self.model(email = user_email, **other_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password , **other_fields):
        
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_staff', True)
        
        return self.create_user(email, password , **other_fields)
    

class CustomUser(AbstractBaseUser, PermissionsMixin):

    """Custom User Model to make Username and email Unique Values
    """

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=120, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=120, blank=True, null=True)
    last_name = models.CharField(max_length=120 , blank=True , null=True)

    def __str__(self):
        return str(self.email)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'password']

    objects = UserManager()

class BlogPost(models.Model):
    user = models.ForeignKey(CustomUser ,blank=True , null=True , on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    content = models.TextField()
    author = models.CharField(max_length=120)
    published_date = models.DateField(default=date.today)
    created_date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', blank=True, null=True)
    categories = models.ManyToManyField('Category', blank=True, null=True)

    def __str__(self):
        return str(self.title)
    
class Tag(models.Model):
    tag_name = models.CharField(max_length=100)


    def __str__(self):
        return str(self.tag_name)
    
class Category(models.Model):
    category_name = models.CharField(max_length=120)

    def __str__(self):
        return str(self.category_name)
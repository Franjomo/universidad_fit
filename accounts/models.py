from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, role='student', **extra_fields):
        if not username:
            raise ValueError("El usuario debe tener un nombre de usuario")
        
        user = self.model(username=username, role=role, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        user = self.create_user(username=username, password=password, role='admin')
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('student', 'Estudiante'),
        ('employee', 'Empleado'),
        ('admin', 'Administrador'),
    ]

    username = models.CharField(max_length=30, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) #Para acceso al admin
    created_at = models.DateTimeField(auto_now_add=True)

    # relaciones
    student = models.OneToOneField('accounts.Student', on_delete=models.SET_NULL, null=True, blank=True, related_name='user')
    employee = models.OneToOneField('accounts.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='user')


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username
    
class Student(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    birth_date = models.DateField()
    campus_code = models.IntegerField()
    birth_place_code = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Employee(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    contract_type = models.CharField(max_length=30)
    employee_type = models.CharField(max_length=30)
    faculty_code = models.IntegerField()
    campus_code = models.IntegerField()
    birth_place_code = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

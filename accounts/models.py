from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from locations.models import Faculty, Area

# --- Custom User Manager ---
class UserManager(BaseUserManager):
    def create_user(self, username, password=None, role='student', **extra_fields):
        if not username:
            raise ValueError("El usuario debe tener un nombre de usuario (username).")
        user = self.model(username=username, role=role, **extra_fields)
        user.set_password(password)  # Usa hash interno de Django
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

# --- User Model ---
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('STUDENT', 'Student'),
        ('EMPLOYEE', 'Employee'),
        ('ADMIN', 'Admin'),
    ]

    username = models.CharField(max_length=30, primary_key=True)
    password_hash = models.CharField(max_length=100, db_column='password_hash')  # mantiene el campo original SQL
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Relaciones opcionales
    student = models.OneToOneField('accounts.Student', on_delete=models.CASCADE, null=True, blank=True, db_column='student_id', related_name='user')
    employee = models.OneToOneField('accounts.Employee', on_delete=models.CASCADE, null=True, blank=True, db_column='employee_id', related_name='user')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = 'users'
        constraints = [
            models.CheckConstraint(
                check=(
                    (models.Q(student__isnull=False, employee__isnull=True) |
                     models.Q(student__isnull=True, employee__isnull=False))
                ),
                name='USERS_ONE_ROLE_CHK'
            )
        ]

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        """
        Sobrescribe el campo password_hash con el hash real
        de Django para mantener compatibilidad con el sistema
        y con el nombre de columna original del SQL.
        """
        if self.password and not self.password.startswith('pbkdf2_'):
            # Django usa pbkdf2_sha256 por defecto
            self.set_password(self.password)
            self.password_hash = self.password  # sincroniza con el campo SQL
        super().save(*args, **kwargs)
    
class Student(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    birth_date = models.DateField()
    birth_place = models.ForeignKey('locations.City', on_delete=models.PROTECT, db_column='birth_place_code')
    campus = models.ForeignKey('locations.Campus', on_delete=models.CASCADE, db_column='campus_code')

    class Meta:
        db_table = 'students'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Employee(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    contract_type = models.ForeignKey('humanResources.ContractType', on_delete=models.PROTECT, db_column='contract_type')
    employee_type = models.ForeignKey('humanResources.EmployeeType', on_delete=models.PROTECT, db_column='employee_type')
    faculty = models.ForeignKey('locations.Faculty', on_delete=models.CASCADE, db_column='faculty_code')
    campus = models.ForeignKey('locations.Campus', on_delete=models.CASCADE, db_column='campus_code')
    birth_place = models.ForeignKey('locations.City', on_delete=models.PROTECT, db_column='birth_place_code')

    class Meta:
        db_table = 'employees'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
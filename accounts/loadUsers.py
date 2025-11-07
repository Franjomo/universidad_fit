import os
from dotenv import load_dotenv
import django
import datetime

# 1️⃣ Cargar .env antes que nada
load_dotenv(dotenv_path=r"D:\Icesi\Sexto_Semestre\Intensivos2\Proyecto\universidad_fit\.env")

# 2️⃣ Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "universidad_fit.settings")
django.setup()

from django.db import connection
print("Conectando a la base de datos:", connection.settings_dict['NAME'])

import datetime
from accounts.models import User, Student, Employee

# --- Estudiantes ---
students_data = [
    ('laura.h', '2001', 'hash_lh123'),
    ('pedro.m', '2002', 'hash_pm123'),
    ('ana.s', '2003', 'hash_as123'),
    ('luis.r', '2004', 'hash_lr123'),
    ('sofia.g', '2005', 'hash_sg123'),
]

for username, student_id, password in students_data:
    try:
        student = Student.objects.get(id=student_id)
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'role': 'STUDENT',
                'student': student,
                'is_active': True,
                'created_at': datetime.datetime.now()
            }
        )
        # Hashear la contraseña
        user.set_password(password)
        user.save()
        print(f"Usuario estudiante {username} creado con contraseña hasheada.")
    except Student.DoesNotExist:
        print(f"Error: Student con id={student_id} no existe.")

# --- Empleados ---
employees_data = [
    ('juan.p', '1001', 'hash_jp123'),
    #('maria.g', '1002', 'hash_mg123'), Comentado porque es admin (preguntar a profe que hacer con admins)
    ('carlos.l', '1003', 'hash_cl123'),
    ('carlos.m', '1004', 'hash_cm123'),
    ('sandra.o', '1005', 'hash_so123'),
    ('paula.r', '1007', 'hash_pr123'),
    ('andres.c', '1008', 'hash_ac123'),
]

for username, employee_id, password in employees_data:
    try:
        employee = Employee.objects.get(id=employee_id)
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'role': 'EMPLOYEE',
                'employee': employee,
                'is_active': True,
                'created_at': datetime.datetime.now()
            }
        )
        # Hashear la contraseña
        user.set_password(password)
        user.save()
        print(f"Usuario empleado {username} creado con contraseña hasheada.")
    except Employee.DoesNotExist:
        print(f"Error: Employee con id={employee_id} no existe.")

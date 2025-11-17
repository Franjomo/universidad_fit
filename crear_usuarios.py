"""
Script para crear usuarios de prueba
Ejecuta: python crear_usuarios.py

NOTA: Este script intenta usar datos existentes de la base de datos.
Si no existen, crea usuarios simples sin restricciones (solo para ADMIN).
"""

import os
import django
from datetime import date

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'universidad_fit.settings')
django.setup()

from accounts.models import User, Student, Employee
from locations.models import City, Campus
from humanResources.models import ContractType, EmployeeType
from locations.models import Faculty

def obtener_o_crear_datos_base():
    """Obtiene o crea los datos base necesarios"""
    datos = {}
    
    try:
        # Intentar obtener una ciudad
        ciudad = City.objects.first()
        if not ciudad:
            print("ADVERTENCIA: No hay ciudades en la base de datos.")
            print("Los usuarios STUDENT y EMPLOYEE no se pueden crear sin datos base.")
            return None
        datos['ciudad'] = ciudad
        
        # Intentar obtener un campus
        campus = Campus.objects.first()
        if not campus:
            print("ADVERTENCIA: No hay campus en la base de datos.")
            return None
        datos['campus'] = campus
        
        # Para empleados, necesitamos más datos
        contract_type = ContractType.objects.first()
        employee_type = EmployeeType.objects.first()
        faculty = Faculty.objects.first()
        
        if contract_type and employee_type and faculty:
            datos['contract_type'] = contract_type
            datos['employee_type'] = employee_type
            datos['faculty'] = faculty
        
    except Exception as e:
        print(f"Error al obtener datos base: {e}")
        return None
    
    return datos

def crear_usuarios():
    """Crea usuarios de prueba para diferentes roles"""
    
    print("=" * 60)
    print("Creando usuarios de prueba...")
    print("=" * 60)
    
    # Obtener datos base
    datos_base = obtener_o_crear_datos_base()
    
    creados = 0
    existentes = 0
    errores = 0
    
    # ===== CREAR USUARIOS ADMIN (no requieren Student/Employee) =====
    admin_users = [
        {'username': 'admin1', 'password': 'admin123', 'descripcion': 'Administrador principal'},
        {'username': 'admin', 'password': 'admin123', 'descripcion': 'Administrador'},
    ]
    
    for admin_data in admin_users:
        username = admin_data['username']
        password = admin_data['password']
        
        if User.objects.filter(username=username).exists():
            print(f"[!] Usuario '{username}' ya existe. Saltando...")
            existentes += 1
            continue
        
        try:
            # Para ADMIN, intentamos crear sin Student/Employee
            # Si falla, creamos un Employee temporal
            try:
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    role='ADMIN',
                    is_staff=True
                )
            except:
                # Si falla por la restricción, creamos un Employee temporal
                if datos_base:
                    employee = Employee.objects.create(
                        id=f'ADM{username}',
                        first_name='Admin',
                        last_name=username.title(),
                        email=f'{username}@icesi.edu.co',
                        contract_type=datos_base.get('contract_type'),
                        employee_type=datos_base.get('employee_type'),
                        faculty=datos_base.get('faculty'),
                        campus=datos_base['campus'],
                        birth_place=datos_base['ciudad']
                    )
                    user = User.objects.create_user(
                        username=username,
                        password=password,
                        role='ADMIN',
                        is_staff=True,
                        employee=employee
                    )
                else:
                    raise Exception("No se pueden crear usuarios sin datos base")
            
            print(f"[OK] Usuario creado: {username} (ADMIN) - {admin_data['descripcion']}")
            creados += 1
        except Exception as e:
            print(f"[ERROR] Error al crear usuario '{username}': {str(e)}")
            errores += 1
    
    # ===== CREAR USUARIOS ESTUDIANTES =====
    if datos_base:
        estudiantes = [
            {'username': 'estudiante1', 'password': 'estudiante123', 'id': 'EST001', 'nombre': 'Juan', 'apellido': 'Pérez'},
            {'username': 'estudiante2', 'password': 'estudiante123', 'id': 'EST002', 'nombre': 'María', 'apellido': 'García'},
            {'username': 'test', 'password': 'test123', 'id': 'EST003', 'nombre': 'Test', 'apellido': 'Usuario'},
        ]
        
        for est_data in estudiantes:
            username = est_data['username']
            password = est_data['password']
            
            if User.objects.filter(username=username).exists():
                print(f"[!] Usuario '{username}' ya existe. Saltando...")
                existentes += 1
                continue
            
            try:
                # Crear Student primero
                student = Student.objects.create(
                    id=est_data['id'],
                    first_name=est_data['nombre'],
                    last_name=est_data['apellido'],
                    email=f'{username}@icesi.edu.co',
                    birth_date=date(2000, 1, 1),
                    birth_place=datos_base['ciudad'],
                    campus=datos_base['campus']
                )
                
                # Crear User asociado
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    role='STUDENT',
                    student=student
                )
                
                print(f"[OK] Usuario creado: {username} (STUDENT) - {est_data['nombre']} {est_data['apellido']}")
                creados += 1
            except Exception as e:
                print(f"[ERROR] Error al crear estudiante '{username}': {str(e)}")
                errores += 1
        
        # ===== CREAR USUARIOS EMPLEADOS =====
        if datos_base.get('contract_type') and datos_base.get('employee_type') and datos_base.get('faculty'):
            empleados = [
                {'username': 'empleado1', 'password': 'empleado123', 'id': 'EMP001', 'nombre': 'Carlos', 'apellido': 'López'},
                {'username': 'entrenador1', 'password': 'entrenador123', 'id': 'EMP002', 'nombre': 'Ana', 'apellido': 'Martínez'},
            ]
            
            for emp_data in empleados:
                username = emp_data['username']
                password = emp_data['password']
                
                if User.objects.filter(username=username).exists():
                    print(f"[!] Usuario '{username}' ya existe. Saltando...")
                    existentes += 1
                    continue
                
                try:
                    # Crear Employee primero
                    employee = Employee.objects.create(
                        id=emp_data['id'],
                        first_name=emp_data['nombre'],
                        last_name=emp_data['apellido'],
                        email=f'{username}@icesi.edu.co',
                        contract_type=datos_base['contract_type'],
                        employee_type=datos_base['employee_type'],
                        faculty=datos_base['faculty'],
                        campus=datos_base['campus'],
                        birth_place=datos_base['ciudad']
                    )
                    
                    # Crear User asociado
                    user = User.objects.create_user(
                        username=username,
                        password=password,
                        role='EMPLOYEE',
                        employee=employee
                    )
                    
                    print(f"[OK] Usuario creado: {username} (EMPLOYEE) - {emp_data['nombre']} {emp_data['apellido']}")
                    creados += 1
                except Exception as e:
                    print(f"[ERROR] Error al crear empleado '{username}': {str(e)}")
                    errores += 1
        else:
            print("[!] No se pueden crear empleados: faltan datos de ContractType, EmployeeType o Faculty")
    else:
        print("[!] No se pueden crear estudiantes/empleados: faltan datos base (City, Campus)")
    
    # ===== RESUMEN =====
    print("=" * 60)
    print("RESUMEN:")
    print(f"  Usuarios creados: {creados}")
    print(f"  Usuarios existentes: {existentes}")
    print(f"  Errores: {errores}")
    print("=" * 60)
    
    # ===== MOSTRAR CREDENCIALES =====
    print("\nCREDENCIALES DE ACCESO:")
    print("-" * 60)
    
    usuarios_creados = [
        ('admin1', 'admin123', 'ADMIN'),
        ('admin', 'admin123', 'ADMIN'),
        ('estudiante1', 'estudiante123', 'STUDENT'),
        ('estudiante2', 'estudiante123', 'STUDENT'),
        ('test', 'test123', 'STUDENT'),
        ('empleado1', 'empleado123', 'EMPLOYEE'),
        ('entrenador1', 'entrenador123', 'EMPLOYEE'),
    ]
    
    for username, password, role in usuarios_creados:
        if User.objects.filter(username=username).exists():
            print(f"Usuario: {username:<15} | Password: {password:<15} | Rol: {role}")
    
    print("-" * 60)
    print("\nAccede en: http://127.0.0.1:8000/accounts/login/")
    print("=" * 60)

if __name__ == '__main__':
    crear_usuarios()

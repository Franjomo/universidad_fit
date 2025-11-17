"""
Script para crear datos base necesarios (City, Campus, etc.)
Ejecuta: python crear_datos_base.py
"""

import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'universidad_fit.settings')
django.setup()

from locations.models import Country, Department, City, Campus, Faculty
from humanResources.models import ContractType, EmployeeType

def crear_datos_base():
    """Crea los datos base necesarios para crear usuarios"""
    
    print("=" * 60)
    print("Creando datos base...")
    print("=" * 60)
    
    creados = 0
    
    try:
        # Crear País
        country, created = Country.objects.get_or_create(
            code=1,
            defaults={'name': 'Colombia'}
        )
        if created:
            print("[OK] País creado: Colombia")
            creados += 1
        else:
            print("[!] País ya existe: Colombia")
        
        # Crear Departamento
        department, created = Department.objects.get_or_create(
            code=1,
            defaults={'name': 'Valle del Cauca', 'country': country}
        )
        if created:
            print("[OK] Departamento creado: Valle del Cauca")
            creados += 1
        else:
            print("[!] Departamento ya existe: Valle del Cauca")
        
        # Crear Ciudad
        city, created = City.objects.get_or_create(
            code=101,
            defaults={'name': 'Cali', 'department': department}
        )
        if created:
            print("[OK] Ciudad creada: Cali")
            creados += 1
        else:
            print("[!] Ciudad ya existe: Cali")
        
        # Crear Campus
        campus, created = Campus.objects.get_or_create(
            code=1,
            defaults={'name': 'Campus Cali', 'city': city}
        )
        if created:
            print("[OK] Campus creado: Campus Cali")
            creados += 1
        else:
            print("[!] Campus ya existe: Campus Cali")
        
        # Crear Facultad
        faculty, created = Faculty.objects.get_or_create(
            code=1,
            defaults={
                'name': 'Facultad de Ciencias',
                'location': 'Cali',
                'phone_number': '555-1234',
                'dean_id': '1001'
            }
        )
        if created:
            print("[OK] Facultad creada: Facultad de Ciencias")
            creados += 1
        else:
            print("[!] Facultad ya existe: Facultad de Ciencias")
        
        # Crear ContractType
        contract_type, created = ContractType.objects.get_or_create(
            name='Planta'
        )
        if created:
            print("[OK] Tipo de contrato creado: Planta")
            creados += 1
        else:
            print("[!] Tipo de contrato ya existe: Planta")
        
        # Crear EmployeeType
        employee_type, created = EmployeeType.objects.get_or_create(
            name='Instructor'
        )
        if created:
            print("[OK] Tipo de empleado creado: Instructor")
            creados += 1
        else:
            print("[!] Tipo de empleado ya existe: Instructor")
        
        print("=" * 60)
        print(f"RESUMEN: {creados} elementos creados")
        print("=" * 60)
        print("\nAhora puedes ejecutar: python crear_usuarios.py")
        
    except Exception as e:
        print(f"[ERROR] Error al crear datos base: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    crear_datos_base()


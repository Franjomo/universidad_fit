"""
Create simple test users for login testing
This script creates minimal users that can login without complex foreign key requirements
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'universidad_fit.settings')
django.setup()

from accounts.models import User, Student, Employee
from locations.models import City, Campus
from humanResources.models import ContractType, EmployeeType
from datetime import date

def create_test_users():
    print("\n" + "="*60)
    print("Creating Test Users for Login Testing")
    print("="*60)
    
    # Get or create required foreign key objects
    city = City.objects.first()
    campus = Campus.objects.first()
    
    if not city:
        print("ERROR: No City found. Please create at least one City in the database.")
        return
    
    if not campus:
        print("ERROR: No Campus found. Please create at least one Campus in the database.")
        return
    
    # Create test student
    try:
        student = Student.objects.create(
            id='TEST001',
            first_name='Test',
            last_name='Student',
            email='student@unicali.edu.co',
            birth_date=date(2000, 1, 1),
            birth_place=city,
            campus=campus
        )
        
        user = User.objects.create_user(
            username='student',
            password='student123',
            role='STUDENT',
            student=student
        )
        print(f"✅ Created student user: {user.username} / student123")
    except Exception as e:
        print(f"⚠️ Student creation error: {e}")
        # Try to get existing
        try:
            user = User.objects.get(username='student')
            user.set_password('student123')
            user.save()
            print(f"✅ Updated student user: {user.username} / student123")
        except:
            pass
    
    # Create test employee (trainer)
    contract_type = ContractType.objects.first()
    employee_type = EmployeeType.objects.first()
    faculty = campus.faculty if hasattr(campus, 'faculty') else None
    
    if not contract_type or not employee_type:
        print("⚠️ Missing ContractType or EmployeeType. Creating employee without them...")
        # Create employee user without employee record
        try:
            user = User.objects.create_user(
                username='trainer',
                password='trainer123',
                role='EMPLOYEE'
            )
            print(f"✅ Created trainer user (no employee record): {user.username} / trainer123")
        except Exception as e:
            try:
                user = User.objects.get(username='trainer')
                user.set_password('trainer123')
                user.save()
                print(f"✅ Updated trainer user: {user.username} / trainer123")
            except:
                print(f"⚠️ Could not create trainer: {e}")
    else:
        try:
            employee = Employee.objects.create(
                id='TEST1001',
                first_name='Test',
                last_name='Trainer',
                email='trainer@unicali.edu.co',
                contract_type=contract_type,
                employee_type=employee_type,
                faculty=faculty if faculty else Faculty.objects.first(),
                campus=campus,
                birth_place=city
            )
            
            user = User.objects.create_user(
                username='trainer',
                password='trainer123',
                role='EMPLOYEE',
                employee=employee
            )
            print(f"✅ Created trainer user: {user.username} / trainer123")
        except Exception as e:
            print(f"⚠️ Employee creation error: {e}")
            try:
                user = User.objects.get(username='trainer')
                user.set_password('trainer123')
                user.save()
                print(f"✅ Updated trainer user: {user.username} / trainer123")
            except:
                pass
    
    # Create admin user
    try:
        user = User.objects.create_user(
            username='admin',
            password='admin123',
            role='ADMIN',
            is_staff=True
        )
        print(f"✅ Created admin user: {user.username} / admin123")
    except Exception as e:
        try:
            user = User.objects.get(username='admin')
            user.set_password('admin123')
            user.save()
            print(f"✅ Updated admin user: {user.username} / admin123")
        except:
            print(f"⚠️ Could not create admin: {e}")
    
    print("\n" + "="*60)
    print("TEST USER CREDENTIALS:")
    print("="*60)
    print("Student:  username: student  / password: student123")
    print("Trainer:  username: trainer  / password: trainer123")
    print("Admin:    username: admin    / password: admin123")
    print("="*60)
    print("\n✅ Test users created/updated successfully!")

if __name__ == "__main__":
    create_test_users()


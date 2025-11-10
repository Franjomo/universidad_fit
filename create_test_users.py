"""Create test users for the fitness app"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'universidad_fit.settings')
django.setup()

from accounts.models import User, Student, Employee
from academics.models import Program

def create_test_users():
    print("Creating test users...")

    # First, create a test program for students
    try:
        program = Program.objects.first()
        if not program:
            print("Warning: No programs found in database. Student creation may fail.")
            program_id = None
        else:
            program_id = program.id
    except:
        program_id = None

    # Create student record
    student_record = Student.objects.create(
        id='S001',
        first_name='Jane',
        last_name='Student',
        second_last_name='Test',
        date_of_birth='2000-01-01',
        gender='F',
        address='123 Test St',
        phone='1234567890',
        email='student@test.com',
        program_id=program_id
    )

    # Create student user
    student_user = User.objects.create_user(
        username='student',
        password='student123',
        role='STUDENT',
        student=student_record
    )
    print(f"✓ Created student: {student_user.username} / student123")

    # Create employee record
    employee_record = Employee.objects.create(
        id='E001',
        first_name='John',
        last_name='Employee',
        second_last_name='Test',
        date_of_birth='1990-01-01',
        gender='M',
        address='456 Test Ave',
        phone='0987654321',
        email='employee@test.com',
        employee_type='administrative',
        job_title='Administrator',
        hire_date='2020-01-01'
    )

    # Create employee user
    employee_user = User.objects.create_user(
        username='employee',
        password='employee123',
        role='EMPLOYEE',
        employee=employee_record
    )
    print(f"✓ Created employee: {employee_user.username} / employee123")

    print("\nTest users created successfully!")
    print("\n" + "="*50)
    print("LOGIN CREDENTIALS:")
    print("="*50)
    print("Student:  username: student  / password: student123")
    print("Employee: username: employee / password: employee123")
    print("="*50)

if __name__ == "__main__":
    # Clear existing users and related records
    User.objects.all().delete()
    Student.objects.all().delete()
    Employee.objects.all().delete()
    print("Cleared existing users.\n")

    create_test_users()

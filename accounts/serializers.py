 #ESTE CODIGO SE ENCARGA DEL RESTFUL API DE accounts.

from rest_framework import serializers
from .models import User, Student, Employee


class StudentSerializer(serializers.ModelSerializer):
    birth_place_name = serializers.CharField(source='birth_place.name', read_only=True)
    campus_name = serializers.CharField(source='campus.name', read_only=True)
    
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'email', 'birth_date', 
                  'birth_place', 'birth_place_name', 'campus', 'campus_name']
        read_only_fields = ['id']


class EmployeeSerializer(serializers.ModelSerializer):
    contract_type_name = serializers.CharField(source='contract_type.name', read_only=True)
    employee_type_name = serializers.CharField(source='employee_type.name', read_only=True)
    faculty_name = serializers.CharField(source='faculty.name', read_only=True)
    campus_name = serializers.CharField(source='campus.name', read_only=True)
    birth_place_name = serializers.CharField(source='birth_place.name', read_only=True)
    
    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'email', 'contract_type', 
                  'contract_type_name', 'employee_type', 'employee_type_name', 
                  'faculty', 'faculty_name', 'campus', 'campus_name', 
                  'birth_place', 'birth_place_name']
        read_only_fields = ['id']


class UserSerializer(serializers.ModelSerializer):
    student_details = StudentSerializer(source='student', read_only=True)
    employee_details = EmployeeSerializer(source='employee', read_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'role', 'is_active', 'created_at', 
                  'student', 'student_details', 'employee', 'employee_details']
        read_only_fields = ['created_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        """Create user with hashed password"""
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        """Update user, hash password if provided"""
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class UserCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for user creation"""
    class Meta:
        model = User
        fields = ['username', 'password', 'role', 'student', 'employee']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def validate(self, data):
        """Ensure user has either student or employee, not both"""
        student = data.get('student')
        employee = data.get('employee')
        
        if not student and not employee:
            raise serializers.ValidationError("User must be linked to either a student or an employee.")
        if student and employee:
            raise serializers.ValidationError("User cannot be both a student and an employee.")
        
        return data
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

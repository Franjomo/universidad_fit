from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from .models import User, Student, Employee
from .serializers import UserSerializer, StudentSerializer, EmployeeSerializer, UserCreateSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User model.
    Provides CRUD operations for users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    
    def get_permissions(self):
        """Allow anyone to create users, require auth for other operations"""
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user's information"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class StudentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Student model.
    Provides CRUD operations for students.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Optionally filter by campus"""
        queryset = Student.objects.all()
        campus = self.request.query_params.get('campus', None)
        if campus:
            queryset = queryset.filter(campus__code=campus)
        return queryset


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Employee model.
    Provides CRUD operations for employees.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Optionally filter by faculty or employee type"""
        queryset = Employee.objects.all()
        faculty = self.request.query_params.get('faculty', None)
        employee_type = self.request.query_params.get('employee_type', None)
        
        if faculty:
            queryset = queryset.filter(faculty__code=faculty)
        if employee_type:
            queryset = queryset.filter(employee_type__name=employee_type)
        
        return queryset

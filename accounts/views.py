from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
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


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Login endpoint for authentication"""
    email = request.data.get('email', '')
    password = request.data.get('password', '')
    
    if not email or not password:
        return Response(
            {'error': 'Email and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Try to find user by email (if email format) or username
    user = None
    try:
        # Force fresh connection and clear any cached queries
        from django.db import connection, reset_queries
        connection.ensure_connection()
        reset_queries()
        if '@' in email:
            # If it's an email, try to find by student/employee email
            try:
                student = Student.objects.select_related('user').get(email=email)
                user = getattr(student, 'user', None)
                if not user:
                    # Try to get user directly
                    user = User.objects.filter(student=student).first()
            except Student.DoesNotExist:
                pass
            except Student.MultipleObjectsReturned:
                student = Student.objects.select_related('user').filter(email=email).first()
                user = getattr(student, 'user', None) if student else None
                if not user and student:
                    user = User.objects.filter(student=student).first()
            
            if not user:
                try:
                    employee = Employee.objects.get(email=email)
                    if hasattr(employee, 'user') and employee.user:
                        user = employee.user
                except Employee.DoesNotExist:
                    pass
                except Employee.MultipleObjectsReturned:
                    employee = Employee.objects.filter(email=email).first()
                    if hasattr(employee, 'user') and employee.user:
                        user = employee.user
            
            if not user:
                return Response(
                    {'error': f'No user found with email: {email}'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        else:
            # Try as username - use raw SQL as fallback if ORM fails
            try:
                user = User.objects.get(username=email)
            except User.DoesNotExist:
                # Try raw SQL query as fallback
                from django.db import connection
                with connection.cursor() as cursor:
                    cursor.execute("SELECT username, password_hash, role FROM users WHERE username = %s", [email])
                    row = cursor.fetchone()
                    if row:
                        # Create user object from raw data
                        user = User()
                        user.username = row[0]
                        user.password_hash = row[1]
                        user.role = row[2]
                        # Need to get full user object for password check
                        user = User.objects.filter(username=email).first()
                        if not user:
                            return Response(
                                {'error': f'User found in DB but cannot load: {email}'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                            )
                    else:
                        return Response(
                            {'error': f'No user found with username: {email}'},
                            status=status.HTTP_401_UNAUTHORIZED
                        )
            except Exception as e:
                return Response(
                    {'error': f'Error finding user: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        if not user:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Check password directly
        if not user.check_password(password):
            return Response(
                {'error': 'Invalid password'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Generate token (simple token for now, can be upgraded to JWT later)
        from django.contrib.auth import login as django_login
        django_login(request, user)
        
        # Return user data
        serializer = UserSerializer(user)
        return Response({
            'token': 'dummy-token-for-now',  # Replace with JWT token later
            'user': serializer.data
        })
        
    except Exception as e:
        import traceback
        return Response(
            {'error': f'Login failed: {str(e)}', 'traceback': traceback.format_exc()},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """Logout endpoint"""
    from django.contrib.auth import logout as django_logout
    django_logout(request)
    return Response({'message': 'Logged out successfully'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    """Get current authenticated user"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

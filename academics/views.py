from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Program, Subject, Group, Enrollment
from .serializers import ProgramSerializer, SubjectSerializer, GroupSerializer, EnrollmentSerializer


class ProgramViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Program model.
    """
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Program.objects.all()
        area = self.request.query_params.get('area', None)
        if area:
            queryset = queryset.filter(area__code=area)
        return queryset


class SubjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Subject model.
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Subject.objects.all()
        program = self.request.query_params.get('program', None)
        if program:
            queryset = queryset.filter(program__code=program)
        return queryset


class GroupViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Group model.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'NRC'
    
    def get_queryset(self):
        queryset = Group.objects.all()
        subject = self.request.query_params.get('subject', None)
        semester = self.request.query_params.get('semester', None)
        professor = self.request.query_params.get('professor', None)
        
        if subject:
            queryset = queryset.filter(subject__code=subject)
        if semester:
            queryset = queryset.filter(semester=semester)
        if professor:
            queryset = queryset.filter(professor__id=professor)
        
        return queryset


class EnrollmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Enrollment model.
    """
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Enrollment.objects.all()
        student = self.request.query_params.get('student', None)
        group = self.request.query_params.get('group', None)
        status = self.request.query_params.get('status', None)
        
        if student:
            queryset = queryset.filter(student__id=student)
        if group:
            queryset = queryset.filter(group__NRC=group)
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset

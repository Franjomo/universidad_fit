#ESTE CODIGO SE ENCARGA DEL RESTFUL API DE academics.

from rest_framework import serializers
from .models import Program, Subject, Group, Enrollment


class ProgramSerializer(serializers.ModelSerializer):
    area_name = serializers.CharField(source='area.name', read_only=True)
    
    class Meta:
        model = Program
        fields = ['code', 'name', 'area', 'area_name']
        read_only_fields = ['code']


class SubjectSerializer(serializers.ModelSerializer):
    program_name = serializers.CharField(source='program.name', read_only=True)
    
    class Meta:
        model = Subject
        fields = ['code', 'name', 'program', 'program_name']
        read_only_fields = ['code']


class GroupSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    professor_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Group
        fields = ['NRC', 'number', 'semester', 'subject', 'subject_name', 
                  'professor', 'professor_name']
        read_only_fields = ['NRC']
    
    def get_professor_name(self, obj):
        return f"{obj.professor.first_name} {obj.professor.last_name}"


class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    group_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'student_name', 'group', 'group_info', 
                  'enrollment_date', 'status']
    
    def get_student_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"
    
    def get_group_info(self, obj):
        return {
            'NRC': obj.group.NRC,
            'subject': obj.group.subject.name,
            'number': obj.group.number
        }

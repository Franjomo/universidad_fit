#ESTE CODIGO SE ENCARGA DEL RESTFUL API DE locations.

from rest_framework import serializers
from .models import Country, Department, City, Campus, Faculty, Area


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['code', 'name']


class DepartmentSerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source='country.name', read_only=True)
    
    class Meta:
        model = Department
        fields = ['code', 'name', 'country', 'country_name']


class CitySerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    country_name = serializers.CharField(source='department.country.name', read_only=True)
    
    class Meta:
        model = City
        fields = ['code', 'name', 'department', 'department_name', 'country_name']


class CampusSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)
    
    class Meta:
        model = Campus
        fields = ['code', 'name', 'city', 'city_name']


class FacultySerializer(serializers.ModelSerializer):
    dean_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Faculty
        fields = ['code', 'name', 'location', 'phone_number', 'dean_id', 'dean_name']
    
    def get_dean_name(self, obj):
        if obj.dean_id:
            from accounts.models import Employee
            try:
                dean = Employee.objects.get(id=obj.dean_id)
                return f"{dean.first_name} {dean.last_name}"
            except Employee.DoesNotExist:
                return None
        return None


class AreaSerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(source='faculty.name', read_only=True)
    coordinator_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Area
        fields = ['code', 'name', 'faculty', 'faculty_name', 'coordinator_id', 'coordinator_name']
    
    def get_coordinator_name(self, obj):
        from accounts.models import Employee
        try:
            coordinator = Employee.objects.get(id=obj.coordinator_id)
            return f"{coordinator.first_name} {coordinator.last_name}"
        except Employee.DoesNotExist:
            return None

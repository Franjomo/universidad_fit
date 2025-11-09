from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Country, Department, City, Campus, Faculty, Area
from .serializers import (CountrySerializer, DepartmentSerializer, CitySerializer,
                          CampusSerializer, FacultySerializer, AreaSerializer)


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAuthenticated]


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Department.objects.all()
        country = self.request.query_params.get('country', None)
        if country:
            queryset = queryset.filter(country__code=country)
        return queryset


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = City.objects.all()
        department = self.request.query_params.get('department', None)
        if department:
            queryset = queryset.filter(department__code=department)
        return queryset


class CampusViewSet(viewsets.ModelViewSet):
    queryset = Campus.objects.all()
    serializer_class = CampusSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Campus.objects.all()
        city = self.request.query_params.get('city', None)
        if city:
            queryset = queryset.filter(city__code=city)
        return queryset


class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    permission_classes = [IsAuthenticated]


class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Area.objects.all()
        faculty = self.request.query_params.get('faculty', None)
        if faculty:
            queryset = queryset.filter(faculty__code=faculty)
        return queryset

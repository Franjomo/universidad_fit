from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CountryViewSet, DepartmentViewSet, CityViewSet,
                    CampusViewSet, FacultyViewSet, AreaViewSet)

router = DefaultRouter()
router.register(r'countries', CountryViewSet, basename='country')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'cities', CityViewSet, basename='city')
router.register(r'campuses', CampusViewSet, basename='campus')
router.register(r'faculties', FacultyViewSet, basename='faculty')
router.register(r'areas', AreaViewSet, basename='area')

urlpatterns = [
    path('', include(router.urls)),
]

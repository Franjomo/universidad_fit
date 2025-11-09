from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProgramViewSet, SubjectViewSet, GroupViewSet, EnrollmentViewSet

router = DefaultRouter()
router.register(r'programs', ProgramViewSet, basename='program')
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')

urlpatterns = [
    path('', include(router.urls)),
]

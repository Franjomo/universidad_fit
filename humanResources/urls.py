from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContractTypeViewSet, EmployeeTypeViewSet

router = DefaultRouter()
router.register(r'contract-types', ContractTypeViewSet, basename='contract-type')
router.register(r'employee-types', EmployeeTypeViewSet, basename='employee-type')

urlpatterns = [
    path('', include(router.urls)),
]

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import ContractType, EmployeeType
from .serializers import ContractTypeSerializer, EmployeeTypeSerializer


class ContractTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for ContractType model.
    Lookup tables typically only need list/retrieve operations.
    """
    queryset = ContractType.objects.all()
    serializer_class = ContractTypeSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'name'


class EmployeeTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for EmployeeType model.
    Lookup tables typically only need list/retrieve operations.
    """
    queryset = EmployeeType.objects.all()
    serializer_class = EmployeeTypeSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'name'

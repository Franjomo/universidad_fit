#ESTE CODIGO SE ENCARGA DEL RESTFUL API DE humanResources.

from rest_framework import serializers
from .models import ContractType, EmployeeType


class ContractTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractType
        fields = ['name']


class EmployeeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeType
        fields = ['name']

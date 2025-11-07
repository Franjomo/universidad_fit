from django.db import models

class ContractType(models.Model):
    name = models.CharField(max_length=30, primary_key=True)

    class Meta:
        db_table = 'contract_types'

    def __str__(self):
        return self.name

class EmployeeType(models.Model):
    name = models.CharField(max_length=30, primary_key=True)

    class Meta:
        db_table = 'employee_types'

    def __str__(self):
        return self.name
